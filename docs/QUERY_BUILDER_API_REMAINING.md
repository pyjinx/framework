# Laravel 13 Query Builder Remaining Inventory

Machine comparison of `references/framework/src/Illuminate/Database/Query/Builder.php` against `framework/Illuminate/Database/QueryBuilder.py`.

## Surface counts

- Laravel Query Builder: 228 public method declarations.
- PyJinx QueryBuilder: 117 public methods.
- Name-normalized matches: 112.
- Directly missing names: 116.
- Alias/shape matches: 2.

A name mismatch is not automatically a behavior gap. Each candidate requires Laravel source comparison and a focused behavioral test.

## Implemented aliases / shape differences
- `from` → existing PyJinx `from_`
- `average` → existing PyJinx `avg`

## SQLite-supported candidate gaps

These are the next behavior candidates unless Laravel source or SQLite grammar blocks them.
- [x] `joinWhere` — SQLite literal join condition; `tests/test_query_builder.py::test_join_where_compares_join_column_to_literal`.
- [x] `joinSub` — SQLite subquery join through aliased SQLAlchemy subqueries; `tests/test_query_builder.py::test_join_sub_and_cross_join_sqlite_contracts`.
- [x] `leftJoinWhere` — shares the SQLite literal join implementation and binding boundary.
- [x] `leftJoinSub` — shares the SQLite aliased subquery join implementation.
- [ ] `rightJoin`
- [ ] `rightJoinWhere`
- [ ] `rightJoinSub`
- [x] `crossJoin` — SQLite cross join via a true join predicate.
- [x] `crossJoinSub` — SQLite cross join against an aliased subquery.
- [ ] `mergeWheres`
- [x] `orWhereNotBetween` — SQLite boolean `OR` negative range predicate.
- [x] `whereValueBetween` — SQLite value bounded by two columns.
- [x] `orWhereValueBetween` — SQLite `OR` value-between predicate.
- [x] `whereValueNotBetween` — SQLite negated value-between predicate.
- [x] `orWhereValueNotBetween` — SQLite `OR` negated value-between predicate.
- [ ] `whereNested`
- [ ] `forNestedWhere`
- [ ] `addNestedWhereQuery`
- [ ] `addWhereExistsQuery`
- [ ] `dynamicWhere`
- [x] `orHaving` — SQLite boolean `OR` aggregate/group predicate.
- [ ] `havingNested`
- [ ] `addNestedHavingQuery`
- [ ] `havingNull`
- [ ] `orHavingNull`
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
- [ ] `timeout`
- [ ] `beforeQuery`
- [ ] `applyBeforeQueryCallbacks`
- [ ] `afterQuery`
- [ ] `applyAfterQueryCallbacks`
- [ ] `toRawSql`
- [ ] `find`
- [ ] `findOr`
- [x] `rawValue` — SQLite raw expression scalar retrieval; `tests/test_query_builder.py::test_projection_and_binding_contracts`.
- [ ] `soleValue`
- [ ] `paginate`
- [ ] `simplePaginate`
- [ ] `cursorPaginate`
- [ ] `getCountForPagination`
- [x] `implode` — SQLite column concatenation over the selected result window.
- [ ] `existsOr`
- [ ] `doesntExistOr`
- [ ] `aggregate`
- [ ] `numericAggregate`
- [ ] `insertOrIgnore`
- [ ] `insertOrIgnoreReturning`
- [ ] `insertUsing`
- [ ] `insertOrIgnoreUsing`
- [ ] `updateFrom`
- [ ] `updateOrInsert`
- [ ] `incrementEach`
- [ ] `decrementEach`
- [x] `getColumns` — SQLite selected-column metadata.
- [x] `getLimit` — SQLite limit metadata.
- [x] `getOffset` — SQLite offset metadata.
- [x] `getRawBindings` — Laravel-shaped binding buckets.
- [x] `setBindings` — validates and replaces a binding bucket.
- [x] `addBinding` — appends scalar or sequence bindings.
- [x] `castBinding` — identity cast for Python-native values.
- [x] `mergeBindings` — merges Laravel-shaped binding buckets.
- [x] `cleanBindings` — filters SQL expression objects.
- [ ] `useWritePdo`
- [ ] `fetchUsing`

- [ ] `union`
- [ ] `unionAll`
## Explicitly blocked by pinned SQLite / backend boundary

- [blocked] `whereJsonOverlaps` — pinned Laravel SQLite grammar lacks `compileJsonOverlaps`.
- [blocked] `orWhereJsonOverlaps` — pinned Laravel SQLite grammar lacks `compileJsonOverlaps`.
- [blocked] `whereJsonDoesntOverlap` — pinned Laravel SQLite grammar lacks `compileJsonOverlaps`.
- [blocked] `orWhereJsonDoesntOverlap` — pinned Laravel SQLite grammar lacks `compileJsonOverlaps`.

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
