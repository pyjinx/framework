from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from sqlalchemy.engine import Engine


class Connection:
    """Laravel-shaped connection boundary over a SQLAlchemy engine."""

    def __init__(
        self,
        engine: Engine,
        name: str,
        config: dict | None = None,
    ) -> None:
        self.engine = engine
        self._name = name
        self._config = dict(config or {})
        self.reconnector: Callable[[Connection], object] | None = None

    @property
    def url(self):
        return self.engine.url

    def __getattr__(self, name: str):
        return getattr(self.engine, name)

    def connect(self):
        return self.engine.connect()

    def begin(self):
        return self.engine.begin()

    def raw_connection(self):
        return self.engine.raw_connection()

    def get_pdo(self):
        return self.raw_connection()

    def get_raw_pdo(self):
        return self.get_pdo()

    def get_read_pdo(self):
        return self.get_pdo()

    def get_name(self) -> str:
        return self._name

    def get_name_with_read_write_type(self, connection_type: str | None = None) -> str:
        return f"{self._name}::{connection_type}" if connection_type else self._name

    def get_config(self, option: str | None = None):
        if option is None:
            return dict(self._config)
        value = self._config
        for segment in option.split("."):
            if not isinstance(value, dict) or segment not in value:
                return None
            value = value[segment]
        return value

    def get_driver_name(self) -> str | None:
        return self.get_config("driver")

    def get_database_name(self):
        return self.get_config("database")

    def get_table_prefix(self) -> str:
        return str(self.get_config("prefix") or "")

    def set_table_prefix(self, prefix: str) -> Connection:
        self._config["prefix"] = prefix
        return self

    def set_reconnector(self, reconnector: Callable[[Connection], object]) -> Connection:
        self.reconnector = reconnector
        return self

    def reconnect(self):
        if self.reconnector is None:
            raise RuntimeError("Lost connection and no reconnector available.")
        return self.reconnector(self)

    def disconnect(self) -> None:
        self.engine.dispose()

    def purge(self) -> None:
        self.disconnect()

    def dispose(self) -> None:
        self.disconnect()
