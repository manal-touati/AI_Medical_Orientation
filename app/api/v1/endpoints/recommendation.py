from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.questionnaire import QuestionnaireRequest
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.post("/", response_model=RecommendationResponse)
def get_recommendation(payload: QuestionnaireRequest, db: Session = Depends(get_db)):
    service = RecommendationService(db)
    return service.recommend(payload)