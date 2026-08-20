# Laravel 13.x Feature Coverage — Todo Checklist

Source reference:
- Laravel API surface index used: `https://api.laravel.com/docs/13.x/index.html`

## Reference and snapshot metadata

- **Last reviewed:** 2026-08-20
- **Feature checklist:** 11/38 implementation-present, 4/38 partial, 23/38 not started
- **Exact parity audit:** 0/38 verified exact; 15/38 partial; 23/38 not started
- **Audit method:** compare the local Laravel 13 reference projects and framework source, inspect the Laravel 13.x API namespace index, and run focused PyJinx behavior checks where a runtime exists.
- **Audit conclusion:** every implementation-present area remains provisional; no area currently has evidence for 100% Laravel 13 parity.
- **Quality-risk categories:** 3 (performance, code smell, memory leak)
-  - Performance issues: 0 identified (pending baseline audit)
-  - Code smells: 0 identified (pending baseline audit)
-  - Memory leak risks: 0 identified (pending baseline audit)
- **Source of truth:** This file is the tracked feature coverage backlog used by roadmap and planning updates.
- **Provisional status:** This backlog reflects a starting PoC baseline. Marking an area `[x]` or `[~]` is not a release completion signal; it only indicates current implementation presence that must be revalidated.

## Legend

- **[x]** = implementation exists in current codebase only; production completion requires revalidation and evidence.
- **[~]** = partial implementation in current codebase; behavior requires proof before release.
- **[ ]** = not implemented

## Coverage checklist

1. [x] **Foundation lifecycle** (`Illuminate\Foundation`)
   - `Foundation.Application`, bootstrap flow, providers, and HTTP/console kernel classes are present.
   - Gaps: full Laravel application bootstrap policy, maintenance mode, exception rendering parity, and service registration lifecycle guarantees still incomplete.

2. [x] **Container / service resolver** (`Illuminate\Container`)
   - Binding API, singleton/scoped bindings, aliases, contextual resolution, constructor injection, extenders, tags, rebinding, parameter overrides, and structured resolution errors are present.
   - Gaps: full Laravel closure/contextual edge parity, attribute bindings, method bindings, and complete resolution semantics.

3. [~] **Routing** (`Illuminate\Routing`)
   - `Router`, route groups, route names/middleware chaining, URL generation, resource/API resource routes, route caching, and route collection/dispatch.
   - Gaps: implicit model binding, advanced nested resource conventions, and full route verb edge cases.

4. [x] **HTTP layer** (`Illuminate\Http`)
   - Request wrapper, ASGI/WSGI adapters, pipeline entry path, request bags.
   - ASGI adapter currently minimal and request lifecycle is intentionally early-stage.

5. [x] **Middleware pipeline** (`Illuminate\Pipeline` + `Router` middleware hooks)
   - Global and group middleware primitives exist.
   - Gaps: extensive middleware built-ins beyond `HandleCors` and robust error handling wrappers.

6. [~] **Validation** (`Illuminate\Validation`)
   - Rule system and validator response exist with multiple built-in rules.
   - Missing: full rule parity, custom message/catalog parity, and complete request-form integration.

7. [x] **Configuration** (`Illuminate\Config`)
   - `Repository` + bootstrap config loading and environment file handling.

8. [x] **Events / dispatcher** (`Illuminate\Events`)
   - Basic dispatcher, event service provider, and base dispatchable model.

9. [x] **Collections** (`Illuminate\Collections`)
   - Helpers and collection primitives are present.

10. [x] **Conditionable / macro-style fluent helpers** (`Illuminate\Conditionable`)
    - `Conditionable` trait-like helper exists.

11. [x] **Support utilities & facades** (`Illuminate\Support`)
    - `ServiceProvider`, facades base, `Str`, higher-order helpers.

12. [x] **Logging** (`Illuminate\Log`)
    - Logger + log manager + service provider.

13. [x] **View** (`Illuminate\View`)
    - Jinja-backed view factory + provider.

14. [~] **Auth** (`Illuminate\Auth`)
    - Gate and middleware scaffolding; user contract placeholder.
    - Missing: guard manager, provider adapters, session/web authentication flows.

15. [ ] **Database / ORM** (`Illuminate\Database` / `Illuminate\Database\Eloquent`)
    - Only a small `Serializable` utility exists; no SQLAlchemy-backed models/migrations/query builder.

16. [ ] **Queueing** (`Illuminate\Queue`)
    - No queue contracts/workers/failed job stores implemented.

17. [ ] **Cache** (`Illuminate\Cache`)
    - No cache repository, stores, lock/rate limiting support.

