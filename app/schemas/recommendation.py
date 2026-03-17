from typing import List, Optional

from pydantic import BaseModel, Field


class RecommendationItem(BaseModel):
    specialty_name: str
    similarity_score: float
    explanation: Optional[str] = None


class RedFlagItem(BaseModel):
    keyword: str
    severity: str
    message: str


class DetectedSymptomItem(BaseModel):
    canonical_name: str
    matched_terms: List[str]
    category: str
    severity_hint: str
    body_zone: Optional[str] = None
    specialties: List[str]
    is_red_flag: bool
    red_flag_message: Optional[str] = None


class RecommendationResponse(BaseModel):
    enriched_input: Optional[str] = None
    recommendations: List[RecommendationItem]
    red_flags: List[RedFlagItem] = Field(default_factory=list)
    warning: str
    detected_symptoms: List[DetectedSymptomItem] = Field(default_factory=list)