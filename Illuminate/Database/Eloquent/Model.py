from datetime import datetime, timezone
import json

from Illuminate.Support.Facades.DB import DB


class Model:
    table = None
    primary_key = "id"
    timestamps = True
    fillable = []
    casts = {}
    _event_listeners = {}

    def __init__(self, attributes=None, exists=False):
        self._attributes = dict(attributes or {})
        self._exists = exists
        self._original = dict(self._attributes)

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
    def find_or_fail(cls, identifier):
        instance = cls.find(identifier)
        if instance is None:
            raise LookupError(f"{cls.__name__} [{identifier}] was not found.")
        return instance

    @classmethod
    def create(cls, attributes):
        return cls().fill(attributes).save()

    def fill(self, attributes):
        if self.fillable:
            accepted = {
                key: value for key, value in attributes.items() if key in self.fillable
            }
        elif "*" in self.guarded:
            accepted = {}
        else:
            accepted = {
                key: value for key, value in attributes.items() if key not in self.guarded
            }

        self._attributes.update(accepted)
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
                key: value
                for key, value in self._attributes.items()
                if key != self.primary_key
            }
            self._query_builder().where(self.primary_key, identifier).update(updates)
            self._fire_event("updated", halt=False)
        else:
            if not self._fire_event("creating"):
                return False
            identifier = self._query_builder().insert(self._attributes)
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
        deleted = self._query_builder().where(self.primary_key, identifier).delete()
        self._exists = False
        self._fire_event("deleted", halt=False)
        return deleted > 0

    def to_dict(self):
        return {
            key: self._serialize_value(key, value)
            for key, value in self._attributes.items()
            if key not in self.hidden
        }

    def _serialize_value(self, key, value):
        if isinstance(value, datetime):
            return value.isoformat()
        if self.casts.get(key) == "json" and isinstance(value, str):
            return json.loads(value)
        return value

    def _cast_value(self, key, value):
        cast = self.casts.get(key)
        if value is None or cast is None:
            return value
        if cast == "datetime" and isinstance(value, str):
            return datetime.fromisoformat(value)
        if cast in {"int", "integer"}:
            return int(value)
        if cast in {"float", "double"}:
            return float(value)
        if cast in {"bool", "boolean"}:
            return bool(value)
        if cast == "json" and isinstance(value, str):
            return json.loads(value)
        return value

    def __getattr__(self, name):
        try:
            return self._cast_value(name, self._attributes[name])
        except KeyError as error:
            raise AttributeError(name) from error
