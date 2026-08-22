from __future__ import annotations

from typing import Any, Callable


class RequestGuard:
    """Request callback guard with per-request user caching."""

    def __init__(
        self,
        callback: Callable[[Any], Any],
        request: Any,
        provider: Any = None,
    ) -> None:
        self.callback = callback
        self.request = request
        self.provider = provider
        self._user = None
        self._resolved = False

    def user(self):
        if not self._resolved:
            self._user = self.callback(self.request)
            self._resolved = True
        return self._user

    def check(self) -> bool:
        return self.user() is not None

    def guest(self) -> bool:
        return not self.check()

    def id(self):
        user = self.user()
        if user is None:
            return None
        identifier = getattr(user, "get_auth_identifier", None)
        return identifier() if callable(identifier) else getattr(user, "id", None)

    def validate(self, credentials: dict[str, Any] | None = None) -> bool:
        return self.check()

    def has_user(self) -> bool:
        return self._user is not None

    def set_user(self, user: Any) -> RequestGuard:
        self._user = user
        self._resolved = True
        return self

    def set_request(self, request: Any) -> RequestGuard:
        self.request = request
        self._user = None
        self._resolved = False
        return self

    def get_provider(self):
        return self.provider
