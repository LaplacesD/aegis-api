"""SQLAlchemy repository implementations."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from aegis.domain.repositories import (
    OrderRepository,
    ProductRepository,
    UserRepository,
)

if TYPE_CHECKING:
    from aegis.domain.entities import Order, Product, User


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy-backed repository for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        self._session.add(user)

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._session.get(User, user_id)
        return result

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)  # type: ignore[attr-defined]
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, user: User) -> None:
        await self._session.merge(user)

    async def delete(self, user_id: uuid.UUID) -> None:
        stmt = delete(User).where(User.id == user_id)  # type: ignore[attr-defined]
        await self._session.execute(stmt)


class SQLAlchemyOrderRepository(OrderRepository):
    """SQLAlchemy-backed repository for Order entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, order: Order) -> None:
        self._session.add(order)

    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        result = await self._session.get(Order, order_id)
        return result

    async def get_by_user(self, user_id: uuid.UUID) -> list[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)  # type: ignore[attr-defined]
            .order_by(Order.created_at.desc())  # type: ignore[attr-defined]
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, order: Order) -> None:
        await self._session.merge(order)


class SQLAlchemyProductRepository(ProductRepository):
    """SQLAlchemy-backed repository for Product entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, product: Product) -> None:
        self._session.add(product)

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        result = await self._session.get(Product, product_id)
        return result

    async def list_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.name)  # type: ignore[attr-defined]
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, product: Product) -> None:
        await self._session.merge(product)
