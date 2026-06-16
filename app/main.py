"""
main.py — AI Cold Email Generator · Streamlit UI
Run via:  python run.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

import streamlit as st
from app.portfolio import PortfolioManager
from app.chains import EmailGenerator

# ── page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Cold Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS — clean light theme ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #f5f6fa !important;
    font-family: 'Inter', sans-serif !important;
    color: #1a1f36 !important;
}

section.main .block-container {
    padding: 0 2rem 3rem !important;
    max-width: 1380px;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e4e7f0 !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }

/* ── hero ── */
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 2.6rem 2.5rem 2rem;
    margin: 1.5rem 0 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(102,126,234,0.28);
}
.hero::before {
    content:'';
    position:absolute; top:-80px; right:-60px;
    width:300px; height:300px;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
    border-radius:50%;
}
.hero::after {
    content:'';
    position:absolute; bottom:-50px; left:5%;
    width:200px; height:200px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius:50%;
}
.hero-badge {
    display:inline-flex; align-items:center; gap:6px;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius:20px; padding:4px 14px;
    font-size:0.71rem; font-weight:600; color:#fff;
    letter-spacing:0.08em; text-transform:uppercase; margin-bottom:1rem;
}
.hero h1 {
    font-size:2.4rem; font-weight:700; color:#fff;
    margin:0 0 0.5rem; line-height:1.2;
    text-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.hero p { color:rgba(255,255,255,0.82); font-size:0.97rem; line-height:1.65; margin:0; max-width:620px; }
.hero-stats { display:flex; gap:2.5rem; margin-top:1.6rem; }
.stat { display:flex; flex-direction:column; }
.stat-num { font-size:1.5rem; font-weight:700; color:#fff; }
.stat-label { font-size:0.68rem; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:0.07em; margin-top:2px; }

/* ── flow steps ── */
.flow-steps { display:flex; margin:0 0 1.8rem; gap:0; }
.flow-step {
    flex:1; text-align:center;
    background:#fff; border:1px solid #e4e7f0;
    padding:0.75rem 0.4rem; position:relative;
    transition: background 0.2s;
}
.flow-step:first-child { border-radius:10px 0 0 10px; }
.flow-step:last-child  { border-radius:0 10px 10px 0; }
.flow-step:hover { background:#f0f2ff; }
.flow-step-num { font-size:1.1rem; }
.flow-step-label { font-size:0.62rem; color:#8b92b8; margin-top:3px; text-transform:uppercase; letter-spacing:0.05em; font-weight:500; }
.flow-arrow { position:absolute; right:-7px; top:50%; transform:translateY(-50%); color:#c5cae0; font-size:1rem; z-index:2; }

/* ── section label ── */
.section-label {
    font-size:0.7rem; font-weight:600; color:#8b92b8;
    text-transform:uppercase; letter-spacing:0.1em;
    margin-bottom:0.6rem; display:flex; align-items:center; gap:8px;
}
.section-label::after { content:''; flex:1; height:1px; background: linear-gradient(90deg, #e4e7f0, transparent); }

/* ── textarea ── */
.stTextArea textarea {
    background: #ffffff !important;
    border: 1.5px solid #dde1ef !important;
    border-radius: 12px !important;
    color: #1a1f36 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
}
.stTextArea textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.14) !important;
}
.stTextArea textarea::placeholder { color: #b0b7d4 !important; }

/* ── text inputs ── */
.stTextInput input {
    background: #fff !important;
    border: 1.5px solid #dde1ef !important;
    border-radius: 8px !important;
    color: #1a1f36 !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.12) !important;
}
.stSelectbox > div > div {
    background: #fff !important;
    border: 1.5px solid #dde1ef !important;
    border-radius: 8px !important;
    color: #1a1f36 !important;
}

/* ── generate button ── */
.stButton > button {
    width:100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.72rem 2rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 18px rgba(102,126,234,0.38) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    box-shadow: 0 6px 26px rgba(102,126,234,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── email window ── */
.email-wrapper {
    background: #fff;
    border: 1.5px solid #e4e7f0;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.email-topbar {
    background: #f5f6fa;
    border-bottom: 1px solid #e4e7f0;
    padding: 0.65rem 1.2rem;
    display: flex; align-items: center; gap: 7px;
}
.email-dot { width:11px; height:11px; border-radius:50%; }
.email-fname {
    font-size:0.72rem; color:#a0a8c8;
    font-family:'JetBrains Mono', monospace;
    margin-left:8px;
}
.email-subject-bar {
    padding: 0.8rem 1.5rem 0;
    font-size:0.72rem; font-weight:700; color:#667eea;
    text-transform:uppercase; letter-spacing:0.07em;
    border-bottom: 1px solid #f0f2fa;
}
.email-body {
    padding: 1.3rem 1.6rem 1.5rem;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 0.92rem; line-height: 1.85;
    color: #2a2f50; white-space: pre-wrap;
    min-height: 280px;
}
.email-placeholder {
    padding: 3rem 1.5rem;
    min-height: 280px; display:flex;
    align-items:center; justify-content:center;
    flex-direction:column; gap:0.8rem;
}
.email-placeholder-icon { font-size:2.8rem; opacity:0.25; }
.email-placeholder-text { color:#b0b7d4; font-size:0.87rem; text-align:center; line-height:1.6; }

/* ── info cards ── */
.info-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:0.8rem; margin:0.8rem 0; }
.info-card {
    background:#fff; border:1.5px solid #e4e7f0;
    border-radius:12px; padding:1rem 1.1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.info-card-label { font-size:0.67rem; color:#a0a8c8; text-transform:uppercase; letter-spacing:0.09em; font-weight:600; margin-bottom:0.3rem; }
.info-card-value { font-size:0.93rem; color:#1a1f36; font-weight:600; }

/* ── skill pills ── */
.skills-wrap { display:flex; flex-wrap:wrap; gap:6px; margin:0.4rem 0 0.8rem; }
.skill-pill {
    background:#f0f2ff; border:1.5px solid #d4d9ff;
    color:#5566cc; border-radius:20px;
    padding:3px 12px; font-size:0.75rem; font-weight:500;
}

/* ── project cards ── */
.proj-card {
    background:#fff; border:1.5px solid #e4e7f0;
    border-left:3px solid #667eea; border-radius:10px;
    padding:0.9rem 1.1rem; margin-bottom:0.6rem;
    box-shadow:0 1px 6px rgba(0,0,0,0.04);
    transition: border-left-color 0.2s, box-shadow 0.2s;
}
.proj-card:hover { border-left-color:#764ba2; box-shadow:0 3px 14px rgba(102,126,234,0.12); }
.proj-card-title { font-size:0.88rem; font-weight:600; color:#1a1f36; margin-bottom:0.2rem; }
.proj-card-desc { font-size:0.79rem; color:#6b7599; line-height:1.55; margin-bottom:0.35rem; }
.proj-card-link { font-size:0.74rem; color:#667eea; font-family:'JetBrains Mono',monospace; text-decoration:none; }
.proj-card-link:hover { color:#764ba2; }

/* ── sidebar sections ── */
.sb-section {
    background:#f9faff; border:1px solid #eceef8;
    border-radius:10px; padding:1rem; margin-bottom:0.9rem;
}
.sb-title {
    font-size:0.67rem; color:#a0a8c8; font-weight:700;
    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;
}
.api-status {
    display:inline-flex; align-items:center; gap:6px;
    padding:4px 11px; border-radius:20px;
    font-size:0.71rem; font-weight:600; margin-top:4px;
}
.api-ok     { background:#ecfdf5; border:1px solid #a7f3d0; color:#059669; }
.api-miss   { background:#fff1f2; border:1px solid #fecdd3; color:#e11d48; }

/* ── divider ── */
.divider { height:1px; background:linear-gradient(90deg,transparent,#dde1ef,transparent); margin:1.6rem 0; }

/* ── download button ── */
[data-testid="stDownloadButton"] > button {
    background:#f0f2ff !important;
    border:1.5px solid #d4d9ff !important;
    color:#5566cc !important;
    border-radius:8px !important;
    font-size:0.84rem !important;
    font-weight:500 !important;
    box-shadow:none !important;
    margin-top:0.5rem;
}
[data-testid="stDownloadButton"] > button:hover {
    background:#e4e8ff !important;
    box-shadow: 0 2px 10px rgba(102,126,234,0.2) !important;
    transform:none !important;
}

/* ── labels ── */
label, .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    color: #4a5280 !important; font-size: 0.82rem !important; font-weight: 500 !important;
}

/* ── spinner ── */
.stSpinner > div { border-top-color: #667eea !important; }
</style>
""", unsafe_allow_html=True)

