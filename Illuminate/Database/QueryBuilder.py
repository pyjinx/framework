from collections.abc import Mapping
from datetime import date, datetime, time
from sqlalchemy import (
    MetaData,
    Select,
    Table,
    and_,
    delete,
    exists,
    func,
    insert,
    or_,
    select,
    text,
    tuple_,
    update,
)
from sqlalchemy.dialects.sqlite import insert as sqlite_insert


class QueryBuilder:
    def __init__(self, manager, table_name: str, connection_name=None):
        self.manager = manager
        self.connection_name = connection_name
        self.table_name = manager.prefixed_table_name(table_name, connection_name)
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
        self._joins = []
        self._aliased_columns = []
        self._loaded_tables = None
        self._lock = None

    # ---- Select ----

    def select(self, *columns):
        self._columns = columns or ("*",)
        return self

    def add_select(self, *columns):
        """Add columns to the current select, mirroring addSelect()."""
        if not self._columns or self._columns == ("*",):
            self._columns = tuple(columns)
        else:
            self._columns = tuple(self._columns) + tuple(columns)
        return self

    def add_select_aliased(self, column, alias):
        """Select a qualified column under an alias."""
        self._aliased_columns.append((column, alias))
        return self

    def distinct(self):
        self._distinct = True
        return self

    # ---- Joins ----

    def join(self, table, first, operator="=", second=None):
        """Add an inner join clause."""
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("inner", table, first, operator, second))
        self._loaded_tables = None
        return self

    def left_join(self, table, first, operator="=", second=None):
        """Add a left join clause."""
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("left", table, first, operator, second))
        self._loaded_tables = None
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

    def where_all(self, columns, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(
            ("multi", "and", list(columns), ("all", operator, value, False))
        )
        return self

    def or_where_all(self, columns, operator="=", value=None):
        return self.where_all(columns, operator, value)._set_last_where_boolean("or")

    def where_any(self, columns, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(
            ("multi", "and", list(columns), ("any", operator, value, False))
        )
        return self

    def or_where_any(self, columns, operator="=", value=None):
        return self.where_any(columns, operator, value)._set_last_where_boolean("or")

    def where_none(self, columns, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(
            ("multi", "and", list(columns), ("any", operator, value, True))
        )
        return self

    def or_where_none(self, columns, operator="=", value=None):
        return self.where_none(columns, operator, value)._set_last_where_boolean("or")

    def _set_last_where_boolean(self, boolean):
        kind, _, columns, value = self._where_clauses[-1]
        self._where_clauses[-1] = (kind, boolean, columns, value)
        return self

    def where_column(self, first, operator="=", second=None):
        if second is None:
            second = operator
            operator = "="
        self._where_clauses.append(("column", "and", first, (operator, second)))
        return self

    def or_where_column(self, first, operator="=", second=None):
        if second is None:
            second = operator
            operator = "="
        self._where_clauses.append(("column", "or", first, (operator, second)))
        return self

    def where_between_columns(self, column, values):
        low, high = values
        self._where_clauses.append(
            ("between_columns", "and", column, (low, high, False))
        )
        return self

    def or_where_between_columns(self, column, values):
        low, high = values
        self._where_clauses.append(
            ("between_columns", "or", column, (low, high, False))
        )
        return self

    def where_not_between_columns(self, column, values):
        low, high = values
        self._where_clauses.append(
            ("between_columns", "and", column, (low, high, True))
        )
        return self

    def or_where_not_between_columns(self, column, values):
        low, high = values
        self._where_clauses.append(("between_columns", "or", column, (low, high, True)))
        return self

    def where_date(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        if isinstance(value, datetime | date):
            value = value.strftime("%Y-%m-%d")
        self._where_clauses.append(("date", "and", column, (operator, value)))
        return self

    def or_where_date(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        if isinstance(value, datetime | date):
            value = value.strftime("%Y-%m-%d")
        self._where_clauses.append(("date", "or", column, (operator, value)))
        return self

    def where_time(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        if isinstance(value, datetime):
            value = value.strftime("%H:%M:%S")
        elif isinstance(value, time):
            value = value.strftime("%H:%M:%S")
        self._where_clauses.append(("time", "and", column, (operator, value)))
        return self

    def or_where_time(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        if isinstance(value, datetime):
            value = value.strftime("%H:%M:%S")
        elif isinstance(value, time):
            value = value.strftime("%H:%M:%S")
        self._where_clauses.append(("time", "or", column, (operator, value)))
        return self

    @staticmethod
    def _calendar_value(kind, value):
        if isinstance(value, datetime | date):
            formats = {"day": "%d", "month": "%m", "year": "%Y"}
            return value.strftime(formats[kind])
        if kind in {"day", "month"}:
            return str(value).zfill(2)
        return str(value)

    def _where_calendar(self, kind, column, operator, value, boolean):
        value = self._calendar_value(kind, value)
        self._where_clauses.append((kind, boolean, column, (operator, value)))
        return self

    def where_day(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("day", column, operator, value, "and")

    def or_where_day(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("day", column, operator, value, "or")

    def where_month(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("month", column, operator, value, "and")

    def or_where_month(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("month", column, operator, value, "or")

    def where_year(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("year", column, operator, value, "and")

    def or_where_year(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        return self._where_calendar("year", column, operator, value, "or")

    def where_json_contains(self, column, value):
        self._where_clauses.append(("json_contains", "and", column, (value, False)))
        return self

    def or_where_json_contains(self, column, value):
        self._where_clauses.append(("json_contains", "or", column, (value, False)))
        return self

    def where_json_doesnt_contain(self, column, value):
        self._where_clauses.append(("json_contains", "and", column, (value, True)))
        return self

    def or_where_json_doesnt_contain(self, column, value):
        self._where_clauses.append(("json_contains", "or", column, (value, True)))
        return self

    def where_json_contains_key(self, column):
        self._where_clauses.append(("json_key", "and", column, False))
        return self

    def or_where_json_contains_key(self, column):
        self._where_clauses.append(("json_key", "or", column, False))
        return self

    def where_json_doesnt_contain_key(self, column):
        self._where_clauses.append(("json_key", "and", column, True))
        return self

    def or_where_json_doesnt_contain_key(self, column):
        self._where_clauses.append(("json_key", "or", column, True))
        return self

    def where_json_length(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(("json_length", "and", column, (operator, value)))
        return self

    def or_where_json_length(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(("json_length", "or", column, (operator, value)))
        return self

    def where_row_values(self, columns, operator, values):
        columns = list(columns)
        values = list(values)
        if len(columns) != len(values):
            raise ValueError("The number of columns must match the number of values")
        self._where_clauses.append(("row_values", "and", columns, (operator, values)))
        return self

    def or_where_row_values(self, columns, operator, values):
        columns = list(columns)
        values = list(values)
        if len(columns) != len(values):
            raise ValueError("The number of columns must match the number of values")
        self._where_clauses.append(("row_values", "or", columns, (operator, values)))
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

    def chunk(self, count: int, callback):
        if count < 1:
            raise ValueError("The chunk size should be at least 1.")
        if not self._orders:
            raise RuntimeError(
                "You must specify an order_by clause when using this function."
            )

        offset = self._offset or 0
        remaining = self._limit
        page = 1

        while True:
            limit = count if remaining is None else min(count, remaining)
            if limit == 0:
                break

            results = self.offset(offset).limit(limit).get()
            result_count = len(results)
            if result_count == 0:
                break

            if remaining is not None:
                remaining = max(remaining - result_count, 0)

            if callback(results, page) is False:
                return False

            page += 1
            offset += count
            if result_count != count:
                break

        return True

    def each(self, callback, count: int = 1000):
        return self.chunk(
            count,
            lambda rows, _page: all(
                callback(row, index) is not False for index, row in enumerate(rows)
            ),
        )

    def cursor(self):
        statement = self._build_select()

        def iterate():
            with self.manager._query_connection(self.connection_name) as connection:
                result = connection.execute(statement)
                for row in result.mappings():
                    yield dict(row)

        return iterate()

    # ---- Write operations ----

    def insert(self, values):
        """Insert one record (dict) or multiple records (list of dicts)."""
        table = self._table()
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            if isinstance(values, list):
                connection.execute(insert(table), values)
                return True
            result = connection.execute(insert(table).values(**values))
            return (
                result.inserted_primary_key[0] if result.inserted_primary_key else None
            )

    def insert_get_id(self, values: dict):
        """Insert a record and return the primary key."""
        table = self._table()
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            result = connection.execute(insert(table).values(**values))
            return (
                result.inserted_primary_key[0] if result.inserted_primary_key else None
            )

    def upsert(self, values, unique_by, update_columns=None) -> int:
        """Insert values or update matching SQLite rows."""
        if not unique_by:
            raise ValueError("The unique columns must not be empty.")
        if not values:
            return 0

        rows = [values] if isinstance(values, Mapping) else list(values)
        rows = [dict(sorted(row.items())) for row in rows]
        table = self._table()

        if update_columns is not None and not update_columns:
            with self.manager._query_connection(
                self.connection_name, write=True
            ) as connection:
                connection.execute(sqlite_insert(table).values(rows))
            return 1

        unique_columns = [unique_by] if isinstance(unique_by, str) else list(unique_by)
        if update_columns is None:
            update_columns = list(rows[0])

        statement = sqlite_insert(table).values(rows)
        if isinstance(update_columns, Mapping):
            update_values = dict(update_columns)
        else:
            update_values = {
                column: statement.excluded[column] for column in update_columns
            }
        statement = statement.on_conflict_do_update(
            index_elements=unique_columns, set_=update_values
        )

        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            return connection.execute(statement).rowcount

    # ---- Row locks ----

    def lock(self, value=True):
        self._lock = value
        return self

    def lock_for_update(self):
        return self.lock(True)

    def shared_lock(self):
        return self.lock(False)

    def update(self, values: dict) -> int:
        table = self._table()
        statement = update(table).values(**values)
        statement = self._apply_wheres(table, statement)
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            return connection.execute(statement).rowcount

    def delete(self) -> int:
        table = self._table()
        statement = delete(table)
        statement = self._apply_wheres(table, statement)
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            return connection.execute(statement).rowcount

    def truncate(self):
        """Remove all rows from the table."""
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
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
        with self.manager._query_connection(
            self.connection_name, write=True
        ) as connection:
            return connection.execute(statement).rowcount

    def decrement(self, column, amount=1, extra=None):
        """Decrement a column's value."""
        return self.increment(column, -amount, extra)

    # ---- Read operations ----

    def get(self):
        statement = self._build_select()
        with self.manager._query_connection(self.connection_name) as connection:
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
            agg_expr = fn(self._resolve_column(column))
        statement = select(agg_expr).select_from(table)
        statement = self._apply_wheres(table, statement)
        with self.manager._query_connection(self.connection_name) as connection:
            result = connection.execute(statement).scalar()
        return result

    # ---- SQL inspection ----

    def to_sql(self) -> str:
        """Return the compiled parameterized SELECT statement."""
        return str(self._compile_select())

    def get_bindings(self) -> list:
        """Return the compiled SELECT bindings in placeholder order."""
        compiled = self._compile_select()
        parameter_names = compiled.positiontup or tuple(compiled.params)
        return self._flatten_bindings(compiled.params[name] for name in parameter_names)

    # ---- Internals ----

    def _load_tables(self):
        """Lazily autoload the base table and joined tables into one MetaData."""
        if self._loaded_tables is None:
            metadata = MetaData()
            bind = self.manager._query_bind(self.connection_name)
            tables = {
                self.table_name: Table(self.table_name, metadata, autoload_with=bind)
            }
            for _, join_table, _, _, _ in self._joins:
                if join_table not in tables:
                    tables[join_table] = Table(join_table, metadata, autoload_with=bind)
            self._loaded_tables = tables
        return self._loaded_tables

    def _table(self):
        return self._load_tables()[self.table_name]

    def _resolve_column(self, column):
        """Resolve a column reference, supporting table.column qualifiers."""
        if isinstance(column, str) and "." in column:
            table_name, column_name = column.split(".", 1)
            table_name = self.manager.prefixed_table_name(
                table_name, self.connection_name
            )
            return getattr(self._load_tables()[table_name].c, column_name)
        return getattr(self._table().c, column)

    def _json_source(self, column):
        parts = column.split("->")
        source = self._resolve_column(parts[0])
        if len(parts) > 1:
            source = func.json_extract(source, "$." + ".".join(parts[1:]))
        return source

    def _apply_wheres(self, table, statement):
        """Apply all where conditions to any statement (select/update/delete)."""
        and_clauses = []
        or_clauses = []

        for boolean, column, operator, value in self._conditions:
            expr = self._comparison(self._resolve_column(column), operator, value)
            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)

        for kind, boolean, column, val in self._where_clauses:
            if kind == "multi":
                mode, operator, value, negate = val
                expressions = [
                    self._comparison(self._resolve_column(item), operator, value)
                    for item in column
                ]
                if not expressions:
                    continue
                expr = and_(*expressions) if mode == "all" else or_(*expressions)
                if negate:
                    expr = ~expr
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            json_kind = kind in {"json_contains", "json_key", "json_length"}
            row_kind = kind == "row_values"
            base_column = column.split("->", 1)[0] if json_kind else column
            col = None if row_kind else self._resolve_column(base_column)
            if kind == "column":
                operator, right_column = val
                expr = self._comparison(
                    col, operator, self._resolve_column(right_column)
                )
            elif kind == "between_columns":
                low, high, not_between = val
                expr = col.between(
                    self._resolve_column(low), self._resolve_column(high)
                )
                if not_between:
                    expr = ~expr
            elif kind == "date":
                operator, value = val
                expr = self._comparison(func.date(col), operator, value)
            elif kind == "time":
                operator, value = val
                expr = self._comparison(func.time(col), operator, value)
            elif kind == "day":
                operator, value = val
                expr = self._comparison(func.strftime("%d", col), operator, value)
            elif kind == "month":
                operator, value = val
                expr = self._comparison(func.strftime("%m", col), operator, value)
            elif kind == "year":
                operator, value = val
                expr = self._comparison(func.strftime("%Y", col), operator, value)
            elif kind == "json_contains":
                value, not_contains = val
                json_values = func.json_each(self._json_source(column)).table_valued(
                    "value"
                )
                expr = exists(
                    select(1)
                    .select_from(json_values)
                    .where(json_values.c.value == value)
                )
                if not_contains:
                    expr = ~expr
            elif kind == "json_key":
                not_contains = val
                expr = func.json_type(self._json_source(column)).is_not(None)
                if not_contains:
                    expr = ~expr
            elif kind == "json_length":
                operator, value = val
                expr = self._comparison(
                    func.json_array_length(self._json_source(column)),
                    operator,
                    value,
                )
            elif kind == "row_values":
                operator, values = val
                expr = self._comparison(
                    tuple_(*(self._resolve_column(item) for item in column)),
                    operator,
                    tuple(values),
                )
            elif kind == "in":
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

        if self._joins:
            from_clause = table
            for join_type, join_name, first, operator, second in self._joins:
                join_table = self._load_tables()[join_name]
                on_clause = self._comparison(
                    self._resolve_column(first), operator, self._resolve_column(second)
                )
                from_clause = from_clause.join(
                    join_table, on_clause, isouter=join_type == "left"
                )
            statement = statement.select_from(from_clause)

        if self._distinct:
            statement = statement.distinct()

        statement = self._apply_wheres(table, statement)

        for col_name in self._groups:
            statement = statement.group_by(self._resolve_column(col_name))

        for column, operator, value in self._havings:
            statement = statement.having(
                self._comparison(self._resolve_column(column), operator, value)
            )

        for col_name, direction in self._orders:
            col = self._resolve_column(col_name)
            statement = statement.order_by(
                col.asc() if direction == "asc" else col.desc()
            )

        if self._lock is True:
            statement = statement.with_for_update()
        elif self._lock is False:
            statement = statement.with_for_update(read=True)

        if self._limit is not None:
            statement = statement.limit(self._limit)
        if self._offset is not None:
            statement = statement.offset(self._offset)

        return statement

    def _selected_columns(self, table):
        if not self._columns or self._columns == ("*",):
            columns = list(table.c)
        else:
            columns = [self._resolve_column(column) for column in self._columns]
        columns.extend(
            self._resolve_column(column).label(alias)
            for column, alias in self._aliased_columns
        )
        return columns

    def _compile_select(self):
        return self._build_select().compile(
            self.manager._query_bind(self.connection_name),
            compile_kwargs={"render_postcompile": True},
        )

    @staticmethod
    def _flatten_bindings(bindings):
        flattened = []
        for binding in bindings:
            if isinstance(binding, (list, tuple)):
                flattened.extend(QueryBuilder._flatten_bindings(binding))
            else:
                flattened.append(binding)
        return flattened

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