18. [ ] **Session** (`Illuminate\Session`)
    - No session middleware/store/driver integration.

19. [ ] **Cache/Session/Cookie security** (`Illuminate\Cookie`)
    - Cookie facade/IO not fully implemented.

20. [ ] **Mail** (`Illuminate\Mail`)
    - Not implemented.

21. [ ] **Notifications** (`Illuminate\Notifications`)
    - Not implemented.

22. [ ] **Broadcasting / events bridges** (`Illuminate\Broadcasting`)
    - Not implemented.

23. [ ] **Filesystem / storage** (`Illuminate\Filesystem`)
    - Not implemented.

24. [ ] **Redis / cache/store clients** (`Illuminate\Redis`)
    - Not implemented.

25. [ ] **Hashing / encryption** (`Illuminate\Hashing`, `Illuminate\Encryption`, `Illuminate\Contracts\Encryption`)
    - Not implemented.

26. [ ] **Localization / translation** (`Illuminate\Translation`)
    - Not implemented.

27. [ ] **Pagination** (`Illuminate\Pagination`)
    - Not implemented.

28. [ ] **JSON schema / typed DTO schema** (`Illuminate\JsonSchema`)
    - Not implemented.

29. [ ] **Testing stack** (`Illuminate\Testing`, `Foundation\Testing`)
    - No dedicated test helpers, HTTP/API testing DSL, or fake utilities.
30. [~] **Console command surface (`pyjinx` parity)** (`Illuminate\Console` + `Foundation\Console` command modules)
    - Framework includes command bootstrap, grouped list/help output, `serve`, `make:controller`, `route:list`, `route:cache`, and `route:clear`.
    - Missing: broader Artisan command suite (`make:*`, `migrate*`, queue commands, cache/config commands, tinker/about/up/down).

31. [ ] **Scheduling / process orchestration** (`Illuminate\Console\Scheduling`, `Illuminate\Process`)
    - Not implemented.

32. [ ] **HTTP client** (`Illuminate\Http\Client`)
    - Not implemented.

33. [ ] **Image support** (`Illuminate\Image`)
    - Not implemented.

34. [ ] **Pagination / JSON:API resources** (`Illuminate\Http\Resources`, `Foundation\Http\Resources`)
    - Not implemented.

35. [ ] **Concurrency / worker abstractions** (`Illuminate\Concurrency`)
    - Not implemented.

36. [ ] **Foundation boot hooks for cloud/admin/testing extensions** (`Foundation\Cloud`, `Foundation\Queue`, advanced `Foundation\Validation`)
    - Not implemented.

37. [ ] **Hash/crypto/authenticated policy hardening features** (`Illuminate\Auth\Passwords`, `Auth\Notifications`, `Auth\Middleware` full behavior)
    - Not implemented.

38. [ ] **Contract namespaces beyond current baseline** (`Illuminate\Contracts\*`)
    - Only partial contracts exist for Foundation, Container, Http, Support.

## Revalidation result — 2026-08-20

No feature is currently verified as 100% Laravel 13 parity.

| Items | Revalidation result | Evidence |
|---|---|---|
| 1–14 | Partial implementation; not exact parity | Python source namespaces exist, but lifecycle, error, middleware, adapter, provider, validation, and auth behavior differ materially from the Laravel framework reference. |
| 15–29 | Not started or no equivalent subsystem | The corresponding Laravel namespaces are absent from `Illuminate/`; focused namespace inventory confirmed no Database, Queue, Cache, Session, Cookie, Mail, Notifications, Broadcasting, Filesystem, Redis, Hashing, Encryption, Translation, Pagination, JsonSchema, or Testing implementation. |
| 30 | Partial implementation; not exact parity | `pyjinx`, `serve`, grouped command listing, and `make:controller` exist; the broader Artisan command surface is absent. |
| 31–38 | Not started or incomplete contract surface | Scheduling, process, HTTP client, image, JSON API resources, concurrency, extension hooks, password hardening, and most Laravel contracts are absent or incomplete. |

The audit used `references/laravel/`, `references/laravel-demo/`, and the Laravel framework source as authoritative references. `references/python-laravel/` remains historical context only and is not an implementation authority.

## Detailed remaining implementation queue

### Resume point

Next implementation area: finish the Database / ORM foundation and continue the Eloquent port. The DB manager, SQLAlchemy/Alembic boundary, migrations, raw query builder, DB facade, initial User model, casts, and model events exist only as early slices; they are not full Laravel parity.

### Database and Eloquent

