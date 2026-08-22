from collections.abc import Callable
from typing import Any, Self

import sqlalchemy as sa
from sqlalchemy import inspect
from Illuminate.Database.Schema.Blueprint import Blueprint
from sqlalchemy.schema import CreateIndex, CreateTable, DropTable


class SchemaBuilder:
    def __init__(self, manager) -> None:
        self.manager = manager
        self.connection_name: str | None = None

    def connection(self, name: str | None = None) -> Self:
        """Set the connection for the schema operations."""
        self.connection_name = name
        return self

    def _get_connection(self):
        return self.manager.connection(self.connection_name)

    def has_table(self, table_name: str) -> bool:
        return inspect(self._get_connection()).has_table(table_name)

    def has_column(self, table_name: str, column_name: str) -> bool:
        return column_name.lower() in {
            column["name"].lower()
            for column in inspect(self._get_connection()).get_columns(table_name)
        }

    def has_columns(self, table_name: str, columns: list[str]) -> bool:
        available = {
            column["name"].lower()
            for column in inspect(self._get_connection()).get_columns(table_name)
        }
        return all(column.lower() in available for column in columns)

    def get_columns(self, table_name: str) -> list[dict]:
        return inspect(self._get_connection()).get_columns(table_name)

    def get_indexes(self, table_name: str) -> list[dict]:
        return inspect(self._get_connection()).get_indexes(table_name)

    def get_foreign_keys(self, table_name: str) -> list[dict]:
        return inspect(self._get_connection()).get_foreign_keys(table_name)

    def has_view(self, view_name: str) -> bool:
        return view_name in inspect(self._get_connection()).get_view_names()

    def get_tables(self, schema: str | None = None) -> list[dict]:
        return [
            {"name": table_name}
            for table_name in inspect(self._get_connection()).get_table_names(
                schema=schema
            )
        ]

    def get_views(self, schema: str | None = None) -> list[dict]:
        inspector = inspect(self._get_connection())
        return [
            {
                "name": view_name,
                "definition": inspector.get_view_definition(view_name, schema=schema),
            }
            for view_name in inspector.get_view_names(schema=schema)
        ]

    def get_types(self, schema: str | None = None) -> list[dict]:
        return []

    def create(self, table_name: str, callback: Callable[[Blueprint], Any]) -> None:
        """Create a new table on the schema."""
        blueprint = Blueprint(table_name)
        callback(blueprint)

        metadata = sa.MetaData()
        for foreign_key in blueprint.foreign_keys:
            foreign_key.register_referenced_table(metadata)
        table_args = blueprint.columns + blueprint.indexes + blueprint.constraints
        table = sa.Table(table_name, metadata, *table_args)

        with self._get_connection().begin() as conn:
            conn.execute(CreateTable(table))
            for index in table.indexes:
                conn.execute(CreateIndex(index))

    def drop(self, table_name: str) -> None:
        """Drop a table from the schema."""
        metadata = sa.MetaData()
        table = sa.Table(table_name, metadata)
        with self._get_connection().begin() as conn:
            conn.execute(DropTable(table))

    @staticmethod
    def _quote_identifier(identifier: str) -> str:
        if not identifier or "\x00" in identifier:
            raise ValueError("Schema identifiers must be non-empty and NUL-free.")
        return f'"{identifier.replace(chr(34), chr(34) * 2)}"'

    def table(self, table_name: str, callback: Callable[[Blueprint], Any]) -> None:
        blueprint = Blueprint(table_name)
        callback(blueprint)
        quoted_table = self._quote_identifier(table_name)

        with self._get_connection().begin() as connection:
            for command, values in blueprint.commands:
                if command == "rename_column":
                    source, target = values
                    connection.execute(
                        sa.text(
                            f"ALTER TABLE {quoted_table} RENAME COLUMN "
                            f"{self._quote_identifier(source)} TO "
                            f"{self._quote_identifier(target)}"
                        )
                    )
                elif command == "drop_column":
                    for column in values:
                        connection.execute(
                            sa.text(
                                f"ALTER TABLE {quoted_table} DROP COLUMN "
                                f"{self._quote_identifier(column)}"
                            )
                        )

    def drop_if_exists(self, table_name: str) -> None:
        """Drop a table from the schema if it exists."""
        metadata = sa.MetaData()
        table = sa.Table(table_name, metadata)
        with self._get_connection().begin() as conn:
            conn.execute(DropTable(table, if_exists=True))

    def rename(self, source: str, target: str) -> None:
        """Rename a table using quoted SQLite identifiers."""
        if not source or not target or "\x00" in source or "\x00" in target:
            raise ValueError("Table names must be non-empty and NUL-free.")
        quoted_source = f'"{source.replace(chr(34), chr(34) * 2)}"'
        quoted_target = f'"{target.replace(chr(34), chr(34) * 2)}"'
        with self._get_connection().begin() as conn:
            conn.execute(
                sa.text(f"ALTER TABLE {quoted_source} RENAME TO {quoted_target}")
            )
