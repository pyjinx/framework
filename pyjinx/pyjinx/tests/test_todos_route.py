from pathlib import Path
import sys


def _seed_path():
    current = Path(__file__).resolve()

    # Add the nearest framework/Illuminate source root.
    for _ in range(8):
        if (current / "Illuminate").exists():
            if str(current) not in sys.path:
                sys.path.insert(0, str(current))
            break

        current = current.parent

    # Keep the project template root for route/bootstrap import.
    template_root = Path(__file__).resolve().parents[1]
    if str(template_root) not in sys.path:
        sys.path.insert(0, str(template_root))


class _FakeRequestAdapter:
    def __init__(self, path: str, method: str = "POST") -> None:
        self._path = path
        self._method = method

    def get_host(self):
        return "http://localhost"

    def get_url(self):
        return self._path

    def get_full_url(self):
        return self._path

    def get_method(self):
        return self._method

    def get_user(self):
        return None

    def query_data(self):
        return {}

    def post_data(self):
        return {}

    def form_data(self):
        return {}

    def json_data(self):
        return {}

    def files_data(self):
        return {}

    def headers_data(self):
        return {}

    def sessions_data(self):
        return {}

    def cookies_data(self):
        return {}


def test_post_todos_returns_demo_list():
    _seed_path()

    from bootstrap.app import create_app

    app = create_app()

    from Illuminate.Http.Request import Request

    request = Request.create_from(app, _FakeRequestAdapter("/todos", "POST"))
    response = app.make("router").dispatch(request)

    assert response == [
        {"id": 1, "title": "Write first route", "done": True},
        {"id": 2, "title": "Register controller action", "done": True},
        {"id": 3, "title": "Render API response", "done": False},
    ]
