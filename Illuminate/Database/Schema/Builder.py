import sqlalchemy as sa
from Illuminate.Database.Schema.Blueprint import Blueprint
from sqlalchemy.schema import CreateIndex, CreateTable, DropTable


class SchemaBuilder:
    def __init__(self, manager):
        self.manager = manager
        self.connection_name = None

    def connection(self, name):
        """Set the connection for the schema operations."""
        self.connection_name = name
        return self

    def _get_connection(self):
        return self.manager.connection(self.connection_name)

    def create(self, table_name, callback):
        """Create a new table on the schema."""
        blueprint = Blueprint(table_name)
        callback(blueprint)

        # Assemble the SQLAlchemy Table
        metadata = sa.MetaData()
        for foreign_key in blueprint.foreign_keys:
            foreign_key.register_referenced_table(metadata)
        table_args = blueprint.columns + blueprint.indexes + blueprint.constraints
        table = sa.Table(table_name, metadata, *table_args)

        # Execute creation
        with self._get_connection().begin() as conn:
            conn.execute(CreateTable(table))
            for index in table.indexes:
                conn.execute(CreateIndex(index))

    def drop(self, table_name):
        """Drop a table from the schema."""
        metadata = sa.MetaData()
        table = sa.Table(table_name, metadata)
        with self._get_connection().begin() as conn:
            conn.execute(DropTable(table))

    def drop_if_exists(self, table_name):
        """Drop a table from the schema if it exists."""
        metadata = sa.MetaData()
        table = sa.Table(table_name, metadata)
        with self._get_connection().begin() as conn:
            conn.execute(DropTable(table, if_exists=True))

    def rename(self, _from, _to):
        """Rename a table using quoted SQLite identifiers."""
        if not _from or not _to or "\x00" in _from or "\x00" in _to:
            raise ValueError("Table names must be non-empty and NUL-free.")
        source = f'"{_from.replace(chr(34), chr(34) * 2)}"'
        target = f'"{_to.replace(chr(34), chr(34) * 2)}"'
        with self._get_connection().begin() as conn:
            conn.execute(sa.text(f"ALTER TABLE {source} RENAME TO {target}"))
