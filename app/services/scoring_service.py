from app.utils.constants import (
    INTENSITY_BONUS_SPECIALTIES,
    SPECIALTY_LOCATION_KEYWORDS,
)
from app.utils.text_utils import contains_normalized_phrase, normalize_specialty_name


class ScoringService:
    @classmethod
    def compute_location_bonus(cls, location: str | None, specialty_name: str) -> float:
        if not location:
            return 0.0

        specialty_name = normalize_specialty_name(specialty_name)
        keywords = SPECIALTY_LOCATION_KEYWORDS.get(specialty_name, [])

        for keyword in keywords:
            if contains_normalized_phrase(location, keyword):
                return 0.10

        return 0.0

    @classmethod
    def compute_intensity_bonus(cls, intensity: str | None, specialty_name: str) -> float:
        if not intensity:
            return 0.0

        specialty_name = normalize_specialty_name(specialty_name)
        intensity_lower = intensity.lower().strip()

        if specialty_name in INTENSITY_BONUS_SPECIALTIES.get(intensity_lower, set()):
            return 0.05

        return 0.0

    @staticmethod
    def detect_red_flags(user_text: str, specialty: dict) -> tuple[bool, float]:
        red_flags_text = specialty.get("red_flags") or ""
        if not red_flags_text:
            return False, 0.0

        red_flag_terms = [term.strip() for term in red_flags_text.split(",") if term.strip()]
        matches = [term for term in red_flag_terms if contains_normalized_phrase(user_text, term)]

        if matches:
            return True, 0.08

        return False, 0.0

    @staticmethod
    def compute_symptom_reference_bonus(
        detected_symptoms: list[dict],
        specialty_name: str
    ) -> float:
        specialty_name = normalize_specialty_name(specialty_name)

        severity_weight = {
            "low": 0.02,
            "medium": 0.03,
            "high": 0.05,
            "critical": 0.08,
        }

        bonus = 0.0

        for symptom in detected_symptoms:
            specialties = [normalize_specialty_name(name) for name in symptom.get("specialties", [])]

            if specialty_name in specialties:
                bonus += severity_weight.get(symptom.get("severity_hint", "medium"), 0.03)

                if symptom.get("is_red_flag"):
                    bonus += 0.02

        return min(round(bonus, 4), 0.18)

    @staticmethod
    def compute_final_score(
        semantic_score: float,
        location_bonus: float,
        intensity_bonus: float,
        red_flag_bonus: float,
        symptom_reference_bonus: float = 0.0,
    ) -> float:
        metadata_bonus = (
            location_bonus
            + intensity_bonus
            + red_flag_bonus
            + symptom_reference_bonus
        )
        final_score = (semantic_score * 0.80) + metadata_bonus
        return round(min(final_score, 1.0), 4)