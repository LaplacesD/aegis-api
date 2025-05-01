"""Tests for the FastAPI HTTP endpoints."""

from __future__ import annotations

from httpx import AsyncClient


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    async def test_health_returns_ok(self, client: AsyncClient) -> None:
        """GET /health should return 200 with healthy status."""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"


class TestUsersEndpoint:
    """Tests for the /v1/users endpoints."""

    async def test_create_user(self, client: AsyncClient) -> None:
        """POST /v1/users should create a user."""
        payload = {"email": "test@example.com", "name": "Test User"}
        response = await client.post("/v1/users/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["is_active"] is True
        assert "id" in data

    async def test_get_user_not_found(self, client: AsyncClient) -> None:
        """GET /v1/users/{id} should return 404 for non-existent user."""
        response = await client.get(
            "/v1/users/00000000-0000-0000-0000-000000000000"
        )
        assert response.status_code == 404

    async def test_get_user_by_id(self, client: AsyncClient) -> None:
        """GET /v1/users/{id} should return the created user."""
        create_resp = await client.post(
            "/v1/users/", json={"email": "get@test.com", "name": "Getter"}
        )
        user_id = create_resp.json()["id"]

        response = await client.get(f"/v1/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "get@test.com"
