# Laravel 13.x Feature Coverage — Todo Checklist

Source reference:
- Laravel API surface index used: `https://api.laravel.com/docs/13.x/index.html`

## Reference and snapshot metadata

- **Last reviewed:** 2026-08-22
- **Feature checklist:** 11/38 implementation-present, 5/38 partial, 22/38 not started
- **Exact parity audit:** 0/38 verified exact; 16/38 partial; 22/38 not started
- **Audit method:** compare the local Laravel 13 reference projects and framework source, inspect the Laravel 13.x API namespace index, and run focused PyJinx behavior checks where a runtime exists.
- **Audit conclusion:** every implementation-present area remains provisional; no area currently has evidence for 100% Laravel 13 parity.
- **Quality-risk categories:** 3 (performance, code smell, memory leak)
-  - Performance issues: 0 identified (pending baseline audit)
-  - Code smells: 0 identified (pending baseline audit)
-  - Memory leak risks: 0 identified (pending baseline audit)
- **Source of truth:** This file is the tracked feature coverage backlog used by roadmap and planning updates.
- **Provisional status:** This backlog reflects a starting PoC baseline. Marking an area `[x]` or `[~]` is not a release completion signal; it only indicates current implementation presence that must be revalidated.

## Autonomous execution loop

The continuous source-first implementation process is defined in
[`AUTONOMOUS_PARITY_LOOP.md`](./AUTONOMOUS_PARITY_LOOP.md). It governs slice
selection, Laravel source comparison, strict TDD, framework/runtime syncing,
evidence updates, and the final acceptance gate.

The complete `laravel/framework/tests/` port is intentionally deferred until
every item in this tracker and its runtime mirror is implemented and
revalidated.

## Legend

- **[x]** = implementation exists in current codebase only; production completion requires revalidation and evidence.
- **[~]** = partial implementation in current codebase; behavior requires proof before release.
- **[ ]** = not implemented

## Coverage checklist

1. [~] **Foundation lifecycle** (`Illuminate\Foundation`)
   - `Foundation.Application`, bootstrap flow, providers, HTTP/console kernel
     classes, and a bounded HTTP exception boundary are present.
   - Exception slice (2026-08-22): the HTTP kernel reports and renders
     uncaught `Exception` values through `exception_handler`; the handler
     offers deterministic report filtering, log-level/context configuration,
     duplicate suppression, render/final-response callbacks, production-safe
     HTML/JSON responses, and debug-gated escaped diagnostics.
   - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
     tests/test_exception_handler.py tests/test_serve_command.py -q` — 8
     focused handler/configuration/kernel/WSGI checks; full suite:
     `uv run --no-sync python3 -m pytest tests/ -q` — 150 passed.
     Source mapping and residuals are in `IMPLEMENTATION_DECISIONS.md`.
   - Gaps: full Laravel bootstrap policy, maintenance mode, complete Laravel
     exception conversion/rendering, and service registration lifecycle
     guarantees remain incomplete.

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

The audit used `references/laravel/` (application) and `references/framework/` (Laravel framework) as authoritative references.

## Detailed remaining implementation queue

### Resume point

Next implementation area: finish the Database / ORM foundation and continue the Eloquent port. The DB manager, SQLAlchemy/Alembic boundary, migrations, raw query builder, DB facade, initial User model, casts, and model events exist only as early slices; they are not full Laravel parity.

### Database and Eloquent

- [ ] Expand the Laravel 13 Database/Eloquent API inventory down to every class and public method.
- [ ] Complete connection configuration parity: default/named connections, URLs, prefixes, strict mode, read/write connections, reconnect and purge behavior.
  - Partial slice (2026-08-22): `DatabaseManager` now resolves default/named SQLite connections, restores defaults through callback failure, validates drivers before URL use, tracks URL/SQLite-option fingerprints, rebuilds changed connections, evicts invalid cached configurations, closes manager-owned sessions, returns registry snapshots, and reports deterministic unknown/unsupported-driver errors.
  - Partial slice (2026-08-22): the manager exposes `get_pdo`,
    `get_raw_pdo`, `get_read_pdo`, `get_name`, and
    `get_name_with_read_write_type` as explicit SQLAlchemy resource/name
    boundaries. `get_pdo` returns a pooled DBAPI connection that callers must
    close; read/write routing is intentionally collapsed to the configured
    SQLite connection.
  - Source mapping: Laravel `Connection::getPdo` (1292–1305),
    `getRawPdo` (1308–1311), `getReadPdo` (1318–1375),
    `getName`/`getNameWithReadWriteType` (1479–1494).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_database.py -q` — 28 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 154 passed.
  - Residual parity gaps: Laravel read/write/direct variants, full URL
    parsing, prefixes, strict mode, non-SQLite drivers, connector
    extensions/events, transaction manager semantics, retries, normalized
    exceptions, and complete connection API remain open. `ValueError` is the
    documented Python analogue of Laravel's `InvalidArgumentException`.