- [ ] Expand the Laravel 13 Database/Eloquent API inventory down to every class and public method.
- [ ] Complete connection configuration parity: default/named connections, URLs, prefixes, strict mode, read/write connections, reconnect and purge behavior.
- [ ] Complete database manager/resolver parity: connection switching, transactions, nested transactions, retries, query listeners, and normalized exceptions.
- [ ] Complete raw query builder parity: insert/update/delete, where variants, joins, aggregates, grouping, ordering, pagination, chunking, cursor reads, upserts, locks, raw bindings, and SQL generation.
- [ ] Complete schema builder parity: tables, columns, indexes, constraints, foreign keys, renames, drops, dialect behavior, and SQLite limitations.
- [ ] Complete migration parity: Laravel-shaped files and paths, batches, status, rollback step/batch, reset, refresh, fresh, pretend, paths, seed integration, and failure recovery.
- [ ] Complete Eloquent model metadata: table, connection, keys, UUID/ULID, incrementing, timestamps, date formats, guarded/fillable, hidden/visible, appends, and serialization.
- [ ] Complete Eloquent attribute behavior: dirty tracking, original values, attribute accessors/mutators, casts, custom casts, encrypted casts, hashed casts, JSON casts, date casts, and mass-assignment exceptions.
- [ ] Complete Eloquent CRUD semantics: find, find-or-fail, first, first-or-fail, create, force-create, save, update, delete, restore, touch, increment, decrement, upsert, and quiet variants.
- [ ] Complete Eloquent model events: boot/booted, retrieved, saving/saved, creating/created, updating/updated, deleting/deleted, restoring/restored, observers, dispatch suppression, and event ordering.
- [ ] Complete Eloquent builders and collections: scopes, macros, collection transformations, lazy collections, chunk/cursor, eager loading, lazy loading, and N+1 controls.
- [ ] Complete Eloquent relationships: belongs-to, has-one, has-many, many-to-many, pivot records, through relations, polymorphic relations, touching, eager constraints, and relationship serialization.
- [ ] Complete soft deletes, factories, seeders, pagination, JSON resources, model policies, and model route binding.

### Authentication, sessions, and security

- [ ] Inventory Laravel Auth, Session, Cookie, Encryption, Hashing, Passwords, and Sanctum APIs class by class.
- [ ] Implement session stores, drivers, session middleware, lifecycle cleanup, regeneration, invalidation, and flash data.
- [ ] Implement cookie creation, signing/encryption, SameSite/Secure/HttpOnly behavior, queues, and response integration.
- [ ] Implement CSRF token generation, validation middleware, rotation, exemptions, and error behavior.
- [ ] Implement web session guard, user providers, login/logout, remember-me, user resolution, and guest/auth middleware.
- [ ] Implement Sanctum-style SPA cookie authentication and bearer personal access tokens; do not invent JWT as the Laravel default.
- [ ] Implement password hashing, reset brokers, token expiry, throttling, notifications, and authentication failure semantics.

### Routing and HTTP

- [ ] Complete implicit route model binding after ORM/provider behavior is available.
- [ ] Complete nested resource and singleton resource conventions, parameter naming, scoped bindings, and missing-model behavior.
- [ ] Complete route URL generation: signed URLs, temporary signed URLs, asset URLs, domains, schemes, defaults, encoded parameters, and missing parameters.
- [ ] Complete route caching: cache invalidation, deterministic artifacts, stale-cache behavior, closure restrictions, and cache command parity.
- [ ] Complete HTTP request/response parity: headers, cookies, files, sessions, body parsing, content negotiation, status codes, streaming, redirects, and response sending.
- [ ] Complete ASGI and WSGI adapters with one shared request/response contract and explicit sync/async lifecycle rules.
- [ ] Complete middleware aliases, groups, priority, exclusions, parameterized middleware, short-circuit behavior, and exception handling.
- [ ] Complete validation rules, messages, custom attributes, form requests, authorization hooks, preparation, and validation response parity.

### Configuration, foundation, and support

- [ ] Complete application builder parity: routing callbacks, middleware callbacks, exception callbacks, command loading, provider loading, and runtime separation.
- [ ] Complete environment/config loading, caching, clearing, merge behavior, typed values, missing keys, and config command behavior.
- [ ] Complete service provider registration/boot/deferred provider/rebinding behavior and package discovery boundaries.
- [ ] Complete events/listeners/subscribers, wildcard listeners, queued behavior boundaries, and event dispatch error semantics.
- [ ] Complete container attributes, method bindings, scoped lifecycle integration, extenders, tags, contextual edge cases, and all resolution errors.
- [ ] Complete support utilities, collections, fluent helpers, facades, macros, string/array helpers, and PHP-to-Python behavior mappings.
- [ ] Complete logging channels, stacks, handlers, context, processors, formatting, levels, exception logging, and redaction.
- [ ] Complete view loading, namespaces, composers/creators, shared data, escaping, environment behavior, and response integration.

