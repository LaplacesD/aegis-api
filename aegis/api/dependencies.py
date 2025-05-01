"""FastAPI dependencies for injecting application services."""

from __future__ import annotations

from typing import AsyncGenerator

from fastapi import Depends, Request

from aegis.application.mediator import Mediator


async def get_mediator(request: Request) -> Mediator:
    """Retrieve the Mediator from the application container.

    Args:
        request: The incoming HTTP request.

    Returns:
        The Mediator instance registered in the container.
    """
    container = request.app.state.container
    mediator = container.get("mediator")
    if mediator is None:
        raise RuntimeError("Mediator not registered in the container.")
    return mediator


async def get_current_user_id(request: Request) -> str:
    """Extract the current user ID from the request state.

    This is set by the authentication middleware.

    Args:
        request: The incoming HTTP request.

    Returns:
        The authenticated user's ID as a string.
    """
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise RuntimeError("User not authenticated.")
    return user_id
