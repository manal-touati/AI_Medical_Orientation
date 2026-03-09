from app.utils.constants import RED_FLAG_KEYWORDS


class RedFlagService:
    @staticmethod
    def detect(user_text: str) -> list[dict]:
        detected = []
        text = user_text.lower()

        for keyword, meta in RED_FLAG_KEYWORDS.items():
            if keyword in text:
                detected.append({
                    "keyword": keyword,
                    "severity": meta["severity"],
                    "message": meta["message"]
                })

        return detected

    @staticmethod
    def has_urgent_red_flag(detected_flags: list[dict]) -> bool:
        return any(flag["severity"] in {"high", "critical"} for flag in detected_flags)

    @staticmethod
    def has_critical_red_flag(detected_flags: list[dict]) -> bool:
        return any(flag["severity"] == "critical" for flag in detected_flags)

    @staticmethod
    def build_warning(detected_flags: list[dict]) -> str:
        if not detected_flags:
            return "This result is an indicative orientation only and not a medical diagnosis."

        if RedFlagService.has_critical_red_flag(detected_flags):
            return (
                "This result is an indicative orientation only and not a medical diagnosis. "
                "Critical warning signs were detected. Seek immediate professional or emergency help."
            )

        if RedFlagService.has_urgent_red_flag(detected_flags):
            return (
                "This result is an indicative orientation only and not a medical diagnosis. "
                "Some warning signs were detected and may require urgent medical attention."
            )

        return "This result is an indicative orientation only and not a medical diagnosis."