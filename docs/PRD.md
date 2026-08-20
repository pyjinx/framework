# PyJinx Framework PRD (v1.0)

## 1) Executive summary

PyJinx currently has a compact internal core in `Illuminate/`, but it does not yet deliver a production-grade Laravel-style developer framework. The v1.0 target is to build a Python-native, ASGI-first framework package (`pyjinx/framework`) plus a thin starter application (`pyjinx/pyjinx`) with deterministic behavior, explicit contracts, strong typing, and high-fidelity DX.

Primary acceptance target: a Laravel-inspired but non-trivial framework slice where a developer can create a real app with `pyjinx new`, run HTTP routes, apply validation, use database models/migrations, serve via ASGI, generate assets via CLI, and validate the app via functional tests.

---

## 2) Why this PRD exists

The repository currently contains core components (DI container, service providers, routing, middleware skeleton, event/exception bootstrap, validation rules, and a very minimal console system), but key contracts are incomplete for production:

- Request/response path is effectively WSGI-biased.
- CLI surface is limited to list/help and a partially scaffolded command base.
- No starter app repository in this codebase.
- No canonical docs, roadmap, or implementation backlog.
- Several public APIs are only partially typed and behaviorally undefined.
- Existing package namespace is still `Illuminate`, which is semantically and architecturally misaligned with PyJinx naming.

The PRD formalizes the target state and controls scope so the framework becomes an executable product contract, not a demo.

---

## 3) Product goals

### 3.1 Must-have goals

1. **Laravel-inspired architecture with Python-native implementation**
   - Keep lifecycle and boundaries (bootstrap → provider registration → middleware → routing → response).
   - Avoid heavy magic; keep object graph explicit.

2. **ASGI-first runtime with WSGI compatibility path**
   - Primary request adapter must be ASGI-native.
   - WSGI support must remain available as compatibility adapter only, not the core path.

3. **CLI parity** (Laravel-like `artisan` style)
   - A `pyjinx` command entrypoint with Laravel-like grouped commands for local dev, scaffolding, database operations, queue/admin tasks.

4. **Split architecture**
   - `pyjinx/framework`: reusable framework package.
   - `pyjinx/pyjinx`: thin starter scaffold (routes, app config, migrations, views, tests, entrypoints).

5. **Typed boundaries and deterministic behavior**
   - Boundaries between app container/config, router, request, auth, validation, and response layers are typed and tested.

6. **Developer experience parity**
   - Predictable bootstrapping, zero-surprise defaults, discoverable generators, and clear error handling.

### 3.2 Nice-to-have goals

- Laravel-analog observability package (Telescope-equivalent).
- Laravel-analog queue worker runtime (Horizon-equivalent).
- Admin package path reserved (Citadel) without blocking framework core delivery.
- Laravel ecosystem expansion wave (auth/session/notifications/broadcasting/queue/testing-style packages) after v1.0, with scope guided by:
  - `https://www.bacancytechnology.com/blog/laravel-ecosystem`
---

## 4) Users and scenarios

### 4.1 Primary user

- Python web-backend developers shipping web APIs and server-rendered apps.

### 4.2 Top scenarios

- New project bootstrap in one command.
- Route/controller setup with middleware, validation, response objects.
- Model + migration + authentication slice in starter app.
- Local command tooling for repeatable operations.
- Inspect requests/responses/events for debugging and production readiness.

---

## 5) Functional requirements

### 5.1 Core runtime and app lifecycle

- **FR-01 Bootstrapping**
  - Deterministic boot sequence with named bootstrap classes.
  - Explicit lifecycle events and phase transitions.

- **FR-02 Application container**
  - Typed dependency resolution with context-sensitive construction.
  - Distinguish singletons from transient instances.
  - Clear errors for unresolved dependencies and circular construction.

- **FR-03 Service providers**
  - Register and boot phases preserved.
  - Config-based provider discovery and ordered loading.
  - Deterministic ordering and duplicate prevention.

- **FR-04 Config + environment**
  - `.env` and `.env.<APP_ENV>` handling.
  - Config files loaded by environment with cacheable path and merge semantics.

- **FR-05 Exceptions and error pages**
  - Global exception pipeline.
  - Dev and production error handlers with safe payloads.

