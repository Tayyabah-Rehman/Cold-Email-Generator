"""
portfolio.py — ChromaDB-backed portfolio store.

Uses a lightweight hash-based embedding (no model download required)
to store and query portfolio projects by tech stack similarity.
"""

import uuid
import math
import hashlib
import pandas as pd
import chromadb
from chromadb.api.types import EmbeddingFunction


# ---------------------------------------------------------------------------
# Custom embedding function (no ONNX / no internet required)
# ---------------------------------------------------------------------------

class TechStackEmbedder(EmbeddingFunction):
    """
    Fast, deterministic embedding for tech-stack strings.

    Each skill/tool is hashed into a 256-dim vector bucket.
    Cosine similarity then measures skill overlap — good enough
    for portfolio matching without any ML model downloads.
    """

    DIM = 256

    def __call__(self, input):  # noqa: A002  (chromadb signature)
        results = []
        for text in input:
            # Split on commas or spaces to get individual tokens
            tokens = [t.strip().lower() for t in text.replace(",", " ").split() if t.strip()]
            vec = [0.0] * self.DIM
            for token in tokens:
                h = int(hashlib.md5(token.encode()).hexdigest(), 16)
                idx = h % self.DIM
                vec[idx] += 1.0
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            results.append([x / norm for x in vec])
        return results


# ---------------------------------------------------------------------------
# Portfolio manager
# ---------------------------------------------------------------------------

class PortfolioManager:
    """Manages a ChromaDB collection of portfolio projects."""

    COLLECTION_NAME = "portfolio_projects"

    def __init__(self, csv_path: str = "data/portfolio.csv"):
        self.csv_path = csv_path
        self._embedder = TechStackEmbedder()
        self._client = chromadb.Client()
        self._collection = None
        self._loaded = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self):
        """Read CSV and upsert all projects into ChromaDB (idempotent)."""
        if self._loaded:
            return

        # Always start fresh so re-loads don't duplicate
        try:
            self._client.delete_collection(self.COLLECTION_NAME)
        except Exception:
            pass

        self._collection = self._client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self._embedder,
        )

        df = pd.read_csv(self.csv_path)
        df.dropna(subset=["Tech Stack", "Project Link"], inplace=True)

        ids, docs, metas = [], [], []
        for _, row in df.iterrows():
            ids.append(str(uuid.uuid4()))
            docs.append(str(row["Tech Stack"]))
            metas.append(
                {
                    "project_link": str(row.get("Project Link", "")),
                    "title": str(row.get("Project Title", "")),
                    "description": str(row.get("Description", "")),
                }
            )

        if ids:
            self._collection.add(documents=docs, metadatas=metas, ids=ids)

        self._loaded = True

    def query(self, skills: list, n_results: int = 5) -> list:
        """
        Return up to `n_results` projects whose tech stack best
        matches the provided skill keywords.

        Returns list of dicts with keys: title, project_link, description.
        """
        if not skills or not self._collection:
            return []

        query_text = " ".join(skills)
        count = self._collection.count()
        if count == 0:
            return []

        results = self._collection.query(
            query_texts=[query_text],
            n_results=min(n_results, count),
        )

        projects = []
        if results and results.get("metadatas"):
            for meta in results["metadatas"][0]:
                projects.append(
                    {
                        "title": meta.get("title", ""),
                        "project_link": meta.get("project_link", ""),
                        "description": meta.get("description", ""),
                    }
                )
        return projects
