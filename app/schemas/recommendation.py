from pydantic import BaseModel
from typing import List, Optional


class RecommendationItem(BaseModel):
    specialty_name: str
    similarity_score: float
    explanation: Optional[str] = None


class RedFlagItem(BaseModel):
    keyword: str
    severity: str
    message: str


class RecommendationResponse(BaseModel):
    enriched_input: Optional[str] = None
    recommendations: List[RecommendationItem]
    red_flags: List[RedFlagItem] = []
    warning: str