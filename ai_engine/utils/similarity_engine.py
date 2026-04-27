from ai_engine.models.embeddings import Embedder 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ai_engine.dataclasses import SimilarityMatch 
from ai_engine.settings import SIMILAR_TO_THRESHOLD


class SimilarityEngine:

    def __init__(self):
        self._model = Embedder()

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a list of texts. Returns normalized float32 array."""
        return self._model.encode(texts, normalize_embeddings=True)

    def embed_one(self, text: str) -> list[float]:
        """Embed a single text and return as plain list (for Neo4j storage)."""
        emb = self._model.encode([text], normalize_embeddings=True)[0]
        return emb.tolist()

    def find_similar(
        self,
        new_clauses:      list[dict],   # [{id, text, embedding}, ...]
        existing_clauses: list[dict],   # from db.get_all_clauses()
        threshold:        float = SIMILAR_TO_THRESHOLD
    ) -> list[SimilarityMatch]:
        """
        Compare new clause embeddings against all existing clause embeddings.
        Returns all pairs above the similarity threshold.
        """
        if not existing_clauses:
            return []

        new_matrix      = np.array([c['embedding'] for c in new_clauses])
        existing_matrix = np.array([c['embedding'] for c in existing_clauses])

        # Shape: (len(new), len(existing))
        scores = cosine_similarity(new_matrix, existing_matrix)

        matches = []
        for i, new_c in enumerate(new_clauses):
            for j, exist_c in enumerate(existing_clauses):
                score = float(scores[i][j])
                if score >= threshold:
                    matches.append(SimilarityMatch(
                        new_clause_id        = new_c['id'],
                        new_clause_text      = new_c['text'],
                        existing_clause_id   = exist_c['id'],
                        existing_clause_text = exist_c['text'],
                        existing_doc_title   = exist_c.get('doc_title', ''),
                        score                = round(score, 4)
                    ))
        return matches