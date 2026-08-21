from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class Container(ABC):
    @abstractmethod
    def bind(self, key: str, binding_resolver: Callable) -> None:
        """Bind a key to a binding resolver."""

    @abstractmethod
    def singleton(self, key: str, binding_resolver: Callable) -> None:
        """Bind a key to a binding resolver as a singleton."""

    @abstractmethod
    def make(self, key: str, make_args: dict[str, Any] | None = None) -> Any:
        """Resolve and create an instance of the given key."""

    @abstractmethod
    def bound(self, key: str) -> bool:
        """Check if a key is bound in the container."""

    @abstractmethod
    def alias(self, abstract_alias: str, alias: str) -> None:
        """Create an alias for an abstract key."""

    @abstractmethod
    def instance(self, key: str, instance: Any) -> Any:
        """Register an instance with a specific key."""

    @abstractmethod
    def forget_binding(self, key: str) -> None:
        """Remove a binding from the container."""

    @abstractmethod
    def forget_instance(self, key: str) -> None:
        """Remove an instance from the container."""

    @abstractmethod
    def flush(self) -> None:
        """flush the container, clearing all bindings and instances."""

    @abstractmethod
    def has(self, key: str) -> bool:
        """Check if a key exists in the container."""

    @abstractmethod
    def get_aliases(self) -> dict[str, str]:
        """Retrieve all aliases in the container."""

    @abstractmethod
    def get_bindings(self) -> dict[str, dict[str, Any]]:
        """Retrieve all bindings in the container."""

    @abstractmethod
    def get_instances(self) -> dict[str, Any]:
        """Retrieve all instances in the container."""

    @abstractmethod
    def get_resolved(self) -> dict[str, bool]:
        """Retrieve the resolved status of bindings."""
