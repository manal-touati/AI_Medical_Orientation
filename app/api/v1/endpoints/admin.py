from fastapi import APIRouter, Depends
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.genai_cache import GenAICache
from app.models.recommendation_result import RecommendationResult
from app.models.request_audit import RequestAudit
from app.models.user_response import UserResponse

router = APIRouter()


@router.get("/responses")
def list_responses(db: Session = Depends(get_db)):
    rows = db.query(UserResponse).order_by(desc(UserResponse.id)).limit(50).all()

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
    rows = db.query(RecommendationResult).order_by(desc(RecommendationResult.id)).limit(100).all()

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
    rows = db.query(GenAICache).order_by(desc(GenAICache.id)).limit(100).all()

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


@router.get("/history")
def request_history(db: Session = Depends(get_db)):
    rows = db.query(RequestAudit).order_by(desc(RequestAudit.id)).limit(200).all()

    return [
        {
            "id": row.id,
            "symptom_description": row.symptom_description,
            "top_specialty": row.top_specialty,
            "response_time_ms": row.response_time_ms,
            "prompt_tokens": row.prompt_tokens,
            "completion_tokens": row.completion_tokens,
            "total_tokens": row.total_tokens,
            "cache_hits": row.cache_hits,
            "cache_misses": row.cache_misses,
            "red_flag_triggered": row.red_flag_triggered,
            "samu_advised": row.samu_advised,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.get("/metrics")
def admin_metrics(db: Session = Depends(get_db)):
    total_requests = db.query(func.count(RequestAudit.id)).scalar() or 0
    avg_latency = db.query(func.avg(RequestAudit.response_time_ms)).scalar() or 0
    total_prompt_tokens = db.query(func.coalesce(func.sum(RequestAudit.prompt_tokens), 0)).scalar() or 0
    total_completion_tokens = db.query(func.coalesce(func.sum(RequestAudit.completion_tokens), 0)).scalar() or 0
    total_tokens = db.query(func.coalesce(func.sum(RequestAudit.total_tokens), 0)).scalar() or 0
    total_cache_hits = db.query(func.coalesce(func.sum(RequestAudit.cache_hits), 0)).scalar() or 0
    total_cache_misses = db.query(func.coalesce(func.sum(RequestAudit.cache_misses), 0)).scalar() or 0
    total_samu = db.query(func.count(RequestAudit.id)).filter(RequestAudit.samu_advised.is_(True)).scalar() or 0
    total_red_flags = db.query(func.count(RequestAudit.id)).filter(RequestAudit.red_flag_triggered.is_(True)).scalar() or 0
    cache_entries = db.query(func.count(GenAICache.id)).scalar() or 0

    total_cache_events = total_cache_hits + total_cache_misses
    cache_hit_ratio = round((total_cache_hits / total_cache_events) * 100, 2) if total_cache_events else 0.0

    latest = db.query(RequestAudit).order_by(desc(RequestAudit.id)).limit(10).all()

    return {
        "kpis": {
            "total_requests": total_requests,
            "average_response_time_ms": round(float(avg_latency), 2),
            "prompt_tokens": int(total_prompt_tokens),
            "completion_tokens": int(total_completion_tokens),
            "total_tokens": int(total_tokens),
            "cache_entries": int(cache_entries),
            "cache_hit_ratio_percent": cache_hit_ratio,
            "samu_alert_count": int(total_samu),
            "red_flag_request_count": int(total_red_flags),
        },
        "recent": [
            {
                "id": row.id,
                "top_specialty": row.top_specialty,
                "response_time_ms": row.response_time_ms,
                "total_tokens": row.total_tokens,
                "cache_hits": row.cache_hits,
                "cache_misses": row.cache_misses,
                "samu_advised": row.samu_advised,
                "created_at": row.created_at,
            }
            for row in latest
        ]
    }