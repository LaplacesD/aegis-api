"""Repository interfaces for Aegis API.

Defines abstract repository contracts following the Repository pattern.
Concrete implementations live in the infrastructure layer.
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aegis.domain.entities import Order, Product, User


class UserRepository(ABC):
    """Repository interface for User entities."""

    @abstractmethod
    async def add(self, user: User) -> None:
        """Persist a new user.

        Args:
            user: The user entity to persist.
        """
        ...

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: UUID of the user.

        Returns:
            The User entity if found, otherwise None.
        """
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email address.

        Args:
            email: Email address to look up.

        Returns:
            The User entity if found, otherwise None.
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> None:
        """Persist changes to an existing user.

        Args:
            user: The user entity with updated state.
        """
        ...

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> None:
        """Remove a user from the repository.

        Args:
            user_id: UUID of the user to delete.
        """
        ...


class OrderRepository(ABC):
    """Repository interface for Order entities."""

    @abstractmethod
    async def add(self, order: Order) -> None:
        """Persist a new order.

        Args:
            order: The order entity to persist.
        """
        ...

    @abstractmethod
    async def get_by_id(self, order_id: uuid.UUID) -> Order | None:
        """Retrieve an order by its unique identifier.

        Args:
            order_id: UUID of the order.

        Returns:
            The Order entity if found, otherwise None.
        """
        ...

    @abstractmethod
    async def get_by_user(self, user_id: uuid.UUID) -> list[Order]:
        """Retrieve all orders belonging to a user.

        Args:
            user_id: UUID of the user.

        Returns:
            List of Order entities.
        """
        ...

    @abstractmethod
    async def update(self, order: Order) -> None:
        """Persist changes to an existing order.

        Args:
            order: The order entity with updated state.
        """
        ...


class ProductRepository(ABC):
    """Repository interface for Product entities."""

    @abstractmethod
    async def add(self, product: Product) -> None:
        """Persist a new product.

        Args:
            product: The product entity to persist.
        """
        ...

    @abstractmethod
    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        """Retrieve a product by its unique identifier.

        Args:
            product_id: UUID of the product.

        Returns:
            The Product entity if found, otherwise None.
        """
        ...

    @abstractmethod
    async def list_all(self) -> list[Product]:
        """Retrieve all products.

        Returns:
            List of all Product entities.
        """
        ...

    @abstractmethod
    async def update(self, product: Product) -> None:
        """Persist changes to an existing product.

        Args:
            product: The product entity with updated state.
        """
        ...
