from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Config.Repository import Repository


class Config(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "config"

    if TYPE_CHECKING:

        @classmethod
        def get(cls, key: str, default: Any = None) -> Any: ...

        @classmethod
        def has(cls, key: str) -> bool: ...

        @classmethod
        def set(cls, key: str, value: Any) -> "Repository": ...

        @classmethod
        def get_all(cls) -> dict: ...
