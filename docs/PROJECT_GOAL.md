# PyJinx Project Goal — 100% Laravel Port to Python

> **This is the canonical statement of project intent.** It is the backup of the
> main decision recorded in long-term memory so it survives across sessions,
> machines, and contributors. If any other doc conflicts with this file, this
> file wins until a documented owner-approved decision supersedes it.

## The Goal

PyJinx is an **exact, bit-by-bit port of Laravel from PHP to Python** — not a
"Laravel-inspired" or "Laravel-flavoured" framework.

We mimic:

- **`laravel/laravel`** — the application skeleton: directory layout
  (`app/`, `bootstrap/`, `config/`, `database/`, `public/`, `resources/`,
  `routes/`, `storage/`, `tests/`), bootstrap flow, providers, route files,
  middleware organization, and configuration structure.
- **`laravel/framework`** — the internals: container, service providers,
  lifecycle, dependency direction, routing, HTTP layer, validation, Eloquent
  ORM, migrations, queues, events, mail, notifications, sessions, cookies,
  caching, filesystems, error semantics, command organization, public APIs,
  contracts, edge cases, and lifecycle transitions.

The port boundary is explicit:

- `laravel/laravel` → `pyjinx/starter/` application repository.
- `laravel/framework` → `framework/` reusable framework repository.
- `pyjinx/framework` → the application's pinned submodule checkout of
  `framework/`; it is not a second framework source repository.

The framework source of truth is `framework/`. Changes are made there, then
the application submodule pointer is advanced to the verified framework commit.
Both repositories are required deliverables. A complete framework port with a
non-parity starter application is not project completion.

The intended distribution model follows Laravel's split exactly: `pyjinx/`
is the project skeleton/template, while generated applications depend on the
published `pyjinx` framework package. The `pyjinx/framework` submodule exists
only for local framework development and parity verification; it is not
intended to be copied into production projects.

Distribution names are transitional until the dedicated Veyra migration:
`pyjinx` is the current framework package, `pyjinx-starter` is the current
skeleton package, and `pyjinx-installer` provides the global `loom` command.
Users should run `loom new hello-world`; generated projects use the same
`loom` executable for `loom serve`, `loom migrate`, and `loom test`. The final
distribution names are planned as `veyra`, `veyra-starter`, and
`veyra-installer`; the executable remains `loom`. Do not create a separate
`pyjinx_core` or `pyjinx_framework` package.

## Fidelity Rule

Behavior, architecture, system design, structure, lifecycle, dependency
direction, error semantics, and internal implementation logic must match
Laravel as closely as technically possible — **100% exact mimicry wherever
technically possible**.

- Anything that is *not* a 100% exact mimic must be fixed or refactored.
- The only allowed differences are those forced by the Python language/runtime.
- Every unavoidable deviation must be:
  1. explicit,
  2. documented with a written rationale,
  3. technically justified, and
  4. backed by focused behavioral evidence (tests).

## Pinned Upstream Baseline

The current compatibility target is **Laravel 13.x**. The port advances by
upstream diffs; it does not restart from zero for every Laravel release.

