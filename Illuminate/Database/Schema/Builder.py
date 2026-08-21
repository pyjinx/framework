import sqlalchemy as sa
from Illuminate.Database.Schema.Blueprint import Blueprint
from sqlalchemy.schema import CreateTable, DropTable


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
        table_args = blueprint.columns + blueprint.indexes
        table = sa.Table(table_name, metadata, *table_args)

        # Execute creation
        with self._get_connection().begin() as conn:
            conn.execute(CreateTable(table))

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
        """Rename a table on the schema."""
        # SQLite doesn't natively support simple ALTER TABLE RENAME cleanly in older versions
        # but modern SQLAlchemy/Alembic handles it. We'll execute raw SQL for now as a fallback.
        with self._get_connection().begin() as conn:
            conn.execute(sa.text(f"ALTER TABLE {_from} RENAME TO {_to}"))
