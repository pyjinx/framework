# Getting Started with PyJinx

This guide shows how to boot a PyJinx application from your package and start handling requests.

> Status note
>
> PyJinx currently exposes core runtime components and route/DI/validation/CLI scaffolding. This guide reflects the intended public API for stable development.

## 1) Install and initialize the framework

Install dependencies (Poetry):

```bash
poetry install
```

Create an application bootstrap file (example: `bootstrap/app.py`):

```python
from pathlib import Path
from Illuminate.Foundation.Application import Application

app = (
    Application.configure(base_path=Path(__file__).resolve().parent.parent)
    .with_routing()
    .with_middleware()
    .with_exceptions()
    .create()
)
```

`Application.configure(...).create()` returns the central `Application` instance.

## 2) Register routes

Use the application router service:

```python
from Illuminate.Foundation.Application import Application
from your_app.controllers.HomeController import HomeController

# from your bootstrap
router = app.make("router")

router.get("/", [HomeController, "index"])  # controller@method style
router.post("/users", [UserController, "store"])
router.get("/health", lambda request: {"status": "ok"})
```

## 3) Serve a request

PyJinx currently runs through the HTTP kernel in WSGI compatibility flow:

```python
from Illuminate.Http.WSGIServer import WSGIServer
from Illuminate.Http.Request import Request


def wsgi_app(environ, start_response):
    # create compatibility server object for this request
    WSGIServer.create_server(environ, start_response)

    # capture framework request object
    request = Request.capture(app)

    response = app.handle_request(request)

    start_response(response.get_status_code(), response.get_headers())
    return [response.get_content().encode("utf-8")]
```

## 4) CLI entrypoint

The intended CLI command is `pilot` (or `python -m pyjinx` fallback). See [CLI docs](./cli.md).

## 5) Starter workflow for first success path

1. Configure routes
2. Register request/response handlers
3. Add validation to inputs
4. Add migrations and run DB commands via CLI
5. Add functional test for route + response

For the required command set, see [CLI reference](../CLI_REFERENCE.md).

## 6) Next

- [Application bootstrap and lifecycle](./application.md)
- [Routing details](./routing.md)
- [Validation](./validation.md)
- [CLI reference](../CLI_REFERENCE.md)