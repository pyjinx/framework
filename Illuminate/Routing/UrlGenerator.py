import re
from urllib.parse import urlencode

from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from Illuminate.Routing.RouteCollection import RouteCollection


class UrlGenerator:
    def __init__(
        self, routes: RouteCollection, request, asset_root: str | None
    ) -> None:
        self._routes = routes
        self._asset_root = asset_root or ""
        self._request = None
        self.set_request(request)

    def set_request(self, request):
        self._request = request
        return self

    def route(self, name: str, parameters=None, absolute: bool = True):
        parameters = dict(parameters or {})
        route = next(
            (
                route
                for route in self._routes.all_routes.values()
                if route.get_name() == name
            ),
            None,
        )
        if route is None:
            raise RouteNotFoundException(f"Route [{name}] not found.")

        uri = route.uri
        used = set()

        def replace(match):
            key = match.group(1) or match.group(2)
            if key not in parameters:
                raise ValueError(f"Missing route parameter: {key}")
            used.add(key)
            return str(parameters[key])

        uri = re.sub(r":(\w+)|\{(\w+)\}", replace, uri)
        query = {key: value for key, value in parameters.items() if key not in used}
        if query:
            uri = f"{uri}?{urlencode(query)}"

        if not absolute:
            return f"/{uri.strip('/')}"

        root = self._asset_root.rstrip("/")
        if not root and self._request is not None:
            root = self._request.get_host().rstrip("/")
        return f"{root}/{uri.strip('/')}"
