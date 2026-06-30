from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.recommendation_feedback import RecommendationFeedback


class FeedbackRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_response_id: int, is_helpful: bool, comment: str | None = None) -> RecommendationFeedback:
        entry = RecommendationFeedback(
            user_response_id=user_response_id,
            is_helpful=is_helpful,
            comment=comment,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_stats(self) -> dict:
        total = self.db.query(func.count(RecommendationFeedback.id)).scalar() or 0
        positive = (
            self.db.query(func.count(RecommendationFeedback.id))
            .filter(RecommendationFeedback.is_helpful.is_(True))
            .scalar() or 0
        )
        negative = total - positive
        ratio = round((positive / total) * 100, 1) if total else 0.0

        return {
            "total_feedback": total,
            "positive": positive,
            "negative": negative,
            "positive_ratio_percent": ratio,
        }
