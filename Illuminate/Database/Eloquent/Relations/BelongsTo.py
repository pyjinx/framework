from Illuminate.Database.Eloquent.Relations.Relation import Relation


class BelongsTo(Relation):
    def __init__(self, query, parent, foreign_key, owner_key, relation_name):
        self.foreign_key = foreign_key
        self.owner_key = owner_key
        self.relation_name = relation_name
        super().__init__(query, parent)

    def add_constraints(self):
        """Set the base constraints on the relation query."""
        # For a BelongsTo relation, we look for the related model whose owner_key
        # matches the parent's foreign_key value.
        # Example: Post belongs to User. Post (parent) has user_id (foreign_key).
        # User (related) has id (owner_key).
        if self.parent._exists:
            foreign_value = getattr(self.parent, self.foreign_key, None)
            self.query.where(self.owner_key, "=", foreign_value)
        else:
            self.query.where(self.owner_key, "=", None)

    def get_results(self):
        if getattr(self.parent, self.foreign_key, None) is None:
            return None
        return self.query.first()

    def associate(self, model):
        """Associate the model instance to the given parent."""
        owner_key_value = getattr(model, self.owner_key)
        setattr(self.parent, self.foreign_key, owner_key_value)
        self.parent._relations[self.relation_name] = model
        return self.parent

    def dissociate(self):
        """Dissociate previously associated model from the given parent."""
        setattr(self.parent, self.foreign_key, None)
        self.parent._relations[self.relation_name] = None
        return self.parent
