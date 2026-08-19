# Request and Response API

## Request object

Core request class: `Illuminate.Http.Request`.

### Create request

- WSGI compatibility flow currently uses:

```python
request = Request.capture(app)
```

### Input helpers

- `request.all()` — merged input + files
- `request.input()` — payload source (query or body depending on method)
- `request.query()` — query params
- `request.form()` / `request.post()` — form/body data
- `request.json()` — JSON payload
- `request.files_data()` / `request.all_files()` — uploaded file data
- `request.header(name)` — header lookup
- `request.cookie(name)` / `request.session(key)`
- `request.route_param("id")`

## Response factory

Core response object: `Illuminate.Routing.ResponseFactory`.

Typical chain:

```python
response = app.make("response")
response.set_status("200 OK")
response.set_headers("Content-Type", "application/json")
response.set_content({"ok": True})
```

## Response serialization

Current factory serializes structured values recursively via `ResponseFactory.serialize(...)` for dict/list/tuple/set/JsonSerializable.

For JSON responses, return Python dict and rely on your adapter to serialize if you build one; for strict JSON response semantics, add a dedicated JSON helper in a derived response contract during hardening.

## Response flow

HTTP kernel flow:

- route result → `prepare_response`
- dispatch `PreparingResponse` and `ResponsePrepared` events
- final response passed back to host adapter

## Current compatibility status

- WSGI adapter is currently the concrete request adapter path.
- ASGI adapter exists in compatibility surface and should become the default in the next release train.

For endpoint-level behavior and middleware interaction, see [middleware](./middleware.md).