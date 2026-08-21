from abc import ABC, abstractmethod


class ServiceProvider(ABC):
    @property
    @abstractmethod
    def booting_callbacks(self):
        """Returns the registered booting callbacks."""

    @property
    @abstractmethod
    def booted_callbacks(self):
        """Returns the registered booted callbacks."""

    @abstractmethod
    def register(self):
        """Registers services in the container."""

    @abstractmethod
    def boot(self):
        """Boots the services."""

    @abstractmethod
    def booting(self, callback):
        """Registers a booting callback."""

    @abstractmethod
    def booted(self, callback):
        """Registers a booted callback."""

    @abstractmethod
    def call_booting_callbacks(self):
        """Calls the registered booting callbacks."""

    @abstractmethod
    def call_booted_callbacks(self):
        """Calls the registered booted callbacks."""
