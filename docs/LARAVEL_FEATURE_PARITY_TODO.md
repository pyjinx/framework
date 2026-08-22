# Laravel 13.x Feature Coverage — Todo Checklist

Source reference:
- Laravel API surface index used: `https://api.laravel.com/docs/13.x/index.html`

## Reference and snapshot metadata

- **Last reviewed:** 2026-08-22
- **Feature checklist:** 10/38 implementation-present, 7/38 partial, 21/38 not started
- **Exact parity audit:** 0/38 verified exact; all 38/38 remain provisional or incomplete
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
   - Response boundary (2026-08-22): Eloquent models implement the
     `JsonSerializable` contract and `Application.handle_request` recursively
     normalizes model/list/dict responses through `ResponseFactory.serialize`;
     controllers can return model objects directly.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_exception_handler.py tests/test_serve_command.py
    tests/test_post_comments_api.py -q` — 9 focused checks; full suite:
     `uv run --no-sync python3 -m pytest tests/ -q` — 167 passed.
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

15. [~] **Database / ORM** (`Illuminate\Database` / `Illuminate\Database\Eloquent`)
    - SQLAlchemy/Alembic-backed database manager, schema/migration/query builders, Eloquent models, relationships, eager loading, soft deletes, casts, and a tested post/comment API scenario exist; broad Laravel parity remains incomplete.

16. [ ] **Queueing** (`Illuminate\Queue`)
    - No queue contracts/workers/failed job stores implemented.

17. [ ] **Cache** (`Illuminate\Cache`)
    - No cache repository, stores, lock/rate limiting support.

18. [~] **Session** (`Illuminate\Session`)
    - In-memory `Store` and file session handler foundations exist with focused tests; middleware, persistent integration, cookies, flash lifecycle, and complete drivers remain unimplemented.

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

## Revalidation result — 2026-08-22

No feature is currently verified as 100% Laravel 13 parity.

| Items | Revalidation result | Evidence |
|---|---|---|
| 1–14 | Partial implementation; not exact parity | Foundation, container, routing, HTTP, middleware, validation, configuration, events, collections, support, logging, views, and Auth have implementation slices but material Laravel lifecycle, API, error, or edge-case gaps. |
| 15–18 | Partial implementation; not exact parity | Database/ORM and Session now have SQLAlchemy/Alembic, Eloquent, relationship, migration, query, session-store, and file-handler slices, but broad Laravel contracts and lifecycle integration remain incomplete. |
| 19–29 | Not started or incomplete subsystem | Cookie security, mail, notifications, broadcasting, filesystem, Redis, encryption/hashing, translation, pagination, JSON schema, and testing helpers remain absent or partial. |
| 30 | Partial implementation; not exact parity | `pyjinx`, `serve`, grouped command listing, `make:controller`, migration, route, and session-related command foundations exist; the broader Artisan command surface remains absent. |
| 31–38 | Not started or incomplete contract surface | Scheduling, process, HTTP client, image, JSON API resources, concurrency, extension hooks, password hardening, and most Laravel contracts remain absent or incomplete. |

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
  - Partial slice (2026-08-22): `build`, `connect_using`, and deterministic
    `calculate_dynamic_connection_name` support Laravel-style dynamic SQLite
    connections. Forced rebuilds purge the previous engine while retaining the
    dynamic configuration for subsequent resolution.
  - Partial slice (2026-08-22): `parse_connection_name` accepts Laravel
    `::read`, `::write`, and `::direct` suffixes. SQLite resolves all three
    names to the same underlying engine while preserving the requested
    read/write type in `get_name_with_read_write_type`.
  - Partial slice (2026-08-22): connection `prefix` configuration is applied
    to raw QueryBuilder, Eloquent-backed queries, and SchemaBuilder table
    operations. Logical application table names remain unprefixed while SQLite
    stores and introspects the prefixed physical names.
  - Partial slice (2026-08-22): `get_config`, `get_driver_name`, and
    `get_database_name` expose Laravel connection metadata with dotted
    configuration lookup and read/write suffix normalization.
  - Partial slice (2026-08-22): `supported_drivers` reports Laravel's
    declared MySQL/MariaDB/PostgreSQL/SQLite/SQL Server driver set, while
    `available_drivers` reports the currently implemented SQLite backend.
  - Partial slice (2026-08-22): named and driver-keyed extension resolvers
    support custom Engine construction through `extend` and
    `forget_extension`, while preserving manager-owned listeners, sessions,
    and cached-engine lifecycle.
  - Source mapping: Laravel `DatabaseManager::supportedDrivers` (414–417),
    `availableDrivers` (424–430), `extend` (439–443),
    `forgetExtension` (450–453), `Connection::getConfig` (1502–1517),
    `getDriverName` (1535–1538), `getDatabaseName` (1766–1770),
    `getPdo` (1292–1305), `getRawPdo` (1308–1311),
    `getReadPdo` (1318–1375), `getName`/`getNameWithReadWriteType` (1479–1494),
    `getTablePrefix`/`setTablePrefix` (1812–1830);
    `DatabaseManager::parseConnectionName` (177–182), `build` (113–125),
    `calculateDynamicConnectionName` (133–138), `connectUsing` (150–169),
    `configuration` (219–231), and `purge` (301–312).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_database.py tests/test_database_exceptions.py -q` — 40 passed;
    full PyJinx suite: `uv run --no-sync python3 -m pytest tests/ -q` — 210
    passed, 20 warnings.
  - Residual parity gaps: full URL parsing, strict mode, non-SQLite drivers,
    connector extensions/events, transaction manager semantics, retries,
    normalized exception integration, and complete connection API remain open.
