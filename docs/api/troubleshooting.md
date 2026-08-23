# Troubleshooting and Common Issues

## App does not boot

Checklist:

1. Verify `app = Application.configure(...).create()` is executed once.
2. Ensure config/route providers are loaded.
3. Check `app.handle_request(...)` receives a request object captured by `Request.capture(app)` in WSGI/ASGI flow.
4. Confirm exceptions are captured via host adapter and not swallowed.

## Unhandled HTTP exceptions

- `Foundation.Http.Kernel` reports an uncaught `Exception` and returns the core
  `ExceptionResponse` rather than re-raising it from the request boundary.
- Send `Accept: application/json` (or a `+json` media type as the first
  preferred value) for a JSON error payload; otherwise the handler returns
  HTML. `Exceptions.should_render_json_when(...)` can override this choice.
- With `app.debug` disabled, a 500 response is limited to `Server Error`.
  Debug mode includes escaped HTML traceback details or a JSON traceback for
  local diagnosis only. It is not an Ignition replacement.
- Configure report filtering, levels, context, callbacks, duplicate
  suppression, rendering, and final response transformation through
  `Application.configure(...).with_exceptions(lambda exceptions: ...).create()`.

## Route not found

- Check HTTP method mapping (`GET` vs `POST`).
- Ensure route prefix/group semantics are applied as expected.
- Check route pattern syntax uses `:param` placeholders (e.g. `/users/:id`).

## Middleware not running

- Confirm middleware name is registered via alias or group.
- Confirm order between global middleware and route middleware.
- Confirm middleware has `handle(request, next)`.

## Validation not returning expected shape

- Ensure rules are correct for key names.
- Confirm payload source (`json` vs form) aligns with request type.
- Verify response contract expects a `ValidationResponse` map.

## CLI command failures

- Run with `--help` first to verify command discovery.
- Use `loom about` for runtime summary.
- For `make:*` commands, inspect overwrite/dry-run semantics before writing files.

## Container binding errors

- Re-register missing binding keys before calling `make()`.
- Use `alias` consistently and avoid circular construction.

## Known limitations to track

- ASGI default not yet fully enforced in runtime wiring.
- Some command and adapter conveniences are still roadmap items.
- Mutable default arguments in some internals are targeted for hardening.

For implementation status and the acceptance plan, see:
- [ROADMAP](../ROADMAP.md)
- [IMPLEMENTATION_PLAN](../IMPLEMENTATION_PLAN.md)