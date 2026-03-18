# symptom_reference_service.py
import json
from functools import lru_cache

from app.utils.text_utils import (
    contains_normalized_phrase,
    normalize_specialty_name,
    unique_preserve_order,
)


class SymptomReferenceService:
    @staticmethod
    @lru_cache(maxsize=4)
    def load_symptoms(path: str = "app/data/symptoms_reference.json") -> list[dict]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def detect_symptoms(self, user_text: str) -> list[dict]:
        symptoms = self.load_symptoms()
        detected = []

        for symptom in symptoms:
            canonical_name = symptom["canonical_name"]
            synonyms = symptom.get("synonyms", [])
            terms = [canonical_name] + synonyms

            matched_terms = [
                term for term in terms
                if contains_normalized_phrase(user_text, term)
            ]

            if matched_terms:
                specialties = [
                    normalize_specialty_name(name)
                    for name in symptom.get("specialties", [])
                ]

                detected.append({
                    "canonical_name": canonical_name,
                    "matched_terms": unique_preserve_order(matched_terms),
                    "category": symptom["category"],
                    "severity_hint": symptom["severity_hint"],
                    "body_zone": symptom.get("body_zone"),
                    "specialties": unique_preserve_order(specialties),
                    "is_red_flag": symptom.get("is_red_flag", False),
                    "red_flag_message": symptom.get("red_flag_message"),
                })

        return detected