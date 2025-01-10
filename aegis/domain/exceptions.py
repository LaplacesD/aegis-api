"""Domain-specific exceptions for Aegis API."""


class DomainError(Exception):
    """Base exception for all domain-level errors."""


class EntityNotFoundError(DomainError):
    """Raised when a requested domain entity cannot be located."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class InvalidOperationError(DomainError):
    """Raised when an operation is invalid for the current entity state."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(DomainError):
    """Raised when domain validation constraints are violated."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation failed on {field}: {message}")
