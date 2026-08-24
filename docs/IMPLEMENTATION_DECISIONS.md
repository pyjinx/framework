# PyJinx Implementation Decisions

## 2026-08-19 — Greenfield execution posture

- **Decision:** Treat this repository as a greenfield re-implementation baseline, not a completed product.
- **Rationale:** The current codebase began as a hobby/PoC and includes partial/provisional implementations.
- **Outcome:** Existing marks in `LARAVEL_FEATURE_PARITY_TODO.md` are planning evidence only; they are not release-complete.

## Accepted rules (binding)

1. **No partial completion by declaration**
   - No backlog item is complete solely from declaration or file presence.
   - Every promoted item requires behavioral evidence.
2. **Strict TDD for all new/changed behavior**
   - Write a failing test first, implement to green, then refactor.
   - `software-engineering-handbook` is the process contract.
3. **Revalidation before release**
   - Revalidate every `[x]` or `[~]` component before release.
   - Add or retain tests covering the promoted contract.
4. **Evidence-first gates**
   - No capability is complete without acceptance evidence.
5. **Quality-risk accounting**
   - Track performance issues, code smells, and memory-leak risks at every
     planning checkpoint; high or unbounded risk blocks promotion.

- Canonical feature baseline: `https://api.laravel.com/docs/13.x/index.html`
- Laravel ecosystem candidates: `./LARAVEL_ECOSYSTEM_CANDIDATES.md`
- Internal status tracker: `./LARAVEL_FEATURE_PARITY_TODO.md`
- Implementation execution plan: `./IMPLEMENTATION_PLAN.md`
- Roadmap: `./ROADMAP.md`

## 2026-08-22 — Laravel Prompts-compatible terminal UI boundary

- **Decision:** Use `prompt_toolkit` for interactive prompt behavior and
  `Rich` for terminal presentation behind a PyJinx-owned console prompt
  boundary.
- **Rationale:** Laravel Prompts provides text, textarea, number, password,
  confirm, select, multiselect, suggest, search, pause, forms, tables,
  spinners, progress, and task output. `prompt_toolkit` supplies input,
  editing, validation, navigation, and completion; `Rich` supplies tables,
  styled output, progress, spinners, and live task presentation.
- **Boundary:** Commands depend on PyJinx prompt/output APIs, not directly on
  either third-party library. Non-interactive fallback, validation,
  cancellation, testing fakes, and output contracts remain PyJinx-owned.
- **Status:** Decision only; implementation remains in the console parity queue.

## 2026-08-22 — Laravel error handling and Ignition-compatible diagnostics

- **Decision:** Port Laravel's core exception reporting/rendering lifecycle
  first, then provide an optional Veyra development renderer inspired by
  Spatie Laravel Ignition.
- **Implemented bounded core:** `Handler.report` now applies explicit ignore
  classes, duplicate-instance suppression, configured log levels, exception
  context callbacks, report callbacks, and a standard Python logger fallback.
  `Handler.render` produces framework-owned `ExceptionResponse` values, uses
  an explicit JSON override or the request's preferred `Accept` media type,
  preserves declared `status_code` and mapping-like `headers`, and lets a
  final response callback post-process the result. The HTTP kernel reports and
  renders uncaught `Exception` values at its request boundary.
- **Safe response policy:** production 500 responses contain only `Server
  Error`; production declared HTTP-status responses retain their message.
  Debug HTML escapes exception text and trace output; debug JSON contains the
  message, Python exception class, and formatted traceback. Optional debug
  detail generation is isolated in `Exceptions/Diagnostics.py`.
- **Dependency rule:** no Ignition, Symfony renderer, or unverified
  `exceptionite` dependency was added. `DevelopmentDiagnostics` uses only
  Python `traceback` and `html`.
- **Source mapping:** Laravel 13 `Foundation/Exceptions/Handler.php`
  `report`/`shouldntReport` (425–545), `render`/response finalization
  (694–750), `shouldReturnJson` (912–930), and JSON conversion
  (1107–1134); `Foundation/Configuration/Exceptions.php` forwarding methods
  (27–79, 118–150, 195–229); and
  `Foundation/Configuration/ApplicationBuilder.php::withExceptions`
  (394–408).
- **Residual parity gaps:** Laravel exception mapping, `dontReportWhen`,
  `stopIgnoring`, exception throttling, exception-provided reporting control,
  validation/authentication/redirect conversion, Symfony HTTP exceptions and
  error views, `Responsable`, console rendering, exact `expectsJson`
  semantics, logger-channel/context parity, and full reportable-handler API
  remain unported. `ExceptionResponse`, `status_code`/mapping `headers`, and
  first-preferred-`Accept` JSON negotiation are explicit Python boundaries to
  replace only with a verified shared HTTP response contract.

## 2026-08-22 — Python-only framework and documentation product

- **Decision:** Keep the Veyra framework core and contributor workflow
  Python-only; Rust/PyO3 is not a required optimization or build path.
- **Rationale:** One-language contribution improves readability,
  maintainability, debuggability, packaging simplicity, and open-source
  participation. Performance work remains measurement-driven and Python-first.
