"""Command to create a new order."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aegis.application.dto import OrderItemDTO


@dataclass
class CreateOrderCommand:
    """Command to place a new order.

    Attributes:
        user_id: The identifier of the user placing the order.
        items: Line items to include in the order.
        shipping_street: Street address for shipping.
        shipping_city: City for shipping.
        shipping_state: State for shipping.
        shipping_zip: ZIP code for shipping.
        shipping_country: Country for shipping.
    """

    user_id: uuid.UUID
    items: list[OrderItemDTO]
    shipping_street: str
    shipping_city: str
    shipping_state: str
    shipping_zip: str
    shipping_country: str
    command_id: uuid.UUID = field(default_factory=uuid.uuid4)
