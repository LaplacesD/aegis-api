"""Value objects for Aegis API.

Implements immutable value objects: Address, Money, Email, and OrderStatus.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass


_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class OrderStatus(str, enum.Enum):
    """Possible states of an order lifecycle."""

    PENDING = "pending"
    SUBMITTED = "submitted"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class Address:
    """Immutable postal address value object.

    Attributes:
        street: Street address line.
        city: City name.
        state: State or region.
        zip_code: Postal / ZIP code.
        country: Country name.
    """

    street: str
    city: str
    state: str
    zip_code: str
    country: str

    def __post_init__(self) -> None:
        if not self.street or not self.city:
            raise ValueError("Street and city are required.")

    def as_full_string(self) -> str:
        """Return the address as a single formatted string."""
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}, {self.country}"


@dataclass(frozen=True)
class Money:
    """Immutable monetary value object.

    Attributes:
        amount: Numeric value (decimal-compatible integer in smallest unit, or float).
        currency: ISO-4217 currency code (default: USD).
    """

    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative.")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a valid 3-letter ISO-4217 code.")

    def __add__(self, other: Money) -> Money:
        """Add two Money values of the same currency."""
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} != {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, factor: int | float) -> Money:
        """Multiply money by a scalar."""
        return Money(amount=self.amount * factor, currency=self.currency)


@dataclass(frozen=True)
class Email:
    """Immutable email address value object with format validation."""

    address: str

    def __post_init__(self) -> None:
        if not _EMAIL_PATTERN.match(self.address):
            raise ValueError(f"Invalid email address: {self.address}")

    def __str__(self) -> str:
        return self.address
