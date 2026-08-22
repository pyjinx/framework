from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class QueryExecuted:
    """Framework event emitted after a database statement succeeds."""

    sql: str
    bindings: list[Any]
    time: float
    connection: Any
    connection_name: str
    read_write_type: str | None = None
