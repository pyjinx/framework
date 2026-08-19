# Routing API

Routing is managed by `Illuminate.Routing.Router`.

## 1) Registering routes

```python
router = app.make("router")

router.get("/", [HomeController, "index"])
router.post("/users", [UserController, "store"])
router.put("/users/:id", [UserController, "update"])
router.delete("/users/:id", [UserController, "destroy"])
```

Supported HTTP verb helpers:
- `get`, `post`, `put`, `patch`, `delete`, `option`

Route action format:

- callable function: `router.get("/", lambda request: {...})`
- controller + method: `[ControllerClass, "method"]`

Route parameters support simple `:name` extraction:

- request to `/users/42` against `/users/:id` maps `route.route_params["id"] == "42"`.

## 2) Route groups

```python
router.group(
    {
        "prefix": "api",
        "middleware": ["auth"],
    },
    lambda: (
        router.get("status", [HealthController, "status"])
    )
)
```

## 3) Middleware, name, and controller middleware

```python
router.get("/posts/{id}", [PostController, "show"]) \
      .name("posts.show") \
      .middleware(["auth", "cache"])
```

Controller middleware hooks are read from the controller when method `middleware()` exists.

## 4) Route listing

Command docs for route listing are in CLI docs (`route:list`).

## 5) Route dispatch flow

1. HTTP kernel resolves request path/method.
2. Router matches request route.
3. Matched route gets route params + query params.
4. Middleware pipeline executes.
5. Route action runs.
6. Response is prepared/dispatched.

## 6) Current caveats

- `Router` and `Route` are functional but the API is still being finalized for production semantics.
- Middleware sorting and some grouping details are planned to be locked down in v1.0 hardening.