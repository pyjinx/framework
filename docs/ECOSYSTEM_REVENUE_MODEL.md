# Laravel Ecosystem Revenue Model and Veyra Opportunities

## Purpose

This document maps monetized Laravel ecosystem products and identifies future
Veyra revenue opportunities. It is planning evidence, not an implementation
claim. Official product pages and terms are authoritative for current pricing;
third-party articles are discovery sources only.

Discovery sources reviewed:

- [LaraCopilot: 50+ Best Laravel Ecosystem Tools for 2026](https://laracopilot.com/blog/best-laravel-ecosystem-tools/)
- [Bacancy: Laravel Ecosystem Guide](https://www.bacancytechnology.com/blog/laravel-ecosystem)

Official pricing references reviewed:

- [Forge pricing](https://laravel.com/forge/pricing)
- [Cloud pricing](https://laravel.com/cloud/pricing)
- [Vapor](https://vapor.laravel.com/)
- [Nova](https://nova.laravel.com/)
- [Nightwatch pricing](https://nightwatch.laravel.com/pricing)
- [Herd](https://herd.laravel.com/)
- [Spark](https://spark.laravel.com/)
- [Envoyer](https://envoyer.io/)

Prices change. Any commercial decision MUST recheck official pricing, terms,
regional taxes, payment processing, infrastructure costs, and support
commitments before launch.

## Product and revenue matrix

| Laravel product/category | Current model | Veyra opportunity | Priority | Boundary |
|---|---|---|---:|---|
| Laravel Forge | Flat monthly plans; cloud-provider/server costs separate | **Veyra Forge**: server provisioning, deployment, SSL, monitoring, teams | P0 | Separate hosted product; not framework core |
| Laravel Cloud | Plan fee plus usage-based compute/storage/network costs | **Veyra Cloud**: managed Veyra hosting, autoscaling, preview environments, queues | P1 | Hosted infrastructure and billing platform |
| Laravel Vapor | Platform subscription plus AWS infrastructure charges | **Veyra Vapor**: serverless deployment control plane for AWS/GCP/Azure | P2 | Cloud adapter/control plane; provider costs pass through |
| Laravel Nova | Commercial per-project or unlimited-project license with update renewals | **Veyra Nova**: commercial admin panel and back-office UI | P1 | Licensed package; core framework remains open |
| Laravel Nightwatch | Free tier plus event/retention-based SaaS plans and enterprise | **Veyra Nightwatch**: application monitoring, traces, jobs, queries, exceptions | P1 | SaaS observability; privacy/retention controls required |
| Laravel Herd | Free local environment plus Pro/team licenses | **Veyra Herd**: local runtime, project manager, database/mail tooling | P2 | Desktop product; platform-specific support cost |
| Laravel Spark | Paid starter-kit license by project scope | **Veyra Spark**: SaaS starter, billing, teams, customer portal | P1 | Commercial starter package; payment providers remain separate |
| Laravel Envoyer | Monthly deployment subscription; Forge now overlaps for new subscriptions | **Veyra Envoyer**: multi-server zero-downtime deployment service | P2 | Avoid duplicate offering with Veyra Forge |
| Laravel Shift | Paid automated upgrade/service workflow | **Veyra Shift**: automated framework upgrade and parity migration service | P2 | Service/SaaS; preserve source-diff evidence |
| Laravel AI/Boost ecosystem | Framework/API package; provider/model usage billed externally | **Veyra AI/Boost**: project-aware coding and migration tools | P2 | Provider costs and privacy remain explicit |
| Laravel Livewire | Open-source reactive PHP UI framework; plugin/commercial ecosystem | **Veyra Livewire**: server-driven reactive components for Python | P1 | Open core; paid components, hosting, support, enterprise |
| Laravel Inertia | Open-source backend/frontend bridge; frontend costs separate | **Veyra Inertia**: server-driven SPA bridge for React/Vue/Svelte | P1 | Open adapter; paid kits, hosting, support, enterprise |
| Laravel Breeze/Jetstream | Free/open-source starter kits | Veyra starter kits, premium templates, support, hosted onboarding | P1 | Core authentication remains free |
| Horizon/Telescope/Pulse/Reverb | Primarily open-source packages/services | Hosted dashboards, enterprise support, managed infrastructure | P1 | Open contracts; optional hosted data plane |
| Sanctum/Passport/Socialite/Cashier | Open-source integrations; provider fees external | Veyra equivalents plus optional managed auth/billing | P1 | Provider fees and compliance remain external |
| Sail/Pint/Prompts/Dusk/Pest | Open-source developer tooling | Premium desktop/CI/team workflows where justified | P2 | Basic developer workflow remains free |
| Filament/Backpack/Orchid/admin ecosystem | Open-core/admin products and plugins | Veyra admin ecosystem and verified plugin marketplace | P2 | Marketplace governance required |
| Spatie/community packages | Open-source packages and services | Veyra registry, verified plugins, support plans | P3 | Respect licenses; do not fork casually |

## Recommended Veyra commercial ladder

### Free open-source core

- Veyra framework.
- CLI and generators.
- ORM, routing, validation, queues, auth, and testing contracts.
- Basic Livewire/Inertia-compatible adapters.
- Local development and self-hosted deployment support.

Commercial pressure MUST NOT weaken Laravel-compatible core behavior.

### Paid developer products

1. **Veyra Forge** — server management and deployment.
2. **Veyra Nova** — commercial admin panel.
3. **Veyra Spark** — SaaS starter and billing portal.
4. **Veyra Livewire Pro** — premium component library and team tooling.
5. **Veyra Inertia Kits** — premium React/Vue/Svelte starter kits.
6. **Veyra Shift** — automated Laravel/PyJinx/Veyra upgrade migrations.

### Hosted services

1. **Veyra Cloud** — managed hosting with plan plus usage billing.
2. **Veyra Nightwatch** — event/retention-based observability SaaS.
3. **Veyra Vapor** — cloud/serverless deployment control plane.
4. **Veyra Envoyer** — multi-server zero-downtime deployment where Forge does
   not already cover the use case.

### Enterprise revenue

- Support contracts and SLAs.
- Private networking and dedicated infrastructure.
- Managed migrations and architecture reviews.
- Compliance/security packages.
- Organization/team controls.
- Private package registries and internal deployment platforms.
- Training and certification.

## Revenue guardrails

- Never weaken or paywall Laravel-parity core behavior.
- Do not claim hosted reliability before resource, failure, backup, and
  incident-response evidence exists.
- Separate subscriptions, usage pass-through, payment processor fees,
  cloud-provider charges, licenses, support, and services in billing design.
- Use explicit retention, redaction, deletion, and tenant-isolation rules for
  hosted diagnostics and observability.
- Every commercial product gets its own contract, dependency boundary, tests,
  pricing document, and migration policy.
- Livewire and Inertia remain ecosystem adapters; neither replaces the parity
  core.

## Admission order

1. Complete Laravel framework parity and current contract tests.
2. Stabilize the Veyra namespace/CLI migration after parity work.
3. Ship free starter kits and Livewire/Inertia adapters.
4. Build the Forge-like deployment control plane.
5. Build Nova-like admin and Spark-like SaaS starter products.
6. Add Cloud/Nightwatch/Vapor/Envoyer hosted products with operations,
   billing, support, and security owners.
7. Add marketplace and enterprise programs after package governance exists.