### 5.2 Routing and HTTP

- **FR-06 Routing API**
  - `Router` supports HTTP verbs and route params.
  - Route groups, prefixes, names, middleware attachment.

- **FR-07 Middleware pipeline**
  - Global, group, and alias middleware.
  - Ordered execution with short-circuit/error behavior.

- **FR-08 Request/response adapters**
  - ASGI adapter as first-class.
  - Request facade exposes query/json/form/files/headers/session/cookie access by contract.
  - Response factory supports JSON, text, and templated responses.

### 5.3 Validation and forms

- **FR-09 Request validation**
  - Laravel-like rule DSL retained as boundary contract.
  - Integrated request validation for both form and JSON payloads.

- **FR-10 Error shape**
  - Deterministic validation error contract suitable for API clients.

### 5.4 Auth and authorization

- **FR-11 Auth service contract**
  - User resolution contract and guard strategy.

- **FR-12 Authorization gates**
  - Ability/policy registration and inspection.
  - Middleware/route-level enforcement.

### 5.5 Database and model layer

- **FR-13 ORM and schema layer**
  - SQLAlchemy-first model definition.
  - Alembic migration commands from CLI.

- **FR-14 Repository pattern integration**
  - Optional service-level data access pattern while still exposing ORM sessions when needed.

### 5.6 Queues, events, and background execution

- **FR-15 Stable queue contract in framework core**
  - Core defines contract and events, not framework-specific implementation lock-in.

- **FR-16 Horizon-like runtime package boundary (future slice)**
  - Worker process manager, retry/dead-letter policy, dashboard-friendly metadata.

### 5.7 Logs and observability

- **FR-17 Event stream and logs**
  - Structured events for bootstrap, routing, response preparation, and command execution.
  - Non-sensitive request/command metadata.

- **FR-18 Telescope-like package path**
  - Separate package reads core events and telemetry contracts.

### 5.8 CLI and scaffolding parity (Laravel-style)

- **FR-19 CLI entrypoint**
  - Global command is `pyjinx` (and local `python -m pyjinx` fallback).
  - Root command groups follow `make:*`, `queue:*`, `migrate:*`, `config:*`, `route:*` conventions.

- **FR-20 Required command surface for v1.0**

  | Category | Laravel analog | PyJinx minimum command | Contract |
  |---|---|---|---|
  | App lifecycle | `serve`, `up`, `down` | `pyjinx serve`, `pyjinx up`, `pyjinx down` | Start/stop dev runtime and optional maintenance mode |
  | Scaffold | `make:model`, `make:controller`, `make:migration`, `make:middleware`, `make:command` | `pyjinx make:model`, `pyjinx make:controller`, `pyjinx make:migration`, `pyjinx make:middleware`, `pyjinx make:command` | Files generated from deterministic stubs + overwrite policy |
  | Routing | `route:list` | `pyjinx route:list` | Deterministic route discovery output |
  | Database | `migrate`, `migrate:status`, `migrate:rollback`, `db:seed` | `pyjinx migrate`, `pyjinx migrate:status`, `pyjinx migrate:rollback`, `pyjinx db:seed` | Alembic-backed execution + exit status contracts |
  | Queue | `queue:work`, `queue:retry`, `queue:failed` | `pyjinx queue:work`, `pyjinx queue:retry`, `pyjinx queue:failed` | Queue contract execution and monitoring hooks |
  | Cache/config | `config:cache`, `config:clear`, `cache:clear` | `pyjinx config:cache`, `pyjinx config:clear`, `pyjinx cache:clear` | Idempotent file cache with safe invalidation |
  | Diagnostics | `tinker`, `route:list`, `about` | `pyjinx tinker`, `pyjinx about` | Safe shell/repl and summary commands |

- **FR-21 CLI behavior requirements**
  - `--help`, `--quiet`, `--version` supported consistently.
  - Deterministic exit codes.
  - Discoverable command listing grouped by namespace.

- **FR-22 Optional facade behavior for existing users**
  - Framework can expose optional static facades where safe, but typed direct APIs remain canonical.

### 5.9 Packaging and scaffold separation