### Console and operational features

- [ ] Inventory every Laravel Artisan command and option from Laravel 13.
- [ ] Complete `make:*` commands and generator stubs, overwrite policy, namespaces, options, output, and error behavior.
- [ ] Complete migration, database, cache, config, route, view, event, queue, auth, and storage command groups.
- [ ] Complete command input/output semantics, ANSI styles, help, quiet/silent modes, verbosity, interaction, exit codes, and command lifecycle.
- [ ] Complete scheduling, process execution, task mutexes, interrupts, retries, and worker lifecycle.

### Remaining Laravel services

- [ ] Implement cache stores, repositories, locks, tagging, rate limiting, serialization, and cache commands.
- [ ] Implement queues, connectors, jobs, workers, retries, failed jobs, middleware, batches, and queue commands.
- [ ] Implement mail, notifications, channels, templates, transports, fakes, and delivery failure behavior.
- [ ] Implement broadcasting, broadcasters, channel authorization, events, and queue integration.
- [ ] Implement filesystem disks, adapters, visibility, temporary URLs, streams, and storage commands.
- [ ] Implement Redis connections, commands, pipelines, locks, pub/sub, and configuration.
- [ ] Implement translation/localization loaders, pluralization, fallback locales, JSON translations, and missing-key behavior.
- [ ] Implement pagination, API resources, JSON:API resources, links, metadata, and serialization.
- [ ] Implement HTTP client requests, pending requests, retries, middleware, pools, fakes, responses, and exceptions.
- [ ] Implement image, concurrency, process, cloud/admin/testing extension, and remaining foundation namespaces.

### Contracts and acceptance

- [ ] Expand every `Illuminate.Contracts.*` namespace from the Laravel 13 API index.
- [ ] Add contract tests for every promoted public method and observable error.
- [ ] Add integration tests for every lifecycle boundary and cross-component interaction.
- [ ] Add compatibility tests for each supported database driver and declared dependency version.
- [ ] Record every intentional PHP-to-Python deviation with rationale, owner, and removal/review condition.
- [ ] Do not mark any checklist item complete until its full mapped surface has evidence.

### Deferred exhaustive test-suite port

- [ ] Port the complete `laravel/framework/tests/` suite into Python equivalents.
- [ ] Preserve every Laravel test scenario, boundary, failure, lifecycle, and integration assertion.
- [ ] Map PHPUnit/Pest helpers to PyJinx testing helpers without weakening assertions.
- [ ] Run the ported suite per component and against the full framework integration.
- [ ] Track intentional PHP-runtime differences separately from implementation failures.
- [ ] Do not treat this deferred suite port as current coverage until it is implemented and passing.

---

## Action policy

- Keep this checklist as the single source-of-truth for Laravel parity backlog.
- Treat all `[x]`/`[~]` statuses as provisional until revalidated by fresh green tests under strict TDD.
- Keep a per-iteration quality-risk count (performance issues, code smells, memory leak risks) and track deltas in acceptance notes.
- Mark this file as done only when behavior is proven by tests, not by declarations.
- This codebase started as a hobby/PoC; implement from scratch where coverage is required, and enforce full behavior proof for any promoted area.
- For any item moved to `[x]`, file an evidence test case before release in acceptance notes.
- Parity review must compare file/folder layout, lifecycle and dependency architecture, system design, behavior and error semantics, command organization, and implementation logic—not only exported names.
- Differences from Laravel are allowed only for unavoidable PHP-to-Python runtime or language constraints; each difference requires a written rationale and focused evidence.
- When Laravel delegates a subsystem to Symfony or another authoritative dependency, PyJinx must prefer one equivalent Python source of truth rather than maintain competing implementations.
- Any adapter must be thin, explicit, and limited to the PHP-to-Python boundary; dependency behavior and framework behavior must not silently diverge.
- Dependency selection must assess feature coverage, extensibility, maintenance and release health, compatibility, performance, and replacement cost before adoption.
- An incomplete or stagnant dependency must not block parity progress; when no suitable maintained equivalent exists, PyJinx must own the subsystem behind an explicit replaceable boundary with contract tests and a documented exit path.