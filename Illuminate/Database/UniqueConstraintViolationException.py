from typing import Any

from Illuminate.Database.QueryException import QueryException


class UniqueConstraintViolationException(QueryException):
    """A query failure caused by a unique constraint violation."""

    def __init__(
        self,
        connection_name: str,
        sql: str,
        bindings: list[Any],
        previous: BaseException,
        connection_details: dict[str, Any] | None = None,
        read_write_type: str | None = None,
    ) -> None:
        super().__init__(
            connection_name,
            sql,
            bindings,
            previous,
            connection_details,
            read_write_type,
        )
        self.index: str | None = None
        self.columns: list[str] = []

    def set_index(self, index: str | None):
        self.index = index
        return self

    def set_columns(self, columns: list[str]):
        self.columns = list(columns)
        return self
