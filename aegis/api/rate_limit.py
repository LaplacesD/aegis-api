"""Rate limiting middleware for aegis-api."""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RateLimitExceeded(Exception):
    """Raised when a client exceeds the rate limit."""

    def __init__(self, client_id: str, limit: int, window: int) -> None:
        self.client_id = client_id
        self.limit = limit
        self.window = window
        super().__init__(
            f"Rate limit exceeded for {client_id}: "
            f"{limit} requests per {window}s"
        )


class InMemoryRateLimiter:
    """Simple in-memory sliding-window rate limiter."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)

    def _prune(self, client_id: str, now: float) -> None:
        cutoff = now - self.window_seconds
        self._clients[client_id] = [
            ts for ts in self._clients[client_id] if ts > cutoff
        ]

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        self._prune(client_id, now)
        if len(self._clients[client_id]) >= self.max_requests:
            return False
        self._clients[client_id].append(now)
        return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware that applies rate limiting per client."""

    def __init__(
        self,
        app,
        max_requests: int = 100,
        window_seconds: int = 60,
        client_id_extractor: Callable[[Request], str] | None = None,
    ) -> None:
        super().__init__(app)
        self.limiter = InMemoryRateLimiter(max_requests, window_seconds)
        self._extract_client = client_id_extractor or self._default_extractor

    @staticmethod
    def _default_extractor(request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next) -> Response:
        client_id = self._extract_client(request)
        if not self.limiter.is_allowed(client_id):
            return Response(
                content='{"detail":"Too many requests"}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(self.limiter.window_seconds)},
            )
        return await call_next(request)
