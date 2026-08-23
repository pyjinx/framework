# Getting Started with PyJinx

This guide creates a PyJinx project, defines one web route, and renders the
first response in a browser. It follows the Laravel-style command boundary:
`pyjinx` creates projects; `loom` runs inside a project.

## 1) Install the CLI and create an application

Install the global project creator with uv:

```bash
uv tool install --upgrade pyjinx-installer
```

Create a project from anywhere. Replace `hello-world` with your project name:

```bash
pyjinx new hello-world
cd hello-world
uv sync
source .venv/bin/activate
loom serve
```

`uv sync` creates the project-local `.venv` when it does not exist. On Windows
PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

The development server is available at <http://localhost:8000>.

## 2) Define the web route

The generated starter keeps the route file explicit:

```python
# routes/web.py
from Illuminate.Support.Facades.Route import Route

from app.Http.Controllers.HomeController import HomeController


Route.get("/", [HomeController, "index"]).name("home").middleware("web")
```

## 3) Add the controller

The controller returns the starter welcome view:

```python
# app/Http/Controllers/HomeController.py
from Illuminate.Http.Request import Request
from Illuminate.Support.Facades.View import View
from Illuminate.controller import Controller


class HomeController(Controller):
    def index(self, request: Request):
        return View.make("welcome")
```

## 4) View the response in your browser

With `loom serve` running, open <http://localhost:8000/>. The browser renders
the starter welcome page titled **“PyJinx — Laravel-shaped Python framework”**.
Customize the response in `resources/views/welcome.html`.

For project-local command contracts, see the [CLI reference](../CLI_REFERENCE.md).
