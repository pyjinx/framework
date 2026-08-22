from __future__ import annotations

from collections.abc import Callable
from typing import Any


class AuthenticationException(Exception):
    """Raised when no configured authentication guard authenticates a request."""

    _redirect_to_callback: Callable[[Any], str | None] | None = None

    def __init__(
        self,
        message: str = "Unauthenticated.",
        guards: list[str] | None = None,
        redirect_to: str | None = None,
    ) -> None:
        super().__init__(message)
        self._guards = list(guards or [])
        self._redirect_to = redirect_to

    def guards(self) -> list[str]:
        return list(self._guards)

    def redirect_to(self, request: Any) -> str | None:
        if self._redirect_to:
            return self._redirect_to
        callback = type(self)._redirect_to_callback
        if callback is not None:
            return callback(request)
        return None

    @classmethod
    def redirect_using(cls, callback: Callable[[Any], str | None]) -> None:
        cls._redirect_to_callback = callback
