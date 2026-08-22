from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Database.Schema.Blueprint import Blueprint
    from Illuminate.Database.Schema.Builder import SchemaBuilder


class Schema(metaclass=Facade):
    """Laravel-compatible schema facade with static type information."""

    @classmethod
    def get_facade_accessor(cls) -> str:
        return "db.schema"

    if TYPE_CHECKING:

        @classmethod
        def connection(cls, name: str | None = None) -> "SchemaBuilder": ...

        @classmethod
        def create(
            cls, table_name: str, callback: Callable[["Blueprint"], Any]
        ) -> None: ...

        @classmethod
        def drop(cls, table_name: str) -> None: ...

        @classmethod
        def drop_if_exists(cls, table_name: str) -> None: ...

        @classmethod
        def table(
            cls, table_name: str, callback: Callable[["Blueprint"], Any]
        ) -> None: ...

        @classmethod
        def rename(cls, source: str, target: str) -> None: ...