| Baseline | Pin |
|---|---|
| Laravel major | `13.x` |
| `laravel/framework` source snapshot | `references/framework` at `8cb299dc2c07227f0cb664a2d53d0cde7839eaaf` |
| `laravel/laravel` source snapshot | `references/laravel` at `4a27aeaa890579f6b70e4bbd9d44c96056174119` |
| Compatibility line | `PyJinx Laravel 13.x` |
| Upstream release reference | [Laravel 13 release notes](https://laravel.com/docs/13.x/releases) |

### Upgrade policy

When Laravel publishes a new minor, patch, or major version:

1. Preserve the current pinned snapshot and green evidence.
2. Read the official release notes and upstream changelog.
3. Update the Laravel source snapshot only in a dedicated upgrade slice.
4. Diff the upstream framework/application sources and API index.
5. Port changed behavior, contracts, errors, tests, and documentation only.
6. Run the focused parity tests and the complete ported Laravel test suite.
7. Record intentional PHP-to-Python deviations and update the compatibility
   line only after the evidence is green.

Minor and patch updates should normally be incremental. A major release may
require coordinated changes, but existing ported behavior and tests remain the
starting point; reimplementation from scratch is prohibited unless an
explicit architecture decision proves the old baseline incompatible.

## Authoritative References

| Source | Role |
|---|---|
| `references/laravel/` | Authoritative PHP application skeleton (`laravel/laravel`) |
| `references/framework/` | Authoritative PHP framework source (`laravel/framework`) |
| `references/laravel-demo/` | Debugging aid for bootstrap/app/route/provider lifecycle |
| Laravel 13.x API docs (`https://api.laravel.com/docs/13.x/index.html`) | Public API surface baseline |

Do **not** invent behavior. When implementing a feature, read the
corresponding Laravel source first and translate its logic, naming, ordering,
and failure semantics into Python.

## Established Deviations (Python-runtime-forced)

These are the currently accepted, documented deviations:

1. **snake_case method names** mirror Laravel's camelCase
   (`belongsTo` → `belongs_to`, `firstOrCreate` → `first_or_create`) because
   PEP 8 is the Python convention.
2. **Relationships are called as methods** (`user.posts().get()`) instead of
   magic properties (`$user->posts`) because Python methods and properties
   share one namespace; attribute-style access would collide with real
   attributes.
3. **SQLAlchemy 2.x Core + Alembic** back the query builder, schema builder,
   and migrations behind a thin PyJinx-owned `Illuminate.Database`
   compatibility layer — PyJinx owns its API surface, return shapes,
   exceptions, and lifecycle semantics rather than leaking SQLAlchemy objects.

Anything beyond these requires a new written entry before implementation.

## Future Public Identity

The selected future public framework name is **Veyra**. The current PyJinx
package, namespace, CLI, and repositories remain unchanged until a dedicated
compatibility-preserving migration slice after Laravel parity work.

Future migration checklist:

- Python package and namespace: `veyra`
- CLI executable: `veyra`
- Starter identity: `veyra-starter`
- GitHub organization repositories currently named:
  - `pyjinx/framework`
  - `pyjinx/starter`
- Check PyPI, GitHub, domains, and trademarks before migration.
- Preserve import/CLI compatibility aliases for the documented migration
  window, then remove obsolete paths only after the clean cutover.

## Python-Only Contribution Strategy

The framework core remains Python-only. Rust/PyO3 is not a required runtime,
build dependency, or contributor path. This keeps the implementation readable,
maintainable, debuggable, and accessible to the widest open-source contributor
base. Performance work remains Python-first and must be measured before any
future architecture change.

## Website and Documentation Deliverables

The project will provide a public website and Laravel-quality API/developer
documentation covering:

- installation and project creation;
- lifecycle and architecture;
- routing, middleware, HTTP, validation, and exceptions;
- database, Eloquent, migrations, queues, events, auth, and services;
- CLI commands and Laravel-compatible options;
- API reference for every promoted public class, method, and contract;
- migration guides, compatibility policy, examples, and troubleshooting;
- Veyra ecosystem products, pricing boundaries, and hosted-service policy.

The website MUST clearly explain that Veyra is highly inspired by and
behaviorally ported from Laravel where applicable, without implying Laravel
ownership, endorsement, or affiliation. Required upstream license, copyright,
and attribution notices MUST be preserved. Marketing credit beyond legal
obligations is not a framework implementation requirement.

## Future Open-Source Publication Boundary

The current `pyjinx/framework` and `pyjinx/starter` repositories are private
until the Veyra migration and release audit are complete.

Before public release:

- do not publish internal roadmap, parity-audit, implementation-decision,
  autonomous-loop, revenue-planning, or private operational documents by
  default;
- curate public website/API documentation separately;
- audit the export for secrets, private notes, internal paths, unreleased
  commercial plans, licenses, copyright, and attribution obligations;
- explicitly approve the public file manifest and release repository layout.

## Engineering Process Requirement

Every implementation, review, debugging, testing, and delivery slice MUST
follow the repository's `software-engineering-handbook` skill:

- Read the handbook README and applicable chapters before non-trivial work.
- Map authoritative sources, contracts, dependencies, risks, and affected
  callers before editing.
- Use strict test-first behavioral verification for permanent changes.
- Record material architecture decisions, unavoidable deviations, and residual
  risks durably.
- Verify the actual changed surface and report evidence without overstating
  coverage.
- Treat the complete `laravel/framework/tests/` port as a future acceptance
  requirement; current focused tests are not full Laravel coverage.

The continuous execution protocol is
[`AUTONOMOUS_PARITY_LOOP.md`](./AUTONOMOUS_PARITY_LOOP.md). It continues
dependency-ready parity slices until both trackers are complete and
revalidated; only then does the exhaustive Laravel framework test-suite port
begin.

## Verification Policy

- Strict TDD: failing test → implement → green → refactor.
- No feature is "done" by declaration; behavioral evidence is required.
- Parity review compares layout, lifecycle, architecture, error semantics,
  command organization, and implementation logic — not just exported names.
- Progress tracking lives in [`LARAVEL_FEATURE_PARITY_TODO.md`](./LARAVEL_FEATURE_PARITY_TODO.md).
