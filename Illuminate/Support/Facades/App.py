from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class App(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "app"

    if TYPE_CHECKING:

        @classmethod
        def make(cls, abstract: Any, parameters: dict | None = None) -> Any: ...

        @classmethod
        def bound(cls, abstract: Any) -> bool: ...

        @classmethod
        def base_path(cls, path: str = "") -> Any: ...
