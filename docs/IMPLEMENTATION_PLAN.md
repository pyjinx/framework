# PyJinx Implementation Plan (Framework + Starter + CLI parity)

Reference trackers and implementation posture:

- Laravel parity baseline: `https://api.laravel.com/docs/13.x/index.html`
- Internal coverage backlog: [Laravel feature coverage and todo list](./LARAVEL_FEATURE_PARITY_TODO.md)
- Engineering posture: [Implementation decisions](./IMPLEMENTATION_DECISIONS.md)
- Laravel ecosystem expansion reference: `https://www.bacancytechnology.com/blog/laravel-ecosystem`
## Delivery model

Use short, shippable milestones:


1. **Explode known gaps** → patch only behavior-correctness gaps.
2. **Add stable contracts** → make behavior explicit and typed.
3. **Implement slice-by-slice** → one vertical slice per milestone.
4. **Verify with targeted tests** → no behavior lands without proof.

---

## Workstream 1: Core runtime contract hardening

### 1.1 Container and application lifecycle

**Files:**
- `Illuminate/Container/Container.py`
- `Illuminate/Foundation/Application.py`
- `Illuminate/Foundation/Configuration/ApplicationBuilder.py`

**Tasks:**
1. Replace mutable-default container arguments with sentinel-safe defaults.
2. Separate binding metadata from resolved cache semantics.
3. Clarify `make/resolve/instance` behavior and error classes.
4. Add dependency graph introspection helper for diagnostics.
5. Ensure provider registration stores deterministic order and idempotence.

**Acceptance:**
- `Container` raises deterministic, explicit exceptions for missing binding, invalid constructor args, and circular usage.
- Application registers providers exactly once in deterministic order.

### 1.2 Bootstrap and exception handling

**Files:**
- `Illuminate/Foundation/Bootstrap/*.py`
- `Illuminate/Exceptions/Handler.py`
- `Illuminate/Foundation/Http/Kernel.py`
- `Illuminate/Foundation/Console/Kernel.py`

**Tasks:**
1. Extract startup sequence into a typed state machine.
2. Enforce idempotent bootstrap with clear re-entrant behavior.
3. Normalize bootstrap event dispatch + failures to prevent partial state.
4. Ensure console and HTTP kernels share common initialization guarantees.

**Acceptance:**
- Re-running kernel boot does not duplicate side effects.
- Initialization failure returns typed boundary errors and always exits with consistent state.

### 1.3 Request/response contract

**Files:**
- `Illuminate/Http/Request.py`
- `Illuminate/Http/Response.py` *(new if absent)*
- `Illuminate/Http/RequestAdapter.py`
- `Illuminate/Http/W*Adapter.py`
- `Illuminate/Http/ServerBag/ASGIServer.py`

**Tasks:**
1. Implement explicit ASGI adapter and wire router/application call path to use it by default.
2. Keep WSGI adapter behind compatibility module.
3. Add response normalization helpers (JSON/text/html) and status/header management contract.
4. Ensure request object exposes stable helpers without leaking unknown server internals.

**Acceptance:**
- End-to-end ASGI request path emits deterministic response object.
- WSGI path continues to work via compatibility adapter.

### 1.4 Routing and middleware correctness

**Files:**
- `Illuminate/Routing/Router.py`
- `Illuminate/Routing/Route.py`
- `Illuminate/Routing/RouteCollection.py`
- `Illuminate/Pipeline/Pipeline.py`

**Tasks:**
1. Fix route matching for method/path edge cases and parameter extraction.
2. Validate middleware resolution and alias/group precedence.
3. Ensure pipeline preserves output order and supports short-circuit errors.
4. Add route-group merge and naming semantics tests.

**Acceptance:**
- Route groups, named routes, parameter routes, and middleware precedence work deterministically.

### 1.5 Validation and forms

**Files:**
- `Illuminate/Validation/*`
- `Illuminate/Foundation/Http/FormRequest.py`

**Tasks:**
1. Convert `Validator` and rule execution to strict request payload contract.
2. Introduce common validation response envelope.
3. Add `FormRequest` integration for request-specific rules.
4. Add tests for nested fields, nullable behavior, and message mapping.

**Acceptance:**
- Validation contract is stable and consumable by controller and API clients.

---

## Workstream 2: CLI parity implementation

### 2.1 CLI command framework foundation

