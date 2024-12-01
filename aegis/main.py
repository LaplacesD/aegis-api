"""FastAPI application factory for the Aegis API."""

from fastapi import FastAPI

from aegis.container import Container
from aegis.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional settings override. If omitted, loads from environment.

    Returns:
        Configured FastAPI application instance.
    """
    if settings is None:
        settings = Settings()

    container = Container(settings=settings)

    app = FastAPI(
        title="Aegis API",
        version="0.1.0",
        description="Aegis microservice with DDD/CQRS architecture",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.state.container = container

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()
