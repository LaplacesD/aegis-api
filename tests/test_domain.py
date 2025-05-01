"""Unit tests for domain entities, value objects, and events."""

from __future__ import annotations

import uuid

import pytest

from aegis.domain.entities import Order, OrderItem, Product, User
from aegis.domain.events import OrderPlaced, UserCreated
from aegis.domain.exceptions import ValidationError
from aegis.domain.value_objects import Address, Email, Money, OrderStatus


class TestUser:
    """Tests for the User entity."""

    def test_create_user(self) -> None:
        """A user should be created with default values."""
        user = User(email=Email("alice@example.com"), name="Alice")
        assert user.name == "Alice"
        assert str(user.email) == "alice@example.com"
        assert user.is_active is True
        assert user.id is not None

    def test_deactivate_user(self) -> None:
        """Deactivating a user should set is_active to False."""
        user = User(email=Email("bob@example.com"), name="Bob")
        user.deactivate()
        assert user.is_active is False

    def test_rename_user(self) -> None:
        """Renaming a user should update the name."""
        user = User(email=Email("carol@example.com"), name="Carol")
        user.rename("Carolyn")
        assert user.name == "Carolyn"


class TestProduct:
    """Tests for the Product entity."""

    def test_create_product(self) -> None:
        """A product should be created with given attributes."""
        product = Product(
            name="Widget",
            price=Money(amount=9.99),
            stock_quantity=100,
        )
        assert product.name == "Widget"
        assert product.price.amount == 9.99
        assert product.stock_quantity == 100

    def test_restock_adds_inventory(self) -> None:
        """Restocking should add to stock_quantity."""
        product = Product(name="Gadget", price=Money(amount=19.99), stock_quantity=10)
        product.restock(5)
        assert product.stock_quantity == 15

    def test_reserve_reduces_stock(self) -> None:
        """Reserving should reduce stock_quantity."""
        product = Product(name="Gizmo", price=Money(amount=4.99), stock_quantity=20)
        product.reserve(3)
        assert product.stock_quantity == 17

    def test_reserve_insufficient_stock_raises(self) -> None:
        """Reserving more than available should raise."""
        product = Product(name="Gizmo", price=Money(amount=4.99), stock_quantity=1)
        with pytest.raises(ValueError, match="Insufficient stock"):
            product.reserve(5)


class TestOrder:
    """Tests for the Order entity."""

    def test_create_order(self) -> None:
        """An order should start in PENDING status."""
        user_id = uuid.uuid4()
        items = [
            OrderItem(
                product_id=uuid.uuid4(),
                product_name="Item A",
                unit_price=Money(amount=10.0),
                quantity=2,
            )
        ]
        address = Address(
            street="123 Main St", city="Springfield",
            state="IL", zip_code="62701", country="US",
        )
        order = Order(user_id=user_id, items=items, shipping_address=address)
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 1

    def test_order_total(self) -> None:
        """Order total should be sum of item subtotals."""
        user_id = uuid.uuid4()
        items = [
            OrderItem(
                product_id=uuid.uuid4(),
                product_name="Item A",
                unit_price=Money(amount=10.0),
                quantity=2,
            ),
            OrderItem(
                product_id=uuid.uuid4(),
                product_name="Item B",
                unit_price=Money(amount=5.0),
                quantity=3,
            ),
        ]
        address = Address(
            street="456 Oak Ave", city="Portland",
            state="OR", zip_code="97201", country="US",
        )
        order = Order(user_id=user_id, items=items, shipping_address=address)
        assert order.total.amount == 35.0  # (10*2) + (5*3)

    def test_submit_order(self) -> None:
        """Submitting a PENDING order should transition to SUBMITTED."""
        user_id = uuid.uuid4()
        items = [
            OrderItem(
                product_id=uuid.uuid4(),
                product_name="Item",
                unit_price=Money(amount=1.0),
                quantity=1,
            )
        ]
        address = Address("1 Main St", "City", "ST", "00000", "US")
        order = Order(user_id=user_id, items=items, shipping_address=address)
        order.submit()
        assert order.status == OrderStatus.SUBMITTED

    def test_submit_non_pending_raises(self) -> None:
        """Submitting a non-PENDING order should raise."""
        user_id = uuid.uuid4()
        items = [
            OrderItem(
                product_id=uuid.uuid4(),
                product_name="X",
                unit_price=Money(amount=1.0),
                quantity=1,
            )
        ]
        address = Address("1 Main St", "City", "ST", "00000", "US")
        order = Order(user_id=user_id, items=items, shipping_address=address)
        order.submit()
        with pytest.raises(ValueError, match="Cannot submit"):
            order.submit()


class TestEmail:
    """Tests for the Email value object."""

    def test_valid_email(self) -> None:
        """A valid email should be accepted."""
        email = Email("user@example.com")
        assert str(email) == "user@example.com"

    def test_invalid_email(self) -> None:
        """An invalid email should raise."""
        with pytest.raises(ValueError, match="Invalid email"):
            Email("not-an-email")


class TestMoney:
    """Tests for the Money value object."""

    def test_money_creation(self) -> None:
        """Money should store amount and currency."""
        m = Money(amount=10.50, currency="USD")
        assert m.amount == 10.50
        assert m.currency == "USD"

    def test_money_addition(self) -> None:
        """Adding same-currency money should work."""
        a = Money(amount=5.0)
        b = Money(amount=3.0)
        assert (a + b).amount == 8.0

    def test_money_currency_mismatch(self) -> None:
        """Adding different currencies should raise."""
        a = Money(amount=5.0, currency="USD")
        b = Money(amount=3.0, currency="EUR")
        with pytest.raises(ValueError, match="Currency mismatch"):
            _ = a + b


class TestDomainEvents:
    """Tests for domain event creation."""

    def test_user_created_event(self) -> None:
        """UserCreated event should carry user data."""
        event = UserCreated(
            user_id=uuid.uuid4(),
            email="new@user.com",
            name="New User",
        )
        assert event.email == "new@user.com"
        assert event.event_id is not None

    def test_order_placed_event(self) -> None:
        """OrderPlaced event should carry order data."""
        event = OrderPlaced(
            order_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            total_amount=100.0,
            currency="USD",
        )
        assert event.total_amount == 100.0
