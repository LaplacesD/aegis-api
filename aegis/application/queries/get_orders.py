"""Query to retrieve orders."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class GetOrdersQuery:
    """Query to retrieve orders by user.

    Attributes:
        user_id: Filter orders for this user.
        limit: Maximum number of orders to return.
        offset: Number of orders to skip for pagination.
    """

    user_id: uuid.UUID
    limit: int = 20
    offset: int = 0
    query_id: uuid.UUID = field(default_factory=uuid.uuid4)
