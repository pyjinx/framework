from __future__ import annotations

from typing import Any, Self

import sqlalchemy as sa


def _index_name(table_name, columns, index_type):
    return f"{table_name}_{'_'.join(columns)}_{index_type}".lower().replace("-", "_").replace(".", "_")

def _apply_default(column, value):
    column.default = value
    if value is None:
        column.server_default = None
        return
    if isinstance(value, str):
        value = value.replace("'", "''")
        text_value = sa.text(f"'{value}'")
    else:
        text_value = sa.text(str(value))
    column.server_default = sa.DefaultClause(text_value)


class ForeignKeyDefinition:
    """Fluent definition of a SQLite foreign key constraint."""

    def __init__(self, blueprint: Blueprint, columns: tuple[str, ...], name: str | None = None):
        self._blueprint = blueprint
        self._columns = tuple(columns)
        self._name = name or _index_name(blueprint.table_name, self._columns, "foreign")
        self._references = None
        self._table = None
        self._on_delete = None
        self._on_update = None

    def references(self, columns: str | list[str]) -> Self:
        self._references = (columns,) if isinstance(columns, str) else tuple(columns)
        return self

    def on(self, table: str) -> Self:
        self._table = table
        return self

    def register_referenced_table(self, metadata):
        if self._table is None or self._references is None:
            return

        table = metadata.tables.get(self._table)
        if table is None:
            table = sa.Table(self._table, metadata)
        for column in self._references:
            if column not in table.c:
                table.append_column(sa.Column(column))

    def on_delete(self, action: str) -> Self:
        self._on_delete = action
        return self

    def on_update(self, action: str) -> Self:
        self._on_update = action
        return self

    def cascade_on_delete(self) -> Self:
        return self.on_delete("cascade")

    def restrict_on_delete(self) -> Self:
        return self.on_delete("restrict")

    def null_on_delete(self) -> Self:
        return self.on_delete("set null")

    def no_action_on_delete(self) -> Self:
        return self.on_delete("no action")

    def cascade_on_update(self) -> Self:
        return self.on_update("cascade")

    def restrict_on_update(self) -> Self:
        return self.on_update("restrict")

    def null_on_update(self) -> Self:
        return self.on_update("set null")

    def no_action_on_update(self) -> Self:
        return self.on_update("no action")

    def as_constraint(self) -> sa.ForeignKeyConstraint:
        if self._references is None or self._table is None:
            raise ValueError(
                "Foreign keys must specify both referenced columns and a referenced table."
            )
        if len(self._columns) != len(self._references):
            raise ValueError(
                "Foreign key columns and referenced columns must have equal length."
            )

        return sa.ForeignKeyConstraint(
            self._columns,
            tuple(f"{self._table}.{column}" for column in self._references),
            name=self._name,
            ondelete=self._on_delete,
            onupdate=self._on_update,
        )


class ColumnDefinition:
    """Fluent column modifier matching Laravel ColumnDefinition methods."""

    def __init__(self, blueprint: Blueprint, column: str):
        self._blueprint = blueprint
        self._column = column

    def _column_definition(self) -> sa.Column[Any]:
        return next(
            column
            for column in self._blueprint.columns
            if column.name == self._column
        )

    def nullable(self, is_nullable: bool = True) -> Self:
        self._column_definition().nullable = is_nullable
        return self

    def default(self, value: Any) -> Self:
        _apply_default(self._column_definition(), value)
        return self

    def _fluent_index_name(self, value: str | bool | None) -> str | bool | None:
        if value is False:
            return False
        return None if value is True else value

    def unique(self, index_name: str | bool | None = None) -> Self:
        index_name = self._fluent_index_name(index_name)
        if index_name is not False:
            self._blueprint.unique(self._column, index_name)
        return self

    def index(self, index_name: str | bool | None = None) -> Self:
        index_name = self._fluent_index_name(index_name)
        if index_name is not False:
            self._blueprint.index(self._column, index_name)
        return self

    def primary(self, index_name: str | bool | None = None) -> Self:
        index_name = self._fluent_index_name(index_name)
        if index_name is not False:
            self._blueprint.primary(self._column, index_name)
        return self

    def __getattr__(self, name: str) -> Any:
        return getattr(self._blueprint, name)

class ForeignIdColumnDefinition(ColumnDefinition):
    """Fluent modifier for a foreign ID column."""

    def __init__(self, blueprint: Blueprint, column: str):
        super().__init__(blueprint, column)
        self._column = column

    def nullable(self, is_nullable: bool = True) -> Self:
        return super().nullable(is_nullable)

    def default(self, value: Any) -> Self:
        return super().default(value)

    def constrained(
        self,
        table: str | None = None,
        column: str | None = None,
        index_name: str | None = None,
    ) -> Self:
        column = column or "id"
        if table is None:
            base = self._column.removesuffix(f"_{column}")
            table = f"{base}ies" if base.endswith("y") else f"{base}s"

        return self.references(column, index_name).on(table)

    def references(self, column: str, index_name: str | None = None) -> Self:
        return self._blueprint.foreign(self._column, index_name).references(column)


