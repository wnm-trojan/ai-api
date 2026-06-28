"""Application entry point."""
from fastapi import FastAPI

from src.core.config import settings
from src.infrastructure.logging.logger import setup_logging
from src.presentation.exception_handlers.domain_handlers import domain_error_handler
from src.presentation.middleware.setup import setup_middleware
from src.presentation.routers.chat_routers import (
    chat_router,
    json_router,
    stream_router,
    tool_router,
)
from src.presentation.schemas.chat_schemas import HealthResponseSchema
from src.domain.exceptions import DomainError


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="AI API",
        description="FastAPI + OpenAI",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    setup_middleware(app)
    app.add_exception_handler(DomainError, domain_error_handler)

    app.include_router(chat_router)
    app.include_router(stream_router)
    app.include_router(json_router)
    app.include_router(tool_router)

    @app.get("/health", response_model=HealthResponseSchema, tags=["Health"])
    async def health():
        return HealthResponseSchema(
            status="healthy",
            version=settings.app_version,
            openai_configured=bool(settings.openai_api_key),
        )

    return app


app = create_app()
