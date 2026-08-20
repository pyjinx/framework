from typing import TYPE_CHECKING

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Database.QueryBuilder import QueryBuilder


class DB(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "db"

    if TYPE_CHECKING:

        @classmethod
        def table(
            cls,
            table_name: str,
            connection_name: str | None = None,
        ) -> "QueryBuilder": ...
