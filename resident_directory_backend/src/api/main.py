from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.core.config import Settings
from src.api.core.db import init_engine
from src.api.deps import auth as auth_deps
from src.api.routers import auth as auth_router
from src.api.routers import residents as residents_router

logging.basicConfig(level=logging.INFO)

openapi_tags = [
    {"name": "health", "description": "Service health and diagnostics."},
    {"name": "auth", "description": "Admin authentication."},
    {"name": "residents", "description": "Resident public and admin management endpoints."},
]


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Environment variables required:
      - JWT_SECRET
      - ADMIN_PASSWORD
    Optional:
      - ADMIN_USERNAME (default: admin)
      - JWT_ALGORITHM (default: HS256)
      - ACCESS_TOKEN_EXPIRE_MINUTES (default: 60)
      - CORS_ALLOW_ORIGINS (default: '*')
      - DB_CONNECTION_TXT or DB_CONNECTION_TXT_PATH

    Returns:
      - FastAPI app instance.
    """
    settings = Settings.from_env()

    app = FastAPI(
        title="Resident Directory API",
        description=(
            "Backend API for the Resident Directory app. "
            "Provides public resident browsing/search and admin-protected CRUD."
        ),
        version="1.0.0",
        openapi_tags=openapi_tags,
    )

    # Store settings on app.state for access by dependency overrides.
    app.state.settings = settings

    # CORS: allow React frontend.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Wire dependencies overrides (single canonical settings object).
    def _get_settings_from_state() -> Settings:
        return app.state.settings

    auth_deps.get_settings = _get_settings_from_state  # type: ignore[assignment]
    auth_router.get_settings = _get_settings_from_state  # type: ignore[assignment]

    @app.on_event("startup")
    def _startup() -> None:
        # Initialize DB engine/session factory.
        init_engine(settings)

    @app.get(
        "/",
        tags=["health"],
        summary="Health check",
        description="Returns a simple response if the service is running.",
        operation_id="health_check",
    )
    def health_check() -> dict:
        return {"message": "Healthy"}

    app.include_router(auth_router.router)
    app.include_router(residents_router.router)

    return app


app = create_app()
