class ModelNotFoundException(LookupError):
    """Raised when implicit route binding cannot resolve a model."""

    def __init__(self, model, identifier):
        self.model = model
        self.identifiers = [identifier]
        super().__init__(
            f"No query results for model [{model.__name__}] [{identifier}]."
        )
