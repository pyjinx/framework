class Relation:
    def __init__(self, query, parent):
        self.query = query
        self.parent = parent
        self.related = query.model_class
        self.add_constraints()

    def add_constraints(self):
        """Set the base constraints on the relation query."""
        raise NotImplementedError

    def get_results(self):
        """Get the results of the relationship."""
        raise NotImplementedError

    def get(self):
        """Execute the query as a "select" statement."""
        return self.query.get()


    def __getattr__(self, name):
        """Forward missing methods to the query builder."""
        return getattr(self.query, name)
    def match(self, models, results, relation):
        """Match the eagerly loaded results to their parents."""
        raise NotImplementedError
