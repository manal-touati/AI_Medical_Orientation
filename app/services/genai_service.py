from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.cache_service import CacheService
from app.utils.hash_utils import build_sha256


class GenAIService:
    def __init__(self, db: Session):
        self.db = db
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache_service = CacheService(db)

    def _chat_completion(self, system_prompt: str, user_prompt: str) -> str | None:
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            content = response.choices[0].message.content
            return content.strip() if content else None
        except Exception:
            return None

    def enrich_short_input(self, text: str) -> str | None:
        cache_type = "short_input_enrichment"
        cache_key = build_sha256(f"{cache_type}:{text}")

        cached = self.cache_service.get(cache_key)
        if cached:
            return cached.output_text

        system_prompt = "You help improve short symptom descriptions for semantic analysis."
        user_prompt = (
            "Rewrite the following symptom description to make it clearer and more descriptive "
            "for a semantic analysis system. Do not invent severe symptoms. Keep it medically neutral.\n\n"
            f"Input: {text}"
        )

        output = self._chat_completion(system_prompt, user_prompt)
        if output:
            self.cache_service.set(
                cache_key=cache_key,
                cache_type=cache_type,
                input_text=text,
                output_text=output
            )
        return output

    def generate_explanation(
        self,
        user_text: str,
        specialty_name: str,
        specialty_description: str
    ) -> str | None:
        cache_type = "specialty_explanation"
        cache_input = f"{user_text}||{specialty_name}||{specialty_description}"
        cache_key = build_sha256(f"{cache_type}:{cache_input}")

        cached = self.cache_service.get(cache_key)
        if cached:
            return cached.output_text

        system_prompt = (
            "You are a medical orientation assistant. "
            "You must not diagnose. You only explain why a specialty may be relevant."
        )
        user_prompt = (
            "You are generating a short educational explanation for a medical specialty orientation system. "
            "Explain why this specialty may be relevant based on the user's symptoms. "
            "Do not provide a diagnosis. Mention clearly that this is not a medical diagnosis.\n\n"
            f"User symptoms: {user_text}\n"
            f"Suggested specialty: {specialty_name}\n"
            f"Specialty description: {specialty_description}"
        )

        output = self._chat_completion(system_prompt, user_prompt)
        if output:
            self.cache_service.set(
                cache_key=cache_key,
                cache_type=cache_type,
                input_text=cache_input,
                output_text=output
            )
        return output