**Files:**
- `pyproject.toml` (add dependencies and entrypoints)
- `Illuminate/Foundation/Console/Application.py`
- `Illuminate/Foundation/Console/Command.py`
- `Illuminate/Foundation/Console/Kernel.py`
- `Illuminate/Foundation/Console/ContainerCommandLoader.py`
- Add CLI runner module (new, e.g., `Illuminate/Foundation/Console/Runner.py`)

**Tasks:**
1. Introduce the CLI entrypoint and wire one command dispatcher.
2. Add command discovery registry with strict command object metadata (`name`, `description`, `aliases`, `options`, `arguments`).
3. Standardize output style, exit codes, global flags, and Laravel Prompts-compatible interactive behavior through a PyJinx-owned prompt boundary backed by `prompt_toolkit` and `Rich`.
4. Preserve existing minimal list/help semantics while migrating internals.

**Acceptance:**
- Running `pyjinx --help` prints consistent root help with command groups.
- `list`/`help` behavior remains backward-compatible.

### 2.2 Command set for v1.0

**Files (new/updated):**
- `Illuminate/Foundation/Console/Commands/` *(new package)*
- `Illuminate/Foundation/Console/Commands/Serve.py`
- `Illuminate/Foundation/Console/Commands/New.py`
- `Illuminate/Foundation/Console/Commands/Make.py`
- `Illuminate/Foundation/Console/Commands/RouteList.py`
- `Illuminate/Foundation/Console/Commands/Migrate*.py`
- `Illuminate/Foundation/Console/Commands/Queue*.py`

**Tasks:**
1. Implement command parser and routing for:
   - `pyjinx new`
   - `pyjinx serve`
   - `pyjinx make:model`
   - `pyjinx make:controller`
   - `pyjinx make:middleware`
   - `pyjinx make:command`
   - `pyjinx route:list`
   - `pyjinx migrate`
   - `pyjinx migrate:status`
   - `pyjinx migrate:rollback`
   - `pyjinx db:seed`
   - `pyjinx queue:work`
   - `pyjinx queue:retry`
   - `pyjinx queue:failed`
2. Add stub loading + overwrite/collision guard.
3. Provide command metadata for help text and grouped listing.
4. Add command integration tests (smoke + golden for help output).

**Acceptance:**
- All listed commands execute with safe no-op mode in test environment.
- Command failure returns non-zero with actionable message and logs contract context.

### 2.3 Starter-oriented helpers

**Files:**
- `Illuminate/Foundation/Console/GeneratorCommand.py`
- `Illuminate/Foundation/Console/GeneratorCommand.py` (finish stub implementation)
- New stub catalog under framework package.

**Tasks:**
1. Finalize generator contract and file template interpolation.
2. Add templates for controller, request, migration, command, model, middleware.
3. Add `--force`, `--dry-run`, `--quiet` generation options.
4. Add tests validating generated file shape + overwrite behavior.

**Acceptance:**
- Generated files are deterministic across runs with stable templates.

---

## Workstream 3: Starter repository (`pyjinx/starter`) creation

### 3.1 Project skeleton structure

**Outside this repo in intended sibling package:**
- `pyjinx/starter` directory layout.

**Tasks:**
1. Create app entrypoints and bootstrap file.
2. Add `routes/web.py`, `routes/api.py`, sample controller, sample request, sample model.
3. Add migrations/bootstrap for a minimal user/auth table and sample domain model.
4. Add `.env.example`, config modules for app/database/logging/services.
5. Add test suite scaffold with at least one functional flow.

**Acceptance:**
- `pyjinx new` produces a runnable skeleton that boots and serves a smoke route.

### 3.2 Vertical slice contract in starter

**Tasks:**
1. Route, controller, request validation, model create/retrieve.
2. Authentication check path + authorization policy check.
3. Exception + JSON error response path.
4. One functional test covering full HTTP/DB/validation flow.

**Acceptance:**
- `functional_smoke` test is green against local SQLite/temporary DB.

---

## Workstream 4: Foundation for observability and queues (adjacent packages)

### 4.1 Queue contract

**Files:**
- New contracts under framework (queue interfaces/events).
- Existing queue package path (future package).

**Tasks:**
1. Specify `Job`, `Queue`, `Worker`, `Result` contracts in framework.
2. Add default local in-memory/in-process driver for development.
3. Add CLI commands to inspect and retry jobs.

