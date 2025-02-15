"""Application layer for Aegis API.

Implements CQRS pattern with commands, queries, and their handlers.
"""

from aegis.application.commands import CreateOrderCommand, UpdateUserCommand
from aegis.application.queries import GetOrdersQuery, GetUserQuery
from aegis.application.dto import UserDTO, OrderDTO, ProductDTO
from aegis.application.handlers import CommandHandler, QueryHandler
from aegis.application.mediator import Mediator

__all__ = [
    "CreateOrderCommand",
    "UpdateUserCommand",
    "GetOrdersQuery",
    "GetUserQuery",
    "UserDTO",
    "OrderDTO",
    "ProductDTO",
    "CommandHandler",
    "QueryHandler",
    "Mediator",
]
