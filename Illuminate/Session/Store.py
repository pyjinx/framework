from __future__ import annotations

import secrets
from typing import Any


class Store:
    """Small Laravel-shaped session attribute bag pending real handlers."""

    def __init__(self, name: str = "pyjinx", session_id: str | None = None) -> None:
        self.name = name
        self.id = session_id or secrets.token_urlsafe(24)
        self.attributes: dict[str, Any] = {}
        self.started = False

    def start(self) -> Store:
        self.started = True
        return self

    def all(self) -> dict[str, Any]:
        return dict(self.attributes)

    def get(self, key: str, default: Any = None) -> Any:
        return self.attributes.get(key, default)

    def put(self, key: str | dict[str, Any], value: Any = None) -> Store:
        if isinstance(key, dict):
            self.attributes.update(key)
        else:
            self.attributes[key] = value
        return self

    def exists(self, key: str) -> bool:
        return key in self.attributes

    def missing(self, key: str) -> bool:
        return not self.exists(key)

    def has(self, *keys: str) -> bool:
        return all(self.get(key) is not None for key in keys)

    def has_any(self, *keys: str) -> bool:
        return any(self.get(key) is not None for key in keys)

    def pull(self, key: str, default: Any = None) -> Any:
        return self.attributes.pop(key, default)

    def push(self, key: str, value: Any) -> Store:
        values = self.attributes.setdefault(key, [])
        if not isinstance(values, list):
            raise TypeError(f"Session value [{key}] is not a list.")
        values.append(value)
        return self

    def increment(self, key: str, amount: int = 1) -> int:
        value = int(self.get(key, 0)) + amount
        self.attributes[key] = value
        return value

    def decrement(self, key: str, amount: int = 1) -> int:
        return self.increment(key, -amount)

    def forget(self, *keys: str) -> Store:
        for key in keys:
            self.attributes.pop(key, None)
        return self

    def flush(self) -> Store:
        self.attributes.clear()
        return self

    def invalidate(self) -> bool:
        self.flush()
        self.regenerate()
        return True

    def regenerate(self, destroy: bool = False) -> bool:
        self.id = secrets.token_urlsafe(24)
        return True

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.id

    def token(self) -> Any:
        return self.get("_token")

    def regenerate_token(self) -> None:
        self.put("_token", secrets.token_urlsafe(32))
