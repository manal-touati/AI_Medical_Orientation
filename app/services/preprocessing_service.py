class PreprocessingService:
    @staticmethod
    def build_user_text(
        symptom_description: str,
        intensity: str | None,
        duration: str | None,
        location: str | None,
        additional_context: str | None
    ) -> str:
        parts = [
            f"Symptômes: {symptom_description}",
            f"Intensité: {intensity}" if intensity else "",
            f"Durée: {duration}" if duration else "",
            f"Localisation: {location}" if location else "",
            f"Contexte additionnel: {additional_context}" if additional_context else "",
        ]
        return " ".join(part for part in parts if part).strip()