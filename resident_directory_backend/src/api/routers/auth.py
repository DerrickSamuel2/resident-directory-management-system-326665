from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.core.auth import create_access_token
from src.api.core.config import Settings
from src.api.schemas.auth import LoginRequest, TokenResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """Dependency to be overridden by main.py with the real Settings."""
    raise RuntimeError("get_settings must be overridden in main.py.")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Admin login",
    description="Validate admin credentials and return a JWT access token.",
    operation_id="auth_login",
)
def login(payload: LoginRequest, settings: Settings = Depends(get_settings)) -> TokenResponse:
    """
    Authenticate an admin.

    Notes:
      - This implementation uses ADMIN_USERNAME + ADMIN_PASSWORD env vars.
      - If/when admins are stored in DB, keep the API contract stable and change only validation backend.
    """
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    token = create_access_token(settings, subject=payload.username)
    logger.info("Admin login succeeded user=%s", payload.username)
    return TokenResponse(access_token=token, token_type="bearer")
