from sentence_transformers import SentenceTransformer
from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.SBERT_MODEL)

    def encode(self, texts: list[str]):
        return self.model.encode(texts, convert_to_numpy=True)