- [ ] Complete database manager/resolver parity: connection switching, transactions, nested transactions, retries, query listeners, and normalized exceptions.
  - Partial slice (2026-08-22): `DatabaseManager.transaction` accepts a callback, passes its managed SQLAlchemy `Session`, commits and returns the callback result, and preserves the existing no-callback context-manager form. Nested transactions share that session and use SQLAlchemy `begin_nested()` savepoints; recognized Laravel concurrency messages or SQLSTATE `40001` retry an outer callback transaction through its requested attempt count. `after_commit` executes immediately outside a transaction or after the root transaction commits; `after_rollback` runs only for the failed savepoint/root transaction, with nested callback order preserved.
  - Partial slice (2026-08-22): `DatabaseManager.listen` emits a Python
    `QueryExecuted` event after each successful SQLAlchemy cursor execution,
    including SQL, ordered bindings, elapsed milliseconds, engine, and
    connection name. Listener callbacks are invoked in registration order.
  - Source mapping: Laravel `Connection::listen` (1115–1118),
    `Connection::logQuery` (906–933), and `Events\QueryExecuted` (5–79).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_database.py -q` — 27 passed, plus full PyJinx evidence:
    `uv run --no-sync python3 -m pytest tests/ -q` — 153 passed. This maps
    Laravel query events to SQLAlchemy engine cursor lifecycle hooks.
    Canonical and runtime manager, event contract, and tracker copies are
    synchronized.
  - Residual parity gaps: SQLAlchemy has no Laravel
    `DatabaseTransactionsManager`, transaction lifecycle events, or
    query-grammar savepoint compilation. Query event dispatch still lacks
    Laravel's application event dispatcher integration, read/write/direct
    classification, raw SQL substitution, threshold handlers, and complete
    connection API. The available DBAPI exception surface cannot faithfully
    normalize every Laravel concurrency or lost-connection case, and nested
    concurrency errors are re-raised rather than translated to Laravel's
    `DeadlockException`; direct Laravel `beginTransaction`/`commit`/`rollBack`
    APIs remain unported.
- [ ] Complete raw query builder parity: insert/update/delete, where variants, joins, aggregates, grouping, ordering, pagination, chunking, cursor reads, upserts, locks, raw bindings, and SQL generation.
  - Partial slice (2026-08-22): `QueryBuilder.upsert` now maps Laravel's SQLite conflict-target behavior for one or many mappings, default/exact update-column lists, and associative static update values; empty values return `0`, while an empty update list uses a plain insert. `lock`, `lock_for_update`, and `shared_lock` retain Laravel's lock state and use SQLAlchemy's equivalent boolean `with_for_update` modes. `to_sql` and `get_bindings` expose the compiled parameterized SELECT and flattened positional bindings without execution.
  - Partial slice (2026-08-22): `where_column` and `or_where_column`
    compare two qualified columns without creating value bindings, preserving
    Laravel's column-condition operator semantics. `where_between_columns`,
    `or_where_between_columns`, `where_not_between_columns`, and
    `or_where_not_between_columns` compare a column against two column
    boundaries without value bindings. SQLite `where_date`,
    `or_where_date`, `where_time`, and `or_where_time` extract date/time
    portions with Laravel's two-argument equality shorthand and comparison
    operators.
  - Source mapping: Laravel `Query\Builder::whereColumn` (1172–1205),
    `orWhereColumn` (1208–1211), `whereBetweenColumns` (1640–1654),
    `orWhereBetweenColumns` (1673–1676), `whereNotBetweenColumns`
    (1697–1700), `whereDate`/`orWhereDate` (1801–1838),
    `whereTime`/`orWhereTime` (1849–1886), `lock` (3339),
    `lockForUpdate` (3355), `sharedLock` (3365), `toSql` (3447),
    `upsert` (4378), and `getBindings` (4625); SQLite upsert grammar at
    `Query/Grammars/SQLiteGrammar.php::compileUpsert` (356) and lock behavior
    at `SQLiteGrammar.php::compileLock` (31).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_query_builder.py -q` — 45 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 157 passed.
  - Residual parity gaps: this is SQLite-only (`DatabaseManager` currently
    supports SQLite); SQLAlchemy has no Laravel connection grammar, binding
    buckets/cleaning, before-query callbacks, write-PDO routing, or
    `toRawSql` substitution. Day/month/year extraction, JSON, nested,
    subquery, full-text, relationship, and remaining Laravel where variants
    remain unported. SQLite emits no locking clause, as Laravel's SQLite
    grammar does; custom lock strings are retained as state but not rendered.
    Laravel expression objects and non-SQLite grammar-specific upsert/lock
    semantics remain unported.
