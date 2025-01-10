"""Domain entities for Aegis API.

Defines core business entities: User, Product, Order, and OrderItem.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aegis.domain.value_objects import Address, Email, Money, OrderStatus


class User:
    """Represents a user in the system.

    Attributes:
        id: Unique identifier.
        email: User's email address.
        name: Display name.
        is_active: Whether the user account is active.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    def __init__(
        self,
        email: Email,
        name: str,
        user_id: uuid.UUID | None = None,
        is_active: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = user_id or uuid.uuid4()
        self.email = email
        self.name = name
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def rename(self, new_name: str) -> None:
        """Change the user's display name.

        Args:
            new_name: New display name for the user.
        """
        self.name = new_name
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<User {self.id} {self.email}>"


class Product:
    """Represents a product in the catalog.

    Attributes:
        id: Unique identifier.
        name: Product name.
        description: Detailed product description.
        price: Current price.
        stock_quantity: Available inventory count.
        is_available: Whether the product can be purchased.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    def __init__(
        self,
        name: str,
        price: Money,
        description: str = "",
        stock_quantity: int = 0,
        product_id: uuid.UUID | None = None,
        is_available: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = product_id or uuid.uuid4()
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.is_available = is_available
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def adjust_price(self, new_price: Money) -> None:
        """Update the product price.

        Args:
            new_price: The new price to set.
        """
        self.price = new_price
        self.updated_at = datetime.utcnow()

    def restock(self, quantity: int) -> None:
        """Add inventory to the product.

        Args:
            quantity: Number of units to add.

        Raises:
            ValueError: If quantity is negative.
        """
        if quantity < 0:
            raise ValueError("Restock quantity must be non-negative.")
        self.stock_quantity += quantity
        self.updated_at = datetime.utcnow()

    def reserve(self, quantity: int) -> None:
        """Reserve inventory for an order.

        Args:
            quantity: Number of units to reserve.

        Raises:
            ValueError: If there is insufficient stock.
        """
        if quantity > self.stock_quantity:
            raise ValueError(f"Insufficient stock: {self.stock_quantity} < {quantity}")
        self.stock_quantity -= quantity
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Product {self.id} {self.name}>"


class OrderItem:
    """A single line item within an order.

    Attributes:
        product_id: Identifier of the product.
        product_name: Snapshot of the product name at order time.
        unit_price: Price per unit at order time.
        quantity: Number of units ordered.
    """

    def __init__(
        self,
        product_id: uuid.UUID,
        product_name: str,
        unit_price: Money,
        quantity: int,
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.unit_price = unit_price
        self.quantity = quantity

    @property
    def subtotal(self) -> Money:
        """Calculate the subtotal for this line item."""
        return Money(
            amount=self.unit_price.amount * self.quantity,
            currency=self.unit_price.currency,
        )

    def __repr__(self) -> str:
        return f"<OrderItem {self.product_name} x{self.quantity}>"


class Order:
    """Represents a customer order.

    Attributes:
        id: Unique identifier.
        user_id: Identifier of the ordering user.
        items: Line items in the order.
        status: Current order status.
        shipping_address: Destination address.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    def __init__(
        self,
        user_id: uuid.UUID,
        items: list[OrderItem],
        shipping_address: Address,
        order_id: uuid.UUID | None = None,
        status: OrderStatus | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        from aegis.domain.value_objects import OrderStatus

        self.id = order_id or uuid.uuid4()
        self.user_id = user_id
        self.items = list(items)
        self.shipping_address = shipping_address
        self.status = status or OrderStatus.PENDING
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @property
    def total(self) -> Money:
        """Calculate the total order value."""
        if not self.items:
            from aegis.domain.value_objects import Money

            return Money(amount=0, currency="USD")
        currency = self.items[0].unit_price.currency
        total_amount = sum(item.subtotal.amount for item in self.items)
        return Money(amount=total_amount, currency=currency)

    def submit(self) -> None:
        """Transition the order from PENDING to SUBMITTED."""
        from aegis.domain.value_objects import OrderStatus

        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot submit order in status {self.status}")
        self.status = OrderStatus.SUBMITTED
        self.updated_at = datetime.utcnow()

    def ship(self) -> None:
        """Transition the order from SUBMITTED to SHIPPED."""
        from aegis.domain.value_objects import OrderStatus

        if self.status != OrderStatus.SUBMITTED:
            raise ValueError(f"Cannot ship order in status {self.status}")
        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.utcnow()

    def cancel(self) -> None:
        """Cancel the order (only if not already shipped)."""
        from aegis.domain.value_objects import OrderStatus

        if self.status == OrderStatus.SHIPPED:
            raise ValueError("Cannot cancel an order that has already shipped.")
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"<Order {self.id} {self.status.value}>"
