class Attribute:
    """Accessor/mutator value object matching Laravel's Attribute class."""

    def __init__(self, get=None, set=None):
        self.get = get
        self.set = set
        self.with_caching = False
        self.with_object_caching = True

    @classmethod
    def make(cls, get=None, set=None):
        return cls(get, set)

    @classmethod
    def get(cls, callback):
        return cls(get=callback)

    @classmethod
    def set(cls, callback):
        return cls(set=callback)

    def without_object_caching(self):
        self.with_object_caching = False
        return self

    def should_cache(self):
        self.with_caching = True
        return self
