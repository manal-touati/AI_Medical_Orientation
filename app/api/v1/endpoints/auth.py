import secrets

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.config import settings
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    username_ok = secrets.compare_digest(
        payload.username.encode("utf-8"),
        b"admin",
    )
    password_ok = secrets.compare_digest(
        payload.password.encode("utf-8"),
        settings.ADMIN_PASSWORD.encode("utf-8"),
    )
    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides.",
        )
    token = create_access_token(subject="admin")
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
