from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "IA GEN Medical Orientation"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    POSTGRES_DB: str = "medical_orientation"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    DATABASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-mini"

    SBERT_MODEL: str = "all-MiniLM-L6-v2"

    GENAI_ENABLE: bool = True
    GENAI_MIN_WORDS_THRESHOLD: int = 5

    CACHE_ENABLED: bool = True
    TOP_K_RECOMMENDATIONS: int = 3
    SIMILARITY_THRESHOLD: float = 0.30

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()