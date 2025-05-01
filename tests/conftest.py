"""Pytest configuration and shared fixtures for Aegis API tests."""

from __future__ import annotations

from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from aegis.config import Settings
from aegis.main import create_app


@pytest.fixture
def settings() -> Settings:
    """Provide test settings with an in-memory SQLite database."""
    return Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        debug=False,
        secret_key="test-secret-key",
    )


@pytest.fixture
def app(settings: Settings):
    """Provide a FastAPI test application instance."""
    return create_app(settings=settings)


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