- **FR-23 Framework package**
  - Framework package must not include app-specific routes/controllers/resources.

- **FR-24 Starter scaffold package**
  - New project skeleton includes directories for `app`, `config`, `routes`, `resources`, `storage`, `tests`, entry points.
  - Scaffold pins a compatible framework version.

### 5.10 Testing

- **FR-25 Verification policy**
  - Functional slices with pytest.
  - Contract tests for CLI commands and HTTP kernel lifecycle.
  - Regression tests for validation and route dispatch.

---

## 6) Non-functional requirements

- **NFR-01 Performance**
  - No unbounded request-side allocations on route dispatch.
  - Avoid avoidable copying in middleware/dispatch chains.
  - Track performance regressions with explicit perf budgets for critical paths.
- **NFR-02 Performance and leak audit**
  - Include a baseline performance smoke check in every phase exit.
  - Zero unbounded retention of request/route/container state across requests.
- **NFR-03 Reliability**
  - Explicit failure semantics for timeouts, retries, and partial initialization.
  - No silent swallow of critical exceptions.
  - Define deterministic shutdown and cleanup points for long-running resources.
- **NFR-04 Security**
  - No secret leakage to logs.
  - CSRF/session/auth defaults that are safe by default.
  - Hard boundary for user input at request validation points.
- **NFR-05 Maintainability**
  - Minimal magic; explicit service/provider contracts.
  - Public contracts documented and versioned.
  - Quarterly code-smell review for complexity hotspots and duplication patterns.
- **NFR-06 Developer ergonomics**
  - CLI and scaffold operations are deterministic and scriptable.
- **NFR-07 Compatibility**
  - Avoid breaking compatibility where migration path can be avoided.
  - Temporary compatibility adapters must have explicit deprecation/removal condition.
- **NFR-08 Memory safety**
  - No request-bound caches without TTL/size/eviction controls.
  - No global state that grows unbounded across test or production runs.

---

## 7) Out of scope

- Full SaaS multi-tenancy controls.
- Enterprise policy engines in v1.0 core.
- Proprietary metrics/monitoring backend vendor lock-in.
- Automatic migration of third-party Laravel apps.

---

## 8) Constraints and assumptions

- The current codebase started as a PoC/baseline; feature and quality claims are revalidated under strict TDD before production-ready status.
- Framework and scaffold repositories remain distinct.
- Python >=3.10.
- Laravel ecosystem expansion (select packages from the linked ecosystem catalog) is planned as a post-v1.0 phased effort.
- Queue and observability packages can be first-class sibling packages in later phases.

---

## 9) Acceptance gates (v1.0 candidate)

1. Run `pyjinx new` then scaffold app bootstraps.
2. Define and serve at least one route via ASGI.
3. Validate payload with rule DSL from request class.
4. Run migration create + migrate + rollback on starter db.
5. Execute command list, make-controller, route-list, and serve command without runtime errors.
6. Complete at least one functional test covering full stack slice:
   request => validation => controller => response.
7. Publish artifact for both framework package and starter.

---

## 10) Versioning and delivery

- Core framework versions follow semantic versioning.
- Starter compatibility metadata tracks supported framework major/minor.
- Breaking contract changes require migration doc + release note + compatibility matrix.

---

## 11) Decision risks

- **Namespace transition risk**: continuing `Illuminate` namespace may conflict with long-term product identity.
- **CLI surface creep**: many Laravel-like commands can become pass-through wrappers; implementation must prioritize value.
- **Over-abstracted scaffolding**: generator layers must not become pass-through-only abstractions.
- **Performance regression risk**: route/container/validation hot paths can degrade under realistic middleware and request volume.
- **Code-smell accumulation risk**: duplicated generator/dispatch logic can hide correctness debt.
- **Memory leak risk**: caches, global state, and lifecycle registries can retain request/call objects indefinitely.
---

## 12) References

- Existing codebase paths reviewed:
  - `Illuminate/Foundation/Application.py`
  - `Illuminate/Foundation/Http/Kernel.py`
  - `Illuminate/Foundation/Console/*`
  - `Illuminate/Routing/*`
  - `Illuminate/Validation/*`
- Existing project constraints and conventions are enforced by repository-level strategy and prior decision records.