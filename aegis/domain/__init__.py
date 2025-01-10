"""Domain layer for Aegis API."""

from aegis.domain.entities import User, Order, Product, OrderItem
from aegis.domain.value_objects import Address, Money, Email, OrderStatus
from aegis.domain.events import DomainEvent, UserCreated, OrderPlaced, OrderShipped
from aegis.domain.repositories import UserRepository, OrderRepository, ProductRepository
from aegis.domain.exceptions import (
    DomainError,
    EntityNotFoundError,
    InvalidOperationError,
    ValidationError,
)

__all__ = [
    "User",
    "Order",
    "Product",
    "OrderItem",
    "Address",
    "Money",
    "Email",
    "OrderStatus",
    "DomainEvent",
    "UserCreated",
    "OrderPlaced",
    "OrderShipped",
    "UserRepository",
    "OrderRepository",
    "ProductRepository",
    "DomainError",
    "EntityNotFoundError",
    "InvalidOperationError",
    "ValidationError",
]
