from app.db.base import Base
from app.db.session import engine
from app.models import recommendation_feedback  # noqa: F401 — enregistre la table


def init_db() -> None:
    Base.metadata.create_all(bind=engine)