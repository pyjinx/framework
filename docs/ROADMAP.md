# PyJinx Roadmap

## Canonical feature parity tracking

- Laravel reference baseline: https://api.laravel.com/docs/13.x/index.html
- Internal coverage tracker: [Laravel feature coverage and todo list](./LARAVEL_FEATURE_PARITY_TODO.md)
- Working policy and execution posture: [Implementation decisions](./IMPLEMENTATION_DECISIONS.md)
- Future ecosystem mapping: https://www.bacancytechnology.com/blog/laravel-ecosystem

## Purpose

Version bands are placeholders and should be adjusted against release policy.

---

## North-star milestones

- **M0** — Current baseline: core framework primitives exist but incomplete for production.
- **M1** — Framework core stabilized (ASGI-first, typed lifecycle contracts, robust routing/middleware).
- **M2** — CLI parity baseline (`pyjinx` command, generators, `serve`, `migrate`, `make:*`, `route:list`).
- **M3** — Starter scaffold (`pyjinx/starter`) delivered with one vertical slice.
- **M4** — Queue + observability ecosystem and optional facade tightening.
- **M5** — Hardened public release with migration docs and release train gates.

---

## Release phase plan

## Phase 0 — Consolidation and architecture cleanup

**Goal:** capture current state and remove blocking architecture hazards before adding new features.

### Scope

- Freeze current APIs that are currently externally used.
- Add baseline contracts and API-level guardrails to match intended ownership boundaries.
- Clarify bootstrap and container semantics.

### Deliverables

- Architectural decision notes for:
  - Application bootstrap lifecycle.
  - Service provider contract.
  - Request/Response ownership.
  - Container dependency semantics.
- Temporary risk register for all current partial implementations (mutable defaults, silent failures, mutable class-level state).
- Baseline static analysis and a minimal lint/test smoke list.

### Acceptance

- Developer can list bootstrap steps and provider execution order without reading source.
- Known hazards are documented and each hazard has assigned owner and expected resolution slice.

---

## Phase 1 — Core framework correctness hardening

**Goal:** make routing/middleware/container/validation/error handling reliable enough for first production slice.

### Scope

- Container:
  - remove mutable default arguments where currently used.
  - enforce deterministic dependency error messages.
  - clarify singleton/contextual binding behavior.
- Kernel + bootstrap:
  - unify request/console boot sequence and failure semantics.
- Request/response:
  - finish ASGI adapter path and make WSGI path an adapter.
- Routing:
  - harden matching, middleware sorting, route-grouping semantics.
- Exceptions:
  - predictable exception lifecycle and failure translation layer.
- Logging/observability hook points:
  - explicit event emissions for request lifecycle and command execution.
- Validation:
  - formalize validated payload contract and error response shape.

### Deliverables

- `pyjinx/framework` version with stable core runtime primitives.
- Migration notes for any changed error shapes.
- Unit tests for container, route dispatch, middleware order, and validation edges.

### Acceptance

- Route dispatch works for grouped routes and middleware.
- ASGI request enters framework through a dedicated adapter.
- Invalid dependencies and unresolvable inputs fail with explicit typed errors.

---

## Phase 2 — CLI foundation and Laravel-style command parity

**Goal:** add production-usable CLI toolchain with Typer/Click command surface.

### Scope

- Add executable entrypoints:
  - `pyjinx` global installer command.
  - `loom` project-local framework command.
  - stable `--help`, `--version`, global options.
- Command groups:
  - `pyjinx new`, `loom serve`, `loom tinker`, `loom about`.
  - `loom make:model|controller|middleware|command|migration|request|factory`.
  - `loom route:list`.
  - `loom migrate|migrate:status|migrate:rollback|db:seed`.
  - `loom queue:work|queue:retry|queue:failed`.
- Stubs and generation:
  - deterministic stubs, overwrite policy, dry-run mode, and namespace/path inference.
- Command test harness with snapshot/integration tests.

### Deliverables

- CLI package or module integrated into framework package.
- Command registry metadata and command discovery strategy.
- Test fixtures for core CLI output and exit codes.

### Acceptance

- `loom --help` enumerates available project commands and groups.
- `loom serve` launches ASGI app with clear startup/stop behavior.
- `loom make:controller` writes deterministic skeleton.
- `loom route:list` reports route table from loaded bootstrap routes.

---

## Phase 3 — Starter scaffold release (`pyjinx/starter`)

**Goal:** provide the thin app repo that depends on framework and demonstrates the vertical slice.

### Scope

- Create `pyjinx/starter` scaffold repo structure:
  - `app/`, `routes/`, `config/`, `resources/views/`, `database/migrations/`, `tests/`, `.env.example`.
- Add `pyproject.toml` dependency on framework package semver-compatible.
- Include first-class boot entrypoints:
  - `loom serve` delegating to ASGI app.
- Add baseline modules:
  - sample controller,
  - sample route definitions,
  - sample request validation,
  - authentication middleware stubs,
  - sample view/JSON response route.