- [~] **Database / ORM** (`Illuminate\Database` / `Illuminate\Database\Eloquent`)
    - SQLAlchemy/Alembic-backed manager, query/schema builders, migrations, and early Eloquent slices exist; broad Laravel API parity remains incomplete.
- [ ] Complete schema builder parity: tables, columns, indexes, constraints, foreign keys, renames, drops, dialect behavior, and SQLite limitations.
  - Partial slice (2026-08-22): SQLite schema creation materializes `foreign_id(...).constrained()` foreign-key constraints with `on_delete`/`on_update` actions, named single/composite `unique` and `index` definitions, fluent column modifiers, and escaped string defaults.
  - Source mapping: `Blueprint::unique` (662), `index` (675), `foreign` (741), `foreignId` (1037), `indexCommand` (1772), `createIndexName` (1815), `ColumnDefinition` fluent modifiers, `ForeignIdColumnDefinition::constrained` (37) and `references` (52), `ForeignKeyDefinition` action helpers, and `Builder::create` (518)/`rename` (610).
  - Evidence: `cd port/pyjinx && uv run --no-sync pytest tests/test_schema_builder.py -q` — 8 passed; full PyJinx suite: 135 passed (database FK metadata, conventional/called index names, unique enforcement, invalid-reference rejection, `ON DELETE CASCADE`, explicit-vs-fluent unique overloads, quoted defaults, boolean fluent index/primary naming, quoted identifiers, and None-default behavior). Canonical/runtime schema code and tracker copies are synchronized.
  - Residual parity gaps: SQLite-only creation; table alteration; column/index/foreign-key drops and renames; inspection; full types/modifiers/default expressions; composite/self-referential FKs; irregular plural inference; and non-SQLite grammar behavior.
- [ ] Complete migration parity: Laravel-shaped files and paths, batches, status, rollback step/batch, reset, refresh, fresh, pretend, paths, seed integration, and failure recovery.
  - Partial slice (2026-08-22): `migrate:status --pending` now filters out applied revisions and reports `No pending migrations` when its filtered result is empty. The existing unfiltered status output remains available and reports `No migrations found` when the migration directory has no revisions.
  - Source mapping: `references/framework/src/Illuminate/Database/Console/Migrations/StatusCommand.php` `handle` (64–102) and `getStatusFor` (112–128); current Laravel's repository implementation is `DatabaseMigrationRepository.php` `getRan` (47–53) and `getMigrationBatches` (104–110), rather than a `MigrationRepository.php` file.
  - Evidence: `cd port/pyjinx && uv run --no-sync pytest tests/test_migration_commands.py -q` — 1 passed; current full-suite evidence is 142 passed (one generated migration is applied, a second remains pending and is the sole `--pending` result, then applying it yields `No pending migrations`). Canonical/runtime CLI documentation and parity trackers are synchronized.
  - Residual parity gaps: Alembic's version table has no Laravel migration-name/batch repository, so applied statuses do not show batch numbers and rollback cannot implement Laravel `--step` or `--batch`; status still lacks Laravel database/path/realpath options, missing-repository diagnostics, and pending exit-status propagation.
- [ ] Complete Eloquent model metadata: table, connection, keys, UUID/ULID, incrementing, timestamps, date formats, guarded/fillable, hidden/visible, appends, and serialization.
  - Partial slice (2026-08-22): `Model.to_dict()` now serializes arrayable attributes and loaded model/list relations through a visible allow-list followed by hidden exclusion. It provides chainable snake-case counterparts for Laravel's hidden/visible controls (`get/set/merge_hidden`, `get/set/merge_visible`, `make_visible`, `make_hidden`, and conditional forms) and appends controls (`append`, `get/set/merge_appends`, `has_appended`, `without_appends`). Appended legacy getter and `Attribute` values serialize on demand; configured appends are instance-local.
  - Source mapping: `Model.php` `toArray` (2033–2038); `HasAttributes.php` `attributesToArray` (225–252), `getArrayableAttributes` (364–367), `getArrayableAppends` (374–385), `getArrayableRelations`/`getArrayableItems` (436–458), and append controls (2447–2515); `HidesAttributes.php` hidden/visible controls (42–173). Earlier key metadata maps `Model.php` `getKeyName`/`setKeyName` (2324–2340), `getKeyType`/`setKeyType` (2357–2373), `getIncrementing`/`setIncrementing` (2380–2396), `getKey` (2403–2406), and `getRouteKey`/`getRouteKeyName` (2467–2480).
  - Evidence: `cd port/pyjinx && uv run --no-sync pytest tests/test_eloquent_model.py -q` — 11 passed (visible-then-hidden ordering, legacy and `Attribute` appends, chainability/deduplication/conditional visibility, loaded relation/model-list filtering, and mutable-input isolation); full PyJinx suite: 142 passed. Canonical/runtime `Model.py` and parity trackers are synchronized.
  - Residual parity gaps: table/connection metadata, UUID/ULID behavior, timestamp column/date-format and JSON serialization APIs, full cast/custom-cast and encrypted/hashed serialization, recursion prevention, Laravel's snake-case relation-key option and generic Arrayable collections, attribute-based route-key resolution, and broad relationship/eager-loading parity remain unported.
