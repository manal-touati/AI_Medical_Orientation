# questionnaire.py
from pydantic import BaseModel, Field
from typing import Optional


class QuestionnaireRequest(BaseModel):
    symptom_description: str = Field(..., min_length=3)
    intensity: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    additional_context: Optional[str] = None