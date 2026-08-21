from typing import Any


class MiddlewareNameResolver:
    @classmethod
    def resolve(
        cls,
        name: str,
        map: dict[str, Any],
        middleware_groups: dict[str, list[str | Any]],
    ):
        if isinstance(name, str):
            if name in map:
                return map[name]

            if name in middleware_groups:
                resolved_group = []

                for item in middleware_groups[name]:
                    if isinstance(item, str):
                        resolved_middleware = cls.resolve(item, map, middleware_groups)

                        if resolved_middleware:
                            resolved_group.append(resolved_middleware)
                    else:
                        resolved_group.append(item)

                return resolved_group

        if hasattr(name, "handle"):
            return name

        return None
