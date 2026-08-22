import inspect
from typing import get_type_hints

from Illuminate.Database.Eloquent.Model import Model
from Illuminate.Database.Eloquent.ModelNotFoundException import ModelNotFoundException


class ImplicitRouteBinding:
    """Resolve route parameters from Laravel-style model type hints."""

    @staticmethod
    def resolve_for_route(route, action):
        parameters = dict(route.route_params or {})
        try:
            type_hints = get_type_hints(action)
        except (NameError, TypeError):
            type_hints = getattr(action, "__annotations__", {})

        for parameter in inspect.signature(action).parameters.values():
            parameter_name = parameter.name
            if parameter_name not in parameters:
                continue

            model_class = type_hints.get(parameter_name, parameter.annotation)
            if not isinstance(model_class, type) or not issubclass(model_class, Model):
                continue

            parameter_value = parameters[parameter_name]
            if isinstance(parameter_value, model_class):
                continue

            model = model_class.resolve_route_binding(parameter_value)
            if model is None:
                raise ModelNotFoundException(model_class, parameter_value)

            parameters[parameter_name] = model

        route.set_route_params(parameters)
        return route