# ── read API key — supports BOTH variable names ───────────────────────────────
env_key = (
    os.getenv("GROQ_API_KEY", "").strip()
    or os.getenv("GEMINI_API_KEY", "").strip()
)

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0.4rem 0 1.4rem;">
        <span style="font-size:1.8rem;">✉️</span>
        <div>
            <div style="font-weight:700;color:#1a1f36;font-size:1rem;line-height:1.2;">Cold Email AI</div>
            <div style="font-size:0.7rem;color:#a0a8c8;">LangChain · ChromaDB · Groq</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── API config section ──
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">🔑 API Configuration</div>', unsafe_allow_html=True)

    if env_key:
        # Key found in .env — show status, no input needed
        groq_api_key = env_key
        st.markdown('<span class="api-status api-ok">✓ API key loaded from .env</span>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:0.74rem;color:#a0a8c8;margin-top:0.6rem;line-height:1.5;">'
            'Your <code style="background:#eceef8;padding:1px 5px;border-radius:4px;font-size:0.72rem;">GEMINI_API_KEY</code> '
            'in <code style="background:#eceef8;padding:1px 5px;border-radius:4px;font-size:0.72rem;">.env</code> '
            'is being used as the Groq key. No need to enter anything here.</p>',
            unsafe_allow_html=True,
        )
    else:
        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Free key at console.groq.com — or add GROQ_API_KEY to your .env file",
        )
        if groq_api_key:
            st.markdown('<span class="api-status api-ok">✓ Key entered</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="api-status api-miss">✗ Key not found</span>', unsafe_allow_html=True)
            st.markdown(
                '<p style="font-size:0.74rem;color:#a0a8c8;margin-top:0.5rem;line-height:1.5;">'
                'Add <code style="background:#eceef8;padding:1px 5px;border-radius:4px;">GROQ_API_KEY=gsk_...</code> '
                'to your <code style="background:#eceef8;padding:1px 5px;border-radius:4px;">.env</code> file '
                'to skip this step permanently.</p>',
                unsafe_allow_html=True,
            )

    model_choice = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"],
        help="70b = best quality · 8b = fastest",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── sender profile ──
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">👤 Your Profile</div>', unsafe_allow_html=True)
    sender_name = st.text_input("Full Name", value="Tayyabah Rehman")
    sender_role = st.text_input("Title / Status", value="MPhil AI Student & ML Engineer")
    sender_bio  = st.text_area(
        "Short Bio",
        value=(
            "MPhil AI student at University of the Punjab specializing in computer vision "
            "and deep learning. I build production-grade systems: an ALPR pipeline (95.11% "
            "OCR accuracy), multi-road vehicle counting with web UI, and AI automation tools. "
            "Seeking AI/ML engineering roles."
        ),
        height=110,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── portfolio & settings ──
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">📂 Portfolio & Settings</div>', unsafe_allow_html=True)
    uploaded_csv = st.file_uploader("Custom portfolio.csv", type=["csv"])
    n_projects   = st.slider("Portfolio matches", 1, 5, 3)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.68rem;color:#c0c6e0;text-align:center;margin-top:0.5rem;">'
        '<a href="https://github.com/Tayyabah-Rehman" style="color:#a0a8c8;text-decoration:none;">'
        'github.com/Tayyabah-Rehman</a></div>',
        unsafe_allow_html=True,
    )

