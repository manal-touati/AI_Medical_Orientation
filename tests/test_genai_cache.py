from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.genai_cache import GenAICache
from app.services.cache_service import CacheService
from app.services.genai_service import GenAIService
from app.utils.hash_utils import build_sha256


# ---------------------------------------------------------------------------
# Fixtures — base SQLite en mémoire isolée par test
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------------
# CacheService — tests unitaires
# ---------------------------------------------------------------------------

class TestCacheService:

    def test_get_returns_none_when_key_absent(self, db_session):
        """Un cache vide doit retourner None pour n'importe quelle clé."""
        service = CacheService(db_session)
        result = service.get("cle_inexistante")
        assert result is None

    def test_set_creates_entry(self, db_session):
        """set() doit persister une entrée récupérable ensuite."""
        service = CacheService(db_session)
        key = build_sha256("specialty_explanation:symptomes||Cardiologie||desc")

        entry = service.set(
            cache_key=key,
            cache_type="specialty_explanation",
            input_text="symptomes",
            output_text="Explication générée.",
        )

        assert entry.id is not None
        assert entry.cache_key == key
        assert entry.output_text == "Explication générée."

    def test_get_returns_entry_after_set(self, db_session):
        """get() doit retrouver l'entrée créée par set()."""
        service = CacheService(db_session)
        key = build_sha256("short_input_enrichment:mal au ventre")

        service.set(
            cache_key=key,
            cache_type="short_input_enrichment",
            input_text="mal au ventre",
            output_text="Douleur abdominale diffuse.",
        )

        cached = service.get(key)
        assert cached is not None
        assert cached.output_text == "Douleur abdominale diffuse."
        assert cached.cache_type == "short_input_enrichment"

    def test_set_is_idempotent(self, db_session):
        """Un double set() sur la même clé ne doit pas créer de doublon."""
        service = CacheService(db_session)
        key = build_sha256("specialty_explanation:texte||Neurologie||desc")

        first = service.set(
            cache_key=key,
            cache_type="specialty_explanation",
            input_text="texte",
            output_text="Première explication.",
        )
        second = service.set(
            cache_key=key,
            cache_type="specialty_explanation",
            input_text="texte",
            output_text="Deuxième explication.",
        )

        count = db_session.query(GenAICache).filter_by(cache_key=key).count()
        assert count == 1
        assert first.id == second.id
        # La valeur originale est conservée
        assert second.output_text == "Première explication."

    def test_cache_key_is_sha256(self, db_session):
        """La clé de cache doit être un hash SHA256 (64 caractères hexadécimaux)."""
        key = build_sha256("specialty_explanation:test||Dermatologie||desc")
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)

    def test_two_different_inputs_produce_different_keys(self, db_session):
        """Deux entrées différentes doivent produire des clés différentes."""
        key1 = build_sha256("specialty_explanation:douleur||Cardiologie||desc")
        key2 = build_sha256("specialty_explanation:fièvre||Infectiologie||desc")
        assert key1 != key2


# ---------------------------------------------------------------------------
# GenAIService — comportement du cache (sans appel OpenAI réel)
# ---------------------------------------------------------------------------

class TestGenAIServiceCache:

    def _make_service(self, db_session) -> GenAIService:
        """Instancie GenAIService avec un client OpenAI mocké."""
        with patch("app.services.genai_service.OpenAI"):
            service = GenAIService(db_session)
        return service

    def test_enrich_short_input_uses_cache_on_second_call(self, db_session):
        """Le deuxième appel identique doit retourner cache_hit=True sans appel LLM."""
        service = self._make_service(db_session)

        # Pré-remplir le cache manuellement
        text = "mal au dos"
        cache_key = build_sha256(f"short_input_enrichment:{text}")
        CacheService(db_session).set(
            cache_key=cache_key,
            cache_type="short_input_enrichment",
            input_text=text,
            output_text="Douleur lombaire persistante.",
        )

        result = service.enrich_short_input(text)

        assert result["cache_hit"] is True
        assert result["text"] == "Douleur lombaire persistante."
        assert result["total_tokens"] == 0

    def test_enrich_short_input_calls_llm_on_cache_miss(self, db_session):
        """Sur un cache miss, le LLM doit être appelé et le résultat mis en cache."""
        service = self._make_service(db_session)

        # Simuler la réponse OpenAI
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Douleur thoracique antérieure."
        mock_response.usage.prompt_tokens = 30
        mock_response.usage.completion_tokens = 12
        mock_response.usage.total_tokens = 42
        service.client.chat.completions.create.return_value = mock_response

        result = service.enrich_short_input("douleur poitrine")

        assert result["cache_hit"] is False
        assert result["text"] == "Douleur thoracique antérieure."
        assert result["total_tokens"] == 42

        # Vérifier que le résultat est bien mis en cache
        key = build_sha256("short_input_enrichment:douleur poitrine")
        cached = CacheService(db_session).get(key)
        assert cached is not None
        assert cached.output_text == "Douleur thoracique antérieure."

    def test_generate_explanation_cache_hit(self, db_session):
        """generate_explanation doit retourner le cache sans appel LLM si présent."""
        service = self._make_service(db_session)

        user_text = "douleur thoracique"
        specialty_name = "Cardiologie"
        specialty_description = "Spécialité des maladies du cœur."
        cache_input = f"{user_text}||{specialty_name}||{specialty_description}"
        cache_key = build_sha256(f"specialty_explanation:{cache_input}")

        CacheService(db_session).set(
            cache_key=cache_key,
            cache_type="specialty_explanation",
            input_text=cache_input,
            output_text="La Cardiologie est pertinente car les symptômes évoquent une atteinte cardiaque.",
        )

        result = service.generate_explanation(user_text, specialty_name, specialty_description)

        assert result["cache_hit"] is True
        assert "Cardiologie" in result["text"]
        assert result["total_tokens"] == 0
