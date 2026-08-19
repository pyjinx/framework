# Middleware API

Middleware runs through the pipeline before a route action.

## 1) Registering middleware

- Global middleware list is resolved from `Kernel.middleware` in app configuration.
- Route middleware aliases and groups can be registered on the router.

```python
router = app.make("router")
router.alias_middleware("auth", "your.project.middleware.AuthMiddleware")
router.middleware_group("api", ["auth", "throttle"])
```

## 2) Middleware contract

A middleware class needs a `handle(request, next)` method:

```python
from collections.abc import Callable

class ExampleMiddleware:
    def handle(self, request, next: Callable[[object], object]):
        # before
        response = next(request)
        # after
        return response
```

Pipeline contract behavior:

1. receives request
2. calls `next(request)` to continue chain
3. returns response or callable output from downstream

## 3) Kernel middleware priorities

HTTP kernel exposes middleware priority list and allows overriding to avoid ordering surprises.

## 4) Route middleware usage

```python
router.get("/admin", [AdminController, "index"]).middleware(["auth", "admin"])
```

## 5) Built-in middleware

- `Illuminate.Foundation.Http.Middleware.HandlePrecognitiveRequests` exists as a pass-through placeholder.
- Additional middleware types are expected in later milestones.

## 6) Notes for implementation parity

- The middleware API aligns with Laravel-style `handle($request, $next)` flow.
- For production, add exception-safe wrappers and short-circuiting docs in command/queue runbooks.