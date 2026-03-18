# cache_service.py
from sqlalchemy.orm import Session

from app.models.genai_cache import GenAICache


class CacheService:
    def __init__(self, db: Session):
        self.db = db

    def get(self, cache_key: str) -> GenAICache | None:
        return (
            self.db.query(GenAICache)
            .filter(GenAICache.cache_key == cache_key)
            .first()
        )

    def set(
        self,
        cache_key: str,
        cache_type: str,
        input_text: str,
        output_text: str
    ) -> GenAICache:
        existing = self.get(cache_key)
        if existing:
            return existing

        obj = GenAICache(
            cache_key=cache_key,
            cache_type=cache_type,
            input_text=input_text,
            output_text=output_text
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj