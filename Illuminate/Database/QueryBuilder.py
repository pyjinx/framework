from sqlalchemy import MetaData, Select, Table, and_, delete, func, insert, or_, select, text, update


class QueryBuilder:
    def __init__(self, manager, table_name: str, connection_name=None):
        self.manager = manager
        self.table_name = table_name
        self.connection_name = connection_name
        self._columns = None
        self._conditions = []
        self._or_conditions = []
        self._where_clauses = []
        self._limit = None
        self._offset = None
        self._orders = []
        self._groups = []
        self._havings = []
        self._distinct = False

    # ---- Select ----

    def select(self, *columns):
        self._columns = columns or ("*",)
        return self

    def distinct(self):
        self._distinct = True
        return self

    # ---- Where clauses ----

    def where(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._conditions.append(("and", column, operator, value))
        return self

    def or_where(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._conditions.append(("or", column, operator, value))
        return self

    def where_in(self, column, values):
        self._where_clauses.append(("in", "and", column, list(values)))
        return self

    def or_where_in(self, column, values):
        self._where_clauses.append(("in", "or", column, list(values)))
        return self

    def where_not_in(self, column, values):
        self._where_clauses.append(("not_in", "and", column, list(values)))
        return self

    def or_where_not_in(self, column, values):
        self._where_clauses.append(("not_in", "or", column, list(values)))
        return self

    def where_null(self, column):
        self._where_clauses.append(("null", "and", column, None))
        return self

    def or_where_null(self, column):
        self._where_clauses.append(("null", "or", column, None))
        return self

    def where_not_null(self, column):
        self._where_clauses.append(("not_null", "and", column, None))
        return self

    def or_where_not_null(self, column):
        self._where_clauses.append(("not_null", "or", column, None))
        return self

    def where_between(self, column, values):
        low, high = values
        self._where_clauses.append(("between", "and", column, (low, high)))
        return self

    def or_where_between(self, column, values):
        low, high = values
        self._where_clauses.append(("between", "or", column, (low, high)))
        return self

    def where_not_between(self, column, values):
        low, high = values
        self._where_clauses.append(("not_between", "and", column, (low, high)))
        return self

    # ---- Ordering ----

    def order_by(self, column, direction="asc"):
        direction = direction.lower()
        if direction not in ("asc", "desc"):
            raise ValueError('Order direction must be "asc" or "desc".')
        self._orders.append((column, direction))
        return self

    def order_by_desc(self, column):
        return self.order_by(column, "desc")

    def latest(self, column="created_at"):
        return self.order_by(column, "desc")

    def oldest(self, column="created_at"):
        return self.order_by(column, "asc")

    # ---- Grouping ----

    def group_by(self, *columns):
        self._groups.extend(columns)
        return self

    def having(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._havings.append((column, operator, value))
        return self

    # ---- Limit / Offset ----

    def limit(self, value: int):
        self._limit = value
        return self

    def offset(self, value: int):
        self._offset = value
        return self

    def skip(self, value: int):
        return self.offset(value)

    def take(self, value: int):
        return self.limit(value)

    def for_page(self, page: int, per_page: int = 15):
        return self.offset((page - 1) * per_page).limit(per_page)

    # ---- Write operations ----

    def insert(self, values):
        """Insert one record (dict) or multiple records (list of dicts)."""
        table = self._table()
        with self.manager.connection(self.connection_name).begin() as connection:
            if isinstance(values, list):
                connection.execute(insert(table), values)
                return True
            result = connection.execute(insert(table).values(**values))
            return result.inserted_primary_key[0] if result.inserted_primary_key else None

    def insert_get_id(self, values: dict):
        """Insert a record and return the primary key."""
        table = self._table()
        with self.manager.connection(self.connection_name).begin() as connection:
            result = connection.execute(insert(table).values(**values))
            return result.inserted_primary_key[0] if result.inserted_primary_key else None

    def update(self, values: dict) -> int:
        table = self._table()
        statement = update(table).values(**values)
        statement = self._apply_wheres(table, statement)
        with self.manager.connection(self.connection_name).begin() as connection:
            return connection.execute(statement).rowcount

    def delete(self) -> int:
        table = self._table()
        statement = delete(table)
        statement = self._apply_wheres(table, statement)
        with self.manager.connection(self.connection_name).begin() as connection:
            return connection.execute(statement).rowcount

    def truncate(self):
        """Remove all rows from the table."""
        with self.manager.connection(self.connection_name).begin() as connection:
            connection.execute(text(f"DELETE FROM {self.table_name}"))

    def increment(self, column, amount=1, extra=None):
        """Increment a column's value."""
        table = self._table()
        col = getattr(table.c, column)
        values = {column: col + amount}
        if extra:
            values.update(extra)
        statement = update(table).values(**values)
        statement = self._apply_wheres(table, statement)
        with self.manager.connection(self.connection_name).begin() as connection:
            return connection.execute(statement).rowcount

    def decrement(self, column, amount=1, extra=None):
        """Decrement a column's value."""
        return self.increment(column, -amount, extra)

    # ---- Read operations ----

    def get(self):
        statement = self._build_select()
        engine = self.manager.connection(self.connection_name)
        with engine.connect() as connection:
            rows = connection.execute(statement).mappings().all()
        return [dict(row) for row in rows]

    def first(self):
        rows = self.limit(1).get()
        return rows[0] if rows else None

    def value(self, column):
        """Get a single column's value from the first result."""
        row = self.first()
        if row is None:
            return None
        return row.get(column)

    def pluck(self, column, key=None):
        """Get a list of column values, optionally keyed by another column."""
        if key is not None:
            original_columns = self._columns
            self._columns = (key, column)
            rows = self.get()
            self._columns = original_columns
            return {row[key]: row[column] for row in rows}
        original_columns = self._columns
        self._columns = (column,)
        rows = self.get()
        self._columns = original_columns
        return [row[column] for row in rows]

    def exists(self) -> bool:
        return self.first() is not None

    def doesnt_exist(self) -> bool:
        return not self.exists()

    # ---- Aggregates ----

    def count(self, column="*") -> int:
        return self._aggregate(func.count, column) or 0

    def sum(self, column):
        return self._aggregate(func.sum, column) or 0

    def avg(self, column):
        return self._aggregate(func.avg, column)

    average = avg

    def min(self, column):
        return self._aggregate(func.min, column)

    def max(self, column):
        return self._aggregate(func.max, column)

    def _aggregate(self, fn, column):
        table = self._table()
        if column == "*":
            agg_expr = fn()
        else:
            agg_expr = fn(getattr(table.c, column))
        statement = select(agg_expr).select_from(table)
        statement = self._apply_wheres(table, statement)
        engine = self.manager.connection(self.connection_name)
        with engine.connect() as connection:
            result = connection.execute(statement).scalar()
        return result

    # ---- Internals ----

    def _table(self):
        return Table(
            self.table_name,
            MetaData(),
            autoload_with=self.manager.connection(self.connection_name),
        )

    def _apply_wheres(self, table, statement):
        """Apply all where conditions to any statement (select/update/delete)."""
        and_clauses = []
        or_clauses = []

        # Simple comparison conditions
        for boolean, column, operator, value in self._conditions:
            expr = self._comparison(getattr(table.c, column), operator, value)
            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)

        # Complex where clauses (in, null, between, etc.)
        for kind, boolean, column, val in self._where_clauses:
            col = getattr(table.c, column)
            if kind == "in":
                expr = col.in_(val)
            elif kind == "not_in":
                expr = col.notin_(val)
            elif kind == "null":
                expr = col.is_(None)
            elif kind == "not_null":
                expr = col.isnot(None)
            elif kind == "between":
                expr = col.between(val[0], val[1])
            elif kind == "not_between":
                expr = ~col.between(val[0], val[1])
            else:
                continue

            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)

        # Combine: all AND clauses together, then OR with each OR clause
        if and_clauses and or_clauses:
            combined = or_(and_(*and_clauses), *or_clauses)
            statement = statement.where(combined)
        elif and_clauses:
            for clause in and_clauses:
                statement = statement.where(clause)
        elif or_clauses:
            statement = statement.where(or_(*or_clauses))

        return statement

    def _build_select(self) -> Select:
        """Build a complete SELECT statement."""
        table = self._table()
        columns = self._selected_columns(table)
        statement = select(*columns)

        if self._distinct:
            statement = statement.distinct()

        # Apply where clauses
        statement = self._apply_wheres(table, statement)

        # Group by
        for col_name in self._groups:
            statement = statement.group_by(getattr(table.c, col_name))

        # Having
        for column, operator, value in self._havings:
            col = getattr(table.c, column)
            statement = statement.having(self._comparison(col, operator, value))

        # Order by
        for col_name, direction in self._orders:
            col = getattr(table.c, col_name)
            statement = statement.order_by(col.asc() if direction == "asc" else col.desc())

        if self._limit is not None:
            statement = statement.limit(self._limit)
        if self._offset is not None:
            statement = statement.offset(self._offset)

        return statement

    def _selected_columns(self, table):
        if not self._columns or self._columns == ("*",):
            return list(table.c)
        return [getattr(table.c, column) for column in self._columns]

    @staticmethod
    def _comparison(column, operator, value):
        comparisons = {
            "=": column == value,
            "==": column == value,
            "!=": column != value,
            "<>": column != value,
            ">": column > value,
            ">=": column >= value,
            "<": column < value,
            "<=": column <= value,
            "like": column.like(value),
            "not like": ~column.like(value),
        }
        if operator not in comparisons:
            raise ValueError(f"Unsupported where operator: {operator}")
        return comparisons[operator]
