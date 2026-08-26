from collections.abc import Mapping
from datetime import date, datetime, time
from sqlalchemy import (
    MetaData,
    Select,
    Table,
    and_,
    bindparam,
    case,
    delete,
    exists,
    func,
    insert,
    literal,
    or_,
    select,
    text,
    tuple_,
    true,
    update,
)
from sqlalchemy.dialects.sqlite import insert as sqlite_insert


class QueryBuilder:
    def __init__(self, manager, table_name: str, connection_name=None):
        self.manager = manager
        self.connection_name = connection_name
        self.table_name = manager.prefixed_table_name(table_name, connection_name)
        self._from_subquery = None
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
        self._join_sources = {}
        self._aliased_columns = []
        self._loaded_tables = None
        self._raw_selects = []
        self._raw_orders = []
        self._raw_groups = []
        self._raw_havings = []
        self._bindings = {
            binding_type: []
            for binding_type in (
                "select",
                "from",
                "join",
                "where",
                "groupBy",
                "having",
                "order",
                "union",
                "unionOrder",
            )
        }
        self._lock = None
        self._timeout = None
        self._before_query_callbacks = []
        self._after_query_callbacks = []
        self._in_order_of = []
        self._unions = []
        self._union_orders = []
        self._union_limit = None
        self._union_offset = None

    # ---- Select ----

    def select(self, *columns):
        self._columns = columns or ("*",)
        return self
    def select_raw(self, expression: str, bindings=None):
        self._raw_selects.append(
            self._raw_expression(expression, [] if bindings is None else bindings)
        )
        self._columns = ()
        return self

    def select_sub(self, query_or_callback, alias: str):
        query = query_or_callback
        if callable(query_or_callback):
            query = QueryBuilder(self.manager, self.table_name, self.connection_name)
            result = query_or_callback(query)
            if isinstance(result, QueryBuilder):
                query = result
        if not isinstance(query, QueryBuilder):
            raise TypeError("A subselect projection requires a QueryBuilder.")
        self._raw_selects.append(query._build_select().scalar_subquery().label(alias))
        self._columns = ()
        return self

    def from_(self, table_name: str):
        self.table_name = self.manager.prefixed_table_name(
            table_name, self.connection_name
        )
        self._from_subquery = None
        self._loaded_tables = None
        return self

    def from_sub(self, query_or_callback, alias: str):
        query = query_or_callback
        if callable(query_or_callback):
            query = QueryBuilder(self.manager, self.table_name, self.connection_name)
            result = query_or_callback(query)
            if isinstance(result, QueryBuilder):
                query = result
        if not isinstance(query, QueryBuilder):
            eloquent_query = getattr(query, "query", None)
            if isinstance(eloquent_query, QueryBuilder):
                query = eloquent_query
        if not isinstance(query, QueryBuilder):
            raise TypeError("A derived table source requires a QueryBuilder.")

        self.table_name = alias
        self._from_subquery = query._build_select().subquery(alias)
        self._loaded_tables = None
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
    def join_where(self, table, first, operator="=", second=None):
        """Add a join whose second operand is a bound literal value."""
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("inner", table, first, operator, second, True))
        self._loaded_tables = None
        return self

    def left_join_where(self, table, first, operator="=", second=None):
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("left", table, first, operator, second, True))
        self._loaded_tables = None
        return self

    def left_join(self, table, first, operator="=", second=None):
        """Add a left join clause."""
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("left", table, first, operator, second))
        self._loaded_tables = None
        return self
    def _coerce_join_subquery(self, query_or_callback, alias: str):
        query = query_or_callback
        if callable(query_or_callback):
            query = QueryBuilder(self.manager, self.table_name, self.connection_name)
            result = query_or_callback(query)
            if isinstance(result, QueryBuilder):
                query = result
        if not isinstance(query, QueryBuilder):
            eloquent_query = getattr(query, "query", None)
            if isinstance(eloquent_query, QueryBuilder):
                query = eloquent_query
        if not isinstance(query, QueryBuilder):
            raise TypeError("A join subquery requires a QueryBuilder.")
        subquery = query._build_select().subquery(alias)
        self._join_sources[alias] = subquery
        return alias

    def join_sub(
        self, query_or_callback, alias: str, first, operator="=", second=None
    ):
        alias = self._coerce_join_subquery(query_or_callback, alias)
        self._joins.append(("inner", alias, first, operator, second))
        self._loaded_tables = None
        return self

    def left_join_sub(
        self, query_or_callback, alias: str, first, operator="=", second=None
    ):
        alias = self._coerce_join_subquery(query_or_callback, alias)
        self._joins.append(("left", alias, first, operator, second))
        self._loaded_tables = None
        return self

    def cross_join(self, table):
        table = self.manager.prefixed_table_name(table, self.connection_name)
        self._joins.append(("cross", table, None, None, None))
        self._loaded_tables = None
        return self

    def cross_join_sub(self, query_or_callback, alias: str):
        alias = self._coerce_join_subquery(query_or_callback, alias)
        self._joins.append(("cross", alias, None, None, None))
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

    def where_raw(self, sql: str, bindings=None, boolean: str = "and"):
        self._where_clauses.append(
            ("raw", boolean, sql, [] if bindings is None else bindings)
        )
        return self

    def or_where_raw(self, sql: str, bindings=None):
        return self.where_raw(sql, bindings, "or")

    def where_null_safe_equals(self, column, value, boolean: str = "and"):
        self._where_clauses.append(("null_safe_equals", boolean, column, value))
        return self

    def or_where_null_safe_equals(self, column, value):
        return self.where_null_safe_equals(column, value, "or")

    def where_not(self, column, operator="=", value=None, boolean: str = "and"):
        if value is None:
            value = operator
            operator = "="
        self._where_clauses.append(("not_basic", boolean, column, (operator, value)))
        return self

    def or_where_not(self, column, operator="=", value=None):
        return self.where_not(column, operator, value, "or")

    def where_like(
        self,
        column,
        value,
        case_sensitive: bool = False,
        boolean: str = "and",
        not_like: bool = False,
    ):
        self._where_clauses.append(
            ("like", boolean, column, (value, case_sensitive, not_like))
        )
        return self

    def or_where_like(self, column, value, case_sensitive: bool = False):
        return self.where_like(column, value, case_sensitive, "or")

    def where_not_like(
        self, column, value, case_sensitive: bool = False, boolean: str = "and"
    ):
        return self.where_like(column, value, case_sensitive, boolean, True)

    def or_where_not_like(self, column, value, case_sensitive: bool = False):
        return self.where_not_like(column, value, case_sensitive, "or")

    def where_exists(self, callback_or_query, boolean: str = "and", not_exists=False):
        query = callback_or_query
        if callable(callback_or_query):
            query = QueryBuilder(self.manager, self.table_name, self.connection_name)
            result = callback_or_query(query)
            if isinstance(result, QueryBuilder):
                query = result
        if not isinstance(query, QueryBuilder):
            raise TypeError("An exists predicate requires a QueryBuilder.")
        self._where_clauses.append(("exists", boolean, query, not_exists))
        return self

    def or_where_exists(self, callback_or_query, not_exists=False):
        return self.where_exists(callback_or_query, "or", not_exists)

    def where_not_exists(self, callback_or_query, boolean: str = "and"):
        return self.where_exists(callback_or_query, boolean, True)

    def or_where_not_exists(self, callback_or_query):
        return self.where_exists(callback_or_query, "or", True)
    def add_where_exists_query(self, query, boolean: str = "and", not_exists=False):
        if not isinstance(query, QueryBuilder):
            raise TypeError("An exists subquery requires a QueryBuilder.")
        self._where_clauses.append(("exists", boolean, query, not_exists))
        return self

    def for_nested_where(self):
        return QueryBuilder(
            self.manager, self.table_name, self.connection_name
        ).from_(self.table_name)

    def add_nested_where_query(self, query, boolean: str = "and"):
        if not isinstance(query, QueryBuilder):
            raise TypeError("A nested where requires a QueryBuilder.")
        if not query._where_clauses and not query._conditions:
            return self
        self._where_clauses.append(("nested", boolean, query, None))
        return self

    def where_nested(self, callback, boolean: str = "and"):
        nested = self.for_nested_where()
        result = callback(nested) if callable(callback) else nested
        if isinstance(result, QueryBuilder):
            nested = result
        return self.add_nested_where_query(nested, boolean)

    def or_where_nested(self, callback):
        return self.where_nested(callback, "or")

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

    @staticmethod
    def _validate_flat_in_values(values):
        if isinstance(values, QueryBuilder):
            return values
        values = list(values)
        if any(isinstance(value, (list, tuple, set, frozenset)) for value in values):
            raise ValueError("Nested arrays may not be passed to whereIn method.")
        return values

    def where_in(self, column, values, boolean="and", not_in=False):
        values = self._validate_flat_in_values(values)
        kind = "not_in" if not_in else "in"
        self._where_clauses.append((kind, boolean, column, values))
        return self

    def or_where_in(self, column, values):
        return self.where_in(column, values, "or")

    def where_not_in(self, column, values, boolean="and"):
        return self.where_in(column, values, boolean, True)

    def or_where_not_in(self, column, values):
        return self.where_not_in(column, values, "or")

    def where_integer_in_raw(
        self, column, values, boolean: str = "and", not_in: bool = False
    ):
        flattened = []
        for value in values:
            if isinstance(value, (list, tuple, set, frozenset)):
                flattened.extend(value)
            else:
                flattened.append(value)
        normalized = [int(value) for value in flattened]
        self._where_clauses.append(
            ("integer_raw", boolean, column, (normalized, not_in))
        )
        return self

    def or_where_integer_in_raw(self, column, values):
        return self.where_integer_in_raw(column, values, "or")

    def where_integer_not_in_raw(self, column, values, boolean: str = "and"):
        return self.where_integer_in_raw(column, values, boolean, True)

    def or_where_integer_not_in_raw(self, column, values):
        return self.where_integer_not_in_raw(column, values, "or")

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
    def or_where_not_between(self, column, values):
        low, high = values
        self._where_clauses.append(("not_between", "or", column, (low, high)))
        return self

    def where_value_between(self, value, columns, not_between=False):
        low, high = columns
        self._where_clauses.append(
            ("value_between", "and", (low, high), (value, not_between))
        )
        return self

    def or_where_value_between(self, value, columns):
        low, high = columns
        self._where_clauses.append(
            ("value_between", "or", (low, high), (value, False))
        )
        return self

    def where_value_not_between(self, value, columns):
        return self.where_value_between(value, columns, True)

    def or_where_value_not_between(self, value, columns):
        low, high = columns
        return self._append_value_between(
            value, low, high, "or", True
        )

    def _append_value_between(self, value, low, high, boolean, not_between):
        self._where_clauses.append(
            ("value_between", boolean, (low, high), (value, not_between))
        )
        return self

    # ---- Ordering ----

    def order_by(self, column, direction="asc"):
        direction = direction.lower()
        if direction not in ("asc", "desc"):
            raise ValueError('Order direction must be "asc" or "desc".')
        self._orders.append((column, direction))
        return self

    def order_by_raw(self, expression: str, bindings=None):
        self._raw_orders.append(
            self._raw_expression(expression, [] if bindings is None else bindings)
        )
        return self
    def order_by_desc(self, column):
        return self.order_by(column, "desc")

    def latest(self, column="created_at"):
        return self.order_by(column, "desc")

    def oldest(self, column="created_at"):
        return self.order_by(column, "asc")

    def in_random_order(self, seed=""):
        """Add a SQLite ``RANDOM()`` ordering clause.

        Mirrors Laravel ``Query\\Builder::inRandomOrder`` by emitting a
        raw ``orderByRaw("RANDOM()")`` clause; an optional ``seed`` is
        accepted to match the Laravel signature but does not alter the
        compiled clause because SQLite ``RANDOM()`` is non-deterministic.
        """
        return self.order_by_raw("RANDOM()", [])

    def in_order_of(self, column, values):
        """Order rows by a custom sequence of values.

        Mirrors Laravel ``Query\\Builder::inOrderOf`` by emitting a
        ``CASE WHEN`` ordering clause; ``values`` may be a list, tuple,
        or any iterable of scalars, and ``None`` is preserved as a
        trailing default branch. Empty values are a no-op.
        """
        if values is None:
            return self
        try:
            values_list = list(values)
        except TypeError:
            values_list = [values]
        if not values_list:
            return self
        self._in_order_of.append((column, values_list))
        return self

    def union(self, query, all=False):
        """Compose a UNION with another query.

        Mirrors Laravel ``Query\\Builder::union`` by accepting either a
        ``QueryBuilder`` instance or a closure that configures a fresh
        sub-builder. Subquery bindings are merged into the current
        ``union`` binding bucket.
        """
        if callable(query):
            sub = self._new_subquery()
            query(sub)
            query = sub
        if not isinstance(query, QueryBuilder):
            raise TypeError(
                "union() requires a QueryBuilder or a callable that "
                "configures a fresh subquery builder."
            )
        self._unions.append({"query": query, "all": bool(all)})
        self.add_binding(query.get_bindings(), "union")
        return self

    def union_all(self, query):
        """Compose a UNION ALL with another query.

        Mirrors Laravel ``Query\\Builder::unionAll``.
        """
        return self.union(query, all=True)

    def _new_subquery(self):
        """Create a fresh QueryBuilder sharing the current connection."""
        return QueryBuilder(
            self.manager, self.table_name, self.connection_name
        )

    # ---- Grouping ----

    def group_by(self, *columns):
        self._groups.extend(columns)
        return self

    def group_by_raw(self, expression: str, bindings=None):
        self._raw_groups.append(
            self._raw_expression(expression, [] if bindings is None else bindings)
        )
        return self

    def having(self, column, operator="=", value=None, boolean="and"):
        if value is None:
            value = operator
            operator = "="
        self._havings.append((column, operator, value, boolean))
        return self

    def or_having(self, column, operator="=", value=None):
        return self.having(column, operator, value, "or")
    def add_nested_having_query(self, query, boolean: str = "and"):
        if not isinstance(query, QueryBuilder):
            raise TypeError("A nested having requires a QueryBuilder.")
        if not query._havings and not query._raw_havings:
            return self
        self._havings.append(("nested", boolean, query, None))
        return self

    def having_nested(self, callback, boolean: str = "and"):
        nested = self.for_nested_where()
        result = callback(nested) if callable(callback) else nested
        if isinstance(result, QueryBuilder):
            nested = result
        return self.add_nested_having_query(nested, boolean)

    def or_having_nested(self, callback):
        return self.having_nested(callback, "or")

    def having_between(self, column, values, boolean="and", not_between=False):
        low, high = values
        self._havings.append(
            (column, "between", (low, high, not_between), boolean)
        )
        return self

    def having_not_between(self, column, values):
        return self.having_between(column, values, not_between=True)

    def or_having_between(self, column, values):
        return self.having_between(column, values, "or")

    def or_having_not_between(self, column, values):
        return self.having_between(column, values, "or", True)

    def having_raw(self, expression: str, bindings=None, boolean: str = "and"):
        self._raw_havings.append(
            (
                self._raw_expression(expression, [] if bindings is None else bindings),
                boolean,
            )
        )
        return self

    def or_having_raw(self, expression: str, bindings=None):
        return self.having_raw(expression, bindings, "or")

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
    def for_page_before_id(self, per_page=15, last_id=0, column="id"):
        self._orders = [order for order in self._orders if order[0] != column]
        if last_id is None:
            self.where_not_null(column)
        else:
            self.where(column, "<", last_id)
        return self.order_by(column, "desc").limit(per_page)

    def for_page_after_id(self, per_page=15, last_id=0, column="id"):
        self._orders = [order for order in self._orders if order[0] != column]
        if last_id is None:
            self.where_not_null(column)
        else:
            self.where(column, ">", last_id)
        return self.order_by(column, "asc").limit(per_page)

    def reorder(self, column=None, direction="asc"):
        self._orders = []
        if column is not None:
            return self.order_by(column, direction)
        return self

    def reorder_desc(self, column):
        return self.reorder(column, "desc")

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
        execution_options = self._execution_options()
        with self.manager._query_connection(self.connection_name) as connection:
            statement = statement.execution_options(**execution_options) if execution_options else statement
            rows = connection.execute(statement).mappings().all()
        rows = [dict(row) for row in rows]
        return self._apply_after_query_callbacks(rows)

    def first(self, columns=None):
        """Return the first row or ``None``.

        Mirrors Laravel ``Query\\Builder::first`` by accepting an
        optional ``columns`` selection; the original projection is
        restored after the row is fetched.
        """
        if columns is None:
            rows = self.limit(1).get()
            return rows[0] if rows else None
        original_columns = self._columns
        try:
            self.select(*self._normalize_columns(columns))
            rows = self.limit(1).get()
            return rows[0] if rows else None
        finally:
            self._columns = original_columns

    @staticmethod
    def _normalize_columns(columns):
        if isinstance(columns, str):
            return [columns]
        if isinstance(columns, (list, tuple)):
            return list(columns)
        return [columns]

    def find(self, id, columns=None):
        """Return the first row whose primary key matches ``id``.

        Mirrors Laravel ``Query\\Builder::find`` by composing a
        primary-key predicate and reusing ``first`` for hydration.
        """
        query = self.where("id", "=", id)
        return query.first(columns) if columns is not None else query.first()

    def find_or(self, id, columns=None, callback=None):
        """Return the matching row or invoke ``callback`` when absent.

        Mirrors Laravel ``Query\\Builder::findOr``: when ``columns`` is
        callable, it is treated as the callback and the default column
        projection is used.
        """
        if callable(columns) and callback is None:
            callback = columns
            columns = None
        row = self.find(id, columns)
        if row is not None:
            return row
        return callback() if callback is not None else None

    def exists_or(self, callback):
        """Return ``True`` when rows exist, otherwise invoke ``callback``.

        Mirrors Laravel ``Query\\Builder::existsOr``.
        """
        return True if self.exists() else callback()

    def doesnt_exist_or(self, callback):
        """Return ``True`` when no rows exist, otherwise invoke ``callback``.

        Mirrors Laravel ``Query\\Builder::doesntExistOr``.
        """
        return True if self.doesnt_exist() else callback()

    def value(self, column):
        """Get a single column's value from the first result."""
        row = self.first()
        if row is None:
            return None
        return row.get(column)

    def raw_value(self, expression: str, bindings=None):
        original_columns = self._columns
        original_raw_selects = list(self._raw_selects)
        original_limit = self._limit
        try:
            self.select_raw(expression, bindings)
            row = self.first()
            return next(iter(row.values())) if row else None
        finally:
            self._columns = original_columns
            self._raw_selects = original_raw_selects
            self._limit = original_limit

    def implode(self, column, glue=""):
        return glue.join(str(value) for value in self.pluck(column))
    def get_columns(self):
        if self._columns is None:
            return []
        return list(self._columns)

    def get_limit(self):
        return self._limit

    def get_offset(self):
        return self._offset

    def timeout(self, seconds):
        """Set a per-statement execution timeout in seconds.

        Mirrors Laravel ``Query\\Builder::timeout`` by rejecting
        non-positive values and clearing the timeout when ``None`` is
        supplied.
        """
        if seconds is not None and (
            not isinstance(seconds, int) or isinstance(seconds, bool) or seconds <= 0
        ):
            raise ValueError("Timeout must be greater than zero.")
        self._timeout = seconds
        return self

    def before_query(self, callback):
        """Register a callback to be invoked before query execution.

        Mirrors Laravel ``Query\\Builder::beforeQuery``. The callback
        receives this builder as its only argument and is invoked once
        by ``_apply_before_query_callbacks`` during SQL compilation or
        statement execution.
        """
        self._before_query_callbacks.append(callback)
        return self

    def _apply_before_query_callbacks(self) -> None:
        """Invoke registered before-query callbacks once and clear them.

        Mirrors Laravel ``Query\\Builder::applyBeforeQueryCallbacks``.
        The callback list is cleared before iteration so a callback
        that re-enters ``to_sql`` cannot re-trigger the same hooks.
        """
        callbacks = self._before_query_callbacks
        self._before_query_callbacks = []
        for callback in callbacks:
            callback(self)

    def after_query(self, callback):
        """Register a callback to be invoked after query execution.

        Mirrors Laravel ``Query\\Builder::afterQuery``. Each callback
        receives the result list and may return a replacement value;
        a falsy return keeps the prior result.
        """
        self._after_query_callbacks.append(callback)
        return self

    def _apply_after_query_callbacks(self, result):
        """Invoke registered after-query callbacks in registration order.

        Mirrors Laravel ``Query\\Builder::applyAfterQueryCallbacks``.
        A callback returning a falsy value preserves the prior result.
        """
        for callback in list(self._after_query_callbacks):
            new_result = callback(result)
            if new_result:
                result = new_result
        return result

    def _execution_options(self) -> dict:
        """Return SQLAlchemy execution options for the current builder.

        Currently translates ``_timeout`` into a per-statement
        ``statement_timeout`` hint through SQLAlchemy's
        ``execution_options`` so SQLite/MySQL backends can honour a
        ``Query\\Builder::timeout`` value.
        """
        if self._timeout is None:
            return {}
        return {"statement_timeout": self._timeout}

    def pluck(self, column, key=None):
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

    @staticmethod
    def _raw_expression(sql, bindings):
        if isinstance(bindings, dict):
            return text(sql).bindparams(**bindings)

        bindings = list(bindings)
        for index, _ in enumerate(bindings):
            sql = sql.replace("?", f":raw_{index}", 1)
        return text(sql).bindparams(
            *[bindparam(f"raw_{index}", value) for index, value in enumerate(bindings)]
        )

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
        """Return the compiled parameterized SELECT statement.

        Mirrors Laravel ``Query\\Builder::toSql`` by running registered
        ``before_query`` callbacks before compiling.
        """
        self._apply_before_query_callbacks()
        return str(self._compile_select())

    def to_raw_sql(self) -> str:
        """Return the SQL with bindings embedded as quoted literals.

        Mirrors Laravel ``Query\\Builder::toRawSql`` by compiling the
        parameterized statement and substituting each ``?`` placeholder
        with its escaped value. ``?`` placeholders inside string literals
        are preserved.
        """
        sql = self.to_sql()
        bindings = self.get_bindings()
        if not bindings:
            return sql
        connection = self.manager.connection(self.connection_name)
        prepared = connection.prepare_bindings(bindings)
        return self._substitute_bindings(sql, prepared, connection)

    def _substitute_bindings(self, sql, bindings, connection) -> str:
        """Replace ``?`` placeholders outside string literals with escaped values.

        Mirrors ``Grammar::substituteBindingsIntoRawSql``: a single
        quote toggles a string-literal region, and doubled ``''`` or
        escaped ``\\'`` are passed through unchanged.
        """
        rendered = []
        binding_index = 0
        in_string = False
        i = 0
        sql_length = len(sql)
        while i < sql_length:
            char = sql[i]
            if in_string:
                rendered.append(char)
                if char == "'" and i + 1 < sql_length and sql[i + 1] == "'":
                    rendered.append("'")
                    i += 2
                    continue
                if char == "'":
                    in_string = False
                i += 1
                continue
            if char == "'":
                rendered.append(char)
                in_string = True
                i += 1
                continue
            if char == "?":
                if binding_index < len(bindings):
                    rendered.append(connection.escape(bindings[binding_index]))
                    binding_index += 1
                else:
                    rendered.append("?")
                i += 1
                continue
            rendered.append(char)
            i += 1
        return "".join(rendered)

    def get_bindings(self) -> list:
        """Return the compiled SELECT bindings in placeholder order."""
        compiled = self._compile_select()
        parameter_names = compiled.positiontup or tuple(compiled.params)
        return self._flatten_bindings(compiled.params[name] for name in parameter_names)

    def get_raw_bindings(self):
        return {binding_type: list(values) for binding_type, values in self._bindings.items()}

    def set_bindings(self, bindings, binding_type="where"):
        if binding_type not in self._bindings:
            raise ValueError(f"Invalid binding type: {binding_type}.")
        self._bindings[binding_type] = list(bindings)
        return self

    def add_binding(self, value, binding_type="where"):
        if binding_type not in self._bindings:
            raise ValueError(f"Invalid binding type: {binding_type}.")
        values = value if isinstance(value, (list, tuple)) else [value]
        self._bindings[binding_type].extend(self.cast_binding(item) for item in values)
        return self

    @staticmethod
    def cast_binding(value):
        return value

    def merge_bindings(self, query):
        if not isinstance(query, QueryBuilder):
            raise TypeError("Bindings can only be merged from a QueryBuilder.")
        for binding_type, values in query._bindings.items():
            self._bindings[binding_type].extend(values)
        return self

    @classmethod
    def clean_bindings(cls, bindings):
        return [
            cls.cast_binding(value)
            for value in bindings
            if not hasattr(value, "_compiler_dispatch")
        ]

    # ---- Internals ----

    def _load_tables(self):
        """Lazily autoload the base table and joined tables into one MetaData."""
        if self._loaded_tables is None:
            metadata = MetaData()
            bind = self.manager._query_bind(self.connection_name)
            if self._from_subquery is not None:
                tables = {self.table_name: self._from_subquery}
            else:
                tables = {
                    self.table_name: Table(
                        self.table_name, metadata, autoload_with=bind
                    )
                }
            for join in self._joins:
                _, join_table, _, _, _ = join[:5]
                if join_table not in tables:
                    if join_table in self._join_sources:
                        tables[join_table] = self._join_sources[join_table]
                    else:
                        tables[join_table] = Table(
                            join_table, metadata, autoload_with=bind
                        )
            self._loaded_tables = tables
        return self._loaded_tables

    def _table(self):
        return self._load_tables()[self.table_name]

    def _resolve_column(self, column):
        """Resolve a column reference, supporting table.column qualifiers."""
        if isinstance(column, str) and "." in column:
            table_name, column_name = column.split(".", 1)
            tables = self._load_tables()
            qualified_table_name = (
                table_name
                if table_name in tables
                else self.manager.prefixed_table_name(
                    table_name, self.connection_name
                )
            )
            return getattr(tables[qualified_table_name].c, column_name)
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
            if kind == "raw":
                expr = self._raw_expression(column, val)
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "not_basic":
                operator, value = val
                expr = ~self._comparison(self._resolve_column(column), operator, value)
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "null_safe_equals":
                expr = self._resolve_column(column).is_(val)
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "integer_raw":
                values, not_in = val
                col = self._resolve_column(column)
                expr = col.notin_(values) if not_in else col.in_(values)
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "like":
                value, case_sensitive, negate = val
                col = self._resolve_column(column)
                if case_sensitive:
                    value = (
                        str(value)
                        .replace("*", "[*]")
                        .replace("?", "[?]")
                        .replace("%", "*")
                        .replace("_", "?")
                    )
                    expr = col.op("GLOB")(value)
                else:
                    expr = col.like(value)
                if negate:
                    expr = ~expr
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "exists":
                expr = exists(column._build_select())
                if val:
                    expr = ~expr
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "nested":
                expr = self._nested_where_expression(column, table)

                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
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
                    select(1).select_from(json_values).where(json_values.c.value == value)
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
                if isinstance(val, QueryBuilder):
                    expr = col.in_(val._build_select())
                else:
                    expr = col.in_(val)
            elif kind == "not_in":
                if isinstance(val, QueryBuilder):
                    expr = col.notin_(val._build_select())
                else:
                    expr = col.notin_(val)
            elif kind == "null":
                expr = col.is_(None)
            elif kind == "not_null":
                expr = col.isnot(None)
            elif kind == "between":
                expr = col.between(val[0], val[1])
            elif kind == "not_between":
                expr = ~col.between(val[0], val[1])
            elif kind == "value_between":
                (low, high), (value, not_between) = column, val
                expr = and_(
                    self._comparison(self._resolve_column(low), "<=", value),
                    self._comparison(self._resolve_column(high), ">=", value),
                )
                if not_between:
                    expr = ~expr
            else:
                continue

            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)
        if and_clauses and or_clauses:
            return statement.where(or_(and_(*and_clauses), *or_clauses))
        if and_clauses:
            for clause in and_clauses:
                statement = statement.where(clause)
            return statement
        if or_clauses:
            return statement.where(or_(*or_clauses))
        return statement

    def _nested_where_expression(self, nested, table):
        """Compile a nested QueryBuilder's wheres into a single SQLAlchemy predicate."""
        synthetic = select(literal(1))
        applied = self._apply_nested_wheres(nested, table, synthetic)
        where_clause = applied.whereclause
        if where_clause is None:
            return literal(True)
        return where_clause

    def _apply_nested_wheres(self, nested, table, statement):
        and_clauses = []
        or_clauses = []
        for boolean, column, operator, value in nested._conditions:
            expr = self._comparison(
                getattr(table.c, column) if isinstance(column, str) else column,
                operator,
                value,
            )
            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)
        for kind, boolean, column, val in nested._where_clauses:
            if kind == "exists":
                expr = exists(column._build_select())
                if val:
                    expr = ~expr
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "nested":
                expr = self._nested_where_expression(column, table)
                if boolean == "or":
                    or_clauses.append(expr)
                else:
                    and_clauses.append(expr)
                continue
            if kind == "raw":
                expr = self._raw_expression(column, val)
            else:
                expr = self._resolve_nested_column(table, kind, column, val)
                if expr is None:
                    continue
            if boolean == "or":
                or_clauses.append(expr)
            else:
                and_clauses.append(expr)
        if and_clauses and or_clauses:
            return statement.where(or_(and_(*and_clauses), *or_clauses))
        if and_clauses:
            for clause in and_clauses:
                statement = statement.where(clause)
            return statement
        if or_clauses:
            return statement.where(or_(*or_clauses))
        return statement

    def _resolve_nested_column(self, table, kind, column, val):
        if isinstance(column, QueryBuilder):
            return None
        if "." in (column or ""):
            table_name, column_name = column.split(".", 1)
            target_table = getattr(table, "table", table)
            try:
                return getattr(target_table.c, column_name)
            except AttributeError:
                pass
        if kind in {"like", "not_like"}:
            col = getattr(table.c, column)
            value, case_sensitive, negate = val
            if case_sensitive:
                value = (
                    str(value)
                    .replace("*", "[*]")
                    .replace("?", "[?]")
                    .replace("%", "*")
                    .replace("_", "?")
                )
                expr = col.op("GLOB")(value)
            else:
                expr = col.like(value)
            return ~expr if negate else expr
        if kind == "in" and isinstance(val, QueryBuilder):
            return getattr(table.c, column).in_(val._build_select())
        if kind == "not_in" and isinstance(val, QueryBuilder):
            return getattr(table.c, column).notin_(val._build_select())
        col = getattr(table.c, column)
        if kind == "between":
            return col.between(val[0], val[1])
        if kind == "not_between":
            return ~col.between(val[0], val[1])
        if kind == "value_between":
            (low, high), (value, not_between) = column, val
            expr = and_(
                self._comparison(getattr(table.c, low), "<=", value),
                self._comparison(getattr(table.c, high), ">=", value),
            )
            return ~expr if not_between else expr
        if kind in {"column", "between_columns"}:
            if kind == "column":
                operator, right_column = val
                return self._comparison(
                    col, operator, getattr(table.c, right_column)
                )
            low, high, not_between = val
            expr = col.between(getattr(table.c, low), getattr(table.c, high))
            return ~expr if not_between else expr
        if kind == "not_basic":
            operator, value = val
            return ~self._comparison(col, operator, value)
        if kind == "null_safe_equals":
            return col.is_(val)
        if kind == "integer_raw":
            values, not_in = val
            return col.notin_(values) if not_in else col.in_(values)
        if kind == "multi":
            mode, operator, value, negate = val
            expressions = [
                self._comparison(getattr(table.c, item), operator, value)
                for item in column
            ]
            if not expressions:
                return None
            expr = and_(*expressions) if mode == "all" else or_(*expressions)
            return ~expr if negate else expr
        if kind in {"date", "time", "day", "month", "year"}:
            extractor = {
                "date": func.date,
                "time": func.time,
                "day": lambda c: func.strftime("%d", c),
                "month": lambda c: func.strftime("%m", c),
                "year": lambda c: func.strftime("%Y", c),
            }[kind]
            operator, value = val
            return self._comparison(extractor(col), operator, value)
        if kind == "null":
            return col.is_(None)
        if kind == "not_null":
            return col.isnot(None)
        return None

    def _nested_having_expression(self, nested):
        synthetic = select(literal(1))
        statement = self._apply_nested_havings(nested, synthetic)
        where_clause = statement.whereclause
        if where_clause is None:
            return literal(True)
        return where_clause

    def _apply_nested_havings(self, nested, statement):
        and_clauses = []
        or_clauses = []
        for having in nested._havings:
            if len(having) == 3:
                column, operator, value = having
                boolean = "and"
            else:
                column, operator, value, boolean = having
            column_expr = nested._resolve_column(column)
            if operator == "between":
                low, high, not_between = value
                expression = column_expr.between(low, high)
                if not_between:
                    expression = ~expression
            else:
                expression = self._comparison(column_expr, operator, value)
            (or_clauses if boolean == "or" else and_clauses).append(expression)
        for expression, boolean in nested._raw_havings:
            (or_clauses if boolean == "or" else and_clauses).append(expression)
        if not and_clauses and not or_clauses:
            return statement
        if and_clauses and or_clauses:
            return statement.having(or_(and_(*and_clauses), *or_clauses))
        if and_clauses:
            return statement.having(and_(*and_clauses))
        return statement.having(or_(*or_clauses))

    def _build_select(self) -> Select:
        """Build a complete SELECT statement."""
        table = self._table()
        columns = self._selected_columns(table)
        statement = select(*columns)

        if self._joins:
            from_clause = table
            for join in self._joins:
                join_type, join_name, first, operator, second = join[:5]
                where_join = len(join) == 6 and join[5]
                join_table = self._load_tables()[join_name]
                if join_type == "cross":
                    on_clause = true()
                else:
                    right = second if where_join else self._resolve_column(second)
                    on_clause = self._comparison(
                        self._resolve_column(first), operator, right
                    )
                from_clause = from_clause.join(
                    join_table, on_clause, isouter=join_type == "left"
                )
            statement = statement.select_from(from_clause)
        if self._raw_selects and not self._joins:
            statement = statement.select_from(table)

        if self._distinct:
            statement = statement.distinct()
        for expression in self._raw_groups:
            statement = statement.group_by(expression)

        statement = self._apply_wheres(table, statement)

        for col_name in self._groups:
            statement = statement.group_by(self._resolve_column(col_name))

        and_havings = []
        or_havings = []
        for having in self._havings:
            if len(having) == 4 and having[0] == "nested":
                _, boolean, query, _ = having
                expression = self._nested_having_expression(query)
                (or_havings if boolean == "or" else and_havings).append(expression)
                continue
            if len(having) == 3:
                column, operator, value = having
                boolean = "and"
            else:
                column, operator, value, boolean = having
            column_expr = self._resolve_column(column)
            if operator == "between":
                low, high, not_between = value
                expression = column_expr.between(low, high)
                if not_between:
                    expression = ~expression
            else:
                expression = self._comparison(column_expr, operator, value)
            (or_havings if boolean == "or" else and_havings).append(expression)
        for expression, boolean in self._raw_havings:
            (or_havings if boolean == "or" else and_havings).append(expression)
        if and_havings and or_havings:
            statement = statement.having(or_(and_(*and_havings), *or_havings))
        elif and_havings:
            statement = statement.having(and_(*and_havings))
        elif or_havings:
            statement = statement.having(or_(*or_havings))

        for col_name, direction in self._orders:
            col = self._resolve_column(col_name)
            statement = statement.order_by(
                col.asc() if direction == "asc" else col.desc()
            )
        for expression in self._raw_orders:
            statement = statement.order_by(expression)
        for column, values in self._in_order_of:
            statement = statement.order_by(self._in_order_of_expression(column, values))

        if self._lock is True:
            statement = statement.with_for_update()
        elif self._lock is False:
            statement = statement.with_for_update(read=True)

        if self._limit is not None:
            statement = statement.limit(self._limit)
        if self._offset is not None:
            statement = statement.offset(self._offset)

        if not self._unions:
            return statement
        return self._compose_union_statement(statement)


    def _compose_union_statement(self, statement):
        """Wrap ``statement`` with UNION/UNION ALL subquery SQL.

        Each registered sub-builder is composed into the outer
        ``Select`` through SQLAlchemy's ``union``/``union_all``
        primitives so parameter binding and dialect compilation remain
        handled by SQLAlchemy. A trailing ``all=True`` entry promotes
        the entire compound to ``UNION ALL`` semantics, matching
        Laravel's behavior where the last ``union($q, true)`` call
        wins.
        """
        from sqlalchemy import union, union_all
        compounds = []
        all_mode = False
        for entry in self._unions:
            sub_query = entry["query"]
            compounds.append(sub_query._build_select())
            if entry["all"]:
                all_mode = True
        if not compounds:
            return statement
        # SQLite rejects ``ORDER BY`` directly inside a UNION operand,
        # so wrap any side that carries one in a subquery. The outer
        # statement is also wrapped when it carries a clause SQLite
        # would reject inside a compound SELECT.
        def _wrap_for_compound(select_stmt):
            inner = select_stmt.subquery()
            return select(inner)
        wrapped = _wrap_for_compound(statement)
        compounds = [_wrap_for_compound(c) for c in compounds]
        if all_mode:
            return union_all(wrapped, *compounds)
        return union(wrapped, *compounds)

    def _in_order_of_expression(self, column, values):
        """Build a SQLAlchemy ``CASE`` expression for ``in_order_of`` ordering.

        ``None`` values become a trailing ``ELSE`` branch, mirroring
        Laravel's last-position ``is null`` ordering.
        """
        column_expr = self._resolve_column(column)
        whens = {}
        position = 1
        for value in values:
            if value is None:
                # The catch-all branch: SQLAlchemy's case(value=...) cannot
                # bind ``None`` directly, so we add a separate ``else_``
                # through ``case(whens=..., else_=...)`` below.
                continue
            whens[value] = position
            position += 1
        if not whens:
            return column_expr.asc()
        # When None is not in the values, NULL rows still need a high
        # position so they sort to the end of the result set.
        else_value = position if any(v is None for v in values) else position
        return case(whens, value=column_expr, else_=else_value)

    def _selected_columns(self, table):
        if self._raw_selects:
            columns = list(self._raw_selects)
        elif not self._columns or self._columns == ("*",):
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
        if operator in {"=", "=="}:
            return column == value
        if operator in {"!=", "<>"}:
            return column != value
        if operator == ">":
            return column > value
        if operator == ">=":
            return column >= value
        if operator == "<":
            return column < value
        if operator == "<=":
            return column <= value
        if operator == "like":
            return column.like(value)
        if operator == "not like":
            return ~column.like(value)
        raise ValueError(f"Unsupported where operator: {operator}")
