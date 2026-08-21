from typing import Any, Self

from Illuminate.Contracts.Http.Request import Request
from Illuminate.Helpers.Util import Util
from Illuminate.Routing.Controllers.HasMiddleware import Middleware


class Route:
    def __init__(
        self,
        methods,
        uri,
        action,
    ) -> None:
        self.methods = methods

        self.uri = uri

        self.action = action

        self.__computed_middleware = None

        self.__route_params: dict = {}

        self.__query_params: dict = {}

        self.__router = None

        self.__application = None

    @property
    def computed_middleware(self):
        return self.__computed_middleware

    @property
    def route_params(self):
        return self.__route_params

    @property
    def query_params(self):
        return self.__query_params

    @property
    def router(self):
        return self.__router

    @property
    def application(self):
        return self.__application

    def set_router(self, router) -> Self:
        self.__router = router

        return self

    def set_application(self, application) -> Self:
        self.__application = application

        return self

    def set_action(self, action: list[Any]) -> None:
        self.action = action

    def get_action(self) -> list[Any]:
        return self.action

    def bind(self, request: Request) -> Self:
        self.request = request

        return self

    def get_name(self):
        return self.action.get("as")

    def name(self, name: str):
        alias = self.action.get("as", "")
        self.action["as"] = f"{alias}{name}" if alias else name
        return self

    def run(self):
        try:
            controller = self.action.get("controller")

            if controller:
                action = self.__run_controller(controller)
            else:
                action = self.__run_callable()

            if not action:
                raise Exception("Invalid route action")

            dependencies = self.application.get_dependencies(action)

            return Util.callback_with_dynamic_args(action, dependencies)
        except Exception as e:
            raise e

    def __run_controller(self, controller):
        controller_object = self.application.make(controller)

        return getattr(controller_object, self.action["uses"])

    def __run_callable(self):
        return self.action["uses"]

    def gather_middleware(self):
        try:
            if not self.__computed_middleware:
                self.__computed_middleware = (
                    self.middleware() + self.controller_middleware()
                )

            return self.__computed_middleware
        except Exception as e:
            raise e

    def middleware(self, middleware=None):
        current_middleware = self.action.get("middleware", [])

        if middleware is None:
            return current_middleware

        if isinstance(middleware, str):
            middleware = [middleware]

        if isinstance(middleware, list):
            self.action["middleware"] = current_middleware + middleware
            return self

        raise Exception("Invalid middleware")

    def controller_middleware(self):
        controller = self.action.get("controller")

        uses = self.action.get("uses")

        middleware_method = getattr(controller, "middleware", list)

        middleware = [
            (
                middleware
                if isinstance(middleware, Middleware)
                else Middleware(middleware)
            )
            for middleware in middleware_method()
        ]

        return [middleware.name for middleware in middleware if middleware.filter(uses)]

    def set_query_params(self, request: Request) -> Self:
        self.__query_params = request.query()

        return self

    def set_route_params(self, route_params: dict[str, Any]) -> Self:
        self.__route_params = route_params

        return self