- [ ] Complete database manager/resolver parity: connection switching,
  transactions, nested transactions, retries, query listeners, and normalized
  exceptions.
  - Partial slice (2026-08-22): `DatabaseManager.transaction` accepts a
    callback, passes its managed SQLAlchemy `Session`, commits and returns the
    callback result, and preserves the existing no-callback context-manager
    form. Nested transactions share that session and use SQLAlchemy
    `begin_nested()` savepoints; recognized Laravel concurrency messages or
    SQLSTATE `40001` retry an outer callback transaction through its requested
    attempt count. `after_commit` executes immediately outside a transaction
    or after the root transaction commits; `after_rollback` runs only for the
    failed savepoint/root transaction, with nested callback order preserved.
  - Partial slice (2026-08-22): direct `begin_transaction`, `commit`, and
    `roll_back(to_level)` APIs keep manual transaction contexts open across
    calls, expose the active session through `DatabaseManager.session`, and
    route QueryBuilder reads/writes through that session. Requested-level
    rollback maps to nested savepoint rollback and invalid levels are no-ops.
  - Partial slice (2026-08-22): `DatabaseManager.listen` emits a Python
    `QueryExecuted` event after each successful SQLAlchemy cursor execution,
    including SQL, ordered bindings, elapsed milliseconds, engine, and
    connection name. Listener callbacks are invoked in registration order.
  - Partial slice (2026-08-22): `disconnect`, `purge`, and `reconnect`
    normalize Laravel `::read`, `::write`, and `::direct` suffixes to the
    collapsed SQLite resource while preserving the public suffix-aware name
    contract. Resource disposal, session cleanup, cache eviction, and
    configuration fingerprint checks now target the underlying connection.
  - Partial slice (2026-08-22): `QueryException` preserves Laravel's
    connection name, SQL, bindings, read/write type, connection details,
    previous exception, formatted message, and raw SQL accessors.
    `UniqueConstraintViolationException` adds chainable index/column metadata;
    `DeadlockException` remains a distinct transaction error type.
  - Source mapping: Laravel
    `Database\Concerns\ManagesTransactions` (26–76, 124–219, 261–378),
    `Connection::listen` (1115–1118), `Connection::logQuery` (906–933),
    `DatabaseManager::disconnect` (320–325),
    `DatabaseManager::purge` (307–312),
    `DatabaseManager::reconnect` (333–344),
    `QueryException` (10–168),
    `UniqueConstraintViolationException` (5–44),
    `DeadlockException` (5–10), and `Events\QueryExecuted` (5–79).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_database.py tests/test_database_exceptions.py -q` — 40 passed;
    full PyJinx evidence: `uv run --no-sync python3 -m pytest tests/ -q` — 210
    passed, 20 warnings.
  - Residual parity gaps: SQLAlchemy has no Laravel
    `DatabaseTransactionsManager`, transaction lifecycle events, or
    query-grammar savepoint compilation. Query event dispatch still lacks
    Laravel's application event dispatcher integration, read/write/direct
    classification, raw SQL substitution, threshold handlers, and complete
    connection API. The available DBAPI exception surface cannot faithfully
    normalize every Laravel concurrency or lost-connection case, and nested
    concurrency errors are re-raised rather than translated to Laravel's
    `DeadlockException`.
- [ ] Complete raw query builder parity: insert/update/delete, where variants, joins, aggregates, grouping, ordering, pagination, chunking, cursor reads, upserts, locks, raw bindings, and SQL generation.
  - Partial slice (2026-08-22): `QueryBuilder.upsert` now maps Laravel's SQLite conflict-target behavior for one or many mappings, default/exact update-column lists, and associative static update values; empty values return `0`, while an empty update list uses a plain insert. `lock`, `lock_for_update`, and `shared_lock` retain Laravel's lock state and use SQLAlchemy's equivalent boolean `with_for_update` modes. `to_sql` and `get_bindings` expose the compiled parameterized SELECT and flattened positional bindings without execution.
  - Partial slice (2026-08-22): `where_column` and `or_where_column`
    compare two qualified columns without creating value bindings, preserving
    Laravel's column-condition operator semantics. `where_between_columns`,
    `or_where_between_columns`, `where_not_between_columns`, and
    `or_where_not_between_columns` compare a column against two column
    boundaries without value bindings. SQLite `where_date`,
    `or_where_date`, `where_time`, and `or_where_time` extract date/time
    portions. `where_day`, `or_where_day`, `where_month`, `or_where_month`,
    `where_year`, and `or_where_year` extract zero-padded calendar parts with
    Laravel's two-argument equality shorthand and comparison operators.
    `where_json_contains`, `or_where_json_contains`,
    `where_json_doesnt_contain`, and `or_where_json_doesnt_contain` use
    SQLite `json_each` for scalar array membership. JSON path sources are
    supported for `where_json_contains`; `where_json_contains_key`,
    `or_where_json_contains_key`, `where_json_doesnt_contain_key`,
    `or_where_json_doesnt_contain_key`, `where_json_length`, and
    `or_where_json_length` use SQLite `json_type` and `json_array_length`.
    `where_row_values` and `or_where_row_values` compare tuples of columns
    against bound tuples and reject mismatched column/value lengths.
  - Partial slice (2026-08-22): `where_all`, `where_any`, and `where_none`
    group equality/comparison predicates across multiple columns, with
    `or_where_*` variants preserving the outer boolean. Raw and Eloquent
    builders expose the same snake-case API.
  - Partial slice (2026-08-22): ordered `chunk` pagination delivers pages
    with Laravel's boolean callback/early-stop behavior, `each` applies an
    item callback through chunking, and `cursor` returns a lazy Python
    generator over ordered result mappings. Missing order clauses and invalid
    chunk sizes fail deterministically.
  - Partial slice (2026-08-22): Eloquent Builder wraps the same chunk and
    cursor operations and hydrates each row into the configured model class.
  - Partial slice (2026-08-22): `where_exists`, `where_not_exists`, and
    `or_where_*` variants accept subquery builders or callback-configured
    subqueries, including `from_` table selection, and compile SQLite EXISTS
    predicates.
  - Partial slice (2026-08-22): `where_like`, `where_not_like`, and `or_where_*`
    variants support case-insensitive SQLite LIKE and Laravel-compatible
    case-sensitive GLOB pattern conversion.
  - Partial slice (2026-08-22): Eloquent Builder forwards exists and like
    predicates while preserving model hydration and fluent chaining.
  - Partial slice (2026-08-22): Eloquent Builder forwards null-safe equality,
    scalar negated comparisons, and integer raw predicates with model hydration
    preserved.
  - Partial slice (2026-08-22): `where_in` and `where_not_in` reject nested
    arrays before query execution, matching Laravel's invalid-argument boundary.
  - Partial slice (2026-08-22): `where_raw` and `or_where_raw` support
    positional `?` bindings through SQLAlchemy bind parameters. Comparison
    construction now avoids evaluating unsupported operators eagerly, allowing
    NULL equality predicates to compile correctly.
  - Partial slice (2026-08-22): `select_raw` supports parameterized raw
    expressions as the selected projection and automatically retains the base
    table as the FROM clause.
  - Partial slice (2026-08-22): `select_sub` accepts a QueryBuilder or callback
    subquery and hydrates the scalar result under the requested alias.
  - Partial slice (2026-08-22): `from_sub` accepts a QueryBuilder or callback,
    compiles it as an aliased derived table, and exposes the derived columns to
    outer selects and qualified predicates. Switching back through `from_`
    clears the derived source.
  - Partial slice (2026-08-22): Eloquent Builder forwards `from_sub` and
    accepts another Eloquent builder as the derived source while preserving
    model hydration.
  - Partial slice (2026-08-22): `order_by_raw` supports parameterized raw
    ordering expressions while preserving existing fluent order clauses.
  - Partial slice (2026-08-22): `group_by_raw` supports parameterized raw
    GROUP BY expressions while preserving ordinary group ordering.
  - Partial slice (2026-08-22): `having_raw` and `or_having_raw` support
    parameterized aggregate HAVING expressions.
  - Partial slice (2026-08-22): Eloquent Builder forwards raw WHERE,
    SELECT, ORDER BY, GROUP BY, and HAVING methods with fluent model queries.
  - Source mapping: Laravel `Query\Builder::whereRaw` (1292–1305),
    `orWhereRaw` (1308–1310), `selectRaw` (356–366),
    `selectSub` (327–334), `fromSub` (376–381),
    `orderByRaw` (3119–3126),
    `groupByRaw` (2690–2703), `havingRaw` (2944–2968), and
    `orHavingRaw` (2978–2981).
  - Source mapping: Laravel `Query\Builder::whereIn` (1422–1455),
    `orWhereIn` (1465–1467), `whereNotIn` (1478–1481), and
    `orWhereNotIn` (1490–1492).
  - Source mapping: Laravel `Query\Builder::whereNot` (1139–1155),
    `orWhereNot` (1158–1160), `whereNullSafeEquals` (1386–1397),
    `orWhereNullSafeEquals` (1406–1408), SQLite
    `SQLiteGrammar::whereNullSafeEquals` (87–90),
    `whereExists` (2143–2162), `orWhereExists` (2166–2172),
    `whereNotExists` (2178–2181), `orWhereNotExists` (2189–2191),
    `whereLike` (1323–1336), `orWhereLike` (1346–1349),
    `whereNotLike` (1360–1363), `orWhereNotLike` (1373–1376),
    `whereIntegerInRaw` (1504–1521), `orWhereIntegerInRaw` (1530–1533),
    `whereIntegerNotInRaw` (1543–1545), `orWhereIntegerNotInRaw` (1555–1558),
    Eloquent Builder forwarding, `whereColumn` (1172–1205),
    `orWhereColumn` (1208–1211), `whereBetweenColumns` (1640–1654),
    `orWhereBetweenColumns` (1673–1676), `whereNotBetweenColumns` (1697–1700),
    `whereDate`/`orWhereDate` (1801–1838), `whereTime`/`orWhereTime`
    (1849–1886), `whereDay`/`orWhereDay` (1897–1938),
    `whereMonth`/`orWhereMonth` (1949–1990), `whereYear`/`orWhereYear`
    (2001–2038), `whereJsonContains`/`orWhereJsonContains` (2260–2282),
    `whereJsonDoesntContain`/`orWhereJsonDoesntContain` (2293–2308),
    `whereJsonContainsKey`/`orWhereJsonContainsKey` (2377–2395),
    `whereJsonDoesntContainKey`/`orWhereJsonDoesntContainKey` (2404–2418),
    `whereJsonLength`/`orWhereJsonLength` (2429–2468),
    `whereRowValues`/`orWhereRowValues` (2223–2248),
    `whereAll`/`orWhereAll` (2574–2599), `whereAny`/`orWhereAny` (2611–2636),
    `whereNone`/`orWhereNone` (2648–2663), `chunk` (39–79),
    `each` (112–121), Eloquent Builder chunk/cursor forwarding, `cursor`
    (3786–3799), `lock` (3339), `lockForUpdate` (3355), `sharedLock` (3365),
    `toSql` (3447), `fromSub` (376), `upsert` (4378), and `getBindings` (4625);
    SQLite upsert grammar at `Query/Grammars/SQLiteGrammar.php::compileUpsert`
    (356) and lock behavior at `Query/Grammars/SQLiteGrammar.php::compileLock`
    (31).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_query_builder.py tests/test_eloquent_model.py -q` — 85 passed;
    full PyJinx suite: `uv run --no-sync python3 -m pytest tests/ -q` — 206
    passed, 20 warnings.
  - Residual parity gaps: this is SQLite-only (`DatabaseManager` currently
    supports SQLite); JSON object/complex-array containment, overlaps,
    SQL grammar abstraction, binding buckets/cleaning, before-query callbacks,
    write-PDO routing, and `toRawSql` substitution remain incomplete. Nested,
    subquery, full-text, relationship, and remaining Laravel where variants
    remain unported. SQLite emits no locking clause, as Laravel's SQLite
    grammar does; custom lock strings are retained as state but not rendered.
    Laravel expression objects and non-SQLite grammar-specific upsert/lock
    semantics remain unported.
