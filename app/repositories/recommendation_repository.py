
# recommendation_repository.py

from sqlalchemy.orm import Session

from app.models.recommendation_result import RecommendationResult


class RecommendationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_many(self, user_response_id: int, recommendations: list[dict]) -> list[RecommendationResult]:
        results = []

        for item in recommendations:
            result = RecommendationResult(
                user_response_id=user_response_id,
                specialty_name=item["specialty_name"],
                similarity_score=item["similarity_score"],
                explanation=item.get("explanation"),
            )
            self.db.add(result)
            results.append(result)

        self.db.commit()

        for result in results:
            self.db.refresh(result)

        return results