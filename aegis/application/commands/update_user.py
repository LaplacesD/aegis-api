"""Command to update an existing user."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field


@dataclass
class UpdateUserCommand:
    """Command to modify a user's details.

    Attributes:
        user_id: Identifier of the user to update.
        name: New display name (if changing).
        email: New email address (if changing).
    """

    user_id: uuid.UUID
    name: str | None = None
    email: str | None = None
    command_id: uuid.UUID = field(default_factory=uuid.uuid4)
