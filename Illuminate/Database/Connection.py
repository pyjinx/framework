from __future__ import annotations

from collections.abc import Callable

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
        self._read_write_type: str | None = None
        self._read_pdo = None
        self._direct_pdo = None
        self._read_pdo_config: dict = {}
        self._direct_pdo_config: dict = {}
        self.reconnector: Callable[[Connection], object] | None = None
        self._listeners: list[Callable[[object], object]] = []
        self._query_duration_handlers: list[dict] = []
        self._total_query_duration = 0.0
        self._before_callbacks: list[Callable[[str, object], object]] = []

    @property
    def url(self):
        return self.engine.url


    def listen(self, callback: Callable[[object], object]) -> Connection:
        self._listeners.append(callback)
        return self

    def before_executing(
        self, callback: Callable[[str, object], object]
    ) -> Connection:
        self._before_callbacks.append(callback)
        return self

    def _dispatch_before(self, query: str, bindings) -> None:
        for callback in tuple(self._before_callbacks):
            callback(query, bindings)

    def _dispatch_query(self, event) -> None:
        for callback in tuple(self._listeners):
            callback(event)
    def when_querying_for_longer_than(self, threshold: float, handler) -> Connection:
        self._query_duration_handlers.append(
            {"threshold": float(threshold), "handler": handler, "has_run": False}
        )
        return self

    def allow_query_duration_handlers_to_run_again(self) -> None:
        for registered in self._query_duration_handlers:
            registered["has_run"] = False

    def total_query_duration(self) -> float:
        return self._total_query_duration

    def reset_total_query_duration(self) -> None:
        self._total_query_duration = 0.0
        self.allow_query_duration_handlers_to_run_again()

    def _record_query_duration(self, event) -> None:
        self._total_query_duration += event.time
        for registered in self._query_duration_handlers:
            if (
                not registered["has_run"]
                and self._total_query_duration > registered["threshold"]
            ):
                registered["has_run"] = True
                registered["handler"](event)
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
    def select(self, query: str, bindings=(), use_read_pdo: bool = True) -> list[dict]:
        self._dispatch_before(query, bindings)
        with self.engine.connect() as connection:
            return [
                dict(row)
                for row in connection.exec_driver_sql(query, bindings).mappings()
            ]

    def select_one(self, query: str, bindings=(), use_read_pdo: bool = True):
        rows = self.select(query, bindings, use_read_pdo)
        return rows[0] if rows else None

    def scalar(self, query: str, bindings=(), use_read_pdo: bool = True):
        self._dispatch_before(query, bindings)
        with self.engine.connect() as connection:
            return connection.exec_driver_sql(query, bindings).scalar()

    def select_from_write_connection(self, query: str, bindings=()):
        return self.select(query, bindings, use_read_pdo=False)

    def insert(self, query: str, bindings=()) -> bool:
        return self.statement(query, bindings)

    def update(self, query: str, bindings=()) -> int:
        return self.affecting_statement(query, bindings)

    def delete(self, query: str, bindings=()) -> int:
        return self.affecting_statement(query, bindings)

    def statement(self, query: str, bindings=()) -> bool:
        self._dispatch_before(query, bindings)
        with self.engine.begin() as connection:
            connection.exec_driver_sql(query, bindings)
        return True

    def affecting_statement(self, query: str, bindings=()) -> int:
        self._dispatch_before(query, bindings)
        with self.engine.begin() as connection:
            return connection.exec_driver_sql(query, bindings).rowcount

    def unprepared(self, query: str) -> bool:
        return self.statement(query)

    def get_raw_pdo(self):
        return self.get_pdo()

    def get_read_pdo(self):
        return self._read_pdo or self.get_pdo()

    def get_raw_read_pdo(self):
        return self._read_pdo

    def get_direct_pdo(self):
        return self._direct_pdo or self.get_pdo()

    def get_raw_direct_pdo(self):
        return self._direct_pdo

    def set_read_pdo(self, pdo) -> Connection:
        self._read_pdo = pdo
        return self

    def set_read_pdo_config(self, config: dict) -> Connection:
        self._read_pdo_config = dict(config)
        return self

    def set_direct_pdo(self, pdo) -> Connection:
        self._direct_pdo = pdo
        return self

    def set_direct_pdo_config(self, config: dict) -> Connection:
        self._direct_pdo_config = dict(config)
        return self

    def get_direct_pdo_config(self) -> dict:
        return dict(self._direct_pdo_config)

    def has_direct_connection(self) -> bool:
        return bool(self._direct_pdo_config)

    def get_name(self) -> str:
        return self._name

    def set_read_write_type(self, connection_type: str | None) -> Connection:
        self._read_write_type = connection_type
        return self

    def get_name_with_read_write_type(self, connection_type: str | None = None) -> str:
        connection_type = connection_type or self._read_write_type
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
    def get_driver_title(self) -> str | None:
        return self.get_driver_name()

    def get_server_version(self) -> str:
        return ".".join(str(part) for part in self.engine.dialect.server_version_info)

    def get_database_name(self):
        return self.get_config("database")

    def prepare_bindings(self, bindings) -> list:
        """Normalize bindings for safe SQL embedding.

        Mirrors Laravel ``Connection::prepareBindings`` by leaving scalar
        bindings unchanged. Expression-like objects are flattened through
        ``getValue`` when present; binary values are returned as-is.
        """
        prepared = []
        for value in bindings:
            if value is None:
                prepared.append(None)
                continue
            get_value = getattr(value, "getValue", None)
            if callable(get_value):
                try:
                    prepared.append(get_value(self))
                    continue
                except TypeError:
                    prepared.append(value)
                    continue
            prepared.append(value)
        return prepared

    def escape(self, value, binary: bool = False) -> str:
        """Escape ``value`` for safe SQL embedding.

        Mirrors Laravel ``Connection::escape`` for the SQLite backend:
        integers, floats, booleans, and ``None`` are returned as their SQL
        literal form; strings are quoted and escaped by the underlying
        DBAPI ``Connection.quote`` (Python ``sqlite3``).
        """
        if value is None:
            return "null"
        if binary:
            raise RuntimeError(
                "The database connection does not support escaping binary values."
            )
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, int) or isinstance(value, float):
            return str(value)
        if isinstance(value, (bytes, bytearray, memoryview)):
            raise RuntimeError(
                "The database connection does not support escaping binary values."
            )
        if isinstance(value, (list, tuple, dict, set)):
            raise RuntimeError(
                "The database connection does not support escaping arrays."
            )
        text_value = str(value)
        if "\x00" in text_value:
            raise RuntimeError(
                "Strings with null bytes cannot be escaped. Use the binary escape option."
            )
        try:
            text_value.encode("utf-8")
        except UnicodeEncodeError as error:
            raise RuntimeError(
                "Strings with invalid UTF-8 byte sequences cannot be escaped."
            ) from error
        raw = self.engine.raw_connection()
        try:
            quote = getattr(raw, "quote", None)
            if quote is None:
                # Fallback: double any embedded single quotes and wrap.
                return "'" + text_value.replace("'", "''") + "'"
            result = quote(text_value)
        finally:
            try:
                raw.close()
            except Exception:
                pass
        if isinstance(result, bytes):
            result = result.decode("utf-8")
        return str(result)

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
