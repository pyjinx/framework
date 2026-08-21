from abc import ABC, abstractmethod
from datetime import datetime

from Illuminate.Contracts.Http.Request import Request
from Illuminate.Contracts.Http.Response import Response


class Kernel(ABC):
    @property
    @abstractmethod
    def middleware(self):
        """Returns the list of middlewares."""

    @property
    @abstractmethod
    def bootstrappers(self):
        """Returns the list of bootstrappers."""

    @property
    @abstractmethod
    def request_started_at(self) -> datetime:
        """Returns the request start time."""

    @abstractmethod
    def handle(self, request: Request):
        """Handles the incoming request."""

    @abstractmethod
    def terminate(self, request: Request, response: Response):
        """Handles the incoming request."""

    @abstractmethod
    def push_middleware(self):
        """Bootstraps the application if it hasn't been bootstrapped."""