- [ ] Complete Eloquent attribute behavior: dirty tracking, original values, attribute accessors/mutators, casts, custom casts, encrypted casts, hashed casts, JSON casts, date casts, and mass-assignment exceptions.
- [~] Complete Eloquent CRUD semantics: find, find-or-fail, first, first-or-fail, create, force-create, save, update, delete, restore, touch, increment, decrement, upsert, and quiet variants.
  - Partial slice (2026-08-22): `Model.without_events` suppresses model callbacks
    across nested operations with restoration in `finally`; `create_quietly`,
    `force_fill`, `force_create`, `force_create_quietly`, `save_quietly`,
    `update_quietly`, and `delete_quietly` now mirror the corresponding
    Laravel quiet/unguarded boundaries.
  - Source mapping: Laravel `HasEvents::withoutEvents` (447–462),
    `Model::forceFill` (725–728), `Model::saveQuietly` (1371–1374),
    `Model::deleteQuietly` (1776–1779), and `Builder::forceCreate`
    (1256–1264).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 12 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 151 passed.
  - Residual parity gaps: update-or-fail, save-or-fail, save-or-ignore, touch,
    upsert, full dirty/original synchronization, and complete CRUD
    option/error semantics remain open.
- [~] Complete Eloquent model events: boot/booted, retrieved, saving/saved, creating/created, updating/updated, deleting/deleted, restoring/restored, observers, dispatch suppression, and event ordering.
  - Partial slice (2026-08-22): `Model.retrieved` dispatches after persisted
    models are hydrated, while callback dispatch suppression remains shared
    across model classes, nest-safe, and restoration-safe.
  - Source mapping: Laravel `Model::newFromBuilder` (794–805), which fires
    `retrieved` after hydration, and `HasEvents::withoutEvents` (447–462).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 13 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 152 passed.
  - Residual parity gaps: boot/booted discovery, restoring/restored events,
    observers, dispatcher contracts, event faking, and full Laravel event
    ordering remain open.
- [~] Complete Eloquent builders and collections: scopes, macros, collection transformations, lazy collections, chunk/cursor, eager loading, lazy loading, and N+1 controls.
  - Partial slice (2026-08-22): Eloquent builders now expose `create_quietly`,
    `force_create`, and `force_create_quietly` through the model's guarded and
    event-suppression boundaries.
  - Source mapping: Laravel `Builder::createQuietly` (1245–1250),
    `Builder::forceCreate` (1256–1264), and
    `Builder::forceCreateQuietly` (1269–1272).
  - Evidence: `cd port/pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 12 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 151 passed.
  - Residual parity gaps: scopes, macros, collections, lazy collections,
    chunk/cursor, eager/lazy loading, N+1 controls, and the remainder of the
    builder API remain open.
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

- [~] Application builder exception configuration: `with_exceptions(using)`
  binds the core handler and forwards the bounded `Exceptions` configuration
  facade on first resolution. Routing/middleware callbacks, command loading,
  provider loading, and broader runtime separation remain unimplemented.
- [ ] Complete environment/config loading, caching, clearing, merge behavior, typed values, missing keys, and config command behavior.
- [ ] Complete service provider registration/boot/deferred provider/rebinding behavior and package discovery boundaries.
- [~] Framework default provider ownership: `Application` now owns the current
  framework default-provider collection and `config/app.py` lists application
  providers only. Provider merge ordering/deduplication and failed-registration
  state handling are covered. Laravel's 24-provider default collection,
  ProviderRepository/PackageManifest ordering, configured-provider string or
  instance resolution, cache/bootstrap-provider-path handling, flush-state
  behavior, Composer-equivalent discovery, deferred loading, cached manifests,
  and ApplicationBuilder route-provider configuration remain unimplemented.
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