class Blueprint:
    """Represents a database table schema blueprint."""

    def __init__(self, table_name: str) -> None:
        self.table_name = table_name
        self.columns = []
        self.indexes = []
        self.foreign_keys = []

    @property
    def constraints(self) -> list[sa.ForeignKeyConstraint]:
        return [foreign_key.as_constraint() for foreign_key in self.foreign_keys]

    def id(self, column: str = "id") -> ColumnDefinition:
        """Create an auto-incrementing big integer primary key."""
        id_type = sa.BigInteger().with_variant(sa.Integer(), "sqlite")
        self.columns.append(
            sa.Column(column, id_type, primary_key=True, autoincrement=True)
        )
        return ColumnDefinition(self, column)

    def string(self, column: str, length: int = 255) -> ColumnDefinition:
        """Create a string/varchar column."""
        self.columns.append(sa.Column(column, sa.String(length)))
        return ColumnDefinition(self, column)

    def text(self, column: str) -> ColumnDefinition:
        """Create a text column."""
        self.columns.append(sa.Column(column, sa.Text()))
        return ColumnDefinition(self, column)

    def integer(self, column: str) -> ColumnDefinition:
        """Create an integer column."""
        self.columns.append(sa.Column(column, sa.Integer()))
        return ColumnDefinition(self, column)

    def big_integer(self, column: str) -> ColumnDefinition:
        """Create a big integer column."""
        self.columns.append(sa.Column(column, sa.BigInteger()))
        return ColumnDefinition(self, column)

    def boolean(self, column: str) -> ColumnDefinition:
        """Create a boolean column."""
        self.columns.append(sa.Column(column, sa.Boolean()))
        return ColumnDefinition(self, column)

    def float(self, column: str) -> ColumnDefinition:
        """Create a float column."""
        self.columns.append(sa.Column(column, sa.Float()))
        return ColumnDefinition(self, column)

    def timestamp(self, column: str) -> ColumnDefinition:
        """Create a timestamp column."""
        self.columns.append(sa.Column(column, sa.DateTime()))
        return ColumnDefinition(self, column)

    def foreign_id(self, column: str) -> ForeignIdColumnDefinition:
        """Create a non-auto-incrementing integer column for a foreign key."""
        foreign_id_type = sa.BigInteger().with_variant(sa.Integer(), "sqlite")
        self.columns.append(sa.Column(column, foreign_id_type))
        return ForeignIdColumnDefinition(self, column)

    def timestamps(self) -> Self:
        """Add created_at and updated_at timestamp columns."""
        self.timestamp("created_at").nullable()
        self.timestamp("updated_at").nullable()
        return self

    def remember_token(self) -> Self:
        """Add a nullable remember_token string column."""
        self.string("remember_token", 100).nullable()
        return self

    def nullable(self, is_nullable: bool = True) -> Self:
        """Make the last added column nullable."""
        if self.columns:
            self.columns[-1].nullable = is_nullable
        return self

    def default(self, value: Any) -> Self:
        """Set a server default for the last added column."""
        if self.columns:
            _apply_default(self.columns[-1], value)
        return self

    def primary(
        self, columns: str | list[str] | None = None, index_name: str | None = None
    ) -> Self:
        """Set the last column, or supplied columns, as the primary key."""
        if columns is None:
            if self.columns:
                self.columns[-1].primary_key = True
            return self

        columns = (columns,) if isinstance(columns, str) else tuple(columns)
        name = index_name or _index_name(self.table_name, columns, "primary")
        self.indexes.append(sa.PrimaryKeyConstraint(*columns, name=name))
        return self

    def unique(
        self, columns: str | list[str] | None = None, index_name: str | None = None
    ) -> Self:
        if columns is None:
            if not self.columns:
                return self
            columns = (self.columns[-1].name,)
        elif isinstance(columns, str):
            columns = (columns,)
        else:
            columns = tuple(columns)

        name = index_name or _index_name(self.table_name, columns, "unique")
        self.indexes.append(sa.Index(name, *columns, unique=True))
        return self

    def index(
        self, columns: str | list[str], index_name: str | None = None
    ) -> Self:
        """Create a non-unique index for one or more columns."""
        columns = (columns,) if isinstance(columns, str) else tuple(columns)
        name = index_name or _index_name(self.table_name, columns, "index")
        self.indexes.append(sa.Index(name, *columns))
        return self

    def foreign(
        self, columns: str | list[str], index_name: str | None = None
    ) -> ForeignKeyDefinition:
        """Create a fluent foreign key definition for one or more columns."""
        columns = (columns,) if isinstance(columns, str) else tuple(columns)
        foreign_key = ForeignKeyDefinition(self, columns, index_name)
        self.foreign_keys.append(foreign_key)
        return foreign_key