**Acceptance:**
- Queue operations are deterministic with explicit success/fail states.

### 4.2 Telescope-style observability

**Files:**
- Event hooks from framework
- New package entrypoint (future package)

**Tasks:**
1. Capture request lifecycle events + validation + exceptions + command execution.
2. Add redaction and rate/volume controls.
3. Add retention and export format.

**Acceptance:**
- Event stream can reconstruct request -> validation -> response timeline.

---

## Workstream 5: Auth and authorization completion

### 5.1 Auth + gate hardening

**Files:**
- `Illuminate/Auth/*`
- `Illuminate/Foundation/Http/Middleware` auth middleware

**Tasks:**
1. Finalize `User` contract and default guard strategy.
2. Add middleware helpers for route-level authorization.
3. Add policy registration and before/after callbacks lifecycle tests.

**Acceptance:**
- Invalid auth access path returns typed unauthorized response.

---

## Workstream 6: Naming and compatibility transition

### 6.1 Namespace migration

**Files:**
- packaging metadata
- new compatibility facades/aliases

**Tasks:**
1. Introduce `pyjinx` public package alias.
2. Keep `Illuminate` compatibility mapping temporarily with deprecation warnings.
3. Publish migration doc + codemod guidance.

**Acceptance:**
- New docs and examples use `pyjinx`; legacy path remains functional until declared cut-off.

---

## Test strategy by phase

### Unit-level
- Container resolution and service-provider lifecycle.
- Router matching, route parameter extraction, middleware ordering.
- Validation rule execution and validation response contract.
- CLI parser and generator helpers.

### Functional
- Serve one request -> middleware -> controller -> JSON response.
- `pyjinx` command operations.
- Bootstrap and startup lifecycle in both HTTP and CLI entry paths.

### Smoke checks for each release candidate
- Fresh project scaffold.
- `pyjinx serve` + route/list.
- CLI command list/help.
- Simple migration + rollback.

---

## Dependency strategy

- Keep dependency additions minimal and scoped:
  - ASGI stack (Starlette/uvicorn-compatible primitives).
  - SQLAlchemy + Alembic for ORM/migrations.
  - One CLI dispatcher library.
  - `prompt_toolkit` for Laravel Prompts-compatible interactive input.
  - `Rich` for terminal tables, progress, spinners, and styled output.
  - Pydantic/Jinja2/jinja templating for validation and views as required.

---

## Sequencing and risk controls

1. Don’t implement advanced queue/observability before CLI+ASGI baseline is stable.
2. Avoid implementing facade-only abstractions.
3. Maintain checkpoint quality counters for performance issues, code smells, and memory-leak risks; no phase passes without explicit counts.
4. Each phase ends with verifiable acceptance before moving on.
5. Migration windows must be explicit for compatibility changes.

---

## Exit criteria for this implementation phase

- v1.0 feature-complete against PRD sections 5.1–5.9.
- Starter vertical slice passing functional test.
- `pyjinx` command commandset available and documented.
- ASGI request lifecycle is default path.
- Release artifacts and changelog published.

---

## Workstream 7: Laravel ecosystem expansion (post-v1)

### 7.1 Candidate package wave

**Reference:**
- `https://www.bacancytechnology.com/blog/laravel-ecosystem`

**Scope:**
- Select high-value Laravel ecosystem analogs as optional packages (identity/auth extensions, realtime/broadcasting, notifications, job tooling, diagnostics).
- Keep framework core unchanged; all ecosystem packages remain optional siblings with explicit dependency boundaries.
- Add import/setup guides in the relevant package docs before each candidate ships.

**Tasks:**
1. Add an explicit ecosystem candidate matrix in plan updates.
2. Gate each package admission by quality counters and TDD acceptance criteria from this plan.
3. Ship first optional package only when adjacent core contracts are stable and covered by tests.

**Acceptance:**
- Candidate selection, scope, and dependency boundaries are documented and reviewed before implementation.

## Immediate next tasks (next 2 weeks)
1. Finalize PRD/ROADMAP alignment with one explicit namespace decision (`pyjinx` vs `Illuminate` compatibility shim).
2. Add minimal ASGI adapter wiring and bootstrap state contract.
3. Add `pyjinx` command core and command registry.
4. Draft first generator templates for `make:model` and `make:controller`.
5. Add baseline functional test for route->controller->validated response.

This is the execution order that minimizes risk while maximizing usable progress.