import json

from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.response_repository import ResponseRepository
from app.services.embedding_service import EmbeddingService
from app.services.genai_service import GenAIService
from app.services.preprocessing_service import PreprocessingService
from app.services.red_flag_service import RedFlagService
from app.services.scoring_service import ScoringService
from app.services.similarity_service import SimilarityService


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.similarity_service = SimilarityService()
        self.genai_service = GenAIService(db)
        self.response_repository = ResponseRepository(db)
        self.recommendation_repository = RecommendationRepository(db)

    def load_specialties(self, path: str = "app/data/specialties.json") -> list[dict]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def build_default_explanation(specialty_name: str) -> str:
        return (
            f"{specialty_name} may be relevant based on the semantic similarity "
            f"and rule-based matching with the provided symptoms. "
            f"This is not a medical diagnosis."
        )

    def recommend(self, payload):
        user_response = self.response_repository.create(payload)

        user_text = PreprocessingService.build_user_text(
            symptom_description=payload.symptom_description,
            intensity=payload.intensity,
            duration=payload.duration,
            location=payload.location,
            additional_context=payload.additional_context
        )

        enriched_text = None
        if settings.GENAI_ENABLE and len(payload.symptom_description.split()) < settings.GENAI_MIN_WORDS_THRESHOLD:
            enriched_candidate = self.genai_service.enrich_short_input(payload.symptom_description)
            if enriched_candidate:
                enriched_text = enriched_candidate
                user_text = PreprocessingService.build_user_text(
                    symptom_description=enriched_text,
                    intensity=payload.intensity,
                    duration=payload.duration,
                    location=payload.location,
                    additional_context=payload.additional_context
                )

        detected_red_flags = RedFlagService.detect(user_text)

        specialties = self.load_specialties()

        specialty_texts = [
            (
                f"{item['name']}. "
                f"{item['description']}. "
                f"Symptoms: {item['symptoms_associated']}. "
                f"Indications: {item.get('indications', '')}. "
                f"Red flags: {item.get('red_flags', '')}"
            )
            for item in specialties
        ]

        user_vector = self.embedding_service.encode([user_text])[0]
        specialty_vectors = self.embedding_service.encode(specialty_texts)
        similarities = self.similarity_service.compute_similarity(user_vector, specialty_vectors)

        scored_results = []

        for specialty, semantic_score in zip(specialties, similarities):
            location_bonus = ScoringService.compute_location_bonus(payload.location, specialty["name"])
            intensity_bonus = ScoringService.compute_intensity_bonus(payload.intensity, specialty["name"])
            red_flag_detected, red_flag_bonus = ScoringService.detect_red_flags(user_text, specialty)

            final_score = ScoringService.compute_final_score(
                semantic_score=float(semantic_score),
                location_bonus=location_bonus,
                intensity_bonus=intensity_bonus,
                red_flag_bonus=red_flag_bonus
            )

            scored_results.append({
                "specialty": specialty,
                "semantic_score": round(float(semantic_score), 4),
                "location_bonus": round(location_bonus, 4),
                "intensity_bonus": round(intensity_bonus, 4),
                "red_flag_bonus": round(red_flag_bonus, 4),
                "red_flag_detected": red_flag_detected,
                "final_score": final_score
            })

        filtered_results = [
            item for item in scored_results
            if item["final_score"] >= settings.SIMILARITY_THRESHOLD
        ]

        ranked = sorted(
            filtered_results,
            key=lambda x: x["final_score"],
            reverse=True
        )[:settings.TOP_K_RECOMMENDATIONS]

        results = []
        for item in ranked:
            specialty = item["specialty"]

            explanation = None
            if settings.GENAI_ENABLE:
                explanation = self.genai_service.generate_explanation(
                    user_text=user_text,
                    specialty_name=specialty["name"],
                    specialty_description=specialty["description"]
                )

            if not explanation:
                explanation = self.build_default_explanation(specialty["name"])

            results.append({
                "specialty_name": specialty["name"],
                "similarity_score": item["final_score"],
                "explanation": explanation
            })

        if not results:
            results = [{
                "specialty_name": "General Practice",
                "similarity_score": 0.0,
                "explanation": (
                    "No specialty reached the minimum threshold. "
                    "A general practitioner may be the best first point of contact. "
                    "This is not a medical diagnosis."
                )
            }]

        self.recommendation_repository.create_many(
            user_response_id=user_response.id,
            recommendations=results
        )

        return {
            "enriched_input": enriched_text,
            "recommendations": results,
            "red_flags": detected_red_flags,
            "warning": RedFlagService.build_warning(detected_red_flags)
        }