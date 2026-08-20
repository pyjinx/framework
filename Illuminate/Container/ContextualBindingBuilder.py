class ContextualBindingBuilder:
    def __init__(self, container, concrete):
        self.container = container
        self.concrete = concrete
        self.needs_abstract = None

    def needs(self, abstract):
        self.needs_abstract = abstract
        return self

    def give(self, implementation):
        if self.needs_abstract is None:
            raise ValueError("needs() must be called before give()")

        self.container.add_contextual_binding(
            self.concrete,
            self.needs_abstract,
            implementation,
        )
        return self
