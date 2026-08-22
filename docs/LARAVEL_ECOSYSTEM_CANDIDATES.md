# Laravel Ecosystem Candidate Program

Reference: `https://www.bacancytechnology.com/blog/laravel-ecosystem`

## Purpose

Track optional post-v1 ecosystem packages to keep core `pyjinx/framework` small while enabling Laravel-style ecosystem parity where useful.

The expanded ecosystem inventory and commercial planning matrix is maintained
in [`ECOSYSTEM_REVENUE_MODEL.md`](./ECOSYSTEM_REVENUE_MODEL.md).


## Current status

- **Initiation date:** 2026-08-19
- **Phase:** Post-v1 expansion wave
- **Candidate count (initial):** 6 deferred

- Auth + API tokens / OAuth helpers (deferred)
- Notification channels (deferred)
- Broadcasting / realtime events (deferred)
- Task scheduling extensions (deferred)
- Queue worker UX / dashboards (deferred)
- Testing helpers and developer diagnostics extensions (deferred)
- **Livewire-compatible reactive components** (deferred; open adapter plus
  optional premium components, hosting, and support)
- **Inertia-compatible SPA bridge** (deferred; React/Vue/Svelte adapters plus
  optional starter kits, hosting, and support)
- **Forge/Cloud/Vapor/Envoyer-style deployment services** (deferred)
- **Nova/Spark/Nightwatch/Herd-style commercial products** (deferred)

## Admission criteria (per candidate)

1. Core contract needed by current feature slice
2. Minimal coupling strategy
3. TDD-first rollout plan
4. Quality counters updated (performance issues, code smell, memory-leak risk)

## Exit criteria (first wave)

- Candidate package docs, install path, and test coverage are added before release.
- Each candidate explicitly documents what is intentionally out-of-scope.
