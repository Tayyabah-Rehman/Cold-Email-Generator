"""
chains.py — LangChain chains for:
  1. Extracting structured job info from raw JD text.
  2. Generating a personalized cold email given the JD + portfolio links.
"""

import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean_json(raw: str) -> dict:
    """Strip markdown fences and parse the first JSON object found."""
    raw = re.sub(r"```(?:json)?", "", raw).strip().strip("`")
    # Grab the first {...} block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Chain factories
# ---------------------------------------------------------------------------

def make_extract_chain(llm: ChatGroq):
    """Returns a chain that parses a job description into structured JSON."""

    prompt = PromptTemplate.from_template(
        """You are an expert HR analyst.
Extract the following fields from the job description below and return ONLY valid JSON — no markdown, no explanation.

Fields to extract:
- role          : job title / position name
- company       : hiring company name (if mentioned, else "Not specified")
- experience    : years of experience required (e.g. "2+ years", "Fresher", "Not specified")
- skills        : list of required technical skills / tools (as a JSON array of strings)
- description   : a 2–3 sentence summary of what the role involves

Job Description:
{job_description}

Return JSON like:
{{
  "role": "...",
  "company": "...",
  "experience": "...",
  "skills": ["...", "..."],
  "description": "..."
}}"""
    )

    return prompt | llm | StrOutputParser()


def make_email_chain(llm: ChatGroq):
    """Returns a chain that drafts a cold email for a job application."""

    prompt = PromptTemplate.from_template(
        """You are an expert cold email copywriter helping an AI/ML engineer apply for jobs.

Candidate profile:
- Name: {sender_name}
- Current role/status: {sender_role}
- Background: {sender_bio}

Job details:
- Role: {role}
- Company: {company}
- Required experience: {experience}
- Key skills needed: {skills}
- Role summary: {description}

Relevant portfolio projects (from ChromaDB match):
{portfolio_links}

Write a compelling, concise cold email for this job application.

Rules:
1. Subject line must be specific and attention-grabbing.
2. Opening sentence must hook the reader — reference the company or role directly.
3. Second paragraph: 2–3 sentences about relevant experience / skills matching the JD.
4. Third paragraph: mention 1–2 of the portfolio links with context on why they are relevant.
5. Closing: polite CTA to schedule a call or review portfolio. Sign off with the sender's name.
6. Tone: professional yet personable. NOT generic. NOT overly formal.
7. Total length: under 250 words.

Return format — plain text only:
Subject: <subject line>

<email body>"""
    )

    return prompt | llm | StrOutputParser()


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

class EmailGenerator:
    """Wraps both chains and the portfolio manager into a single interface."""

    def __init__(self, groq_api_key: str, model: str = "llama-3.3-70b-versatile"):
        self._llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model,
            temperature=0.7,
        )
        self._extract_chain = make_extract_chain(self._llm)
        self._email_chain = make_email_chain(self._llm)

    def extract_job_info(self, jd_text: str) -> dict:
        raw = self._extract_chain.invoke({"job_description": jd_text})
        try:
            return _clean_json(raw)
        except Exception:
            # Fallback: return raw text in a dict so the app doesn't crash
            return {
                "role": "Unknown",
                "company": "Unknown",
                "experience": "Not specified",
                "skills": [],
                "description": raw[:300],
            }

    def generate_email(
        self,
        job_info: dict,
        portfolio_projects: list[dict],
        sender_name: str,
        sender_role: str,
        sender_bio: str,
    ) -> str:
        # Format portfolio links for prompt
        if portfolio_projects:
            links_text = "\n".join(
                f"- [{p['title']}]({p['project_link']}): {p['description']}"
                for p in portfolio_projects
            )
        else:
            links_text = "No specific projects retrieved — mention GitHub profile."

        return self._email_chain.invoke(
            {
                "sender_name": sender_name,
                "sender_role": sender_role,
                "sender_bio": sender_bio,
                "role": job_info.get("role", "the position"),
                "company": job_info.get("company", "your company"),
                "experience": job_info.get("experience", "Not specified"),
                "skills": ", ".join(job_info.get("skills", [])),
                "description": job_info.get("description", ""),
                "portfolio_links": links_text,
            }
        )
