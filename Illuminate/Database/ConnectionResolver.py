from __future__ import annotations


class ConnectionResolver:
    """Resolve registered database connections by name."""

    def __init__(self, connections: dict[str, object] | None = None) -> None:
        self._connections: dict[str, object] = {}
        self._default: str | None = None
        for name, connection in (connections or {}).items():
            self.add_connection(name, connection)

    def connection(self, name: str | None = None):
        requested = name if name is not None else self.get_default_connection()
        return self._connections[requested]

    def add_connection(self, name: str, connection: object) -> None:
        self._connections[name] = connection

    def has_connection(self, name: str) -> bool:
        return name in self._connections

    def get_default_connection(self) -> str | None:
        return self._default

    def set_default_connection(self, name: str) -> None:
        self._default = name
