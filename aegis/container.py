"""Dependency injection container for Aegis API."""

from dataclasses import dataclass, field

from aegis.config import Settings


@dataclass
class Container:
    """Application dependency injection container.

    Holds all application-level singletons and wiring.
    """

    settings: Settings
    _services: dict = field(default_factory=dict)

    def get(self, key: str, default=None):
        """Retrieve a registered service by key.

        Args:
            key: Service identifier.
            default: Returned if key is not registered.

        Returns:
            The registered service instance, or *default*.
        """
        return self._services.get(key, default)

    def set(self, key: str, service) -> None:
        """Register a service in the container.

        Args:
            key: Service identifier.
            service: The service instance to register.
        """
        self._services[key] = service
