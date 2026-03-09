class PreprocessingService:
    @staticmethod
    def build_user_text(symptom_description: str, intensity: str | None, duration: str | None,
                        location: str | None, additional_context: str | None) -> str:
        parts = [
            f"Symptoms: {symptom_description}",
            f"Intensity: {intensity}" if intensity else "",
            f"Duration: {duration}" if duration else "",
            f"Location: {location}" if location else "",
            f"Additional context: {additional_context}" if additional_context else "",
        ]
        return " ".join(part for part in parts if part).strip()