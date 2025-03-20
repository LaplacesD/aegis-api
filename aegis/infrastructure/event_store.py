"""Event store for event sourcing and audit trail."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from aegis.domain.events import DomainEvent


@dataclass
class StoredEvent:
    """A serialised domain event persisted in the event store.

    Attributes:
        event_id: Unique identifier of the event.
        aggregate_id: The aggregate root ID this event belongs to.
        aggregate_type: Type name of the aggregate (e.g. "Order").
        event_type: Fully-qualified event class name.
        data: JSON-serialisable event payload.
        occurred_at: When the event originally occurred.
        stored_at: When the event was persisted.
    """

    event_id: uuid.UUID
    aggregate_id: str
    aggregate_type: str
    event_type: str
    data: dict[str, Any]
    occurred_at: datetime
    stored_at: datetime = field(default_factory=datetime.utcnow)


class EventStore:
    """In-memory event store for recording domain events.

    In production this would write to a dedicated event store table.
    """

    def __init__(self) -> None:
        self._events: list[StoredEvent] = []

    async def append(self, aggregate_id: str, aggregate_type: str, event: DomainEvent) -> None:
        """Persist a domain event.

        Args:
            aggregate_id: The aggregate root ID.
            aggregate_type: The aggregate type name.
            event: The domain event to store.
        """
        stored = StoredEvent(
            event_id=event.event_id,
            aggregate_id=aggregate_id,
            aggregate_type=aggregate_type,
            event_type=type(event).__name__,
            data=event.__dict__,
            occurred_at=event.occurred_at,
        )
        self._events.append(stored)

    async def get_events_for_aggregate(self, aggregate_id: str) -> list[StoredEvent]:
        """Retrieve all events for a specific aggregate.

        Args:
            aggregate_id: Aggregate root ID to filter by.

        Returns:
            List of stored events, ordered by occurrence.
        """
        return [e for e in self._events if e.aggregate_id == aggregate_id]

    async def get_all_events(self) -> list[StoredEvent]:
        """Retrieve all stored events.

        Returns:
            All events in order of storage.
        """
        return list(self._events)
