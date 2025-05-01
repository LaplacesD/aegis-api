"""FastAPI application factory for the Aegis API."""

from fastapi import FastAPI

from aegis.api.middleware import register_middleware
from aegis.api.v1.users import router as users_router
from aegis.api.v1.orders import router as orders_router
from aegis.api.v1.products import router as products_router
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

    # Register API routers
    app.include_router(users_router)
    app.include_router(orders_router)
    app.include_router(products_router)

    # Register middleware
    register_middleware(app)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy", "version": "0.1.0"}

    return app


app = create_app()
