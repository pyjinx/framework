from app.http.controllers.TodoController import TodoController


def register_routes(app):
    """Register HTTP routes for the starter app."""

    router = app.make("router")
    router.post("/todos", [TodoController, "index"])
