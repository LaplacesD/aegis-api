"""Mediator pattern implementation for decoupled CQRS dispatch."""

from __future__ import annotations

from typing import Any

from aegis.application.handlers import CommandHandler, QueryHandler


class Mediator:
    """Dispatches commands and queries to their registered handlers.

    Provides a central hub that decouples the caller from the handler
    implementation, following the Mediator pattern.
    """

    def __init__(self) -> None:
        self._command_handlers: dict[type, CommandHandler] = {}
        self._query_handlers: dict[type, QueryHandler] = {}

    def register_command(
        self, command_type: type, handler: CommandHandler
    ) -> None:
        """Register a handler for a command type.

        Args:
            command_type: The command class to handle.
            handler: The handler instance.
        """
        self._command_handlers[command_type] = handler

    def register_query(
        self, query_type: type, handler: QueryHandler
    ) -> None:
        """Register a handler for a query type.

        Args:
            query_type: The query class to handle.
            handler: The handler instance.
        """
        self._query_handlers[query_type] = handler

    async def send(self, command: Any) -> Any:
        """Dispatch a command to its registered handler.

        Args:
            command: The command instance to dispatch.

        Returns:
            The result from the command handler.

        Raises:
            ValueError: If no handler is registered for the command type.
        """
        handler = self._command_handlers.get(type(command))
        if handler is None:
            raise ValueError(f"No handler registered for {type(command).__name__}")
        return await handler.handle(command)

    async def query(self, query: Any) -> Any:
        """Dispatch a query to its registered handler.

        Args:
            query: The query instance to dispatch.

        Returns:
            The result from the query handler.

        Raises:
            ValueError: If no handler is registered for the query type.
        """
        handler = self._query_handlers.get(type(query))
        if handler is None:
            raise ValueError(f"No handler registered for {type(query).__name__}")
        return await handler.handle(query)
