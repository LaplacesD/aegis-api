"""Command and query handlers for Aegis API."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class CommandHandler(ABC, Generic[T, R]):
    """Base class for command handlers.

    Type Parameters:
        T: The command type this handler processes.
        R: The return type of the handler.
    """

    @abstractmethod
    async def handle(self, command: T) -> R:
        """Execute the command.

        Args:
            command: The command to handle.

        Returns:
            Handler result.
        """
        ...


class QueryHandler(ABC, Generic[T, R]):
    """Base class for query handlers.

    Type Parameters:
        T: The query type this handler processes.
        R: The return type of the handler.
    """

    @abstractmethod
    async def handle(self, query: T) -> R:
        """Execute the query.

        Args:
            query: The query to handle.

        Returns:
            Query result.
        """
        ...


class CreateOrderHandler(CommandHandler["CreateOrderCommand", "OrderDTO"]):
    """Handler for CreateOrderCommand."""

    def __init__(
        self,
        order_repo: "OrderRepository",
        product_repo: "ProductRepository",
        user_repo: "UserRepository",
    ) -> None:
        self._order_repo = order_repo
        self._product_repo = product_repo
        self._user_repo = user_repo

    async def handle(self, command: "CreateOrderCommand") -> "OrderDTO":
        """Process order creation.

        Args:
            command: The create order command.

        Returns:
            The newly created order as a DTO.

        Raises:
            EntityNotFoundError: If the user or any product is not found.
        """
        from aegis.domain.entities import Order, OrderItem
        from aegis.domain.exceptions import EntityNotFoundError
        from aegis.domain.value_objects import Address, Money

        user = await self._user_repo.get_by_id(command.user_id)
        if user is None:
            raise EntityNotFoundError("User", str(command.user_id))

        items: list[OrderItem] = []
        for item_dto in command.items:
            product = await self._product_repo.get_by_id(item_dto.product_id)
            if product is None:
                raise EntityNotFoundError("Product", str(item_dto.product_id))
            items.append(
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=item_dto.quantity,
                )
            )
            product.reserve(item_dto.quantity)
            await self._product_repo.update(product)

        shipping = Address(
            street=command.shipping_street,
            city=command.shipping_city,
            state=command.shipping_state,
            zip_code=command.shipping_zip,
            country=command.shipping_country,
        )

        order = Order(
            user_id=command.user_id,
            items=items,
            shipping_address=shipping,
        )

        await self._order_repo.add(order)
        return OrderDTO.from_entity(order)


class UpdateUserHandler(CommandHandler["UpdateUserCommand", "UserDTO"]):
    """Handler for UpdateUserCommand."""

    def __init__(self, user_repo: "UserRepository") -> None:
        self._user_repo = user_repo

    async def handle(self, command: "UpdateUserCommand") -> "UserDTO":
        """Process user update.

        Args:
            command: The update user command.

        Returns:
            The updated user as a DTO.

        Raises:
            EntityNotFoundError: If the user is not found.
        """
        from aegis.domain.exceptions import EntityNotFoundError
        from aegis.domain.value_objects import Email

        user = await self._user_repo.get_by_id(command.user_id)
        if user is None:
            raise EntityNotFoundError("User", str(command.user_id))

        if command.name is not None:
            user.rename(command.name)
        if command.email is not None:
            user.email = Email(command.email)

        await self._user_repo.update(user)
        return UserDTO.from_entity(user)


class GetUserHandler(QueryHandler["GetUserQuery", "UserDTO | None"]):
    """Handler for GetUserQuery."""

    def __init__(self, user_repo: "UserRepository") -> None:
        self._user_repo = user_repo

    async def handle(self, query: "GetUserQuery") -> "UserDTO | None":
        """Process user retrieval.

        Args:
            query: The get user query.

        Returns:
            A UserDTO if found, otherwise None.
        """
        user = await self._user_repo.get_by_id(query.user_id)
        if user is None:
            return None
        return UserDTO.from_entity(user)


class GetOrdersHandler(QueryHandler["GetOrdersQuery", "list[OrderDTO]"]):
    """Handler for GetOrdersQuery."""

    def __init__(self, order_repo: "OrderRepository") -> None:
        self._order_repo = order_repo

    async def handle(self, query: "GetOrdersQuery") -> "list[OrderDTO]":
        """Process order retrieval.

        Args:
            query: The get orders query.

        Returns:
            List of OrderDTOs for the requested user.
        """
        orders = await self._order_repo.get_by_user(query.user_id)
        return [OrderDTO.from_entity(order) for order in orders]