- [~] **Database / ORM** (`Illuminate\Database` / `Illuminate\Database\Eloquent`)
    - SQLAlchemy/Alembic-backed manager, query/schema builders, migrations, and early Eloquent slices exist; broad Laravel API parity remains incomplete.
- [ ] Complete schema builder parity: tables, columns, indexes, constraints, foreign keys, renames, drops, dialect behavior, and SQLite limitations.
  - Partial slice (2026-08-22): SQLite schema creation materializes `foreign_id(...).constrained()` foreign-key constraints with `on_delete`/`on_update` actions, named single/composite `unique` and `index` definitions, fluent column modifiers, and escaped string defaults.
  - Partial slice (2026-08-22): `SchemaBuilder.has_table`,
    `has_column`, `has_columns`, and `get_columns` expose SQLite schema
    introspection through SQLAlchemy's inspector with case-insensitive table
    column checks.
  - Partial slice (2026-08-22): `get_indexes` and `get_foreign_keys`
    expose SQLAlchemy inspector metadata for SQLite indexes and foreign-key
    definitions.
  - Partial slice (2026-08-22): `has_view`, `get_tables`, `get_views`, and
    SQLite's empty `get_types` boundary expose table/view metadata through
    SQLAlchemy inspector APIs.
  - Partial slice (2026-08-22): `SchemaBuilder.table` executes Blueprint
    `rename_column` and `drop_column` commands using SQLite's quoted
    `ALTER TABLE` operations with identifier validation.
  - Partial slice (2026-08-22): `SchemaBuilder.drop_columns` forwards Laravel's
    multi-column drop helper through the Blueprint mutation boundary.
  - Source mapping: Laravel `Schema\Builder::hasTable` (169–184),
    `hasView` (194–207), `getTables` (215–237), `getViews` (243–253),
    `getTypes` (256–265), `hasColumn` (270–277), `hasColumns` (284–295),
    `getColumns` (393–409), `getIndexes` (412–481),
    `getForeignKeys` (486–550), `table` (506–510),
    `dropColumns` (560–565), and `Blueprint::dropColumn` (422–427) /
    `renameColumn` (436–439); current creation mapping remains
    `Blueprint::unique` (662), `index` (675), `foreign` (741), `foreignId`
    (1037), `indexCommand` (1772), `createIndexName` (1815),
    `ColumnDefinition` modifiers, `ForeignIdColumnDefinition::constrained`
    (37), `ForeignKeyDefinition` action helpers, and `Builder::create` (518) /
    `rename` (610).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_schema_builder.py -q` — 10 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 189 passed, 20 warnings.
  - Residual parity gaps: SQLite-only creation; remaining table alteration,
    index/foreign-key drops and renames; full types/modifiers/default
    expressions; composite/self-referential FKs; irregular plural inference;
    and non-SQLite grammar behavior.
- [ ] Complete migration parity: Laravel-shaped files and paths, batches, status, rollback step/batch, reset, refresh, fresh, pretend, paths, seed integration, and failure recovery.
  - Partial slice (2026-08-22): `migrate:status --pending` filters out
    applied revisions and reports `No pending migrations` when empty.
    `migrate:rollback --step N` maps positive step counts to Alembic relative
    downgrades, and `--pretend` computes an explicit current-to-target range
    for SQL preview without mutating the database. Required CLI option values
    now support both `--option=value` and `--option value` forms.
  - Source mapping: Laravel `RollbackCommand::handle` (55–71) and
    `getOptions` (79–89), `StatusCommand::handle` (64–102), and
    `ManagesTransactions`; Python implementation:
    `MigrationCommands.MigrateRollbackCommand` and
    `Foundation\Console\Command.parse_options`.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_migration_commands.py -q` — 1 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 186 passed, 20 warnings.
  - Residual parity gaps: Alembic's version table has no Laravel
    migration-name/batch repository, so `--batch` cannot implement Laravel
    semantics; status still lacks Laravel database/path/realpath options,
    missing-repository diagnostics, and pending exit-status propagation.
