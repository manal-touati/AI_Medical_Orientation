from fastapi import APIRouter

from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.questionnaire import router as questionnaire_router
from app.api.v1.endpoints.recommendation import router as recommendation_router

router = APIRouter()
router.include_router(health_router, tags=["Health"])
router.include_router(questionnaire_router, prefix="/questionnaire", tags=["Questionnaire"])
router.include_router(recommendation_router, prefix="/recommendations", tags=["Recommendations"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])