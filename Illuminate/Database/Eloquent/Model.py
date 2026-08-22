import inspect
import json
from datetime import datetime, timezone

from Illuminate.Database.Eloquent.Casts.Attribute import Attribute
from Illuminate.Database.Eloquent.SoftDeletes import SoftDeletes
from Illuminate.Support.Facades.DB import DB


class Model:
    table = None
    primary_key = "id"
    key_type = "int"
    incrementing = True
    timestamps = True
    fillable = []
    guarded = ["*"]
    hidden = []
    visible = []
    appends = []
    casts = {}
    _event_listeners = {}

    def __init__(self, attributes=None, exists=False):
        self._attributes = dict(attributes or {})
        self._exists = exists
        self._original = dict(self._attributes)
        self._relations = {}
        self._appends = list(self.appends)
    @classmethod
    def _listeners(cls):
        if "_event_listeners" not in cls.__dict__:
            cls._event_listeners = {}
        return cls._event_listeners

    @classmethod
    def on(cls, event, callback):
        cls._listeners().setdefault(event, []).append(callback)
        return callback

    @classmethod
    def saving(cls, callback):
        return cls.on("saving", callback)

    @classmethod
    def saved(cls, callback):
        return cls.on("saved", callback)

    @classmethod
    def creating(cls, callback):
        return cls.on("creating", callback)

    @classmethod
    def created(cls, callback):
        return cls.on("created", callback)

    @classmethod
    def updating(cls, callback):
        return cls.on("updating", callback)

    @classmethod
    def updated(cls, callback):
        return cls.on("updated", callback)

    @classmethod
    def deleting(cls, callback):
        return cls.on("deleting", callback)

    @classmethod
    def deleted(cls, callback):
        return cls.on("deleted", callback)

    def _fire_event(self, event, halt=True):
        for callback in self.__class__._listeners().get(event, []):
            if callback(self) is False and halt:
                return False
        return True

    @classmethod
    def query(cls):
        from Illuminate.Database.Eloquent.Builder import Builder

        return Builder(cls)

    @classmethod
    def _query_builder(cls):
        if not cls.table:
            raise ValueError(f"{cls.__name__} must define a table.")
        return DB.table(cls.table)

    @classmethod
    def find(cls, identifier):
        return cls.query().where(cls.primary_key, identifier).first()

    @classmethod
    def all(cls):
        return cls.query().get()

    @classmethod
    def where(cls, column, operator="=", value=None):
        return cls.query().where(column, operator, value)

    @classmethod
    def find_or_fail(cls, identifier):
        instance = cls.find(identifier)
        if instance is None:
            raise LookupError(f"{cls.__name__} [{identifier}] was not found.")
        return instance

    def get_key_name(self):
        return self.primary_key

    def set_key_name(self, key):
        self.primary_key = key
        return self

    def get_key_type(self):
        return self.key_type

    def set_key_type(self, key_type):
        self.key_type = key_type
        return self

    def get_incrementing(self):
        return self.incrementing

    def set_incrementing(self, value):
        self.incrementing = value
        return self

    def get_key(self):
        return getattr(self, self.get_key_name(), None)

    def get_route_key(self):
        route_key_name = getattr(
            type(self), "route_key_name", self.get_key_name()
        )
        return getattr(self, route_key_name, None)

    @classmethod
    def get_route_key_name(cls):
        """Return the model column used for implicit route binding."""
        return getattr(cls, "route_key_name", cls.primary_key)

    @classmethod
    def resolve_route_binding(cls, value, field=None):
        """Resolve a route parameter using the model's route key."""
        field = field or cls.get_route_key_name()
        return cls.query().where(field, value).first()

    @classmethod
    def resolve_soft_deletable_route_binding(cls, value, field=None):
        """Resolve a route parameter while including trashed models."""
        field = field or cls.get_route_key_name()
        return cls.query().with_trashed().where(field, value).first()

    def has_many(self, related_class, foreign_key=None, local_key=None):
        from Illuminate.Database.Eloquent.Relations.HasOneOrMany import HasMany

        foreign_key = foreign_key or f"{self.__class__.__name__.lower()}_id"
        local_key = local_key or self.primary_key
        query = related_class.query()
        return HasMany(query, self, foreign_key, local_key)

    def has_one(self, related_class, foreign_key=None, local_key=None):
        from Illuminate.Database.Eloquent.Relations.HasOneOrMany import HasOne

        foreign_key = foreign_key or f"{self.__class__.__name__.lower()}_id"
        local_key = local_key or self.primary_key
        query = related_class.query()
        return HasOne(query, self, foreign_key, local_key)

    def belongs_to(
        self, related_class, foreign_key=None, owner_key=None, relation_name=None
    ):
        import inspect

        from Illuminate.Database.Eloquent.Relations.BelongsTo import BelongsTo

        if not relation_name:
            # Inspect stack to find the name of the calling method
            frame = inspect.currentframe().f_back
            relation_name = frame.f_code.co_name

        foreign_key = foreign_key or f"{relation_name}_id"
        owner_key = owner_key or related_class.primary_key
        query = related_class.query()
        return BelongsTo(query, self, foreign_key, owner_key, relation_name)

    def belongs_to_many(
        self,
        related_class,
        table=None,
        foreign_pivot_key=None,
        related_pivot_key=None,
        parent_key=None,
        related_key=None,
        relation_name=None,
    ):
        """Define a Laravel-style many-to-many relationship."""
        import inspect

        from Illuminate.Database.Eloquent.Relations.BelongsToMany import (
            BelongsToMany,
        )
        from Illuminate.Support.Str import Str

        if relation_name is None:
            relation_name = inspect.currentframe().f_back.f_code.co_name

        parent_segment = Str.singular(Str.snake(self.__class__.__name__))
        related_segment = Str.singular(Str.snake(related_class.__name__))
        table = table or "_".join(sorted((parent_segment, related_segment)))
        foreign_pivot_key = foreign_pivot_key or f"{parent_segment}_id"
        related_pivot_key = related_pivot_key or f"{related_segment}_id"
        parent_key = parent_key or self.primary_key
        related_key = related_key or related_class.primary_key

        return BelongsToMany(
            related_class.query(),
            self,
            table,
            foreign_pivot_key,
            related_pivot_key,
            parent_key,
            related_key,
            relation_name,
        )

    @classmethod
    def create(cls, attributes):
        return cls().fill(attributes).save()

    def _attribute_definition(self, key):
        """Resolve an annotated Python method returning Laravel's Attribute."""
        method = getattr(type(self), key, None)
        if not callable(method):
            return None
        annotation = inspect.signature(method).return_annotation
        if annotation not in (Attribute, "Attribute"):
            return None
        definition = method(self)
        return definition if isinstance(definition, Attribute) else None

    def _set_attribute_value(self, key, value):
        definition = self._attribute_definition(key)
        if definition is not None and definition.set is not None:
            result = definition.set(value, dict(self._attributes))
            if isinstance(result, dict):
                self._attributes.update(result)
            else:
                self._attributes[key] = result
            return

        legacy_setter = getattr(self, f"set_{key}_attribute", None)
        if callable(legacy_setter):
            legacy_setter(value)
            return

        self._attributes[key] = value

    def fill(self, attributes):
        if self.fillable:
            accepted = {
                key: value for key, value in attributes.items() if key in self.fillable
            }
        elif "*" in self.guarded:
            accepted = {}
        else:
            accepted = {
                key: value
                for key, value in attributes.items()
                if key not in self.guarded
            }

        for key, value in accepted.items():
            self._set_attribute_value(key, value)
        return self

    def save(self):
        if not self._fire_event("saving"):
            return False

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        if self.timestamps:
            if not self._exists:
                self._attributes.setdefault("created_at", now)
            self._attributes["updated_at"] = now

        if self._exists:
            if not self._fire_event("updating"):
                return False
            identifier = self._attributes[self.primary_key]
            updates = {
                key: self._storage_value(key, value)
                for key, value in self._attributes.items()
                if key != self.primary_key
            }
            self._query_builder().where(self.primary_key, identifier).update(updates)
            self._fire_event("updated", halt=False)
        else:
            if not self._fire_event("creating"):
                return False
            identifier = self._query_builder().insert(self._storage_attributes())
            if identifier is not None:
                self._attributes.setdefault(self.primary_key, identifier)
            self._exists = True
            self._fire_event("created", halt=False)

        self._original = dict(self._attributes)
        self._fire_event("saved", halt=False)
        return self

    def update(self, attributes):
        return self.fill(attributes).save()

    def delete(self):
        if not self._exists:
            return False
        if not self._fire_event("deleting"):
            return False
        identifier = self._attributes[self.primary_key]

        if isinstance(self, SoftDeletes):
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            self._query_builder().where(self.primary_key, identifier).update(
                {self.DELETED_AT: now}
            )
            self._attributes[self.DELETED_AT] = now
            self._original = dict(self._attributes)
            self._fire_event("deleted", halt=False)
            return True

        deleted = self._query_builder().where(self.primary_key, identifier).delete()
        self._exists = False
        self._fire_event("deleted", halt=False)
        return deleted > 0

    def increment(self, column, amount=1, extra=None):
        if not self._exists:
            return False
        identifier = self._attributes[self.primary_key]
        self._query_builder().where(self.primary_key, identifier).increment(
            column, amount, extra
        )
        self._attributes[column] = self._attributes.get(column, 0) + amount
        if extra:
            self._attributes.update(extra)
        self._original = dict(self._attributes)
        return self

    def decrement(self, column, amount=1, extra=None):
        return self.increment(column, -amount, extra)

    def fresh(self):
        if not self._exists:
            return None
        return self.__class__.find(self._attributes[self.primary_key])

    def get_arrayable_items(self, values):
        if self.get_visible():
            values = {
                key: value
                for key, value in values.items()
                if key in self.get_visible()
            }
        if self.get_hidden():
            values = {
                key: value
                for key, value in values.items()
                if key not in self.get_hidden()
            }
        return values

    def get_arrayable_attributes(self):
        return self.get_arrayable_items(self._attributes)

    def get_arrayable_appends(self):
        if not self.get_appends():
            return {}
        return self.get_arrayable_items(
            {attribute: attribute for attribute in self.get_appends()}
        )

    def get_arrayable_relations(self):
        return self.get_arrayable_items(self._relations)

    def attributes_to_dict(self):
        attributes = {
            key: self._serialize_value(key, value)
            for key, value in self.get_arrayable_attributes().items()
        }
        for key in self.get_arrayable_appends():
            attributes[key] = self._serialize_appended_value(key)
        return attributes

    def relations_to_dict(self):
        attributes = {}
        for key, value in self.get_arrayable_relations().items():
            if value is None:
                attributes[key] = None
            elif isinstance(value, Model):
                attributes[key] = value.to_dict()
            elif isinstance(value, (list, tuple)) and all(
                isinstance(item, Model) for item in value
            ):
                attributes[key] = [item.to_dict() for item in value]
        return attributes

    def to_dict(self):
        return {**self.attributes_to_dict(), **self.relations_to_dict()}

    def _serialize_appended_value(self, key):
        raw_value = self._attributes.get(key)
        definition = self._attribute_definition(key)
        if definition is not None:
            value = (
                definition.get(raw_value, dict(self._attributes))
                if definition.get is not None
                else raw_value
            )
        else:
            legacy_getter = getattr(self, f"get_{key}_attribute", None)
            value = (
                legacy_getter(raw_value)
                if callable(legacy_getter)
                else self._cast_value(key, raw_value)
            )
        return self._serialize_value(key, value)

    def get_hidden(self):
        return list(self.hidden)

    def set_hidden(self, hidden):
        self.hidden = list(hidden or [])
        return self

    def merge_hidden(self, hidden):
        if hidden:
            self.hidden = list(dict.fromkeys([*self.hidden, *hidden]))
        return self

    def get_visible(self):
        return list(self.visible)

    def set_visible(self, visible):
        self.visible = list(visible or [])
        return self

    def merge_visible(self, visible):
        if visible:
            self.visible = list(dict.fromkeys([*self.visible, *visible]))
        return self

    def make_visible(self, attributes, *additional):
        attributes = self._attribute_names(attributes, additional)
        self.hidden = [attribute for attribute in self.hidden if attribute not in attributes]
        if self.visible:
            self.visible = list(dict.fromkeys([*self.visible, *attributes]))
        return self

    def make_visible_if(self, condition, attributes, *additional):
        return (
            self.make_visible(attributes, *additional)
            if self._condition_value(condition)
            else self
        )

    def make_hidden(self, attributes, *additional):
        attributes = self._attribute_names(attributes, additional)
        self.hidden = list(dict.fromkeys([*self.hidden, *attributes]))
        return self

    def make_hidden_if(self, condition, attributes, *additional):
        return (
            self.make_hidden(attributes, *additional)
            if self._condition_value(condition)
            else self
        )

    def append(self, attributes, *additional):
        return self.merge_appends(self._attribute_names(attributes, additional))

    def get_appends(self):
        return list(self._appends)

    def set_appends(self, appends):
        self._appends = list(appends or [])
        return self

    def merge_appends(self, appends):
        if appends:
            self._appends = list(dict.fromkeys([*self._appends, *appends]))
        return self

    def has_appended(self, attribute):
        return attribute in self.get_appends()

    def without_appends(self):
        return self.set_appends([])

    @staticmethod
    def _attribute_names(attributes, additional):
        if isinstance(attributes, (list, tuple, set)):
            return list(attributes)
        return [attributes, *additional]

    def _condition_value(self, condition):
        return condition(self) if callable(condition) else condition

    def _storage_value(self, key, value):
        cast = self.casts.get(key)
        cast_type = cast.split(":", 1)[0] if isinstance(cast, str) else cast
        if cast_type in {"array", "json", "object"} and value is not None:
            return value if isinstance(value, str) else json.dumps(value)
        return value

    def _storage_attributes(self):
        return {
            key: self._storage_value(key, value)
            for key, value in self._attributes.items()
        }

    def _serialize_value(self, key, value):
        if isinstance(value, datetime):
            return value.isoformat()
        cast = self.casts.get(key)
        cast_type = cast.split(":", 1)[0] if isinstance(cast, str) else cast
        if cast_type in {"array", "json", "object"} and isinstance(value, str):
            return json.loads(value)
        return value

    def _cast_value(self, key, value):
        cast = self.casts.get(key)
        if value is None or cast is None:
            return value
        cast_type, _, precision = (
            cast.partition(":") if isinstance(cast, str) else (cast, "", "")
        )
        if cast_type in {"datetime", "date"} and isinstance(value, str):
            parsed = datetime.fromisoformat(value)
            return parsed.date() if cast_type == "date" else parsed
        if cast_type in {"int", "integer"}:
            return int(value)
        if cast_type in {"float", "real", "double"}:
            return float(value)
        if cast_type == "decimal":
            return round(float(value), int(precision or 2))
        if cast_type in {"bool", "boolean"}:
            if isinstance(value, str):
                return value.strip().lower() not in {"", "0", "false", "off", "no"}
            return bool(value)
        if cast_type in {"array", "json", "object"} and isinstance(value, str):
            return json.loads(value)
        if cast_type == "string":
            return str(value)
        if cast_type == "timestamp":
            return int(value.timestamp()) if isinstance(value, datetime) else int(value)
        return value

    def load(self, *relations):
        """Eager load relations for the model (simplified)."""
        for relation in relations:
            self.get_relation_value(relation)
        return self

    def get_relation_value(self, key):
        if key in self._relations:
            return self._relations[key]

        # If the key corresponds to a method on the model, it's a relationship.
        method = getattr(self.__class__, key, None)
        if callable(method):
            relation = method(self)
            from Illuminate.Database.Eloquent.Relations.Relation import Relation

            if isinstance(relation, Relation):
                results = relation.get_results()
                self._relations[key] = results
                return results

    def __getattribute__(self, name):
        if not name.startswith("_"):
            definition = object.__getattribute__(self, "_attribute_definition")(name)
            if definition is not None and definition.get is not None:
                attributes = object.__getattribute__(self, "_attributes")
                return definition.get(attributes.get(name), dict(attributes))
        return super().__getattribute__(name)

    def __getattr__(self, name):
        if name in self._attributes or self._attribute_definition(name) is not None:
            definition = self._attribute_definition(name)
            raw_value = self._attributes.get(name)
            if definition is not None and definition.get is not None:
                return definition.get(raw_value, dict(self._attributes))

            legacy_getter = getattr(self, f"get_{name}_attribute", None)
            if callable(legacy_getter):
                return legacy_getter(raw_value)
            return self._cast_value(name, raw_value)

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        if name.startswith("_") or name in (
            "table",
            "primary_key",
            "key_type",
            "timestamps",
            "fillable",
            "guarded",
            "hidden",
            "visible",
            "casts",
            "DELETED_AT",
            "incrementing",
        ):
            super().__setattr__(name, value)
        else:
            self._set_attribute_value(name, value)

    def is_dirty(self, *attributes):
        if not attributes:
            return self._attributes != self._original
        return any(
            self._attributes.get(attr) != self._original.get(attr)
            for attr in attributes
        )

    def get_dirty(self):
        return {
            key: value
            for key, value in self._attributes.items()
            if self._original.get(key) != value
        }

    def get_original(self, key=None, default=None):
        if key is None:
            return dict(self._original)
        return self._original.get(key, default)
