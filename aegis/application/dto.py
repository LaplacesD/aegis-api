"""Data Transfer Objects for the Aegis API application layer."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class UserDTO:
    """Data transfer object for User entity.

    Attributes:
        id: User's unique identifier.
        email: User's email address.
        name: User's display name.
        is_active: Whether the user account is active.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    id: uuid.UUID
    email: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_entity(cls, entity: Any) -> UserDTO:
        """Create a DTO from a domain entity.

        Args:
            entity: A User domain entity.

        Returns:
            A new UserDTO instance.
        """
        return cls(
            id=entity.id,
            email=str(entity.email),
            name=entity.name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass
class OrderItemDTO:
    """DTO for an order line item.

    Attributes:
        product_id: Product identifier.
        product_name: Snapshot of product name.
        unit_price: Price per unit.
        quantity: Number of units.
    """

    product_id: uuid.UUID
    product_name: str
    unit_price: float
    quantity: int


@dataclass
class OrderDTO:
    """Data transfer object for Order entity.

    Attributes:
        id: Order's unique identifier.
        user_id: Identifier of the ordering user.
        status: Current order status string.
        total_amount: Order total value.
        currency: Currency code.
        items: Line items in the order.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    total_amount: float
    currency: str
    items: list[OrderItemDTO] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_entity(cls, entity: Any) -> OrderDTO:
        """Create a DTO from a domain entity.

        Args:
            entity: An Order domain entity.

        Returns:
            A new OrderDTO instance.
        """
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            status=entity.status.value,
            total_amount=entity.total.amount,
            currency=entity.total.currency,
            items=[
                OrderItemDTO(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    unit_price=item.unit_price.amount,
                    quantity=item.quantity,
                )
                for item in entity.items
            ],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


@dataclass
class ProductDTO:
    """Data transfer object for Product entity.

    Attributes:
        id: Product's unique identifier.
        name: Product name.
        description: Product description.
        price: Current price.
        stock_quantity: Available inventory.
        is_available: Whether the product is purchasable.
    """

    id: uuid.UUID
    name: str
    description: str = ""
    price: float = 0.0
    currency: str = "USD"
    stock_quantity: int = 0
    is_available: bool = True

    @classmethod
    def from_entity(cls, entity: Any) -> ProductDTO:
        """Create a DTO from a domain entity.

        Args:
            entity: A Product domain entity.

        Returns:
            A new ProductDTO instance.
        """
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price.amount,
            currency=entity.price.currency,
            stock_quantity=entity.stock_quantity,
            is_available=entity.is_available,
        )