- [~] Complete Eloquent model metadata: table, connection, keys, UUID/ULID, incrementing, timestamps, date formats, guarded/fillable, hidden/visible, appends, and serialization.
  - Partial slice (2026-08-22): `Model.to_dict()` now serializes arrayable attributes and loaded model/list relations through a visible allow-list followed by hidden exclusion. It provides chainable snake-case counterparts for Laravel's hidden/visible controls (`get/set/merge_hidden`, `get/set/merge_visible`, `make_visible`, `make_hidden`, and conditional forms) and appends controls (`append`, `get/set/merge_appends`, `has_appended`, `without_appends`). Appended legacy getter and `Attribute` values serialize on demand; configured appends are instance-local. `get_table`/`set_table`, `get_connection_name`/`set_connection`, `qualify_column`, and `get_qualified_key_name` expose table/connection metadata. Models without an explicit table use a snake-case plural fallback; `created_at_column`/`updated_at_column`, timestamp accessors/setters, `get_date_format`/`set_date_format`, and `from_date_time` expose the current timestamp/date-format boundary. Null timestamp columns suppress corresponding writes, and existing dirty timestamp values are preserved.
  - Source mapping: `Model.php` `toArray` (2033–2038), `getConnectionName`/`setConnection` (2236–2251), `getTable`/`setTable` (2301–2318), and `qualifyColumn`/`getQualifiedKeyName` (736–749, 2347–2350); Laravel `Str::snake`/`Str::pluralStudly` default table derivation; `HasTimestamps.php` `updateTimestamps` (87–104), `getCreatedAtColumn`/`getUpdatedAtColumn` (167–180), `setCreatedAt`/`setUpdatedAt` (112–132); `HasAttributes.php` `getDateFormat`/`setDateFormat` (1674–1690), `fromDateTime` (1625–1630), attribute serialization (225–458), and append controls (2447–2515); `HidesAttributes.php` hidden/visible controls (42–173).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest tests/test_eloquent_model.py -q` — 19 passed; full PyJinx suite: `uv run --no-sync python3 -m pytest tests/ -q` — 165 passed.
  - Residual parity gaps: irregular pluralization beyond the conservative fallback, UUID/ULID behavior, resolver-backed connection access, integration of date formats into database serialization/casts, JSON serialization APIs, full cast/custom-cast and encrypted/hashed serialization, recursion prevention, Laravel's snake-case relation-key option and generic Arrayable collections, attribute-based route-key resolution, and broad relationship/eager-loading parity remain unported.
- [~] Complete Eloquent attribute behavior: dirty tracking, original values, attribute accessors/mutators, casts, custom casts, encrypted casts, hashed casts, JSON casts, date casts, and mass-assignment exceptions.
  - Partial slice (2026-08-22): `Model.is_dirty`, `is_clean`, `get_dirty`,
    `get_changes`, `was_changed`, and `get_original` distinguish current
    attributes from the last synchronized original state and retain the last
    successful save changes. `get_raw_original`,
    `sync_original`, `sync_original_attribute`, `sync_original_attributes`,
    and `sync_changes` provide explicit raw-baseline and synchronization
    APIs. Annotated `Attribute` setters can expand one logical assignment into
    multiple persisted attributes, matching the existing getter resolution
    boundary. Primitive `integer`, `float`, `boolean`, `json`, `date`, string,
    timestamp, and fixed-scale `decimal` casts convert stored values at
    attribute access; decimal values use string output and half-up rounding.
  - Source mapping: Laravel `HasAttributes::getDirty` (2301–2315),
    `isDirty`/`isClean` (2222–2238), `getChanges`/`wasChanged`
    (2261–2332), `syncOriginal`/`syncOriginalAttribute`/
    `syncOriginalAttributes`/`syncChanges` (2166–2214),
    `getRawOriginal` (2118–2121), `castAttribute` (848–906),
    `asDecimal` (1536–1543), and `Casts\Attribute` setter contract (5–79).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 16 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 162 passed.
  - Residual parity gaps: cast-aware dirty comparison, original rewinding,
    legacy mutator edge semantics, enum/collection/custom casts,
    encrypted/hashed/JSON/date serialization edge cases, and mass-assignment
    exceptions remain open.
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
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 14 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 160 passed.
  - Residual parity gaps: update-or-fail, save-or-fail, save-or-ignore, touch,
    upsert, cast-aware dirty/original synchronization, and complete CRUD
    option/error semantics remain open.
- [~] Complete Eloquent model events: boot/booted, retrieved, saving/saved, creating/created, updating/updated, deleting/deleted, restoring/restored, observers, dispatch suppression, and event ordering.
  - Partial slice (2026-08-22): `Model.retrieved` dispatches after persisted
    models are hydrated, while callback dispatch suppression remains shared
    across model classes, nest-safe, and restoration-safe.
  - Source mapping: Laravel `Model::newFromBuilder` (794–805), which fires
    `retrieved` after hydration, and `HasEvents::withoutEvents` (447–462).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_model.py -q` — 14 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 160 passed.
  - Residual parity gaps: boot/booted discovery, restoring/restored events,
    observers, dispatcher contracts, event faking, and full Laravel event
    ordering remain open.
