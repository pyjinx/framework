from datetime import datetime, timezone


class SoftDeletes:
    """Laravel-style soft deleting mixin.

    Apply alongside Model (`class Post(SoftDeletes, Model)`) to keep deleted
    rows in the table behind a nullable timestamp column instead of removing
    them. Mirrors Laravel's SoftDeletes trait surface:

    - ``delete()`` stamps ``DELETED_AT`` instead of removing the row.
    - Default queries exclude trashed records.
    - ``trashed()``, ``restore()``, ``force_delete()`` manage lifecycle.
    - Builder scopes: ``with_trashed()``, ``only_trashed()``, ``without_trashed()``.
    """

    DELETED_AT = "deleted_at"

    def trashed(self):
        """Determine if the model instance has been soft deleted."""
        return self._attributes.get(self.DELETED_AT) is not None

    def restore(self):
        """Restore a soft-deleted model instance."""
        if not self._exists:
            return False
        if not self._fire_event("restoring"):
            return False

        updates = {self.DELETED_AT: None}
        if self.timestamps:
            updates["updated_at"] = datetime.now(timezone.utc).replace(tzinfo=None)

        identifier = self._attributes[self.primary_key]
        self._query_builder().where(self.primary_key, identifier).update(updates)

        self._attributes.update(updates)
        self._original = dict(self._attributes)
        self._fire_event("restored", halt=False)
        return True

    def force_delete(self):
        """Force a hard delete on a soft-deleted model."""
        if not self._exists:
            return False
        if not self._fire_event("deleting"):
            return False

        identifier = self._attributes[self.primary_key]
        deleted = self._query_builder().where(self.primary_key, identifier).delete()

        self._exists = False
        self._fire_event("deleted", halt=False)
        return deleted > 0

    @classmethod
    def restoring(cls, callback):
        return cls.on("restoring", callback)

    @classmethod
    def restored(cls, callback):
        return cls.on("restored", callback)
