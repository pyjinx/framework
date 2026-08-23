# PyJinx Framework Documentation

0) **Project goal** (canonical intent — read first):
- [PROJECT_GOAL](./PROJECT_GOAL.md) — 100% Laravel port to Python.

This folder now holds two documentation streams:

1) **Strategy docs** (planning and execution):
- [PRD](./PRD.md)
- [ROADMAP](./ROADMAP.md)
- [IMPLEMENTATION_PLAN](./IMPLEMENTATION_PLAN.md)
- [IMPLEMENTATION_DECISIONS](./IMPLEMENTATION_DECISIONS.md)
- [Laravel ecosystem candidates](./LARAVEL_ECOSYSTEM_CANDIDATES.md)
2) **Developer API docs** (how to use it):
- [API_DOCS](./API_DOCS.md)
- [Getting Started](./api/getting-started.md)
- [Application and Lifecycle](./api/application.md)
- [Container](./api/container.md)
- [Routing](./api/routing.md)
- [Request / Response](./api/request-response.md)
- [Middleware](./api/middleware.md)
- [Validation](./api/validation.md)
- [Configuration](./api/configuration.md)
- [CLI](./api/cli.md)
- [Troubleshooting](./api/troubleshooting.md)
- [Laravel feature parity todo list](./LARAVEL_FEATURE_PARITY_TODO.md)
- [CLI Reference](./CLI_REFERENCE.md)

## Documentation update policy

When the public API changes:

1. Update the relevant API doc page(s).
2. Update CLI_REFERENCE when command surface changes.
3. Update PRD/ROADMAP/IMPLEMENTATION_PLAN when scope or sequencing changes.

## Repository expectations

- Canonical framework package docs live here.
- Starter application documentation should live in the starter repository (`pyjinx/starter`) once created.