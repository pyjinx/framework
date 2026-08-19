# PyJinx API Documentation

This documentation is the developer-facing reference for using the PyJinx framework APIs, similar to `docs.laravel.com`.

- Versioned scope: this repo documents the current `pyjinx/framework` package API and planned API direction for the first stable 1.0 cut.
- For strategy/roadmap decisions, see:
  - [PRD](./PRD.md)
  - [ROADMAP](./ROADMAP.md)
  - [IMPLEMENTATION_PLAN](./IMPLEMENTATION_PLAN.md)

## Docs sections

- [Getting started](./api/getting-started.md)
- [Application bootstrap and lifecycle](./api/application.md)
- [Dependency injection container](./api/container.md)
- [Routing](./api/routing.md)
- [Request & response](./api/request-response.md)
- [Middleware](./api/middleware.md)
- [Validation](./api/validation.md)
- [Configuration and environment](./api/configuration.md)
- [Console / CLI](./api/cli.md)
- [Commands reference](./CLI_REFERENCE.md)
- [Troubleshooting and common errors](./api/troubleshooting.md)

## Documentation policy

- This API documentation tracks practical usage, not implementation details of private internals.
- Any behavior changes to signatures, commands, request lifecycle, or container contracts must update:
  1. the affected guide page,
  2. the CLI reference if command behavior changes,
  3. PRD/roadmap/plan only if scope changed.
- API docs are maintained in markdown-first format and can be published as a static docs site later (MkDocs/Docsify/VitePress).
