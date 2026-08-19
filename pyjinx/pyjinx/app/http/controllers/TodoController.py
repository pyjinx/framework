class TodoController:
    def index(self):
        """Return a demo TODO list for the PoC route sample."""

        return [
            {"id": 1, "title": "Write first route", "done": True},
            {"id": 2, "title": "Register controller action", "done": True},
            {"id": 3, "title": "Render API response", "done": False},
        ]
