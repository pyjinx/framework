from collections.abc import Iterable
from typing import Any


class QueryException(Exception):
    """A database error enriched with the connection and executed query."""

    def __init__(
        self,
        connection_name: str,
        sql: str,
        bindings: Iterable[Any],
        previous: BaseException,
        connection_details: dict[str, Any] | None = None,
        read_write_type: str | None = None,
    ) -> None:
        self.connection_name = connection_name
        self.sql = sql
        self.bindings = list(bindings)
        self.previous = previous
        self.connection_details = dict(connection_details or {})
        self.read_write_type = read_write_type
        super().__init__(self._format_message())
        self.__cause__ = previous

    def _format_message(self) -> str:
        details = self._format_connection_details()
        raw_sql = self._substitute_bindings(self.sql, self.bindings, quoted=False)
        return (
            f"{self.previous} (Connection: {self.connection_name}{details}, "
            f"SQL: {raw_sql})"
        )

    def _format_connection_details(self) -> str:
        if not self.connection_details:
            return ""

        driver = self.connection_details.get("driver", "")
        segments = []
        if driver != "sqlite":
            if self.connection_details.get("unix_socket"):
                segments.append(f"Socket: {self.connection_details['unix_socket']}")
            else:
                host = self.connection_details.get("host", "")
                if isinstance(host, list):
                    host = ", ".join(str(value) for value in host)
                segments.extend(
                    [
                        f"Host: {host}",
                        f"Port: {self.connection_details.get('port', '')}",
                    ]
                )
        segments.append(f"Database: {self.connection_details.get('database', '')}")
        return ", " + ", ".join(segments)

    def get_connection_name(self) -> str:
        return self.connection_name

    def get_sql(self) -> str:
        return self.sql

    def get_raw_sql(self) -> str:
        return self._substitute_bindings(self.sql, self.bindings, quoted=True)

    def get_bindings(self) -> list[Any]:
        return list(self.bindings)

    def get_connection_details(self) -> dict[str, Any]:
        return dict(self.connection_details)

    @staticmethod
    def _substitute_bindings(sql: str, bindings: Iterable[Any], quoted: bool) -> str:
        values = iter(bindings)
        result = []
        in_string = False
        index = 0
        while index < len(sql):
            char = sql[index]
            next_char = sql[index + 1] if index + 1 < len(sql) else ""
            if char == "'":
                result.append(char)
                if next_char == "'":
                    result.append(next_char)
                    index += 2
                    continue
                in_string = not in_string
            elif char == "?" and not in_string:
                try:
                    value = next(values)
                except StopIteration:
                    result.append(char)
                else:
                    result.append(
                        QueryException._format_binding(value, quoted=quoted)
                    )
            else:
                result.append(char)
            index += 1
        return "".join(result)

    @staticmethod
    def _format_binding(value: Any, quoted: bool) -> str:
        if value is None:
            return "NULL" if quoted else ""
        if isinstance(value, bool):
            return "1" if value else "0"
        if isinstance(value, (int, float)):
            return str(value)
        text = str(value)
        if not quoted:
            return text
        return "'" + text.replace("'", "''") + "'"
