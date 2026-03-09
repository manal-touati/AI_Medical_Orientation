from sqlalchemy.orm import Session

from app.models.user_response import UserResponse
from app.schemas.questionnaire import QuestionnaireRequest


class ResponseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: QuestionnaireRequest) -> UserResponse:
        obj = UserResponse(
            symptom_description=payload.symptom_description,
            intensity=payload.intensity,
            duration=payload.duration,
            location=payload.location,
            additional_context=payload.additional_context,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj