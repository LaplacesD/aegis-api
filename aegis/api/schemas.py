"""Pydantic request/response schemas for the API."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str


# ---- User schemas ----


class UserCreateRequest(BaseModel):
    """Request body for creating a user."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserUpdateRequest(BaseModel):
    """Request body for updating a user."""

    name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None


class UserResponse(BaseModel):
    """Response body for a user."""

    id: uuid.UUID
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---- Product schemas ----


class ProductCreateRequest(BaseModel):
    """Request body for creating a product."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str = ""
    price: float = Field(..., gt=0)
    currency: str = "USD"
    stock_quantity: int = Field(default=0, ge=0)


class ProductResponse(BaseModel):
    """Response body for a product."""

    id: uuid.UUID
    name: str
    description: str
    price: float
    currency: str
    stock_quantity: int
    is_available: bool

    model_config = {"from_attributes": True}


# ---- Order schemas ----


class OrderItemRequest(BaseModel):
    """Request body for an order line item."""

    product_id: uuid.UUID
    quantity: int = Field(..., ge=1)


class CreateOrderRequest(BaseModel):
    """Request body for creating an order."""

    items: list[OrderItemRequest] = Field(..., min_length=1)
    shipping_street: str
    shipping_city: str
    shipping_state: str
    shipping_zip: str
    shipping_country: str


class OrderItemResponse(BaseModel):
    """Response body for an order line item."""

    product_id: uuid.UUID
    product_name: str
    unit_price: float
    quantity: int
    subtotal: float


class OrderResponse(BaseModel):
    """Response body for an order."""

    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    total_amount: float
    currency: str
    items: list[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    """Standard error response body."""

    detail: str
    error_code: str | None = None
