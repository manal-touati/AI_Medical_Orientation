from app.utils.constants import RED_FLAG_KEYWORDS
from app.utils.text_utils import contains_normalized_phrase


class RedFlagService:
    @staticmethod
    def detect(user_text: str) -> list[dict]:
        detected = []

        for keyword, meta in RED_FLAG_KEYWORDS.items():
            if contains_normalized_phrase(user_text, keyword):
                detected.append({
                    "keyword": keyword,
                    "severity": meta["severity"],
                    "message": meta["message"],
                })

        return detected

    @staticmethod
    def from_detected_symptoms(detected_symptoms: list[dict]) -> list[dict]:
        results = []

        for symptom in detected_symptoms:
            if symptom.get("is_red_flag"):
                severity = symptom.get("severity_hint", "medium")
                if severity not in {"low", "medium", "high", "critical"}:
                    severity = "medium"

                results.append({
                    "keyword": symptom["canonical_name"],
                    "severity": severity,
                    "message": symptom.get("red_flag_message")
                    or f"{symptom['canonical_name']} peut nécessiter une évaluation médicale.",
                })

        return results

    @staticmethod
    def merge_red_flags(keyword_flags: list[dict], symptom_flags: list[dict]) -> list[dict]:
        merged = {}
        severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}

        for flag in keyword_flags + symptom_flags:
            key = flag["keyword"].strip().lower()
            if key not in merged:
                merged[key] = flag
            else:
                current = merged[key]
                if severity_rank.get(flag["severity"], 0) > severity_rank.get(current["severity"], 0):
                    merged[key] = flag

        return list(merged.values())

    @staticmethod
    def has_urgent_red_flag(detected_flags: list[dict]) -> bool:
        return any(flag["severity"] in {"high", "critical"} for flag in detected_flags)

    @staticmethod
    def has_critical_red_flag(detected_flags: list[dict]) -> bool:
        return any(flag["severity"] == "critical" for flag in detected_flags)

    @staticmethod
    def build_warning(detected_flags: list[dict]) -> str:
        if not detected_flags:
            return "Cette orientation est purement indicative et ne remplace pas un diagnostic médical."

        if RedFlagService.has_critical_red_flag(detected_flags):
            return (
                "Des signes critiques ont été détectés. "
                "Cette orientation reste indicative et ne remplace pas une prise en charge urgente."
            )

        if RedFlagService.has_urgent_red_flag(detected_flags):
            return (
                "Des signaux d’alerte importants ont été détectés. "
                "Cette orientation est indicative et une évaluation médicale rapide est recommandée."
            )

        return "Cette orientation est purement indicative et ne remplace pas un diagnostic médical."