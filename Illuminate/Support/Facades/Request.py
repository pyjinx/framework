from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Http.Request import Request as RequestObject


class Request(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "request"

    if TYPE_CHECKING:

        @classmethod
        def get_url(cls) -> str: ...

        @classmethod
        def get_method(cls) -> str: ...

        @classmethod
        def input(cls) -> dict: ...

        @classmethod
        def query(cls) -> dict: ...

        @classmethod
        def json(cls) -> dict: ...

        @classmethod
        def post(cls) -> dict: ...

        @classmethod
        def header(cls, key: str) -> Any: ...

        @classmethod
        def cookie(cls, key: str) -> Any: ...

        @classmethod
        def user(cls) -> Any: ...

        @classmethod
        def route_param(cls, name: str, default: Any = None) -> Any: ...
