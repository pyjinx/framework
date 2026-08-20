from datetime import datetime

from Illuminate.Support.Facades.DB import DB


class Model:
    table = None
    primary_key = "id"
    timestamps = True
    fillable = []
    guarded = ["*"]
    hidden = []

    def __init__(self, attributes=None, exists=False):
        self._attributes = dict(attributes or {})
        self._exists = exists
        self._original = dict(self._attributes)

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
        now = datetime.utcnow()
        if self.timestamps:
            if not self._exists:
                self._attributes.setdefault("created_at", now)
            self._attributes["updated_at"] = now

        if self._exists:
            identifier = self._attributes[self.primary_key]
            updates = {
                key: value
                for key, value in self._attributes.items()
                if key != self.primary_key
            }
            self._query_builder().where(self.primary_key, identifier).update(updates)
        else:
            identifier = self._query_builder().insert(self._attributes)
            if identifier is not None:
                self._attributes.setdefault(self.primary_key, identifier)
            self._exists = True

        self._original = dict(self._attributes)
        return self

    def update(self, attributes):
        return self.fill(attributes).save()

    def delete(self):
        if not self._exists:
            return False
        identifier = self._attributes[self.primary_key]
        deleted = self._query_builder().where(self.primary_key, identifier).delete()
        self._exists = False
        return deleted > 0

    def to_dict(self):
        return {
            key: value
            for key, value in self._attributes.items()
            if key not in self.hidden
        }

    def __getattr__(self, name):
        try:
            return self._attributes[name]
        except KeyError as error:
            raise AttributeError(name) from error
