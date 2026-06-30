from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.feedback_repository import FeedbackRepository
from app.schemas.questionnaire import QuestionnaireRequest
from app.schemas.recommendation import FeedbackRequest, FeedbackResponse, RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/", response_model=RecommendationResponse)
def get_recommendation(payload: QuestionnaireRequest, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.recommend(payload)


@router.post("/{user_response_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(
    user_response_id: int,
    payload: FeedbackRequest,
    db: Session = Depends(get_db),
):
    repo = FeedbackRepository(db)
    entry = repo.create(
        user_response_id=user_response_id,
        is_helpful=payload.is_helpful,
        comment=payload.comment,
    )
    return {
        "id": entry.id,
        "user_response_id": entry.user_response_id,
        "is_helpful": entry.is_helpful,
        "comment": entry.comment,
    }