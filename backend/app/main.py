"""
Main entry point. Wires settings, logging, the AI provider, rate limiter, CORS,
body-size limit, error handlers and routes into one FastAPI app.

Run (from backend/):  uvicorn app.main:app --reload
API docs:             http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import RateLimiter, api_router, register_error_handlers
from app.api.body_limit import JsonBodyLimit
from app.core.config import Settings, get_settings
from app.core.logging import setup_logging
from app.modules.ai import create_provider

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    setup_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # A missing GEMINI_API_KEY / GEMINI_MODEL stops the server here with a clear message.
        app.state.ai = create_provider(settings)
        app.state.rate_limiter = RateLimiter()
        logger.info("Logo Analyzer API ready (AI model: %s)", settings.gemini_model)
        yield

    app = FastAPI(title="Logo Analyzer API", version="1.0.0", lifespan=lifespan)
    app.add_middleware(JsonBodyLimit)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        expose_headers=["Content-Disposition"],  # lets the frontend read the .txt filename
    )
    register_error_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()