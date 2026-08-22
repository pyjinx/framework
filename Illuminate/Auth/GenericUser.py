from __future__ import annotations

from typing import Any


class GenericUser:
    """Attribute-backed authenticatable user matching Laravel GenericUser."""

    def __init__(self, attributes: dict[str, Any]) -> None:
        self.attributes = dict(attributes)

    def get_auth_identifier_name(self) -> str:
        return "id"

    def get_auth_identifier(self) -> Any:
        return self.attributes.get(self.get_auth_identifier_name())

    def get_auth_password_name(self) -> str:
        return "password"

    def get_auth_password(self) -> Any:
        return self.attributes.get(self.get_auth_password_name())

    def get_remember_token(self) -> Any:
        return self.attributes.get(self.get_remember_token_name())

    def set_remember_token(self, value: Any) -> None:
        self.attributes[self.get_remember_token_name()] = value

    def get_remember_token_name(self) -> str:
        return "remember_token"

    def __getattr__(self, key: str) -> Any:
        try:
            return self.attributes[key]
        except KeyError as error:
            raise AttributeError(key) from error

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "attributes":
            object.__setattr__(self, key, value)
        else:
            self.attributes[key] = value
