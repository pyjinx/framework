from abc import abstractmethod
from pathlib import Path
from typing import Any, Self

from Illuminate.Contracts.Container.Container import Container
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Http.RequestAdapter import RequestAdapter


class Application(Container):
    @property
    @abstractmethod
    def service_providers(self):
        """Returns the list of registered service providers."""

    @property
    @abstractmethod
    def loaded_providers(self):
        """Returns the loaded providers."""

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        """Gets the instance from the container."""

    @abstractmethod
    def is_booted(self) -> bool:
        """Checks if the application is booted."""

    @abstractmethod
    def has_been_bootstrapped(self) -> bool:
        """Checks if the application has been bootstrapped."""

    @abstractmethod
    def before_bootstrapping(self, bootstrapper: str, callback: Any):
        """Registers a callback before bootstrapping."""

    @abstractmethod
    def after_bootstrapping(self, bootstrapper: str, callback: Any):
        """Registers a callback after bootstrapping."""

    @abstractmethod
    def bootstrap_with(self, bootstrappers: list):
        """Bootstraps the application with the given bootstrappers."""

    @abstractmethod
    def base_path(self, path: str = "") -> Path:
        """Returns the base path of the application."""

    @abstractmethod
    def app_path(self, path: str = "") -> Path:
        """Returns the app path of the application."""

    @abstractmethod
    def use_app_path(self, path: Path):
        """Sets the application path."""

    @abstractmethod
    def config_path(self, path: str = "") -> Path:
        """Returns the config path of the application."""

    @abstractmethod
    def use_config_path(self, path: Path):
        """Sets the config path of the application."""

    @abstractmethod
    def bind(self, *args, **kwargs) -> None:
        """Binds an abstract to a concrete implementation."""

    @abstractmethod
    def singleton(self, *args, **kwargs) -> None:
        """Binds a singleton instance to the container."""

    @abstractmethod
    def make(self, *args, **kwargs) -> Any:
        """Resolves an instance from the container."""

    @abstractmethod
    def get_provider(self, base_key: str):
        """Gets the service provider by base key."""

    @abstractmethod
    def register_configured_providers(self) -> Any:
        """Registers providers configured in the application."""

    @abstractmethod
    def boot(self) -> Any:
        """Boots the application."""

    @abstractmethod
    def booting(self, callback: Any):
        """Registers a callback to be called during the booting process."""

    @abstractmethod
    def booted(self, callback: Any):
        """Registers a callback to be called after the boot process."""

    @abstractmethod
    def register(self, provider_class: type):
        """Registers a service provider with the application."""

    @abstractmethod
    def boot_provider(self, service_provider: Any) -> Any:
        """Boots a service provider."""

    @abstractmethod
    def detect_environment(self, callback: Any):
        """Detects the application environment."""

    @abstractmethod
    def provider_is_loaded(self, base_key: str):
        """Gets the service provider by base key."""

    @abstractmethod
    def handle_request(self, request: RequestAdapter):
        """handle incoming request."""

    @abstractmethod
    def handle_command(self, input: ArgvInput):
        """handle command."""

    @abstractmethod
    def terminate(self):
        """terminate application."""

    @abstractmethod
    def running_in_console(self) -> bool:
        """handle command."""

    @abstractmethod
    def set_running_in_console(self) -> Self:
        """handle command."""
