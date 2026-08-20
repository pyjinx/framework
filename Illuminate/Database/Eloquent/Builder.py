class Builder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = model_class._query_builder()

    def where(self, column, operator="=", value=None):
        self.query.where(column, operator, value)
        return self

    def get(self):
        return [
            self.model_class(record, exists=True)
            for record in self.query.get()
        ]

    def first(self):
        record = self.query.first()
        return self.model_class(record, exists=True) if record else None

    def create(self, attributes):
        return self.model_class.create(attributes)
