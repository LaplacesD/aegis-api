"""Internal event bus for publishing domain events to handlers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aegis.domain.events import DomainEvent


class EventBus:
    """Simple in-process event bus for publishing domain events.

    Handlers are registered per event type and invoked synchronously
    when the event is published.
    """

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[Callable[[DomainEvent], Any]]] = {}

    def register(
        self, event_type: type[DomainEvent], handler: Callable[[DomainEvent], Any]
    ) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The domain event class to subscribe to.
            handler: Callable that processes the event.
        """
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event: DomainEvent) -> None:
        """Publish an event to all registered handlers.

        Args:
            event: The domain event instance to publish.
        """
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            result = handler(event)
            if hasattr(result, "__await__"):
                await result

    def remove(self, event_type: type[DomainEvent], handler: Callable) -> None:
        """Unregister a handler for an event type.

        Args:
            event_type: The domain event class.
            handler: The handler to remove.
        """
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)
