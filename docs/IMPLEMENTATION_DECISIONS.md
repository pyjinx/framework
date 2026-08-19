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
