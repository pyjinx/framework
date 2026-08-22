from collections.abc import Callable
from datetime import datetime, timezone
from typing import Any, Self
from Illuminate.Database.Eloquent.SoftDeletes import SoftDeletes


class Builder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = model_class._query_builder()
        self._default_scope_applied = False
        self._with_relations: list[str] = []
        self._where_has_relations = []
        if issubclass(model_class, SoftDeletes):
            self.query.where_null(model_class.DELETED_AT)
            self._default_scope_applied = True

    # ---- Where clauses ----

    def where(self, column: str, operator: str | Any = "=", value: Any = None) -> Self:
        self.query.where(column, operator, value)
        return self

    def or_where(self, column, operator="=", value=None):
        self.query.or_where(column, operator, value)
        return self

    def where_raw(self, sql, bindings=None, boolean="and"):
        self.query.where_raw(sql, bindings, boolean)
        return self

    def or_where_raw(self, sql, bindings=None):
        return self.where_raw(sql, bindings, "or")

    def select_raw(self, expression, bindings=None):
        self.query.select_raw(expression, bindings)
        return self

    def from_sub(self, query_or_callback, alias):
        self.query.from_sub(query_or_callback, alias)
        return self

    def order_by_raw(self, expression, bindings=None):
        self.query.order_by_raw(expression, bindings)
        return self

    def group_by_raw(self, expression, bindings=None):
        self.query.group_by_raw(expression, bindings)
        return self

    def having_raw(self, expression, bindings=None, boolean="and"):
        self.query.having_raw(expression, bindings, boolean)
        return self

    def or_having_raw(self, expression, bindings=None):
        return self.having_raw(expression, bindings, "or")

    def where_null_safe_equals(self, column, value, boolean="and"):
        self.query.where_null_safe_equals(column, value, boolean)
        return self

    def or_where_null_safe_equals(self, column, value):
        return self.where_null_safe_equals(column, value, "or")

    def where_not(self, column, operator="=", value=None, boolean="and"):
        self.query.where_not(column, operator, value, boolean)
        return self

    def or_where_not(self, column, operator="=", value=None):
        return self.where_not(column, operator, value, "or")

    def where_integer_in_raw(self, column, values, boolean="and", not_in=False):
        self.query.where_integer_in_raw(column, values, boolean, not_in)
        return self

    def or_where_integer_in_raw(self, column, values):
        return self.where_integer_in_raw(column, values, "or")

    def where_integer_not_in_raw(self, column, values, boolean="and"):
        return self.where_integer_in_raw(column, values, boolean, True)

    def or_where_integer_not_in_raw(self, column, values):
        return self.where_integer_not_in_raw(column, values, "or")

    def where_exists(self, callback_or_query, boolean="and", not_exists=False):
        self.query.where_exists(callback_or_query, boolean, not_exists)
        return self

    def or_where_exists(self, callback_or_query, not_exists=False):
        return self.where_exists(callback_or_query, "or", not_exists)

    def where_not_exists(self, callback_or_query, boolean="and"):
        return self.where_exists(callback_or_query, boolean, True)

    def or_where_not_exists(self, callback_or_query):
        return self.where_exists(callback_or_query, "or", True)

    def where_like(
        self, column, value, case_sensitive=False, boolean="and", not_like=False
    ):
        self.query.where_like(column, value, case_sensitive, boolean, not_like)
        return self

    def or_where_like(self, column, value, case_sensitive=False):
        return self.where_like(column, value, case_sensitive, "or")

    def where_not_like(self, column, value, case_sensitive=False, boolean="and"):
        return self.where_like(column, value, case_sensitive, boolean, True)

    def or_where_not_like(self, column, value, case_sensitive=False):
        return self.where_not_like(column, value, case_sensitive, "or")

    def where_all(self, columns, operator="=", value=None):
        self.query.where_all(columns, operator, value)
        return self

    def or_where_all(self, columns, operator="=", value=None):
        self.query.or_where_all(columns, operator, value)
        return self

    def where_any(self, columns, operator="=", value=None):
        self.query.where_any(columns, operator, value)
        return self

    def or_where_any(self, columns, operator="=", value=None):
        self.query.or_where_any(columns, operator, value)
        return self

    def where_none(self, columns, operator="=", value=None):
        self.query.where_none(columns, operator, value)
        return self

    def or_where_none(self, columns, operator="=", value=None):
        self.query.or_where_none(columns, operator, value)
        return self

    def chunk(self, count: int, callback):
        return self.query.chunk(
            count,
            lambda rows, page: callback(
                [self.model_class(row, exists=True) for row in rows], page
            ),
        )

    def each(self, callback, count: int = 1000):
        return self.chunk(
            count,
            lambda rows, _page: all(
                callback(user, index) is not False for index, user in enumerate(rows)
            ),
        )

    def cursor(self):
        for row in self.query.cursor():
            yield self.model_class(row, exists=True)

    def with_(self, *relations: str | list[str]) -> Self:
        if len(relations) == 1 and isinstance(relations[0], (list, tuple)):
            relations = tuple(relations[0])
        self._with_relations.extend(str(relation) for relation in relations)
        return self

    def where_has(
        self,
        relation: str,
        callback: Callable[["Builder"], "Builder"] | None = None,
    ) -> Self:
        self._where_has_relations.append((relation, callback))
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

    def _relation_for(self, model, name):
        relation_method = getattr(model, name)
        return relation_method()

    def _apply_where_has(self, models):
        for relation_name, callback in self._where_has_relations:
            prototype = self.model_class({}, exists=False)
            relation = self._relation_for(prototype, relation_name)
            related_builder = relation.query.model_class.query()
            if callback is not None:
                callback(related_builder)
            matching = related_builder.get()
            if hasattr(relation, "owner_key"):
                allowed = {getattr(item, relation.owner_key) for item in matching}
                models = [
                    model
                    for model in models
                    if getattr(model, relation.foreign_key, None) in allowed
                ]
            else:
                allowed = {
                    getattr(item, relation.foreign_key, None) for item in matching
                }
                models = [
                    model
                    for model in models
                    if getattr(model, relation.local_key, None) in allowed
                ]
        return models

    def _eager_load_path(self, models, path):
        if not models or not path:
            return
        relation_name = path[0]
        relation = self._relation_for(models[0], relation_name)
        related_class = relation.query.model_class
        if hasattr(relation, "owner_key"):
            keys = {getattr(model, relation.foreign_key, None) for model in models}
            related = related_class.query().where_in(relation.owner_key, keys).get()
            by_key = {getattr(item, relation.owner_key): item for item in related}
            related_models = []
            for model in models:
                item = by_key.get(getattr(model, relation.foreign_key, None))
                model._relations[relation_name] = item
                if item is not None:
                    related_models.append(item)
        else:
            keys = {getattr(model, relation.local_key, None) for model in models}
            related = related_class.query().where_in(relation.foreign_key, keys).get()
            grouped = {key: [] for key in keys}
            for item in related:
                grouped.setdefault(
                    getattr(item, relation.foreign_key, None), []
                ).append(item)
            related_models = []
            for model in models:
                items = grouped.get(getattr(model, relation.local_key, None), [])
                model._relations[relation_name] = items
                related_models.extend(items)
        self._eager_load_path(related_models, path[1:])

    def _eager_load(self, models):
        for relation in self._with_relations:
            self._eager_load_path(models, relation.split("."))

    # ---- Read operations ----

    def get(self):
        models = [self.model_class(record, exists=True) for record in self.query.get()]
        models = self._apply_where_has(models)
        self._eager_load(models)
        return models

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

    def create_quietly(self, attributes):
        return self.model_class.create_quietly(attributes)

    def force_create(self, attributes):
        return self.model_class.force_create(attributes)

    def force_create_quietly(self, attributes):
        return self.model_class.force_create_quietly(attributes)

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