# ── session state ─────────────────────────────────────────────────────────────
for k, v in [
    ("email_output",""), ("job_info",{}),
    ("matched_projects",[]), ("portfolio_loaded",False), ("portfolio_manager",None),
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── load portfolio ────────────────────────────────────────────────────────────
import tempfile
default_csv = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "portfolio.csv",
)
csv_path = default_csv
if uploaded_csv is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_csv.read())
        csv_path = tmp.name

if not st.session_state.portfolio_loaded:
    with st.spinner("Loading portfolio into ChromaDB…"):
        pm = PortfolioManager(csv_path=csv_path)
        pm.load()
        st.session_state.portfolio_manager = pm
        st.session_state.portfolio_loaded  = True

pm: PortfolioManager = st.session_state.portfolio_manager

# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI-Powered · LangChain · ChromaDB · Groq LLaMA</div>
    <h1>AI Email Generator</h1>
    <p>Paste any job description. The AI extracts requirements, queries your portfolio via ChromaDB vector search, and writes a personalized email — in under 10 seconds.</p>
    <div class="hero-stats">
        <div class="stat"><span class="stat-num">2</span><span class="stat-label">LangChain Chains</span></div>
        <div class="stat"><span class="stat-num">14</span><span class="stat-label">Portfolio Projects</span></div>
        <div class="stat"><span class="stat-num">~8s</span><span class="stat-label">Generation Time</span></div>
        <div class="stat"><span class="stat-num">4</span><span class="stat-label">LLM Models</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── pipeline flow ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="flow-steps">
    <div class="flow-step"><div class="flow-step-num">📋</div><div class="flow-step-label">Paste JD</div><div class="flow-arrow">›</div></div>
    <div class="flow-step"><div class="flow-step-num">🔍</div><div class="flow-step-label">LLM Extracts</div><div class="flow-arrow">›</div></div>
    <div class="flow-step"><div class="flow-step-num">🗄️</div><div class="flow-step-label">ChromaDB Match</div><div class="flow-arrow">›</div></div>
    <div class="flow-step"><div class="flow-step-num">✍️</div><div class="flow-step-label">Email Written</div><div class="flow-arrow">›</div></div>
    <div class="flow-step"><div class="flow-step-num">📬</div><div class="flow-step-label">Send & Win</div></div>
