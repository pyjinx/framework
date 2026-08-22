from __future__ import annotations

import hmac
from collections.abc import Callable
from typing import Any


class EloquentUserProvider:
    """Laravel-shaped provider backed by an Eloquent model class."""

    def __init__(self, hasher: Any, model: type) -> None:
        self.hasher = hasher
        self.model = model
        self.query_callback: Callable[[Any], Any] | None = None

    def retrieve_by_id(self, identifier: Any):
        model = self.create_model()
        return (
            self._new_model_query(model)
            .where(model.get_auth_identifier_name(), identifier)
            .first()
        )

    def retrieve_by_token(self, identifier: Any, token: str):
        model = self.create_model()
        retrieved_model = (
            self._new_model_query(model)
            .where(model.get_auth_identifier_name(), identifier)
            .first()
        )

        if retrieved_model is None:
            return None

        remember_token = retrieved_model.get_remember_token()
        if not remember_token:
            return None

        try:
            return (
                retrieved_model
                if hmac.compare_digest(remember_token, token)
                else None
            )
        except (TypeError, ValueError):
            return None

    def update_remember_token(self, user: Any, token: str) -> None:
        user.set_remember_token(token)
        timestamps = getattr(user, "timestamps", None)
        if timestamps is None:
            user.save()
            return

        user.timestamps = False
        try:
            user.save()
        finally:
            user.timestamps = timestamps

    def retrieve_by_credentials(self, credentials: dict[Any, Any]):
        credentials = {
            key: value
            for key, value in credentials.items()
            if "password" not in str(key)
        }

        if not credentials:
            return None

        query = self._new_model_query()
        for key, value in credentials.items():
            if callable(value):
                value(query)
            elif isinstance(value, (list, tuple, set, frozenset)):
                query.where_in(key, value)
            else:
                query.where(key, value)

        return query.first()

    def validate_credentials(self, user: Any, credentials: dict[str, Any]) -> bool:
        password = credentials.get("password")
        if password is None:
            return False

        stored = user.get_auth_password()
        if stored is None:
            return False

        if callable(getattr(self.hasher, "check", None)):
            return bool(self.hasher.check(password, stored))
        if callable(self.hasher):
            return bool(self.hasher(password, stored))
        raise TypeError("User provider has no password-checking hasher.")

    def rehash_password_if_required(
        self, user: Any, credentials: dict[str, Any], force: bool = False
    ) -> None:
        if not force and not self.hasher.needs_rehash(user.get_auth_password()):
            return

        user.force_fill(
            {user.get_auth_password_name(): self.hasher.make(credentials["password"])}
        ).save()

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

    def get_query_callback(self):
        return self.query_callback

    def _new_model_query(self, model: Any | None = None):
        model = model or self.create_model()
        new_query = getattr(model, "new_query", None)
        query = new_query() if callable(new_query) else self.model.query()
        if self.query_callback is not None:
            self.query_callback(query)
        return query
