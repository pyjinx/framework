class Builder:
    def __init__(self, model_class):
        self.model_class = model_class
        self.query = model_class._query_builder()

    # ---- Where clauses ----

    def where(self, column, operator="=", value=None):
        self.query.where(column, operator, value)
        return self

    def or_where(self, column, operator="=", value=None):
        self.query.or_where(column, operator, value)
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

    # ---- Read operations ----

    def get(self):
        return [
            self.model_class(record, exists=True)
            for record in self.query.get()
        ]

    def first(self):
        record = self.query.first()
        return self.model_class(record, exists=True) if record else None

    def first_or_fail(self):
        instance = self.first()
        if instance is None:
            raise LookupError(
                f"{self.model_class.__name__} was not found."
            )
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

    def increment(self, column, amount=1, extra=None):
        return self.query.increment(column, amount, extra)

    def decrement(self, column, amount=1, extra=None):
        return self.query.decrement(column, amount, extra)

    def update(self, values):
        return self.query.update(values)

    def delete(self):
        return self.query.delete()
