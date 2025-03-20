"""Unit of Work pattern implementation."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aegis.domain.repositories import OrderRepository, ProductRepository, UserRepository
    from aegis.infrastructure.event_store import EventStore


class UnitOfWork(ABC):
    """Abstract Unit of Work providing transactional repository access."""

    @property
    @abstractmethod
    def users(self) -> UserRepository:
        """Access the user repository within the current transaction."""
        ...

    @property
    @abstractmethod
    def orders(self) -> OrderRepository:
        """Access the order repository within the current transaction."""
        ...

    @property
    @abstractmethod
    def products(self) -> ProductRepository:
        """Access the product repository within the current transaction."""
        ...

    @property
    @abstractmethod
    def events(self) -> EventStore:
        """Access the event store within the current transaction."""
        ...

    @abstractmethod
    async def commit(self) -> None:
        """Commit the current transaction."""
        ...

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the current transaction."""
        ...


class SQLAlchemyUnitOfWork(UnitOfWork):
    """SQLAlchemy-backed Unit of Work implementation."""

    def __init__(
        self,
        session,
        user_repo: UserRepository,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        event_store: EventStore,
    ) -> None:
        self._session = session
        self._user_repo = user_repo
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._event_store = event_store

    @property
    def users(self) -> UserRepository:
        return self._user_repo

    @property
    def orders(self) -> OrderRepository:
        return self._order_repo

    @property
    def products(self) -> ProductRepository:
        return self._product_repo

    @property
    def events(self) -> EventStore:
        return self._event_store

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
