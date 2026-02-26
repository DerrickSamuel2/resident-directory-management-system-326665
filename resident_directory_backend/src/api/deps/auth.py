from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.core.auth import decode_access_token
from src.api.core.config import Settings

_security = HTTPBearer(auto_error=False)


# PUBLIC_INTERFACE
def get_settings() -> Settings:
    """FastAPI dependency to access validated Settings (loaded once in app state)."""
    # Filled in at runtime by main.py; see get_settings_from_app_state below.
    raise RuntimeError("Settings dependency must be overridden in main.py.")


# PUBLIC_INTERFACE
def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(_security),
    settings: Settings = Depends(get_settings),
) -> str:
    """
    Enforce admin authentication.

    Contract:
      - Input: Bearer token in Authorization header.
      - Output: admin username (subject) if valid.
      - Errors: 401 if missing/invalid token.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")
    try:
        payload = decode_access_token(settings, credentials.credentials)
        return payload.sub
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
