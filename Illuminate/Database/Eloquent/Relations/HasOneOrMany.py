from Illuminate.Database.Eloquent.Relations.Relation import Relation


class HasOneOrMany(Relation):
    def __init__(self, query, parent, foreign_key, local_key):
        self.foreign_key = foreign_key
        self.local_key = local_key
        super().__init__(query, parent)

    def add_constraints(self):
        """Set the base constraints on the relation query."""
        if self.parent._exists:
            local_value = getattr(self.parent, self.local_key, None)
            self.query.where(self.foreign_key, "=", local_value)
        else:
            self.query.where(self.foreign_key, "=", None)

    def save(self, model):
        """Attach a model instance to the parent model."""
        setattr(model, self.foreign_key, self.get_parent_key())
        return model.save()

    def create(self, attributes):
        """Create a new instance of the related model."""
        attributes = dict(attributes)
        attributes[self.foreign_key] = self.get_parent_key()
        return self.related.create(attributes)

    def get_parent_key(self):
        return getattr(self.parent, self.local_key)


class HasOne(HasOneOrMany):
    def get_results(self):
        return self.query.first()


class HasMany(HasOneOrMany):
    def get_results(self):
        return self.query.get()
