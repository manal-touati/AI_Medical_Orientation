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

    @staticmethod
    def _usage_to_dict(response) -> dict:
        usage = getattr(response, "usage", None)
        if not usage:
            return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        return {
            "prompt_tokens": int(getattr(usage, "prompt_tokens", 0) or 0),
            "completion_tokens": int(getattr(usage, "completion_tokens", 0) or 0),
            "total_tokens": int(getattr(usage, "total_tokens", 0) or 0),
        }

    def _chat_completion(self, system_prompt: str, user_prompt: str) -> dict:
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
            usage = self._usage_to_dict(response)

            return {
                "text": content.strip() if content else None,
                "cache_hit": False,
                "prompt_tokens": usage["prompt_tokens"],
                "completion_tokens": usage["completion_tokens"],
                "total_tokens": usage["total_tokens"],
            }
        except Exception:
            return {
                "text": None,
                "cache_hit": False,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }

    def enrich_short_input(self, text: str) -> dict:
        cache_type = "short_input_enrichment"
        cache_key = build_sha256(f"{cache_type}:{text}")

        cached = self.cache_service.get(cache_key)
        if cached:
            return {
                "text": cached.output_text,
                "cache_hit": True,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }

        system_prompt = (
            "Tu aides à reformuler de courts symptômes pour améliorer une analyse sémantique médicale. "
            "Tu ne poses pas de diagnostic et tu n'inventes pas de nouveaux symptômes graves."
        )
        user_prompt = (
            "Reformule la description suivante de manière plus claire et structurée pour un système "
            "d'orientation médicale. Reste neutre, concise et fidèle au texte.\n\n"
            f"Texte utilisateur : {text}"
        )

        output = self._chat_completion(system_prompt, user_prompt)
        if output["text"]:
            self.cache_service.set(
                cache_key=cache_key,
                cache_type=cache_type,
                input_text=text,
                output_text=output["text"]
            )
        return output

    def generate_explanation(
        self,
        user_text: str,
        specialty_name: str,
        specialty_description: str
    ) -> dict:
        cache_type = "specialty_explanation"
        cache_input = f"{user_text}||{specialty_name}||{specialty_description}"
        cache_key = build_sha256(f"{cache_type}:{cache_input}")

        cached = self.cache_service.get(cache_key)
        if cached:
            return {
                "text": cached.output_text,
                "cache_hit": True,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }

        system_prompt = (
            "Tu es un assistant d'orientation médicale pédagogique. "
            "Tu expliques pourquoi une spécialité peut être pertinente, sans jamais poser de diagnostic."
        )
        user_prompt = (
            "Rédige en français une explication courte, professionnelle et rassurante. "
            "Explique pourquoi la spécialité proposée est pertinente au regard des symptômes. "
            "Indique clairement qu'il ne s'agit pas d'un diagnostic médical.\n\n"
            f"Symptômes : {user_text}\n"
            f"Spécialité proposée : {specialty_name}\n"
            f"Description de la spécialité : {specialty_description}"
        )

        output = self._chat_completion(system_prompt, user_prompt)
        if output["text"]:
            self.cache_service.set(
                cache_key=cache_key,
                cache_type=cache_type,
                input_text=cache_input,
                output_text=output["text"]
            )
        return output