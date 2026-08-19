# pyjinx/pyjinx starter (PoC)

This is a minimal local starter template for the PyJinx framework, modeled after the
Laravel-style `routes + controllers` flow.

## Contents

- `bootstrap/app.py` — bootstraps a tiny app and registers routes
- `routes/web.py` — route definitions
- `app/http/controllers/TodoController.py` — demo controller
- `tests/test_todos_route.py` — simple route test (controller + POST route)

## Run template smoke test

From repository root:

```bash
python -m pytest pyjinx/pyjinx/tests/test_todos_route.py
```

## Route contract

- `POST /todos` → returns 3 demo todo items (no auth middleware).

## Note

This starter is intentionally lightweight for PoC only. It uses a local path dependency
for `pyjinx` and does not include production-safe deployment/CI scaffolding yet.
