import re

from Illuminate.Contracts.Http.Request import Request
from Illuminate.Exceptions.MethodNotAllowedException import MethodNotAllowedException
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Routing.Route import Route


class RouteCollection:
    def __init__(self) -> None:
        self.routes = {}
        self.all_routes = {}

    def add(self, route: Route) -> None:
        for method in route.methods:
            method_wise_routes = self.routes.setdefault(method, {})
            method_wise_routes[route.uri] = route
        self.all_routes[(tuple(route.methods), route.uri)] = route
    def match(self, request: Request):
        method_routes = [
            route
            for route in self.routes.get(request.get_method(), {}).values()
        ]
        route = self._match_against_routes(request, method_routes)
        if route:
            return route.bind(request)

        path_routes = [
            route
            for route in self.all_routes.values()
            if self.__run_match(request, route)
        ]
        if path_routes:
            allowed_methods = [
                method
                for route in path_routes
                for method in route.methods
            ]
            raise MethodNotAllowedException(
                request.get_url(),
                allowed_methods,
            )

        raise RouteNotFoundException(
            f"The route {request.get_url()} could not be found."
        )

    def _match_against_routes(self, request: Request, routes: list[Route]):
        matched_routes = []

        for route in routes:
            matched = self.__run_match(request, route)

            if matched:
                matched_routes.append(matched)

        return matched_routes[0] if matched_routes else None

    def _handle_matched_route(self, request: Request, route: Route | None):
        if route:
            return route.bind(request)

        raise RouteNotFoundException(
            f"The route {request.get_url()} could not be found."
        )

    def __run_match(self, request: Request, route: Route):
        request_path = request.get_url().strip("/")

        route_uri = route.uri.strip("/")

        matches = re.findall(r":(\w+)|\{(\w+)\}", route.uri)
        params = [colon_name or brace_name for colon_name, brace_name in matches]

        if not params:
            return route if route_uri == request_path else None

        pattern = re.sub(r":(\w+)|\{(\w+)\}", r"([^/]+)", route_uri)

        pattern = f"^{pattern}$"

        match = re.match(pattern, request_path)

        if match:
            route_params = dict(zip(params, match.groups()))

            return route.set_route_params(route_params).set_query_params(request)
        else:
            return None
