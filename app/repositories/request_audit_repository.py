from sqlalchemy.orm import Session

from app.models.request_audit import RequestAudit


class RequestAuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        symptom_description: str,
        top_specialty: str | None,
        response_time_ms: int,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cache_hits: int,
        cache_misses: int,
        red_flag_triggered: bool,
        samu_advised: bool,
    ) -> RequestAudit:
        obj = RequestAudit(
            symptom_description=symptom_description,
            top_specialty=top_specialty,
            response_time_ms=response_time_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cache_hits=cache_hits,
            cache_misses=cache_misses,
            red_flag_triggered=red_flag_triggered,
            samu_advised=samu_advised,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj