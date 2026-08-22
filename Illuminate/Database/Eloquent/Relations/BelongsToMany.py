from datetime import datetime, timezone

from Illuminate.Database.Eloquent.Relations.Pivot import Pivot
from Illuminate.Database.Eloquent.Relations.Relation import Relation
from Illuminate.Support.Facades.DB import DB


class BelongsToMany(Relation):
    """Laravel-compatible many-to-many relationship core.

    The implementation follows Laravel's BelongsToMany and
    InteractsWithPivotTable behavior for joining, pivot hydration, attach,
    detach, sync, toggle, and pivot timestamp handling.
    """

    def __init__(
        self,
        query,
        parent,
        table,
        foreign_pivot_key,
        related_pivot_key,
        parent_key,
        related_key,
        relation_name=None,
    ):
        self.parent_key = parent_key
        self.related_key = related_key
        self.relation_name = relation_name
        self.foreign_pivot_key = foreign_pivot_key
        self.related_pivot_key = related_pivot_key
        self.table = table
        self.pivot_columns = []
        self.pivot_created_at = None
        self.pivot_updated_at = None
        self.pivot_values = {}
        self.accessor = "pivot"
        super().__init__(query, parent)

    def add_constraints(self):
        self.perform_join()
        if self.parent._exists:
            self.add_where_constraints()
        else:
            self.query.where(f"{self.table}.{self.foreign_pivot_key}", None)

    def perform_join(self):
        self.query.join(
            self.table,
            f"{self.table}.{self.related_pivot_key}",
            "=",
            f"{self.related.table}.{self.related_key}",
        )
        for column in (
            self.foreign_pivot_key,
            self.related_pivot_key,
            *self.pivot_columns,
        ):
            self.query.add_select_aliased(f"{self.table}.{column}", f"pivot_{column}")
        return self

    def add_where_constraints(self):
        self.query.where(
            f"{self.table}.{self.foreign_pivot_key}",
            "=",
            self.parent._attributes.get(self.parent_key),
        )
        return self

    def get_results(self):
        if not self.parent._exists:
            return []
        return self.get()

    def get(self):
        models = self.query.get()
        self._hydrate_pivot_relation(models)
        return models

    def first(self):
        model = self.query.first()
        if model is None:
            return None
        return self._hydrate_pivot_relation([model])[0]

    def _hydrate_pivot_relation(self, models):
        for model in models:
            attributes = {}
            for key in list(model._attributes):
                if key.startswith("pivot_"):
                    attributes[key[6:]] = model._attributes.pop(key)
            model._relations[self.accessor] = Pivot(
                self.table, attributes=attributes, exists=True
            )
        return models

    def as_(self, accessor):
        self.accessor = accessor
        return self

    def with_pivot(self, *columns):
        self.pivot_columns.extend(columns)
        for column in columns:
            self.query.add_select_aliased(f"{self.table}.{column}", f"pivot_{column}")
        return self

    def with_timestamps(self, created_at=None, updated_at=None):
        self.pivot_created_at = (
            created_at if created_at is not False else None
        ) or "created_at"
        self.pivot_updated_at = (
            updated_at if updated_at is not False else None
        ) or "updated_at"
        columns = [
            column
            for column in (self.pivot_created_at, self.pivot_updated_at)
            if column and column not in self.pivot_columns
        ]
        return self.with_pivot(*columns)

    def where_pivot(self, column, operator="=", value=None):
        self.query.where(self._qualify_pivot(column), operator, value)
        return self

    def order_by_pivot(self, column, direction="asc"):
        self.query.order_by(self._qualify_pivot(column), direction)
        return self

    def _qualify_pivot(self, column):
        return column if "." in column else f"{self.table}.{column}"

    def all_related_ids(self):
        return self._new_pivot_query().pluck(self.related_pivot_key)

    def _new_pivot_query(self):
        return self._new_pivot_statement().where(
            self.foreign_pivot_key,
            "=",
            self.parent._attributes.get(self.parent_key),
        )

    def _new_pivot_statement(self):
        return DB.table(self.table)

    def _parse_ids(self, value):
        if isinstance(value, self.related):
            return {getattr(value, self.related_key): {}}
        if isinstance(value, dict):
            result = {}
            for key, attributes in value.items():
                identifier = (
                    getattr(key, self.related_key)
                    if isinstance(key, self.related)
                    else key
                )
                result[identifier] = dict(attributes or {})
            return result
        if isinstance(value, (list, tuple, set)):
            result = {}
            for item in value:
                identifier = (
                    getattr(item, self.related_key)
                    if isinstance(item, self.related)
                    else item
                )
                result[identifier] = {}
            return result
        return {value: {}}

    def _base_attach_record(self, identifier, attributes):
        record = {
            self.related_pivot_key: identifier,
            self.foreign_pivot_key: self.parent._attributes.get(self.parent_key),
        }
        record.update(self.pivot_values)
        record.update(attributes)
        if self.pivot_created_at or self.pivot_updated_at:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            if self.pivot_created_at:
                record.setdefault(self.pivot_created_at, now)
            if self.pivot_updated_at:
                record.setdefault(self.pivot_updated_at, now)
        return record

    def attach(self, ids, attributes=None, touch=True):
        records = self._parse_ids(ids)
        shared = dict(attributes or {})
        rows = [
            self._base_attach_record(identifier, {**shared, **values})
            for identifier, values in records.items()
        ]
        if rows:
            self._new_pivot_statement().insert(rows)
        return None

    def detach(self, ids=None, touch=True):
        query = self._new_pivot_query()
        if ids is not None:
            identifiers = list(self._parse_ids(ids))
            if not identifiers:
                return 0
            query.where_in(self.related_pivot_key, identifiers)
        return query.delete()

    def sync(self, ids, detaching=True):
        records = self._parse_ids(ids)
        current = self.all_related_ids()
        current_set = set(current)
        requested_set = set(records)
        detached = list(current_set - requested_set) if detaching else []
        if detached:
            self.detach(detached, touch=False)

        attached = []
        updated = []
        for identifier, attributes in records.items():
            if identifier not in current_set:
                self.attach(identifier, attributes, touch=False)
                attached.append(identifier)
            elif attributes:
                changed = (
                    self._new_pivot_query()
                    .where(self.related_pivot_key, "=", identifier)
                    .update(attributes)
                )
                if changed:
                    updated.append(identifier)

        return {
            "attached": attached,
            "detached": detached,
            "updated": updated,
        }

    def sync_without_detaching(self, ids):
        return self.sync(ids, detaching=False)

    def toggle(self, ids, touch=True):
        records = self._parse_ids(ids)
        current = set(self.all_related_ids())
        attached = []
        detached = []
        for identifier in records:
            if identifier in current:
                self.detach(identifier, touch=False)
                detached.append(identifier)
            else:
                self.attach(identifier, records[identifier], touch=False)
                attached.append(identifier)
        return {"attached": attached, "detached": detached, "updated": []}