- **Documentation:** Build a public website and Laravel-quality API reference
  covering every promoted class, method, contract, lifecycle, command, and
  compatibility boundary.
- **Legal clarity:** The website must state that Veyra is highly inspired by
  and behaviorally ported from Laravel where applicable, without implying
  ownership, endorsement, or affiliation. Required upstream notices remain.

## 2026-08-22 — Laravel broadcasting and Veyra Reverb boundary

- **Decision:** Port Laravel broadcasting contracts and event lifecycle before
  implementing a WebSocket server. Provide `log`, `null`, self-hosted
  Reverb-compatible, Pusher, and Ably drivers behind an owned manager.
- **Prerequisites:** Complete ASGI WebSocket lifecycle, events/listeners,
  queues, channel authorization, HTTP authentication, and client protocol
  contracts first. The synchronous WSGI server is not a WebSocket runtime.
- **Boundary:** Core broadcasting owns event names/data, channel authorization,
  public/private/presence channels, queue/transaction ordering, fakes, and
  driver contracts. Provider SDKs and hosted transport stay behind adapters.
- **Ecosystem:** Future open-source `veyra-broadcasting`/Reverb-compatible
  self-hosting and a paid managed WebSocket service remain optional products.

## 2026-08-22 — Laravel provider ownership and package auto-discovery

- **Decision:** Mirror Laravel provider ownership: `pyjinx/starter/` supplies
  application providers; `framework/` supplies framework default and
  framework command providers.
- **Auto-discovery:** Port the Composer equivalent for package provider
  metadata, merge discovered providers with configured providers, and support
  eager/deferred loading with a cached provider manifest.
- **Application boundary:** `AppServiceProvider` contains only
  application-specific bindings and boot behavior. It must not be a catch-all
  for framework database, view, routing, console, or migration services.
- **Commands:** Framework commands belong to framework console providers;
  application commands belong to the application console registration path.
- **Status:** Current PyJinx has partial manual provider loading; this remains
  a source-faithful parity slice.

## 2026-08-22 — Application TDD and package naming boundary

- **Decision:** Generated projects follow a strict pytest-based TDD workflow,
  with `tests/Unit`, `tests/Feature`, deterministic fixtures, database reset
  support, HTTP assertions, model factories, seeders, fakes, and controlled
  date/time fixtures.
- **Commands:** `uv run pytest` is the authoritative application test runner;
  the `loom new hello-world` project creator may add a test convenience wrapper
  that delegates to pytest rather than creating a second test system.
- **Test boundary:** Generated application tests validate application behavior;
  framework parity tests remain in the framework repository. The exhaustive
  Laravel framework test-suite port begins only after parity completion.
- **Current naming:** `pyjinx` is the temporary framework distribution,
  `pyjinx-starter` is the temporary skeleton distribution, and
  `pyjinx-installer` is the future installer distribution. The dedicated Veyra
  migration will use `veyra`, `veyra-starter`, and `veyra-installer`.

## 2026-08-22 — Carbon-equivalent date and time boundary

- **Decision:** Use Pendulum as the closest Python equivalent to Laravel
  Carbon for timezone-aware datetime, date arithmetic, parsing, formatting,
  durations, humanization, and deterministic test clocks.
- **Boundary:** Pendulum remains behind a PyJinx-owned date/time adapter,
  rather than leaking third-party types throughout framework or application
  code. The adapter must preserve Laravel-compatible serialization and
  timezone semantics.
- **SQLite warning policy:** Pendulum adoption must be paired with an
  explicit SQLAlchemy/SQLite datetime binding and hydration strategy. Warning
  filters or blanket suppression are prohibited; the deprecated implicit
  sqlite3 datetime adapter must be eliminated with round-trip evidence.

## 2026-08-23 — Next.js website and documentation platform

- **Decision:** Build the public website with Next.js App Router and use
  Fumadocs (`fumadocs-mdx`, `fumadocs-core`, `fumadocs-ui`,
  `fumadocs-openapi`, and Shiki) for documentation.
- **Routes:** The main marketing site owns `/`; handwritten Markdown/MDX
  documentation lives under `/docs`; generated API reference pages live under
  `/docs/api` or versioned `/docs/api/v1` routes.
- **Source boundary:** Narrative docs remain hand-authored MDX. API pages are
  generated from OpenAPI JSON/YAML produced from the Python framework/API
  contract, avoiding duplicated endpoint definitions.
- **Search/versioning:** Start with Fumadocs' Orama-based search and explicit
  version folders/routes. Move released versions to immutable deployments or
  subdomains when release freezing is required.
- **Alternatives:** Nextra is weaker for integrated OpenAPI; Docusaurus is
  mature but not Next.js; Mintlify has managed-hosting lock-in. Scalar may be
  added later only for a standalone API explorer.
- **Status:** Research-approved architecture; website implementation remains
  a separate workspace and delivery stream.

## 2026-08-23 — Framework CLI and global installer identities

- **Decision:** Keep the global installer executable as `pyjinx`, with
  `pyjinx new hello-world` creating a project. Use `loom` only inside the
  generated project for `loom serve`, `loom migrate`, and `loom test`, matching
  Laravel's Artisan boundary.
