import secrets

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings

_api_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)


def verify_admin(api_key: str | None = Security(_api_key_header)) -> str:
    """
    Dépendance FastAPI — vérifie le header X-Admin-Key sur les routes /admin/*.
    Retourne "admin" si valide, lève une 401 sinon.
    """
    if api_key is None or not secrets.compare_digest(
        api_key.encode("utf-8"),
        settings.ADMIN_PASSWORD.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header X-Admin-Key manquant ou invalide.",
        )
    return "admin"
