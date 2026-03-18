import json
import time
from functools import lru_cache

from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.request_audit_repository import RequestAuditRepository
from app.repositories.response_repository import ResponseRepository
from app.services.embedding_service import EmbeddingService
from app.services.genai_service import GenAIService
from app.services.preprocessing_service import PreprocessingService
from app.services.red_flag_service import RedFlagService
from app.services.scoring_service import ScoringService
from app.services.similarity_service import SimilarityService
from app.services.symptom_reference_service import SymptomReferenceService
from app.utils.constants import SAMU_ALERT_MESSAGE, SAMU_TRIGGER_SEVERITIES


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.similarity_service = SimilarityService()
        self.genai_service = GenAIService(db)
        self.response_repository = ResponseRepository(db)
        self.recommendation_repository = RecommendationRepository(db)
        self.request_audit_repository = RequestAuditRepository(db)
        self.symptom_reference_service = SymptomReferenceService()

    @staticmethod
    @lru_cache(maxsize=4)
    def load_specialties(path: str = "app/data/specialties.json") -> list[dict]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def build_default_explanation(specialty_name: str) -> str:
        return (
            f"La spécialité « {specialty_name} » peut être pertinente au regard de la similarité sémantique "
            f"et des règles métier appliquées aux symptômes saisis. "
            f"Il s'agit d'une orientation indicative et non d'un diagnostic médical."
        )

    @staticmethod
    def build_semantic_user_text(user_text: str, detected_symptoms: list[dict]) -> str:
        canonical_symptoms = [item["canonical_name"] for item in detected_symptoms]
        if not canonical_symptoms:
            return user_text

        canonical_part = ", ".join(canonical_symptoms)
        return f"{user_text} Symptômes canoniques détectés : {canonical_part}"

    @staticmethod
    def build_specialty_corpus(specialties: list[dict]) -> list[str]:
        return [
            (
                f"{item['name']}. "
                f"{item['description']}. "
                f"Symptômes associés : {item['symptoms_associated']}. "
                f"Indications : {item.get('indications', '')}. "
                f"Red flags : {item.get('red_flags', '')}"
            )
            for item in specialties
        ]

    def recommend(self, payload):
        started_at = time.perf_counter()

        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        cache_hits = 0
        cache_misses = 0

        user_response = self.response_repository.create(payload)

        user_text = PreprocessingService.build_user_text(
            symptom_description=payload.symptom_description,
            intensity=payload.intensity,
            duration=payload.duration,
            location=payload.location,
            additional_context=payload.additional_context,
        )

        enriched_text = None
        if settings.GENAI_ENABLE and len(payload.symptom_description.split()) < settings.GENAI_MIN_WORDS_THRESHOLD:
            enrich_meta = self.genai_service.enrich_short_input(payload.symptom_description)
            prompt_tokens += enrich_meta["prompt_tokens"]
            completion_tokens += enrich_meta["completion_tokens"]
            total_tokens += enrich_meta["total_tokens"]
            cache_hits += 1 if enrich_meta["cache_hit"] else 0
            cache_misses += 0 if enrich_meta["cache_hit"] else 1

            if enrich_meta["text"]:
                enriched_text = enrich_meta["text"]
                user_text = PreprocessingService.build_user_text(
                    symptom_description=enriched_text,
                    intensity=payload.intensity,
                    duration=payload.duration,
                    location=payload.location,
                    additional_context=payload.additional_context,
                )

        detected_symptoms = self.symptom_reference_service.detect_symptoms(user_text)

        keyword_red_flags = RedFlagService.detect(user_text)
        symptom_red_flags = RedFlagService.from_detected_symptoms(detected_symptoms)
        detected_red_flags = RedFlagService.merge_red_flags(keyword_red_flags, symptom_red_flags)
        warning = RedFlagService.build_warning(detected_red_flags)

        semantic_user_text = self.build_semantic_user_text(user_text, detected_symptoms)

        specialties = self.load_specialties()
        specialty_texts = self.build_specialty_corpus(specialties)

        user_vector = self.embedding_service.encode([semantic_user_text])[0]
        specialty_vectors = self.embedding_service.encode(specialty_texts)
        similarities = self.similarity_service.compute_similarity(user_vector, specialty_vectors)

        scored_results = []

        for specialty, semantic_score in zip(specialties, similarities):
            location_bonus = ScoringService.compute_location_bonus(payload.location, specialty["name"])
            intensity_bonus = ScoringService.compute_intensity_bonus(payload.intensity, specialty["name"])
            _, red_flag_bonus = ScoringService.detect_red_flags(user_text, specialty)

            symptom_reference_bonus = ScoringService.compute_symptom_reference_bonus(
                detected_symptoms=detected_symptoms,
                specialty_name=specialty["name"],
            )

            final_score = ScoringService.compute_final_score(
                semantic_score=float(semantic_score),
                location_bonus=location_bonus,
                intensity_bonus=intensity_bonus,
                red_flag_bonus=red_flag_bonus,
                symptom_reference_bonus=symptom_reference_bonus,
            )

            scored_results.append({
                "specialty": specialty,
                "semantic_score": round(float(semantic_score), 4),
                "location_bonus": round(location_bonus, 4),
                "intensity_bonus": round(intensity_bonus, 4),
                "red_flag_bonus": round(red_flag_bonus, 4),
                "symptom_reference_bonus": round(symptom_reference_bonus, 4),
                "final_score": final_score,
            })

        sorted_all = sorted(scored_results, key=lambda x: x["final_score"], reverse=True)

        ranked = [
            item for item in sorted_all
            if item["final_score"] >= settings.SIMILARITY_THRESHOLD
        ][:settings.TOP_K_RECOMMENDATIONS]

        if len(ranked) < settings.TOP_K_RECOMMENDATIONS:
            already_selected = {item["specialty"]["name"] for item in ranked}
            for item in sorted_all:
                specialty_name = item["specialty"]["name"]
                if specialty_name not in already_selected:
                    ranked.append(item)
                    already_selected.add(specialty_name)

                if len(ranked) >= settings.TOP_K_RECOMMENDATIONS:
                    break

        results = []
        for item in ranked:
            specialty = item["specialty"]

            explanation = None
            if settings.GENAI_ENABLE:
                explanation_meta = self.genai_service.generate_explanation(
                    user_text=semantic_user_text,
                    specialty_name=specialty["name"],
                    specialty_description=specialty["description"],
                )
                prompt_tokens += explanation_meta["prompt_tokens"]
                completion_tokens += explanation_meta["completion_tokens"]
                total_tokens += explanation_meta["total_tokens"]
                cache_hits += 1 if explanation_meta["cache_hit"] else 0
                cache_misses += 0 if explanation_meta["cache_hit"] else 1
                explanation = explanation_meta["text"]

            if not explanation:
                explanation = self.build_default_explanation(specialty["name"])

            results.append({
                "specialty_name": specialty["name"],
                "similarity_score": item["final_score"],
                "explanation": explanation,
            })

        if not results:
            results = [{
                "specialty_name": "Médecine générale",
                "similarity_score": 0.0,
                "explanation": (
                    "Aucune spécialité n'a dépassé le seuil minimal. "
                    "Un médecin généraliste constitue un bon premier point de contact. "
                    "Il s'agit d'une orientation indicative et non d'un diagnostic médical."
                ),
            }]

        self.recommendation_repository.create_many(
            user_response_id=user_response.id,
            recommendations=results,
        )

        response_time_ms = int((time.perf_counter() - started_at) * 1000)
        top_specialty = results[0]["specialty_name"] if results else None
        samu_advised = any(
            flag["severity"].lower() in SAMU_TRIGGER_SEVERITIES
            for flag in detected_red_flags
        )

        self.request_audit_repository.create(
            symptom_description=payload.symptom_description,
            top_specialty=top_specialty,
            response_time_ms=response_time_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cache_hits=cache_hits,
            cache_misses=cache_misses,
            red_flag_triggered=bool(detected_red_flags),
            samu_advised=samu_advised,
        )

        return {
            "enriched_input": enriched_text,
            "recommendations": results,
            "red_flags": detected_red_flags,
            "warning": SAMU_ALERT_MESSAGE if samu_advised else warning,
            "detected_symptoms": detected_symptoms,
            "meta": {
                "response_time_ms": response_time_ms,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "cache_hits": cache_hits,
                "cache_misses": cache_misses,
                "samu_advised": samu_advised,
            }
        }