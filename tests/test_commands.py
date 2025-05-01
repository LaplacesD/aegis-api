"""Tests for command and query handlers."""

from __future__ import annotations

import uuid

import pytest

from aegis.application.commands.create_order import CreateOrderCommand
from aegis.application.commands.update_user import UpdateUserCommand
from aegis.application.dto import OrderItemDTO
from aegis.application.handlers import (
    CreateOrderHandler,
    GetOrdersHandler,
    GetUserHandler,
    UpdateUserHandler,
)
from aegis.application.mediator import Mediator
from aegis.application.queries.get_orders import GetOrdersQuery
from aegis.application.queries.get_user import GetUserQuery
from aegis.domain.entities import Order, OrderItem, Product, User
from aegis.domain.value_objects import Address, Email, Money


class TestMediator:
    """Tests for the Mediator pattern implementation."""

    def test_register_and_send_command(self) -> None:
        """Mediator should route commands to registered handlers."""
        mediator = Mediator()
        user_repo = _InMemoryUserRepository()
        user = User(email=Email("test@test.com"), name="Test")
        # Add a user so update works
        handler = UpdateUserHandler(user_repo)

        mediator.register_command(UpdateUserCommand, handler)

        # We need to add the user first via the repo
        import asyncio
        asyncio.run(user_repo.add(user))

        command = UpdateUserCommand(user_id=user.id, name="Updated")
        result = asyncio.run(mediator.send(command))

        assert result.name == "Updated"

    def test_unregistered_command_raises(self) -> None:
        """Sending an unregistered command should raise ValueError."""
        mediator = Mediator()
        with pytest.raises(ValueError, match="No handler registered"):
            import asyncio
            asyncio.run(mediator.send(CreateOrderCommand(
                user_id=uuid.uuid4(),
                items=[],
                shipping_street="", shipping_city="",
                shipping_state="", shipping_zip="", shipping_country="",
            )))

    def test_unregistered_query_raises(self) -> None:
        """Querying with an unregistered handler should raise ValueError."""
        mediator = Mediator()
        with pytest.raises(ValueError, match="No handler registered"):
            import asyncio
            asyncio.run(mediator.query(GetUserQuery(user_id=uuid.uuid4())))


class _InMemoryUserRepository:
    """Minimal in-memory repo for testing handlers."""

    def __init__(self):
        self._users: dict[uuid.UUID, User] = {}

    async def add(self, user: User) -> None:
        self._users[user.id] = user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if str(user.email) == email:
                return user
        return None

    async def update(self, user: User) -> None:
        self._users[user.id] = user

    async def delete(self, user_id: uuid.UUID) -> None:
        self._users.pop(user_id, None)
