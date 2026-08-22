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
   - For this codebase, use the `software-engineering-handbook` guidance as the process contract.

3. **Revalidation before release**
   - For every component currently `[x]` or `[~]` in `LARAVEL_FEATURE_PARITY_TODO.md`, rerun implementation/rewrite if behavior is incomplete for the acceptance target.
   - Add/retain tests that cover the promoted contract before release.

4. **Evidence-first gates**
   - No capability is marked complete without evidence in acceptance notes.
   - Behavioral checks must be attached to the relevant roadmap and implementation slices.

5. **Quality-risk accounting (performance/code smell/memory)**
   - At each planning checkpoint, count and document:
     - performance issues,
     - code smells,
     - memory leak risks,
     and treat those counts as first-class blockers alongside feature gaps.
   - Escalation is mandatory if any bucket is high risk or unbounded.

- Canonical feature baseline: `https://api.laravel.com/docs/13.x/index.html`
- Laravel ecosystem candidates: `./LARAVEL_ECOSYSTEM_CANDIDATES.md`
- Internal status tracker: `./LARAVEL_FEATURE_PARITY_TODO.md`
- Implementation execution plan: `./IMPLEMENTATION_PLAN.md`
- Roadmap: `./ROADMAP.md`

## 2026-08-22 — Laravel Prompts-compatible terminal UI boundary

- **Decision:** Use `prompt_toolkit` for interactive prompt behavior and
  `Rich` for terminal presentation behind a PyJinx-owned console prompt
  boundary.
- **Rationale:** Laravel Prompts provides interactive text, textarea, number,
  password, confirm, select, multiselect, suggest, search, pause, forms,
  tables, spinners, progress, and task output. `prompt_toolkit` supplies the
  input/editing/validation/navigation primitives; `Rich` supplies tables,
  styled output, progress, spinners, and live task presentation.
- **Boundary:** Commands MUST depend on PyJinx prompt/output APIs, not directly
  on either third-party library. Non-interactive and CI fallback behavior,
  validation, cancellation, and testing fakes remain PyJinx-owned contracts
  ported from Laravel Prompts.
- **Status:** Decision only; implementation remains in the Laravel console
  parity queue. No dependency is added until its focused parity slice begins.

## 2026-08-22 — Laravel error handling and Ignition-compatible diagnostics

- **Decision:** Port Laravel's core exception reporting/rendering lifecycle
  first, then provide an optional Veyra development error renderer inspired by
  Spatie Laravel Ignition.
- **Core contract:** report filtering, log levels, context, deduplication,
  reportable/renderable callbacks, debug gating, HTTP exception conversion,
  HTML/JSON negotiation, safe production responses, and testing fakes remain
  framework-owned behavior.
- **Optional diagnostics:** stack frames, source context, solutions,
  environment details, and interactive development pages belong behind an
  optional package boundary; they must never replace the core handler.
- **Dependency rule:** `exceptionite` is not currently source-verified as a
  maintained dependency and must not be added by assumption. Evaluate any
  Python renderer against maintenance, security, API, and replacement-cost
  criteria before adoption. Jinja2 and Python traceback/inspect primitives may
  back the first owned renderer.
- **Status:** Future parity slice; current `Handler.py` is not equivalent and
  must remain visibly incomplete in the tracker.

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
