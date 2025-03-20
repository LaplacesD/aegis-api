"""Initial migration: create users, orders, products tables.

Revision ID: 0001_initial
Revises:
Create Date: 2025-03-20 10:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "products",
        sa.Column("id", sa.Uuid(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("price_amount", sa.Float(), nullable=False),
        sa.Column("price_currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("stock_quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Uuid(), nullable=False, primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="pending"),
        sa.Column(
            "shipping_street", sa.String(length=255), nullable=False, server_default=""
        ),
        sa.Column("shipping_city", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("shipping_state", sa.String(length=100), nullable=False, server_default=""),
        sa.Column("shipping_zip", sa.String(length=20), nullable=False, server_default=""),
        sa.Column(
            "shipping_country", sa.String(length=100), nullable=False, server_default=""
        ),
        sa.Column("total_amount", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])

    op.create_table(
        "order_items",
        sa.Column("id", sa.Uuid(), nullable=False, primary_key=True),
        sa.Column("order_id", sa.Uuid(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("product_id", sa.Uuid(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("product_name", sa.String(length=255), nullable=False),
        sa.Column("unit_price_amount", sa.Float(), nullable=False),
        sa.Column("unit_price_currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("quantity", sa.Integer(), nullable=False),
    )
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])

    op.create_table(
        "events",
        sa.Column("id", sa.Uuid(), nullable=False, primary_key=True),
        sa.Column("aggregate_id", sa.String(length=36), nullable=False),
        sa.Column("aggregate_type", sa.String(length=100), nullable=False),
        sa.Column("event_type", sa.String(length=200), nullable=False),
        sa.Column("data", sa.Text(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("stored_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_events_aggregate_id", "events", ["aggregate_id"])


def downgrade() -> None:
    op.drop_table("events")
    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("users")
