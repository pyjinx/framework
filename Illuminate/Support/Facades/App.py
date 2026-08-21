from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade


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
