from pathlib import Path
from types import ModuleType
from typing import Callable
import importlib.util
import sys


def _ensure_dependency(name: str, install: Callable[[], ModuleType]):
    if name in sys.modules:
        return

    if importlib.util.find_spec(name):
        return

    sys.modules[name] = install()


def _install_colorama() -> ModuleType:
    colorama = ModuleType("colorama")

    class _Colors:
        def __getattr__(self, _name: str) -> str:  # pragma: no cover - fallback
            return ""

    colorama.Fore = _Colors()
    colorama.Back = _Colors()
    colorama.Style = _Colors()
    colorama.init = lambda *args, **kwargs: None

    return colorama


def _install_dotenv() -> ModuleType:
    dotenv = ModuleType("dotenv")

    def load_dotenv(*args, **kwargs) -> bool:
        return False

    dotenv.load_dotenv = load_dotenv
    return dotenv


def _install_pluralizer() -> ModuleType:
    pluralizer = ModuleType("pluralizer")

    class Pluralizer:
        def plural(self, value: str) -> str:
            if not value:
                return value

            if value.endswith("s"):
                return value
            if value.endswith("y"):
                return f"{value[:-1]}ies"
            if value.endswith("fe"):
                return f"{value[:-2]}ves"

            return f"{value}s"

        def singular(self, value: str) -> str:
            if not value:
                return value

            if value.endswith("ies"):
                return f"{value[:-3]}y"
            if value.endswith("ves"):
                return f"{value[:-3]}f"
            if value.endswith("s") and len(value) > 1:
                return value[:-1]

            return value

    pluralizer.Pluralizer = Pluralizer
    return pluralizer


def _find_framework_root(start: Path) -> Path:
    current = start.resolve()

    for _ in range(8):
        if (current / "Illuminate").exists():
            return current

        current = current.parent

    raise ModuleNotFoundError(
        "Cannot locate framework source root with Illuminate package from template path"
    )


def create_app(base_path: str | Path | None = None):
    """Create and configure a minimal PoC app instance.

    This mirrors a Laravel-like bootstrap shape while staying lightweight for now:
    base app + route registration.
    """

    _ensure_dependency("colorama", _install_colorama)
    _ensure_dependency("dotenv", _install_dotenv)
    _ensure_dependency("pluralizer", _install_pluralizer)

    template_root = Path(__file__).resolve().parent.parent
    project_root = Path(base_path) if base_path else template_root
    project_root = project_root.resolve()
    framework_root = _find_framework_root(project_root)

    # Keep local module imports stable when this script runs outside the project dir.
    # Also expose the framework source path when running from this repo directly.
    for path in (project_root, framework_root):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))

    from Illuminate.Foundation.Application import Application
    from routes.web import register_routes

    app = (
        Application.configure(base_path=str(project_root))
        .with_routing()
        .with_middleware()
        .with_exceptions()
        .create()
    )

    register_routes(app)

    return app