- [~] Complete Eloquent builders and collections: scopes, macros, collection transformations, lazy collections, chunk/cursor, eager loading, lazy loading, and N+1 controls.
  - Partial slice (2026-08-22): Eloquent builders now expose
    `create_quietly`, `force_create`, and `force_create_quietly` through the
    model's guarded and event-suppression boundaries, plus `with_` nested
    eager-loading and `where_has` relation filtering. Eager loading batches
    has-many and belongs-to related records instead of issuing one query per
    child.
  - Source mapping: Laravel `Builder::with` (1742–1758),
    `QueriesRelationships::whereHas` (170–173), and
    `withWhereHas` (186–190); existing create/force mappings remain in the
    implementation.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_post_comments_api.py tests/test_eloquent_model.py -q` — 21
    passed; full PyJinx suite: `uv run --no-sync python3 -m pytest tests/ -q`
    — 167 passed.
  - Residual parity gaps: scopes, macros, collections, lazy collections,
    chunk/cursor, constrained eager loading, morph relations, relation
    matching, N+1 controls beyond the implemented batch loader, and the
    remainder of the builder API remain open.
- [~] Complete Eloquent relationships: belongs-to, has-one, has-many, many-to-many, pivot records, through relations, polymorphic relations, touching, eager constraints, and relationship serialization.
  - Partial slice (2026-08-22): the application now has `Post`/`Comment`
    models, `User.posts`/`User.comments`, `Post.user`/`Post.comments`, and
    `Comment.post`/`Comment.user` relationships. A deterministic seeder
    creates multiple posts and varied comments across users. The ORM endpoint
    `GET /api/posts?email=...` uses `where_has("user", ...)` and
    `with_(["user", "comments.user"])` to return all posts owned by the user
    with all comments and their authors; the acceptance test compares the
    response against ORM-derived expected relationships.
  - Source mapping: Laravel `Model::hasMany`/`belongsTo`, Eloquent
    `Builder::with`/`whereHas`, and `HasOneOrMany`/`BelongsTo` relation
    boundaries; application implementation is in `app/Models/Post.py`,
    `Comment.py`, `User.py`, `PostController.py`, and the posts/comments
    migration, seeder, and acceptance test.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_post_comments_api.py -q` — 1 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 167 passed.
  - Residual parity gaps: through/polymorphic relations, touching, constrained
    eager loading beyond nested paths, relation matching for arbitrary model
    graphs, collection behavior, complete relation lifecycle events, and
    broad Laravel relationship API parity remain open.