- **Installer boundary:** The `pyjinx-installer` distribution exposes the
  global `pyjinx` executable. The project-local starter executable is `loom`.
- **Migration:** After the Veyra rename, the installer distribution becomes
  `veyra-installer` and its global command becomes `veyra`; the project-local
  executable remains `loom`.
- **Compatibility:** Do not retain a global `loom` alias. The current starter
  `pyjinx` script is replaced by `loom` only for generated project commands.

## 2026-08-23 — Laravel 13 Database/Eloquent API inventory

- **Decision:** Establish a complete source-first Database/Eloquent inventory
  before implementing another ORM behavior. The tracked artifact is
  `docs/DATABASE_ELOQUENT_API_INVENTORY.md`.
- **Scope:** Compare every class/interface/trait and public method under
  `references/framework/src/Illuminate/Database/` against
  `framework/Illuminate/Database/`, with Laravel 13 API documentation as the
  public-contract reference.
- **Baseline:** Laravel contains 250 files, 355 classes/interfaces/traits, and
  2,196 public method declarations in this namespace. PyJinx currently contains
  27 files, 31 classes, and 512 public methods/functions. The inventory is
  therefore a gap map, not a parity claim.
- **Status policy:** `implemented` means a named counterpart exists but still
  needs evidence; `partial` means only a behavior slice exists; `missing` means
  no counterpart; `blocked` is reserved for an authoritative contract that
  cannot be implemented without inventing behavior.
- **Known blocker:** SQLite JSON-overlap methods remain blocked while the pinned
  Laravel SQLite grammar lacks `compileJsonOverlaps`.
- **Runtime mirror evidence:** The `starter/framework/` submodule is restored
  at the canonical inventory revision. The inventory, tracker, and decision
  documents compare byte-identically between canonical and runtime docs.
- **Acceptance:** Each selected implementation slice must have Laravel source
  mapping, strict red-green-refactor tests, synchronized canonical/runtime
  framework state, and warning-as-error regression evidence.

## 2026-08-23 — SQLite connection configuration parity slice

- **Decision:** Implement the Laravel SQLite connection configuration boundary
  before extending other drivers. Configuration URLs are parsed into native
  options, URL-derived values override individual configuration values, and
  SQLite-specific options are applied on each DBAPI connection.
- **Implemented:** driver aliases, SQLite relative/absolute/memory paths,
  boolean/numeric query values, `foreign_key_constraints`, `busy_timeout`,
  `journal_mode`, `synchronous`, `transaction_mode`, custom pragmas,
  reconnect fingerprints for those options, the `ConnectionResolver`
  registered/default lookup API, distinct SQLite `read`/`write` configuration
  overrides, and suffixed session resource normalization.
- **Non-SQLite boundary:** MySQL, MariaDB, PostgreSQL, and SQL Server remain
  advertised as Laravel-supported driver names but are not implemented by the
  SQLite backend. Strict-mode and driver-specific connector behavior remain
  partial and must not be invented without an implemented backend.
- **Implemented:** the initial SQLAlchemy-backed `Connection` adapter exposes
  Laravel-shaped metadata, config, prefix, PDO boundary, reconnect, disconnect,
  purge, and engine-resource methods. DatabaseManager now returns adapters,
  propagates `setReconnector`, and query/schema integration explicitly binds
  underlying SQLAlchemy engines.
- **Implemented:** the adapter also exposes parameterized SQLite
  `select`, `select_one`, `scalar`, `insert`, `update`, `delete`, `statement`,
  `affecting_statement`, and `unprepared` operations, plus read/direct PDO
  metadata and driver/title/server-version accessors.
- **Implemented:** adapter listeners receive manager `QueryExecuted` events
  and before-executing callbacks receive SQL/bindings before adapter operations,
  while the underlying SQLAlchemy engine remains the execution boundary.
- **Residuals:** Complete Laravel `Connection`/PDO method coverage, connector
  events beyond adapter query/before callbacks, full normalized exception/
  lifecycle behavior, strict mode, and non-SQLite connector behavior remain
  open or intentionally blocked.
- **Evidence:** focused connection/adapter metadata/parser/resolver/read-write/
  session/transaction/reconnector/SQL-operation/event tests passed (66 total);
  warning-as-error full starter suite passed (207 tests).

## 2026-08-24 — Database transaction manager parity slice

- **Implemented:** `DatabaseTransactionRecord` stores commit and rollback
  callbacks with nested parent relationships. `DatabaseTransactionsManager`
  tracks pending/committed records, stages commits, rolls back records, and
  exposes callback applicability and record accessors.
- **Boundary:** The manager is integrated with DatabaseManager's transaction
  context for root/nested begin, commit, and rollback record transitions. The
  application event dispatcher receives `QueryExecuted`; adapters support
  before-executing callbacks and cumulative query-duration thresholds. It
  remains limited to SQLite/Python transaction resources; no non-SQLite
  behavior is invented.
- **Evidence:** transaction-manager, query-duration, application-event, and
  manager integration tests passed (4 focused manager tests); warning-as-error
  full starter suite passed (212 tests).
