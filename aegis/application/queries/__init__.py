"""Query definitions for the Aegis API."""

from .get_orders import GetOrdersQuery
from .get_user import GetUserQuery

__all__ = [
    "GetOrdersQuery",
    "GetUserQuery",
]