- [~] Complete soft deletes, factories, seeders, pagination, JSON resources, model policies, and model route binding.
  - Partial slice (2026-08-22): soft-delete restore now respects the model's
    configurable updated timestamp column and suppresses the timestamp update
    when that column is null.
  - Source mapping: Laravel `HasTimestamps::updateTimestamps` (87–104) and
    `SoftDeletes::restore` lifecycle.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_eloquent_soft_deletes.py -q` — 10 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 167 passed.
  - Residual parity gaps: factories, pagination, JSON resources, model
    policies, route binding edge cases, and broad soft-delete lifecycle parity
    remain open.

### Authentication, sessions, and security

- [~] Inventory Laravel Auth, Session, Cookie, Encryption, Hashing, Passwords, and Sanctum APIs class by class.
  - Initial Auth inventory (2026-08-22): Laravel Auth contains
    `AuthManager`, `SessionGuard`, `TokenGuard`, `RequestGuard`,
    `DatabaseUserProvider`, `EloquentUserProvider`, `GenericUser`,
    `AuthenticationException`, guard/provider contracts, authorization
    `Gate`/responses, auth middleware, password brokers/token repositories,
    auth events, and verification/reset notifications. The Contracts/Auth
    namespace includes guard, stateful guard, factory, provider,
    authenticatable, password broker, reset, verification, and authorization
    interfaces.
  - Current PyJinx prerequisite surface: `config/auth.py` declares a web
    session guard, users provider, password broker, and password timeout;
    only bounded `AuthServiceProvider`, `Gate`, and an empty `Authenticate`
    middleware exist.
  - Authentication slice (2026-08-22): `Illuminate.Auth.GenericUser` exposes
    authentication identifiers, password access, remember-token access/update,
    and attribute-backed user values. `AuthenticationException` carries checked
    guards and explicit or callback-generated redirect destinations.
    `RequestGuard` resolves and caches a callback user per request and exposes
    check/guest/id/set-user/request operations. `EloquentUserProvider` retrieves
    users by identifier and credentials, supports collection and callback
    constraints, applies provider query callbacks, validates passwords through
    an injected hasher boundary, rehashes passwords when required, and updates
    remember tokens without timestamp mutations.
  - Source mapping: Laravel `Auth\GenericUser` (21–140),
    `Auth\AuthenticationException` (8–82), `Auth\RequestGuard` (35–88),
    `Auth\EloquentUserProvider` (40–279), `Contracts\Auth\Authenticatable`,
    `Contracts\Auth\Guard`, and `Contracts\Auth\UserProvider`.
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_auth.py tests/test_auth_exception.py tests/test_request_guard.py
    tests/test_user_provider.py -q` — 8 passed; full PyJinx suite:
    `uv run --no-sync python3 -m pytest tests/ -q` — 177 passed, 20 warnings.
  - Source mapping: `references/framework/src/Illuminate/Auth`,
    `Illuminate/Contracts/Auth`, and `Illuminate/Auth/Middleware`.
  - Residual parity gaps: complete public-method inventory, session/cookie
    lifecycle, session/token guards, database user provider, password hashing/
    reset, CSRF, Sanctum, authorization middleware, events/notifications, and
    all non-auth security services remain unimplemented.
- [~] Implement session stores, drivers, session middleware, lifecycle cleanup, regeneration, invalidation, and flash data.
  - Partial slice (2026-08-22): `Illuminate.Session.Store` provides an
    in-memory session attribute bag with start, get/put, existence checks,
    pull/push, counters, forget/flush, invalidate/regenerate, and CSRF token
    primitives. `FileSessionHandler` provides open/close/read/write/destroy/gc
    persistence with expiration and atomic replacement.
  - Source mapping: Laravel `Session\Store` and
    `Session\FileSessionHandler` (10–127).
  - Evidence: `cd pyjinx && uv run --no-sync python3 -m pytest
    tests/test_session_store.py tests/test_file_session_handler.py -q` — 2
    passed; full PyJinx suite: `uv run --no-sync python3 -m pytest tests/ -q`
    — 170 passed.
  - Residual parity gaps: persistent handler integration, request middleware,
    flash aging, dot-notation access, session cookies, concurrency/lifecycle
    semantics, and complete session API.
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