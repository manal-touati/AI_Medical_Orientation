from functools import lru_cache
from threading import Lock

from sentence_transformers import SentenceTransformer

from app.core.config import settings

_MODEL_LOCK = Lock()


@lru_cache(maxsize=2)
def _load_model(model_name: str) -> SentenceTransformer:
    with _MODEL_LOCK:
        # Forcer CPU pour éviter les problèmes de meta tensor / auto device
        model = SentenceTransformer(model_name, device="cpu")
        return model


class EmbeddingService:
    def __init__(self):
        self.model = _load_model(settings.SBERT_MODEL)

    def encode(self, texts: list[str]):
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=16,
            show_progress_bar=False,
        )