</div>
""", unsafe_allow_html=True)

# ── main two-column layout ────────────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-label">📋 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        "jd", height=340,
        placeholder=(
            "Paste the full job description here…\n\n"
            "e.g. We are looking for an ML Engineer with Python, YOLOv8,\n"
            "computer vision, and real-time video analytics experience…"
        ),
        label_visibility="collapsed",
    )
    c1, c2 = st.columns([3, 1])
    with c1:
        gen_btn = st.button("⚡  Generate Email", use_container_width=True)
    with c2:
        if st.button("✕ Clear", use_container_width=True):
            st.session_state.email_output     = ""
            st.session_state.job_info         = {}
            st.session_state.matched_projects = []
            st.rerun()

with right:
    st.markdown('<div class="section-label">📬 Generated Email</div>', unsafe_allow_html=True)

    if st.session_state.email_output:
        raw = st.session_state.email_output
        if raw.startswith("Subject:"):
            lines     = raw.split("\n", 2)
            subj_line = lines[0].replace("Subject:", "").strip()
            body      = "\n".join(lines[2:]).strip() if len(lines) > 2 else lines[-1]
        else:
            subj_line, body = "", raw

        subj_html = f'<div class="email-subject-bar">✉ Subject: {subj_line}</div>' if subj_line else ""

        st.markdown(f"""
        <div class="email-wrapper">
            <div class="email-topbar">
                <span class="email-dot" style="background:#ff5f57;"></span>
                <span class="email-dot" style="background:#febc2e;"></span>
                <span class="email-dot" style="background:#28c840;"></span>
                <span class="email-fname">cold_email.txt</span>
            </div>
            {subj_html}
            <div class="email-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "⬇️  Download as .txt",
            data=st.session_state.email_output,
            file_name="cold_email.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.markdown("""
        <div class="email-wrapper">
            <div class="email-topbar">
                <span class="email-dot" style="background:#ff5f57;"></span>
                <span class="email-dot" style="background:#febc2e;"></span>
                <span class="email-dot" style="background:#28c840;"></span>
            </div>
            <div class="email-placeholder">
                <div class="email-placeholder-icon">✉️</div>
                <div class="email-placeholder-text">
                    Your personalized cold email will appear here.<br>
                    Paste a job description and click <strong>Generate Email</strong>.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── generation ────────────────────────────────────────────────────────────────
