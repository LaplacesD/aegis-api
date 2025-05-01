"""Orders API v1 endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from aegis.api.dependencies import get_mediator
from aegis.api.schemas import (
    CreateOrderRequest,
    OrderItemResponse,
    OrderResponse,
)
from aegis.application.commands.create_order import CreateOrderCommand
from aegis.application.dto import OrderItemDTO
from aegis.application.mediator import Mediator
from aegis.application.queries.get_orders import GetOrdersQuery

router = APIRouter(prefix="/v1/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    body: CreateOrderRequest,
    mediator: Mediator = Depends(get_mediator),
) -> OrderResponse:
    """Place a new order."""
    items = [
        OrderItemDTO(
            product_id=item.product_id,
            product_name="",  # resolved from product repo in handler
            unit_price=0.0,
            quantity=item.quantity,
        )
        for item in body.items
    ]
    command = CreateOrderCommand(
        user_id=uuid.uuid4(),  # would come from auth context
        items=items,
        shipping_street=body.shipping_street,
        shipping_city=body.shipping_city,
        shipping_state=body.shipping_state,
        shipping_zip=body.shipping_zip,
        shipping_country=body.shipping_country,
    )
    result = await mediator.send(command)
    return OrderResponse(
        id=result.id,
        user_id=result.user_id,
        status=result.status,
        total_amount=result.total_amount,
        currency=result.currency,
        items=[
            OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product_name,
                unit_price=item.unit_price,
                quantity=item.quantity,
                subtotal=item.unit_price * item.quantity,
            )
            for item in result.items
        ],
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    user_id: uuid.UUID,
    mediator: Mediator = Depends(get_mediator),
) -> list[OrderResponse]:
    """List orders for a specific user."""
    query = GetOrdersQuery(user_id=user_id)
    results = await mediator.query(query)
    return [
        OrderResponse(
            id=o.id,
            user_id=o.user_id,
            status=o.status,
            total_amount=o.total_amount,
            currency=o.currency,
            items=[
                OrderItemResponse(
                    product_id=item.product_id,
                    product_name=item.product_name,
                    unit_price=item.unit_price,
                    quantity=item.quantity,
                    subtotal=item.unit_price * item.quantity,
                )
                for item in o.items
            ],
            created_at=o.created_at,
            updated_at=o.updated_at,
        )
        for o in results
    ]
