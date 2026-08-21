import sqlalchemy as sa


class Blueprint:
    """Represents a database table schema blueprint."""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns = []
        self.indexes = []

    def id(self, column="id"):
        """Create an auto-incrementing big integer (or standard integer for SQLite) primary key."""
        id_type = sa.BigInteger().with_variant(sa.Integer(), "sqlite")
        col = sa.Column(column, id_type, primary_key=True, autoincrement=True)
        self.columns.append(col)
        return self

    def string(self, column, length=255):
        """Create a string/varchar column."""
        col = sa.Column(column, sa.String(length))
        self.columns.append(col)
        return self

    def text(self, column):
        """Create a text column."""
        col = sa.Column(column, sa.Text())
        self.columns.append(col)
        return self

    def integer(self, column):
        """Create an integer column."""
        col = sa.Column(column, sa.Integer())
        self.columns.append(col)
        return self

    def big_integer(self, column):
        """Create a big integer column."""
        col = sa.Column(column, sa.BigInteger())
        self.columns.append(col)
        return self

    def boolean(self, column):
        """Create a boolean column."""
        col = sa.Column(column, sa.Boolean())
        self.columns.append(col)
        return self

    def float(self, column):
        """Create a float column."""
        col = sa.Column(column, sa.Float())
        self.columns.append(col)
        return self

    def timestamp(self, column):
        """Create a timestamp column."""
        col = sa.Column(column, sa.DateTime())
        self.columns.append(col)
        return self

    def timestamps(self):
        """Add created_at and updated_at timestamp columns."""
        self.timestamp("created_at").nullable()
        self.timestamp("updated_at").nullable()
        return self

    def remember_token(self):
        """Add a remember_token string column."""
        self.string("remember_token", 100).nullable()
        return self

    # Modifiers for the last added column
    def nullable(self, is_nullable=True):
        """Make the last added column nullable."""
        if self.columns:
            self.columns[-1].nullable = is_nullable
        return self

    def default(self, value):
        """Set a default value for the last added column."""
        if self.columns:
            self.columns[-1].default = value
            
            text_val = sa.text(f"'{value}'") if isinstance(value, str) else sa.text(str(value))
            self.columns[-1].server_default = sa.DefaultClause(text_val)
        return self

    def unique(self, index_name=None):
        """Add a unique constraint for the last added column."""
        if self.columns:
            col_name = self.columns[-1].name
            idx_name = index_name or f"{self.table_name}_{col_name}_unique"
            self.indexes.append(sa.UniqueConstraint(col_name, name=idx_name))
        return self

    def foreign(self, column):
        """Define a foreign key constraint for a given column (simplified).
        In a full implementation, this returns a ForeignKeyDefinition to chain `.references().on()`.
        For now, this requires manual setup or we build a full fluent chain.
        """
        # Placeholder for full foreign key fluent API
