"""Products API v1 endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from aegis.api.dependencies import get_mediator
from aegis.api.schemas import ProductCreateRequest, ProductResponse

router = APIRouter(prefix="/v1/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    body: ProductCreateRequest,
) -> ProductResponse:
    """Create a new product."""
    from aegis.domain.entities import Product
    from aegis.domain.value_objects import Money

    product = Product(
        name=body.name,
        price=Money(amount=body.price, currency=body.currency),
        description=body.description,
        stock_quantity=body.stock_quantity,
    )
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price.amount,
        currency=product.price.currency,
        stock_quantity=product.stock_quantity,
        is_available=product.is_available,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
) -> ProductResponse:
    """Retrieve a product by its unique identifier."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Product retrieval not yet implemented.",
    )


@router.get("/", response_model=list[ProductResponse])
async def list_products() -> list[ProductResponse]:
    """List all available products."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Product listing not yet implemented.",
    )
