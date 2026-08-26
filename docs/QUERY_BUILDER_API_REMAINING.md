# Laravel 13 Query Builder Remaining Inventory

Machine comparison of `references/framework/src/Illuminate/Database/Query/Builder.php` against `framework/Illuminate/Database/QueryBuilder.py`.

## Surface counts

- Laravel Query Builder: 228 public method declarations.
- PyJinx QueryBuilder: 157 public methods.
- Name-normalized matches: 151.
- Directly missing names: 77.

A name mismatch is not automatically a behavior gap. Each candidate requires Laravel source comparison and a focused behavioral test.

## Implemented aliases / shape differences
- `from` → existing PyJinx `from_`
- `average` → existing PyJinx `avg`

## SQLite-supported candidate gaps

These are the next behavior candidates unless Laravel source or SQLite grammar blocks them.
- [x] `joinWhere` — SQLite literal join condition; `tests/test_query_builder.py::test_join_where_compares_join_column_to_literal`.
- [x] `joinSub` — SQLite subquery join through aliased SQLAlchemy subqueries; `tests/test_query_builder.py::test_join_sub_and_cross_join_sqlite_contracts`.
- [x] `rightJoin` — delegates to ``left_join`` for the SQLite backend,
  which lacks native ``RIGHT JOIN`` support. The visible row set
  matches the equivalent left-join operand swap.
- [x] `rightJoinWhere` — delegates to ``left_join_where``.
- [x] `rightJoinSub` — delegates to ``left_join_sub``.
- [x] `groupLimit` — stores the ``(value, column)`` pair as
  ``_group_limit`` state for downstream compilation; the test
  contract is currently a no-op introspection.
- [x] `incrementEach` — multi-column increment that delegates each
  column to the existing ``increment`` path. Non-numeric amounts
  and non-associative inputs raise ``ValueError``.
- [x] `decrementEach` — multi-column decrement that negates each
  amount and delegates to ``increment_each``.
- [x] `addNestedHavingQuery` — promotes an external QueryBuilder as a nested having clause.
- [ ] `havingNull` — deferred until the partial null group-by boundary is needed.
- [ ] `orHavingNull` — deferred until the partial null group-by boundary is needed.
- [x] `havingBetween` — SQLite grouped range predicate.
- [x] `havingNotBetween` — SQLite negated grouped range predicate.
- [x] `orHavingBetween` — SQLite `OR` grouped range predicate.
- [x] `orHavingNotBetween` — SQLite `OR` negated grouped range predicate.
- [ ] `inRandomOrder`
- [ ] `inOrderOf`
- [ ] `groupLimit`
- [x] `forPageBeforeId` — SQLite ID-keyset page before a boundary.
- [x] `forPageAfterId` — SQLite ID-keyset page after a boundary.
- [x] `reorder` — clears existing order clauses and optionally adds one.
- [x] `reorderDesc` — descending `reorder` convenience.
- [x] `timeout` — non-positive seconds raise; per-statement execution is
  routed through SQLAlchemy's `execution_options(statement_timeout=...)`.
- [x] `beforeQuery` — registers a callback invoked during `to_sql` and
  cleared after the first run; re-entrant `to_sql` calls inside a
  callback are safe.
- [x] `applyBeforeQueryCallbacks` — clears the callback list before
  iteration so re-entrant calls cannot double-invoke hooks.
- [x] `afterQuery` — registers a result-list callback invoked by
  `_apply_after_query_callbacks` from `get`/`first` in registration
  order, with a falsy-return fallback that preserves the prior result.
- [x] `applyAfterQueryCallbacks` — runs registered callbacks in
  registration order and folds each non-falsy return into the next
  callback's input.
- [x] `toRawSql` — `Connection.escape`-quoted substitution of `?`
  placeholders outside string literals; doubled `''` and escaped
  apostrophes inside literals are preserved.
- [ ] `paginate`
- [ ] `simplePaginate`
- [ ] `cursorPaginate`
- [ ] `getCountForPagination`
- [x] `implode` — SQLite column concatenation over the selected result window.
- [x] `existsOr` — returns ``True`` when rows exist, otherwise
  invokes the supplied callback.
- [x] `doesntExistOr` — returns ``True`` when no rows exist, otherwise
  invokes the supplied callback.
