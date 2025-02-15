"""Query to retrieve a single user."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class GetUserQuery:
    """Query to retrieve a user by their unique identifier.

    Attributes:
        user_id: UUID of the user to look up.
    """

    user_id: uuid.UUID
    query_id: uuid.UUID = field(default_factory=uuid.uuid4)
