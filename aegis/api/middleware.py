"""API middleware for authentication, logging, and error handling."""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from aegis.domain.exceptions import DomainError, EntityNotFoundError

logger = logging.getLogger("aegis.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs request method, path, status code, and duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.monotonic()
        response = await call_next(request)
        duration_ms = (time.monotonic() - start_time) * 1000
        logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Simple authentication middleware that sets request.state.user_id.

    In production this would validate JWT tokens or similar.
    """

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.removeprefix("Bearer ")
            # In production: validate token and extract user_id
            request.state.user_id = token
        else:
            # Set a placeholder for development
            request.state.user_id = str(uuid.uuid4())

        response = await call_next(request)
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catches domain and application exceptions and returns JSON errors."""

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except EntityNotFoundError as exc:
            return JSONResponse(
                status_code=404,
                content={"detail": str(exc), "error_code": "NOT_FOUND"},
            )
        except DomainError as exc:
            return JSONResponse(
                status_code=400,
                content={"detail": str(exc), "error_code": "DOMAIN_ERROR"},
            )
        except ValueError as exc:
            return JSONResponse(
                status_code=422,
                content={"detail": str(exc), "error_code": "VALIDATION_ERROR"},
            )
        except Exception as exc:
            logger.exception("Unhandled exception: %s", exc)
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An internal server error occurred.",
                    "error_code": "INTERNAL_ERROR",
                },
            )


def register_middleware(app: FastAPI) -> None:
    """Register all middleware on the FastAPI application.

    Middleware is applied in registration order (last registered runs first).

    Args:
        app: The FastAPI application instance.
    """
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
