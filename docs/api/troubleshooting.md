# Troubleshooting and Common Issues

## App does not boot

Checklist:

1. Verify `app = Application.configure(...).create()` is executed once.
2. Ensure config/route providers are loaded.
3. Check `app.handle_request(...)` receives a request object captured by `Request.capture(app)` in WSGI/ASGI flow.
4. Confirm exceptions are captured via host adapter and not swallowed.

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
- Use `pilot about` for runtime summary.
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