if gen_btn:
    if not groq_api_key:
        st.error("⚠️  No API key found. Add GROQ_API_KEY to your .env file, or paste it in the sidebar.")
        st.stop()
    if not jd_text.strip():
        st.error("⚠️  Please paste a job description first.")
        st.stop()

    try:
        generator = EmailGenerator(groq_api_key=groq_api_key, model=model_choice)

        with st.spinner("🔍  Extracting job details…"):
            job_info = generator.extract_job_info(jd_text)
            st.session_state.job_info = job_info

        with st.spinner("🗄️  Querying ChromaDB for portfolio matches…"):
            matched = pm.query(job_info.get("skills", []), n_results=n_projects)
            st.session_state.matched_projects = matched

        with st.spinner("✍️  Writing your cold email…"):
            email = generator.generate_email(
                job_info=job_info, portfolio_projects=matched,
                sender_name=sender_name, sender_role=sender_role, sender_bio=sender_bio,
            )
            st.session_state.email_output = email

        st.rerun()
    except Exception as e:
        st.error(f"❌  Error: {e}")

# ── extracted job info ────────────────────────────────────────────────────────
if st.session_state.job_info:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🔍 Extracted Job Intelligence</div>', unsafe_allow_html=True)
    ji = st.session_state.job_info

    st.markdown(f"""
    <div class="info-grid">
        <div class="info-card">
            <div class="info-card-label">Position</div>
            <div class="info-card-value">{ji.get("role","—")}</div>
        </div>
        <div class="info-card">
            <div class="info-card-label">Company</div>
            <div class="info-card-value">{ji.get("company","—")}</div>
        </div>
        <div class="info-card">
            <div class="info-card-label">Experience</div>
            <div class="info-card-value">{ji.get("experience","—")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    skills = ji.get("skills", [])
    if skills:
        pills = "".join(f'<span class="skill-pill">{s}</span>' for s in skills)
        st.markdown(
            '<div style="font-size:0.7rem;font-weight:600;color:#a0a8c8;text-transform:uppercase;'
            'letter-spacing:0.09em;margin-bottom:0.4rem;">Required Skills</div>'
            f'<div class="skills-wrap">{pills}</div>',
            unsafe_allow_html=True,
        )

    desc = ji.get("description","")
    if desc:
        st.markdown(
            f'<div class="info-card" style="margin-top:0.5rem;">'
            f'<div class="info-card-label">Role Summary</div>'
            f'<div style="color:#4a5280;font-size:0.88rem;line-height:1.65;margin-top:0.3rem;">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── matched portfolio ─────────────────────────────────────────────────────────
if st.session_state.matched_projects:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🗂️ ChromaDB Portfolio Matches</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#a0a8c8;font-size:0.82rem;margin-bottom:0.8rem;">'
        'These projects were vector-matched to the job\'s required skills and referenced in your email.</p>',
        unsafe_allow_html=True,
    )
    for p in st.session_state.matched_projects:
        link = p.get("project_link","")
        link_html = f'<a class="proj-card-link" href="{link}" target="_blank">{link}</a>' if link else ""
        st.markdown(
            f'<div class="proj-card">'
            f'<div class="proj-card-title">📁 {p["title"]}</div>'
            f'<div class="proj-card-desc">{p["description"]}</div>'
            f'{link_html}</div>',
            unsafe_allow_html=True,
        )
