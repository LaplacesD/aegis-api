"""Domain events for Aegis API.

Defines events that capture meaningful state changes within the domain.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent:
    """Base class for all domain events.

    Attributes:
        event_id: Unique identifier for this event occurrence.
        occurred_at: Timestamp when the event was raised.
    """

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UserCreated(DomainEvent):
    """Emitted when a new user account is created."""

    user_id: uuid.UUID
    email: str
    name: str


@dataclass
class UserUpdated(DomainEvent):
    """Emitted when a user's details are modified."""

    user_id: uuid.UUID
    changes: dict[str, Any]


@dataclass
class OrderPlaced(DomainEvent):
    """Emitted when a new order is placed."""

    order_id: uuid.UUID
    user_id: uuid.UUID
    total_amount: float
    currency: str


@dataclass
class OrderShipped(DomainEvent):
    """Emitted when an order transitions to shipped status."""

    order_id: uuid.UUID
    tracking_number: str | None = None


@dataclass
class OrderCancelled(DomainEvent):
    """Emitted when an order is cancelled."""

    order_id: uuid.UUID
    reason: str = ""
