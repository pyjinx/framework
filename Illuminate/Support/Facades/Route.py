from typing import TYPE_CHECKING, Any

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.Routing.Router import Router


class Route(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "router"

    if TYPE_CHECKING:

        @classmethod
        def get(cls, uri: str, action: Any) -> "Router": ...

        @classmethod
        def post(cls, uri: str, action: Any) -> "Router": ...

        @classmethod
        def put(cls, uri: str, action: Any) -> "Router": ...

        @classmethod
        def patch(cls, uri: str, action: Any) -> "Router": ...

        @classmethod
        def delete(cls, uri: str, action: Any) -> "Router": ...

        @classmethod
        def group(cls, attributes: dict, route_resolver: Any) -> "Router": ...

        @classmethod
        def resource(cls, name: str, controller: Any, options: dict | None = None) -> "Router": ...

        @classmethod
        def api_resource(cls, name: str, controller: Any, options: dict | None = None) -> "Router": ...
