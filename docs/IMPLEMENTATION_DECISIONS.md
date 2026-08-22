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
- **Core contract:** report filtering, log levels, context, deduplication,
  reportable/renderable callbacks, debug gating, HTTP conversion, HTML/JSON
  negotiation, safe production responses, and testing fakes remain framework
  behavior.
- **Optional diagnostics:** stack frames, source context, solutions,
  environment details, and interactive development pages remain optional and
  must never replace the core handler.
- **Dependency rule:** `exceptionite` is not source-verified as a maintained
  dependency and must not be added by assumption. Evaluate any renderer for
  maintenance, security, API, and replacement cost before adoption. Jinja2 and
  Python traceback/inspect primitives may back an owned renderer.
- **Status:** Future parity slice; current `Handler.py` remains incomplete.

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

- **Decision:** Mirror Laravel provider ownership: `port/pyjinx/` supplies
  application providers; `port/framework/` supplies framework default and
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
