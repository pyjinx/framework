class MethodNotAllowedException(Exception):
    status_code = 405

    def __init__(self, path, allowed_methods):
        allowed = ", ".join(sorted(set(allowed_methods)))
        super().__init__(
            f"The method is not allowed for {path}. Allowed methods: {allowed}."
        )
        self.path = path
        self.allowed_methods = sorted(set(allowed_methods))
        self.headers = {"Allow": allowed}
