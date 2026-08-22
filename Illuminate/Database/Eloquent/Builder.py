from datetime import datetime, timezone

from Illuminate.Database.Eloquent.SoftDeletes import SoftDeletes


class Builder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = model_class._query_builder()
        self._default_scope_applied = False
        if issubclass(model_class, SoftDeletes):
            self.query.where_null(model_class.DELETED_AT)
            self._default_scope_applied = True

    # ---- Where clauses ----

    def where(self, column, operator="=", value=None):
        self.query.where(column, operator, value)
        return self

    def or_where(self, column, operator="=", value=None):
        self.query.or_where(column, operator, value)
        return self

    # ---- Select and joins ----

    def select(self, *columns):
        self.query.select(*columns)
        return self

    def add_select(self, *columns):
        self.query.add_select(*columns)
        return self

    def add_select_aliased(self, column, alias):
        self.query.add_select_aliased(column, alias)
        return self

    def join(self, table, first, operator="=", second=None):
        self.query.join(table, first, operator, second)
        return self

    def left_join(self, table, first, operator="=", second=None):
        self.query.left_join(table, first, operator, second)
        return self

    def where_in(self, column, values):
        self.query.where_in(column, values)
        return self

    def where_not_in(self, column, values):
        self.query.where_not_in(column, values)
        return self

    def where_null(self, column):
        self.query.where_null(column)
        return self

    def where_not_null(self, column):
        self.query.where_not_null(column)
        return self

    def where_between(self, column, values):
        self.query.where_between(column, values)
        return self

    def where_not_between(self, column, values):
        self.query.where_not_between(column, values)
        return self

    # ---- Ordering ----

    def order_by(self, column, direction="asc"):
        self.query.order_by(column, direction)
        return self

    def order_by_desc(self, column):
        self.query.order_by_desc(column)
        return self

    def latest(self, column="created_at"):
        self.query.latest(column)
        return self

    def oldest(self, column="created_at"):
        self.query.oldest(column)
        return self

    # ---- Limit / Offset ----

    def limit(self, value):
        self.query.limit(value)
        return self

    def offset(self, value):
        self.query.offset(value)
        return self

    def skip(self, value):
        return self.offset(value)

    def take(self, value):
        return self.limit(value)

    def for_page(self, page, per_page=15):
        self.query.for_page(page, per_page)
        return self

    # ---- Read operations ----

    def get(self):
        return [self.model_class(record, exists=True) for record in self.query.get()]

    def first(self):
        record = self.query.first()
        return self.model_class(record, exists=True) if record else None

    def first_or_fail(self):
        instance = self.first()
        if instance is None:
            raise LookupError(f"{self.model_class.__name__} was not found.")
        return instance

    def value(self, column):
        return self.query.value(column)

    def pluck(self, column, key=None):
        return self.query.pluck(column, key)

    def exists(self):
        return self.query.exists()

    def doesnt_exist(self):
        return self.query.doesnt_exist()

    # ---- Aggregates ----

    def count(self, column="*"):
        return self.query.count(column)

    def sum(self, column):
        return self.query.sum(column)

    def avg(self, column):
        return self.query.avg(column)

    average = avg

    def min(self, column):
        return self.query.min(column)

    def max(self, column):
        return self.query.max(column)

    # ---- Write operations ----

    def create(self, attributes):
        return self.model_class.create(attributes)

    def increment(self, column, amount=1, extra=None):
        return self.query.increment(column, amount, extra)

    def decrement(self, column, amount=1, extra=None):
        return self.query.decrement(column, amount, extra)

    def update(self, values):
        return self.query.update(values)

    # ---- Soft deleting ----

    def _remove_default_scope(self):
        if not self._default_scope_applied:
            return
        clause = ("null", "and", self.model_class.DELETED_AT, None)
        if clause in self.query._where_clauses:
            self.query._where_clauses.remove(clause)
        self._default_scope_applied = False

    def with_trashed(self):
        """Include soft-deleted records in the query results."""
        self._remove_default_scope()
        return self

    def without_trashed(self):
        """Exclude soft-deleted records from the query results."""
        self._remove_default_scope()
        self.query.where_null(self.model_class.DELETED_AT)
        return self

    def only_trashed(self):
        """Include only soft-deleted records in the query results."""
        self._remove_default_scope()
        self.query.where_not_null(self.model_class.DELETED_AT)
        return self

    def restore(self):
        """Restore all soft-deleted records matching the current query."""
        self.with_trashed()
        return self.query.update({self.model_class.DELETED_AT: None})

    def delete(self):
        if issubclass(self.model_class, SoftDeletes):
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            return self.query.update({self.model_class.DELETED_AT: now})
        return self.query.delete()
