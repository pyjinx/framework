from datetime import date, datetime, timezone
import sqlite3
from typing import Any

import pendulum


def now(tz: str | None = "UTC"):
    """Return a timezone-aware Pendulum datetime."""
    return pendulum.now(tz)


def parse(value: str, tz: str | None = None):
    """Parse an ISO datetime and optionally convert it to a timezone."""
    parsed = pendulum.parse(value)
    return parsed.in_timezone(tz) if tz else parsed


def to_database(value: Any) -> Any:
    """Serialize datetime values for SQLite without deprecated adapters."""
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value.isoformat(" ")
    if isinstance(value, date):
        return value.isoformat()
    return value


def register_sqlite_adapters() -> None:
    """Register explicit datetime/date adapters required by Python 3.12+."""
    sqlite3.register_adapter(datetime, to_database)
    sqlite3.register_adapter(date, to_database)
