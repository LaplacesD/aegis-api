"""Users API v1 endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from aegis.api.dependencies import get_mediator
from aegis.api.schemas import UserCreateRequest, UserResponse, UserUpdateRequest
from aegis.application.commands.update_user import UpdateUserCommand
from aegis.application.dto import UserDTO
from aegis.application.mediator import Mediator
from aegis.application.queries.get_user import GetUserQuery
from aegis.domain.value_objects import Email

router = APIRouter(prefix="/v1/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreateRequest,
    mediator: Mediator = Depends(get_mediator),
) -> UserResponse:
    """Create a new user account."""
    from aegis.domain.entities import User
    from aegis.domain.value_objects import Email

    user = User(email=Email(body.email), name=body.name)
    # In production, would use CreateUserCommand via mediator
    return UserResponse(
        id=user.id,
        email=str(user.email),
        name=user.name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    mediator: Mediator = Depends(get_mediator),
) -> UserResponse:
    """Retrieve a user by their unique identifier."""
    query = GetUserQuery(user_id=user_id)
    result = await mediator.query(query)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return UserResponse(**result.__dict__)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    body: UserUpdateRequest,
    mediator: Mediator = Depends(get_mediator),
) -> UserResponse:
    """Update a user's details."""
    command = UpdateUserCommand(
        user_id=user_id,
        name=body.name,
        email=str(body.email) if body.email else None,
    )
    result = await mediator.send(command)
    return UserResponse(**result.__dict__)
