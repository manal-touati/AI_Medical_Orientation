from __future__ import annotations


class ScoringService:
    LOCATION_KEYWORDS = {
        "Cardiology": ["chest", "thorax", "heart"],
        "Pulmonology": ["chest", "lungs", "breathing"],
        "Neurology": ["head", "brain", "arm", "leg", "face", "left arm", "right arm"],
        "Gastroenterology": ["abdomen", "stomach", "belly", "digestive", "lower abdomen"],
        "Dermatology": ["skin", "scalp", "nails", "face"],
        "Otorhinolaryngology (ENT)": ["ear", "nose", "throat", "sinus", "neck"],
        "Ophthalmology": ["eye", "eyes", "vision", "eyelid"],
        "Rheumatology": ["joint", "joints", "back", "hand", "hands", "wrist", "knee", "shoulder"],
        "Endocrinology": ["general", "whole body"],
        "Nephrology": ["flank", "kidney", "back", "feet", "legs"],
        "Urology": ["pelvis", "pelvic", "urinary", "bladder", "flank"],
        "Gynecology": ["pelvis", "pelvic", "lower abdomen"],
        "Psychiatry": ["general", "mental", "sleep"],
        "Infectious Diseases": ["general", "whole body", "throat", "lungs"],
        "Orthopedics": ["bone", "joint", "back", "knee", "shoulder", "arm", "leg"]
    }

    INTENSITY_BONUS_SPECIALTIES = {
        "high": {"Cardiology", "Pulmonology", "Neurology", "Infectious Diseases", "Orthopedics", "Gynecology"},
        "medium": {"Gastroenterology", "Urology", "Rheumatology", "Dermatology", "Endocrinology"},
        "low": set()
    }

    @classmethod
    def compute_location_bonus(cls, location: str | None, specialty_name: str) -> float:
        if not location:
            return 0.0

        location_lower = location.lower().strip()
        keywords = cls.LOCATION_KEYWORDS.get(specialty_name, [])
        for keyword in keywords:
            if keyword in location_lower:
                return 0.10
        return 0.0

    @classmethod
    def compute_intensity_bonus(cls, intensity: str | None, specialty_name: str) -> float:
        if not intensity:
            return 0.0

        intensity_lower = intensity.lower().strip()
        if specialty_name in cls.INTENSITY_BONUS_SPECIALTIES.get(intensity_lower, set()):
            return 0.05

        return 0.0

    @staticmethod
    def detect_red_flags(user_text: str, specialty: dict) -> tuple[bool, float]:
        red_flags_text = (specialty.get("red_flags") or "").lower()
        user_text_lower = user_text.lower()

        if not red_flags_text:
            return False, 0.0

        red_flag_terms = [term.strip() for term in red_flags_text.split(",") if term.strip()]
        matches = [term for term in red_flag_terms if term in user_text_lower]

        if matches:
            return True, 0.08

        return False, 0.0

    @staticmethod
    def compute_final_score(
        semantic_score: float,
        location_bonus: float,
        intensity_bonus: float,
        red_flag_bonus: float
    ) -> float:
        metadata_bonus = location_bonus + intensity_bonus + red_flag_bonus
        final_score = (semantic_score * 0.80) + metadata_bonus
        return round(min(final_score, 1.0), 4)