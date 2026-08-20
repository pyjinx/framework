from sqlalchemy import MetaData, Select, Table, select


class QueryBuilder:
    def __init__(self, manager, table_name: str, connection_name=None):
        self.manager = manager
        self.table_name = table_name
        self.connection_name = connection_name
        self._columns = None
        self._conditions = []
        self._limit = None
        self._offset = None

    def select(self, *columns):
        self._columns = columns or ("*",)
        return self

    def where(self, column, operator="=", value=None):
        if value is None:
            value = operator
            operator = "="
        self._conditions.append((column, operator, value))
        return self

    def limit(self, value: int):
        self._limit = value
        return self

    def offset(self, value: int):
        self._offset = value
        return self

    def get(self):
        statement = self._statement()
        with self.manager.connection(self.connection_name).connect() as connection:
            rows = connection.execute(statement).mappings().all()
        return [dict(row) for row in rows]

    def first(self):
        rows = self.limit(1).get()
        return rows[0] if rows else None

    def _statement(self) -> Select:
        engine = self.manager.connection(self.connection_name)
        table = Table(self.table_name, MetaData(), autoload_with=engine)
        columns = self._selected_columns(table)
        statement = select(*columns)
        for column, operator, value in self._conditions:
            expression = getattr(table.c, column)
            statement = statement.where(self._comparison(expression, operator, value))
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
        }
        if operator not in comparisons:
            raise ValueError(f"Unsupported where operator: {operator}")
        return comparisons[operator]
