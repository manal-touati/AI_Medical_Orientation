from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.recommendation_result import RecommendationResult
from app.models.user_response import UserResponse
from app.models.genai_cache import GenAICache
router = APIRouter()


@router.get("/responses")
def list_responses(db: Session = Depends(get_db)):
    rows = db.query(UserResponse).order_by(desc(UserResponse.id)).limit(20).all()

    return [
        {
            "id": row.id,
            "symptom_description": row.symptom_description,
            "intensity": row.intensity,
            "duration": row.duration,
            "location": row.location,
            "additional_context": row.additional_context,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.get("/recommendations")
def list_recommendations(db: Session = Depends(get_db)):
    rows = db.query(RecommendationResult).order_by(desc(RecommendationResult.id)).limit(50).all()

    return [
        {
            "id": row.id,
            "user_response_id": row.user_response_id,
            "specialty_name": row.specialty_name,
            "similarity_score": row.similarity_score,
            "explanation": row.explanation,
            "created_at": row.created_at,
        }
        for row in rows
    ]



@router.get("/genai-cache")
def list_genai_cache(db: Session = Depends(get_db)):
    rows = db.query(GenAICache).order_by(desc(GenAICache.id)).limit(50).all()

    return [
        {
            "id": row.id,
            "cache_key": row.cache_key,
            "cache_type": row.cache_type,
            "input_text": row.input_text,
            "output_text": row.output_text,
            "created_at": row.created_at,
        }
        for row in rows
    ]