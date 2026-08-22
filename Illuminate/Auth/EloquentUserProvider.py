from __future__ import annotations

from collections.abc import Callable
from typing import Any


class EloquentUserProvider:
    """Laravel-shaped provider backed by an Eloquent model class."""

    def __init__(self, hasher: Any, model: type) -> None:
        self.hasher = hasher
        self.model = model
        self.query_callback: Callable[[Any], Any] | None = None

    def retrieve_by_id(self, identifier: Any):
        return self.model.query().where(self._identifier_name(), identifier).first()

    def retrieve_by_token(self, identifier: Any, token: str):
        user = self.retrieve_by_id(identifier)
        if user is None:
            return None
        return user if user.get_remember_token() == token else None

    def update_remember_token(self, user: Any, token: str) -> None:
        user.set_remember_token(token)
        user.save()

    def retrieve_by_credentials(self, credentials: dict[str, Any]):
        query = self.model.query()
        for key, value in credentials.items():
            if key not in {"password", "remember_token"}:
                query = query.where(key, value)
        if self.query_callback is not None:
            query = self.query_callback(query)
        return query.first()

    def validate_credentials(self, user: Any, credentials: dict[str, Any]) -> bool:
        password = credentials.get("password")
        if password is None:
            return False
        stored = user.get_auth_password()
        if callable(getattr(self.hasher, "check", None)):
            return bool(self.hasher.check(password, stored))
        if callable(self.hasher):
            return bool(self.hasher(password, stored))
        raise TypeError("User provider has no password-checking hasher.")

    def create_model(self):
        return self.model()

    def get_hasher(self):
        return self.hasher

    def set_hasher(self, hasher: Any):
        self.hasher = hasher
        return self

    def get_model(self):
        return self.model

    def set_model(self, model: type):
        self.model = model
        return self

    def with_query(self, callback: Callable[[Any], Any] | None = None):
        self.query_callback = callback
        return self

    def _identifier_name(self) -> str:
        return self.model().get_auth_identifier_name() if hasattr(
            self.model(), "get_auth_identifier_name"
        ) else self.model.primary_key