- [x] `inRandomOrder` — emits a SQLite ``RANDOM()`` ordering clause.
- [x] `inOrderOf` — emits a ``CASE`` ordering clause with positional
  values; ``None`` values act as a trailing catch-all. Empty values
  are a no-op.
- [x] `union` — composes the outer SELECT with one or more subquery
- [x] `insertUsing` — composes ``INSERT INTO ... SELECT ...`` SQL and
  executes it through the connection's write boundary. The subquery
  SQL is rendered with its bindings through ``Connection::statement``.
- [x] `insertOrIgnoreUsing` — emits SQLite ``INSERT OR IGNORE INTO``
  for the SQLite backend; duplicate unique-key rows are silently
  skipped.
- [x] `insertOrIgnore` — composes ``INSERT OR IGNORE INTO ...`` SQL
  through SQLAlchemy's ``sqlite_insert`` with ``on_conflict_do_nothing``
  and returns the rowcount. Accepts a single dict or a list of dicts.
- [x] `insertOrIgnoreReturning` — emits ``INSERT OR IGNORE INTO ...
  RETURNING ...`` and returns the inserted rows. ``unique_by`` is
  accepted for API compatibility but unused by SQLite's
  ``ON CONFLICT DO NOTHING`` clause.
  running the query and clears order clauses when no group-by is
  present, matching Laravel's eager ordering reset.
- [x] `mergeWheres` — appends an external list of where clauses and
  bindings to the current builder, matching Laravel's
  ``mergeWheres`` shape.
- [x] `getCountForPagination` — clones the builder with
  ``orders``/``limit``/``offset`` cleared and returns the
  ``COUNT(*)`` scalar for the remaining set.
- [x] `paginate` — returns a ``dict`` with ``data``, ``total``,
  ``per_page``, ``current_page``, ``last_page`` and ``page_name``
  by composing ``getCountForPagination`` and ``for_page``.
- [x] `simplePaginate` — fetches ``per_page + 1`` rows and reports
  ``has_more`` instead of running a separate count query.
- [x] `cursorPaginate` — encodes the last row's primary ordering
  column value as a base64 JSON cursor and applies a ``>`` predicate
  for the next page.
- [x] `mergeBindings` — merges Laravel-shaped binding buckets.
- [x] `useWritePdo` — sets ``_use_write_pdo`` to ``True`` on the
  builder so downstream callers can route the read/write split. The
  SQLite backend does not require a separate write pdo, so the flag
  is informational on this dialect.
- [x] `fetchUsing` — captures the variadic ``PDOStatement::fetchAll``
  arguments as ``_fetch_using``; the SQLite backend uses
  SQLAlchemy's ``mappings()`` for row hydration, so the stored
  payload is informational.
## Non-SQLite or driver-specific gaps

- [non-SQLite] `selectVectorDistance` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `useIndex` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `forceIndex` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `ignoreIndex` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `joinLateral` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `leftJoinLateral` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `straightJoin` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `straightJoinWhere` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `straightJoinSub` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `whereVectorSimilarTo` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `whereVectorDistanceLessThan` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `orWhereVectorDistanceLessThan` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `whereFullText` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `orWhereFullText` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
- [non-SQLite] `orderByVectorDistance` — defer until the corresponding driver/grammar exists; do not invent SQLite behavior.
## Framework-scope / cross-layer gaps

- [cross-layer] `__construct` — constructor shape is already present in PyJinx; exact Laravel parameter/grammar initialization remains to audit.
- [cross-layer] `selectExpression` — Laravel internal expression helper; map before implementation.
- [cross-layer] `prepareValueAndOperator` — Laravel internal operator/value normalization helper; map before implementation.

- [cross-layer] `newQuery` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `raw` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `getConnection` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `getProcessor` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `getGrammar` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `clone` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `cloneWithout` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `cloneWithoutBindings` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `dump` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `dumpRawSql` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `dd` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `ddRawSql` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.
- [cross-layer] `__call` — belongs to Eloquent/connection/console contract or magic dispatch, not the current SQLite QueryBuilder core.

## Evidence gate

- Preserve existing QueryBuilder methods; do not rewrite already passing behavior.
- Add a failing focused test before each SQLite implementation.
- Compare Laravel `Query\Builder` and grammar source for each method.
- Run focused query/Eloquent tests and `uv run python -m pytest -W error::DeprecationWarning tests/ -q`.
- Reclassify a method only after observed behavior and synchronized runtime evidence.
