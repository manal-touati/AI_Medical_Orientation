from fastapi import APIRouter

router = APIRouter()

@router.get("/template")
def get_questionnaire_template():
    return {
        "fields": [
            "symptom_description",
            "intensity",
            "duration",
            "location",
            "additional_context"
        ]
    }