- Include functional acceptance test for vertical slice:
  - route + validation + model + auth-ish authorization check + response assertion.

### Deliverables

- Published starter app template.
- Documentation: getting-started + generator guide + lifecycle notes.
- Example migration file and startup script.

### Acceptance

- New app can be created from framework command and boot without manual edits.
- `pyjinx new` + `loom serve` and one protected route test pass.

---

## Phase 4 — Ecosystem: queue + observability

**Goal:** provide adjacent packages while keeping framework core small.

### Scope

- Queue:
  - define queue contract in framework core and simple default adapter.
  - worker command and state model.
- Observability:
  - add event collector package (Telescope-like) built on framework events.
  - UI or storage backend path chosen (file/DB backend) with retention policy.
- Authz/security hardening:
  - align middleware/gate behavior with contract-level authorization.

### Deliverables

- `pyjinx/queue` and `pyjinx/telescope` (or equivalent stable names) package paths and docs.
- CLI hooks: `queue:*` commands.
- Observability install/config guides.

### Acceptance

- Queue task lifecycle captured and restart-safe.
- Observability captures request lifecycle, failed validations, exception events, and command actions.
- Retention policy prevents unbounded growth.

---

## Phase 5 — Name/compatibility rationalization

**Goal:** complete transition to Python-native naming while preserving compatibility where required.

### Scope

- Introduce a canonical export surface (`pyjinx` package API root).
- Keep `Illuminate` as compatibility shim only where required.
- Provide migration notes and deprecation timeline.

### Deliverables

- Compatibility layer map and removed legacy touchpoints with explicit deadlines.
- Versioned migration plan for import paths and CLI aliases.

### Acceptance

- New apps use `pyjinx` namespace by default.
- Compatibility shim documents and enforces warnings or deprecation logs.

---

## Phase 6 — Release hardening and packaging

**Goal:** make v1.0 release reliable and auditable.

### Scope

- Packaging, CI, docs, website, and release assets.
- Dependency policy and CVE update path.
- Golden-path documentation, API reference, and reproducible bootstrap.
- Public website explaining Veyra's Laravel inspiration, compatibility target,
  legal notices, and non-affiliation clearly.

### Deliverables

- `pyjinx/framework` 1.0.0 with semantic release.
- Starter `pyjinx/starter` versioned compatibility.
- Changelog and migration instructions.

### Acceptance

- Deterministic install and reproducible smoke test.
- Evidence bundle includes verification commands and pass/fail status.

## Phase 7 — Laravel ecosystem expansion (post-v1)

**Goal:** evaluate and implement selected Laravel ecosystem packages as optional, composable add-ons without core bloat.

### Scope

- Use ecosystem candidates from:
  - `https://www.bacancytechnology.com/blog/laravel-ecosystem`
- Prioritize packages where stable contracts add immediate value to core developer workflows.
- Keep each candidate as a separate package/repo slice with explicit boundaries and migration notes.
- Add docs, tests, and install instructions before each package ships.

### Deliverables

- `docs/LARAVEL_ECOSYSTEM_CANDIDATES.md` (or equivalent tracker entry) listing candidates, rationale, dependencies, and risk gates.
- Post-v1 acceptance criteria and TDD checks for each implemented package.
- Optional install path and usage guide for first candidate wave.

### Acceptance

- No candidate enters implementation before acceptance criteria and quality counters are updated.
- First ecosystem package ships only if it does not increase coupling or leak global state.

---
## Cross-cutting workstreams

- **Security**: every phase must preserve redaction guarantees for logs/events.
- **Performance**: add low-cost micro-benchmarks where relevant (route dispatch, container make, CLI startup), and log regression deltas.
- **Quality debt tracking**: maintain a running count of code smells and memory-leak risks; block release on unbounded growth.
- **Docs**: every phase updates `docs/` and contract docs in lockstep with behavior.
- **Testing**: no new capability without automated proof in scope.

---

## Delivery order and precedence

If resource-limited, execution precedence is:
1. Core correctness (Phase 1)
2. CLI foundation (Phase 2)
3. Starter + vertical slice (Phase 3)
4. Ecosystem packages (Phase 4)
5. Naming transition (Phase 5)
6. Release hardening (Phase 6)

7. Laravel ecosystem expansion (Phase 7)
8. Future maintenance / hardening follow-ups (if any)
 
CLI parity is intentionally in Phase 2 before advanced observability so developers can operate and scaffold during validation of every later phase.
## Risks and mitigation

- **Phase bleed (over-coupling)**: keep framework and optional packages separate.
- **CLI overgrowth**: implement command slices with explicit priority; avoid implementing every Laravel command in phase 2.
- **ASGI migration failure**: keep WSGI bridge tests while ASGI is adopted as default.
- **Migration gap with namespace**: retain alias layer until deprecation windows close.

---

## Open dependency assumptions

- Framework will use proven third-party components and avoid reimplementing mature surfaces.
- CLI parity should use a single robust library (Typer or Click) for consistency.
- Queue and observability packages remain optional to avoid expanding core blast radius.