# Laravel 13 Database / Eloquent API Inventory

Generated inventory for the PyJinx parity goal.

## Scope and evidence method

- Laravel source: `references/framework/src/Illuminate/Database/`.
- PyJinx source: `framework/Illuminate/Database/`.
- Public API reference: Laravel 13 API index and namespace pages.
- Each Laravel PHP file, class, and public method is listed below.
- Method rows are provisional status checklists, not exact-parity claims.

## Inventory totals

| Source | Files | Classes / interfaces / traits | Public methods |
|---|---:|---:|---:|
| Laravel 13 Database namespace | 250 | 355 | 2196 |
| PyJinx Database namespace | 27 | 31 | 512 |

Laravel has a substantially larger surface. No area is exact parity until every listed method has behavioral evidence.

## Area summary

| Area | Laravel files | Laravel classes | Laravel public methods | PyJinx files | PyJinx classes | PyJinx public methods | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| `Capsule` | 1 | 1 | 12 | 0 | 0 | 0 | `missing` |
| `Concerns` | 6 | 6 | 41 | 0 | 0 | 0 | `missing` |
| `Connectors` | 9 | 9 | 12 | 0 | 0 | 0 | `missing` |
| `Console` | 24 | 35 | 33 | 0 | 0 | 0 | `missing` |
| `Eloquent` | 108 | 190 | 1067 | 11 | 12 | 236 | `partial` |
| `Events` | 24 | 27 | 16 | 2 | 1 | 0 | `partial` |
| `Migrations` | 6 | 10 | 59 | 0 | 0 | 0 | `partial` |
| `Query` | 17 | 18 | 347 | 0 | 0 | 0 | `partial` |
| `Schema` | 23 | 25 | 391 | 2 | 5 | 60 | `partial` |
| `__root__` | 32 | 34 | 218 | 12 | 13 | 216 | `partial` |

Status meanings: `implemented` means a named PyJinx counterpart exists but still needs evidence; `partial` means only a subset or behavior slice exists; `missing` means no counterpart; `blocked` is reserved for contracts intentionally deferred by the pinned Laravel/SQLite source.

## Laravel file/class/method checklist

### `Capsule/Manager.php` — `missing`
- **class `Manager`** — `missing`
  - `__construct()` — `missing`
  - `connection()` — `missing`
  - `table()` — `missing`
  - `schema()` — `missing`
  - `getConnection()` — `missing`
  - `addConnection()` — `missing`
  - `bootEloquent()` — `missing`
  - `setFetchMode()` — `missing`
  - `getDatabaseManager()` — `missing`
  - `getEventDispatcher()` — `missing`
  - `setEventDispatcher()` — `missing`
  - `__callStatic()` — `missing`

### `ClassMorphViolationException.php` — `partial`
- **class `ClassMorphViolationException`** — `partial`
  - `__construct()` — `partial`

### `Concerns/BuildsQueries.php` — `missing`
- **class `BuildsQueries`** — `missing`
  - `chunk()` — `missing`
  - `chunkMap()` — `missing`
  - `each()` — `missing`
  - `chunkById()` — `missing`
  - `chunkByIdDesc()` — `missing`
  - `orderedChunkById()` — `missing`
  - `eachById()` — `missing`
  - `lazy()` — `missing`
  - `lazyById()` — `missing`
  - `lazyByIdDesc()` — `missing`
  - `first()` — `missing`
  - `firstOrFail()` — `missing`
  - `sole()` — `missing`
  - `tap()` — `missing`
  - `pipe()` — `missing`

### `Concerns/BuildsWhereDateClauses.php` — `missing`
- **class `BuildsWhereDateClauses`** — `missing`
  - `wherePast()` — `missing`
  - `whereNowOrPast()` — `missing`
  - `orWherePast()` — `missing`
  - `orWhereNowOrPast()` — `missing`
  - `whereFuture()` — `missing`
  - `whereNowOrFuture()` — `missing`
  - `orWhereFuture()` — `missing`
  - `orWhereNowOrFuture()` — `missing`
  - `whereToday()` — `missing`
  - `whereBeforeToday()` — `missing`
  - `whereTodayOrBefore()` — `missing`
  - `whereAfterToday()` — `missing`
  - `whereTodayOrAfter()` — `missing`
  - `orWhereToday()` — `missing`
  - `orWhereBeforeToday()` — `missing`
  - `orWhereTodayOrBefore()` — `missing`
  - `orWhereAfterToday()` — `missing`
  - `orWhereTodayOrAfter()` — `missing`

### `Concerns/CompilesJsonPaths.php` — `missing`
- **class `CompilesJsonPaths`** — `missing`

### `Concerns/ExplainsQueries.php` — `missing`
- **class `ExplainsQueries`** — `missing`
  - `explain()` — `missing`

### `Concerns/ManagesTransactions.php` — `missing`
- **class `ManagesTransactions`** — `missing`
  - `transaction()` — `missing`
  - `beginTransaction()` — `missing`
  - `commit()` — `missing`
  - `rollBack()` — `missing`
  - `transactionLevel()` — `missing`
  - `afterCommit()` — `missing`
  - `afterRollBack()` — `missing`

### `Concerns/ParsesSearchPath.php` — `missing`
- **class `ParsesSearchPath`** — `missing`

### `ConcurrencyErrorDetector.php` — `partial`
- **class `ConcurrencyErrorDetector`** — `partial`
  - `causedByConcurrencyError()` — `partial`

### `ConfigurationUrlParser.php` — `partial`
- **class `ConfigurationUrlParser`** — `partial`

### `Connection.php` — `partial`
- **class `Connection`** — `partial`
  - `__construct()` — `partial`
  - `useDefaultQueryGrammar()` — `partial`
  - `useDefaultSchemaGrammar()` — `partial`
  - `useDefaultPostProcessor()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `table()` — `partial`
  - `query()` — `partial`
  - `selectOne()` — `partial`
  - `scalar()` — `partial`
  - `selectFromWriteConnection()` — `partial`
  - `select()` — `partial`
  - `selectResultSets()` — `partial`
  - `cursor()` — `partial`
  - `insert()` — `partial`
  - `update()` — `partial`
  - `delete()` — `partial`
  - `statement()` — `partial`
  - `affectingStatement()` — `partial`
  - `unprepared()` — `partial`
  - `threadCount()` — `partial`
  - `pretend()` — `partial`
  - `withoutPretending()` — `partial`
  - `bindValues()` — `partial`
  - `prepareBindings()` — `partial`
  - `logQuery()` — `partial`
  - `whenQueryingForLongerThan()` — `partial`
  - `allowQueryDurationHandlersToRunAgain()` — `partial`
  - `totalQueryDuration()` — `partial`
  - `resetTotalQueryDuration()` — `partial`
  - `reconnect()` — `partial`
  - `reconnectIfMissingConnection()` — `partial`
  - `disconnect()` — `partial`
  - `beforeStartingTransaction()` — `partial`
  - `beforeExecuting()` — `partial`
  - `listen()` — `partial`
  - `raw()` — `partial`
  - `escape()` — `partial`
  - `hasModifiedRecords()` — `partial`
  - `recordsHaveBeenModified()` — `partial`
  - `setRecordModificationState()` — `partial`
  - `forgetRecordModificationState()` — `partial`
  - `useWriteConnectionWhenReading()` — `partial`
  - `getPdo()` — `partial`
  - `getRawPdo()` — `partial`
  - `getReadPdo()` — `partial`
  - `getRawReadPdo()` — `partial`
  - `getDirectPdo()` — `partial`
  - `getRawDirectPdo()` — `partial`
  - `setPdo()` — `partial`
  - `setReadPdo()` — `partial`
  - `setReadPdoConfig()` — `partial`
  - `setDirectPdo()` — `partial`
  - `setDirectPdoConfig()` — `partial`
  - `getDirectPdoConfig()` — `partial`
  - `hasDirectConnection()` — `partial`
  - `setReconnector()` — `partial`
  - `getName()` — `partial`
  - `getNameWithReadWriteType()` — `partial`
  - `getConfig()` — `partial`
  - `getDriverName()` — `partial`
  - `getDriverTitle()` — `partial`
  - `getQueryGrammar()` — `partial`
  - `setQueryGrammar()` — `partial`
  - `getSchemaGrammar()` — `partial`
  - `setSchemaGrammar()` — `partial`
  - `getPostProcessor()` — `partial`
  - `setPostProcessor()` — `partial`
  - `getEventDispatcher()` — `partial`
  - `setEventDispatcher()` — `partial`
  - `unsetEventDispatcher()` — `partial`
  - `setTransactionManager()` — `partial`
  - `unsetTransactionManager()` — `partial`
  - `pretending()` — `partial`
  - `getQueryLog()` — `partial`
  - `getRawQueryLog()` — `partial`
  - `flushQueryLog()` — `partial`
  - `enableQueryLog()` — `partial`
  - `disableQueryLog()` — `partial`
  - `logging()` — `partial`
  - `getDatabaseName()` — `partial`
  - `setDatabaseName()` — `partial`
  - `setReadWriteType()` — `partial`
  - `getTablePrefix()` — `partial`
  - `setTablePrefix()` — `partial`
  - `withoutTablePrefix()` — `partial`
  - `getServerVersion()` — `partial`
  - `resolverFor()` — `partial`
  - `getResolver()` — `partial`
  - `__clone()` — `partial`

### `ConnectionInterface.php` — `partial`
- **class `ConnectionInterface`** — `partial`
  - `table()` — `partial`
  - `raw()` — `partial`
  - `selectOne()` — `partial`
  - `scalar()` — `partial`
  - `select()` — `partial`
  - `cursor()` — `partial`
  - `insert()` — `partial`
  - `update()` — `partial`
  - `delete()` — `partial`
  - `statement()` — `partial`
  - `affectingStatement()` — `partial`
  - `unprepared()` — `partial`
  - `prepareBindings()` — `partial`
  - `transaction()` — `partial`
  - `beginTransaction()` — `partial`
  - `commit()` — `partial`
  - `rollBack()` — `partial`
  - `transactionLevel()` — `partial`
  - `pretend()` — `partial`
  - `getDatabaseName()` — `partial`

### `ConnectionResolver.php` — `partial`
- **class `ConnectionResolver`** — `partial`
  - `__construct()` — `partial`
  - `connection()` — `partial`
  - `addConnection()` — `partial`
  - `hasConnection()` — `partial`
  - `getDefaultConnection()` — `partial`
  - `setDefaultConnection()` — `partial`

### `ConnectionResolverInterface.php` — `partial`
- **class `ConnectionResolverInterface`** — `partial`
  - `connection()` — `partial`
  - `getDefaultConnection()` — `partial`
  - `setDefaultConnection()` — `partial`

### `Connectors/Concerns/ConfiguresPooledConnections.php` — `missing`
- **class `ConfiguresPooledConnections`** — `missing`

### `Connectors/ConnectionFactory.php` — `missing`
- **class `ConnectionFactory`** — `missing`
  - `__construct()` — `missing`
  - `make()` — `missing`
  - `createConnector()` — `missing`

### `Connectors/Connector.php` — `missing`
- **class `Connector`** — `missing`
  - `createConnection()` — `missing`
  - `getOptions()` — `missing`
  - `getDefaultOptions()` — `missing`
  - `setDefaultOptions()` — `missing`

### `Connectors/ConnectorInterface.php` — `missing`
- **class `ConnectorInterface`** — `missing`
  - `connect()` — `missing`

### `Connectors/MariaDbConnector.php` — `missing`
- **class `MariaDbConnector`** — `missing`

### `Connectors/MySqlConnector.php` — `missing`
- **class `MySqlConnector`** — `missing`
  - `connect()` — `missing`

### `Connectors/PostgresConnector.php` — `missing`
- **class `PostgresConnector`** — `missing`
  - `connect()` — `missing`

### `Connectors/SQLiteConnector.php` — `missing`
- **class `SQLiteConnector`** — `missing`
  - `connect()` — `missing`

### `Connectors/SqlServerConnector.php` — `missing`
- **class `SqlServerConnector`** — `missing`
  - `connect()` — `missing`

### `Console/Concerns/InteractsWithPooledConnections.php` — `missing`
- **class `InteractsWithPooledConnections`** — `missing`

### `Console/DatabaseInspectionCommand.php` — `missing`
- **class `DatabaseInspectionCommand`** — `missing`

### `Console/DbCommand.php` — `missing`
- **class `DbCommand`** — `missing`
  - `handle()` — `missing`
  - `getConnection()` — `missing`
  - `commandArguments()` — `missing`
  - `commandEnvironment()` — `missing`
  - `getCommand()` — `missing`

### `Console/DumpCommand.php` — `missing`
- **class `DumpCommand`** — `missing`
  - `handle()` — `missing`

### `Console/Factories/FactoryMakeCommand.php` — `missing`
- **class `FactoryMakeCommand`** — `missing`
- **class `being`** — `missing`
- **class `with`** — `missing`
- **class `path`** — `missing`

### `Console/Migrations/BaseCommand.php` — `missing`
- **class `BaseCommand`** — `missing`

### `Console/Migrations/FreshCommand.php` — `missing`
- **class `FreshCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`
- **class `name`** — `missing`

### `Console/Migrations/InstallCommand.php` — `missing`
- **class `InstallCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`

### `Console/Migrations/MigrateCommand.php` — `missing`
- **class `MigrateCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`
- **class `name`** — `missing`

### `Console/Migrations/MigrateMakeCommand.php` — `missing`
- **class `MigrateMakeCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`
- **class `loaders`** — `missing`

### `Console/Migrations/RefreshCommand.php` — `missing`
- **class `RefreshCommand`** — `missing`
  - `handle()` — `missing`
- **class `name`** — `missing`

### `Console/Migrations/ResetCommand.php` — `missing`
- **class `ResetCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`

### `Console/Migrations/RollbackCommand.php` — `missing`
- **class `RollbackCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`

### `Console/Migrations/StatusCommand.php` — `missing`
- **class `StatusCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`

### `Console/Migrations/TableGuesser.php` — `missing`
- **class `TableGuesser`** — `missing`
  - `guess()` — `missing`

### `Console/MonitorCommand.php` — `missing`
- **class `MonitorCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`

### `Console/PruneCommand.php` — `missing`
- **class `PruneCommand`** — `missing`
  - `handle()` — `missing`

### `Console/Seeds/SeedCommand.php` — `missing`
- **class `SeedCommand`** — `missing`
  - `__construct()` — `missing`
  - `handle()` — `missing`
- **class `name`** — `missing`
- **class `name`** — `missing`

### `Console/Seeds/SeederMakeCommand.php` — `missing`
- **class `SeederMakeCommand`** — `missing`
  - `handle()` — `missing`
- **class `being`** — `missing`
- **class `path`** — `missing`

### `Console/Seeds/WithoutModelEvents.php` — `missing`
- **class `WithoutModelEvents`** — `missing`
  - `withoutModelEvents()` — `missing`

### `Console/ShowCommand.php` — `missing`
- **class `ShowCommand`** — `missing`
  - `handle()` — `missing`

### `Console/ShowModelCommand.php` — `missing`
- **class `ShowModelCommand`** — `missing`
  - `handle()` — `missing`

### `Console/TableCommand.php` — `missing`
- **class `TableCommand`** — `missing`
  - `handle()` — `missing`

### `Console/WipeCommand.php` — `missing`
- **class `WipeCommand`** — `missing`
  - `handle()` — `missing`

### `DatabaseManager.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/DatabaseManager.py`.
- **class `DatabaseManager`** — `partial`
  - `__construct()` — `partial`
  - `connection()` — `partial`
  - `build()` — `partial`
  - `calculateDynamicConnectionName()` — `partial`
  - `connectUsing()` — `partial`
  - `purge()` — `partial`
  - `disconnect()` — `partial`
  - `reconnect()` — `partial`
  - `usingConnection()` — `partial`
  - `getDefaultConnection()` — `partial`
  - `setDefaultConnection()` — `partial`
  - `supportedDrivers()` — `partial`
  - `availableDrivers()` — `partial`
  - `extend()` — `partial`
  - `forgetExtension()` — `partial`
  - `getConnections()` — `partial`
  - `setReconnector()` — `partial`
  - `setApplication()` — `partial`
  - `__call()` — `partial`

### `DatabaseServiceProvider.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/DatabaseServiceProvider.py`.
- **class `DatabaseServiceProvider`** — `partial`
  - `boot()` — `partial`
  - `register()` — `partial`
- **class `which`** — `partial`

### `DatabaseTransactionRecord.php` — `partial`
- **class `DatabaseTransactionRecord`** — `partial`
  - `__construct()` — `partial`
  - `addCallback()` — `partial`
  - `addCallbackForRollback()` — `partial`
  - `executeCallbacks()` — `partial`
  - `executeCallbacksForRollback()` — `partial`
  - `getCallbacks()` — `partial`
  - `getCallbacksForRollback()` — `partial`

### `DatabaseTransactionsManager.php` — `partial`
- **class `DatabaseTransactionsManager`** — `partial`
  - `__construct()` — `partial`
  - `begin()` — `partial`
  - `commit()` — `partial`
  - `stageTransactions()` — `partial`
  - `rollback()` — `partial`
  - `addCallback()` — `partial`
  - `addCallbackForRollback()` — `partial`
  - `callbackApplicableTransactions()` — `partial`
  - `afterCommitCallbacksShouldBeExecuted()` — `partial`
  - `getPendingTransactions()` — `partial`
  - `getCommittedTransactions()` — `partial`

### `DeadlockException.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/DeadlockException.py`.
- **class `DeadlockException`** — `partial`

### `DetectsConcurrencyErrors.php` — `partial`
- **class `DetectsConcurrencyErrors`** — `partial`

### `DetectsLostConnections.php` — `partial`
- **class `DetectsLostConnections`** — `partial`

### `Eloquent/Attributes/Appends.php` — `partial`
- **class `Appends`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Boot.php` — `partial`
- **class `Boot`** — `partial`

### `Eloquent/Attributes/CollectedBy.php` — `partial`
- **class `CollectedBy`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Connection.php` — `partial`
- **class `Connection`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/DateFormat.php` — `partial`
- **class `DateFormat`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Fillable.php` — `partial`
- **class `Fillable`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Guarded.php` — `partial`
- **class `Guarded`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Hidden.php` — `partial`
- **class `Hidden`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Initialize.php` — `partial`
- **class `Initialize`** — `partial`

### `Eloquent/Attributes/ObservedBy.php` — `partial`
- **class `ObservedBy`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/RouteKey.php` — `partial`
- **class `RouteKey`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Scope.php` — `partial`
- **class `Scope`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/ScopedBy.php` — `partial`
- **class `ScopedBy`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Table.php` — `partial`
- **class `Table`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Touches.php` — `partial`
- **class `Touches`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Unguarded.php` — `partial`
- **class `Unguarded`** — `partial`

### `Eloquent/Attributes/UseEloquentBuilder.php` — `partial`
- **class `UseEloquentBuilder`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/UseFactory.php` — `partial`
- **class `UseFactory`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/UsePolicy.php` — `partial`
- **class `UsePolicy`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/UseResource.php` — `partial`
- **class `UseResource`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/UseResourceCollection.php` — `partial`
- **class `UseResourceCollection`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/Visible.php` — `partial`
- **class `Visible`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/WithoutIncrementing.php` — `partial`
- **class `WithoutIncrementing`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Attributes/WithoutTimestamps.php` — `partial`
- **class `WithoutTimestamps`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/BroadcastableModelEventOccurred.php` — `partial`
- **class `BroadcastableModelEventOccurred`** — `partial`
  - `__construct()` — `partial`
  - `broadcastOn()` — `partial`
  - `broadcastAs()` — `partial`
  - `broadcastWith()` — `partial`
  - `onChannels()` — `partial`
  - `shouldBroadcastNow()` — `partial`
  - `event()` — `partial`

### `Eloquent/BroadcastsEvents.php` — `partial`
- **class `BroadcastsEvents`** — `partial`
  - `bootBroadcastsEvents()` — `partial`
  - `broadcastCreated()` — `partial`
  - `broadcastUpdated()` — `partial`
  - `broadcastTrashed()` — `partial`
  - `broadcastRestored()` — `partial`
  - `broadcastDeleted()` — `partial`
  - `newBroadcastableModelEvent()` — `partial`
  - `broadcastOn()` — `partial`
  - `broadcastConnection()` — `partial`
  - `broadcastQueue()` — `partial`
  - `broadcastAfterCommit()` — `partial`

### `Eloquent/BroadcastsEventsAfterCommit.php` — `partial`
- **class `BroadcastsEventsAfterCommit`** — `partial`
  - `broadcastAfterCommit()` — `partial`

### `Eloquent/Builder.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Builder.py`.
- **class `Builder`** — `partial`
  - `__construct()` — `partial`
  - `make()` — `partial`
  - `withGlobalScope()` — `partial`
  - `withoutGlobalScope()` — `partial`
  - `withoutGlobalScopes()` — `partial`
  - `withoutGlobalScopesExcept()` — `partial`
  - `removedScopes()` — `partial`
  - `whereKey()` — `partial`
  - `whereKeyNot()` — `partial`
  - `except()` — `partial`
  - `where()` — `partial`
  - `firstWhere()` — `partial`
  - `orWhere()` — `partial`
  - `whereNot()` — `partial`
  - `orWhereNot()` — `partial`
  - `latest()` — `partial`
  - `oldest()` — `partial`
  - `hydrate()` — `partial`
  - `fillAndInsert()` — `partial`
  - `fillAndInsertOrIgnore()` — `partial`
  - `fillAndInsertGetId()` — `partial`
  - `fillForInsert()` — `partial`
  - `fromQuery()` — `partial`
  - `find()` — `partial`
  - `findSole()` — `partial`
  - `findMany()` — `partial`
  - `findOrFail()` — `partial`
  - `findOrNew()` — `partial`
  - `findOr()` — `partial`
  - `firstOrNew()` — `partial`
  - `firstOrCreate()` — `partial`
  - `createOrFirst()` — `partial`
  - `updateOrCreate()` — `partial`
  - `incrementOrCreate()` — `partial`
  - `firstOrFail()` — `partial`
  - `firstOr()` — `partial`
  - `sole()` — `partial`
  - `value()` — `partial`
  - `soleValue()` — `partial`
  - `valueOrFail()` — `partial`
  - `get()` — `partial`
  - `getModels()` — `partial`
  - `eagerLoadRelations()` — `partial`
- **public method `getRelation()`** — `partial`
- **public method `afterQuery()`** — `partial`
- **public method `applyAfterQueryCallbacks()`** — `partial`
- **public method `cursor()`** — `partial`
- **public method `pluck()`** — `partial`
- **public method `modelKeys()`** — `partial`
- **public method `paginate()`** — `partial`
- **public method `simplePaginate()`** — `partial`
- **public method `cursorPaginate()`** — `partial`
- **public method `create()`** — `partial`
- **public method `createQuietly()`** — `partial`
- **public method `forceCreate()`** — `partial`
- **public method `forceCreateQuietly()`** — `partial`
- **public method `update()`** — `partial`
- **public method `upsert()`** — `partial`
- **public method `touch()`** — `partial`
- **public method `increment()`** — `partial`
- **public method `decrement()`** — `partial`
- **public method `incrementEach()`** — `partial`
- **public method `decrementEach()`** — `partial`
- **public method `delete()`** — `partial`
- **public method `forceDelete()`** — `partial`
- **public method `onDelete()`** — `partial`
- **public method `hasNamedScope()`** — `partial`
- **public method `scopes()`** — `partial`
- **public method `applyScopes()`** — `partial`
- **public method `with()`** — `partial`
- **public method `without()`** — `partial`
- **public method `withOnly()`** — `partial`
- **public method `newModelInstance()`** — `partial`
- **public method `withAttributes()`** — `partial`
- **public method `withCasts()`** — `partial`
- **public method `withSavepointIfNeeded()`** — `partial`
- **public method `getQuery()`** — `partial`
- **public method `setQuery()`** — `partial`
- **public method `toBase()`** — `partial`
- **public method `getEagerLoads()`** — `partial`
- **public method `setEagerLoads()`** — `partial`
- **public method `withoutEagerLoad()`** — `partial`
- **public method `withoutEagerLoads()`** — `partial`
- **public method `getLimit()`** — `partial`
- **public method `getOffset()`** — `partial`
- **public method `getModel()`** — `partial`
- **public method `setModel()`** — `partial`
- **public method `qualifyColumn()`** — `partial`
- **public method `qualifyColumns()`** — `partial`
- **public method `getMacro()`** — `partial`
- **public method `hasMacro()`** — `partial`
- **public method `getGlobalMacro()`** — `partial`
- **public method `hasGlobalMacro()`** — `partial`
- **public method `__get()`** — `partial`
- **public method `__call()`** — `partial`
- **public method `__callStatic()`** — `partial`
- **public method `clone()`** — `partial`
- **public method `onClone()`** — `partial`
- **public method `__clone()`** — `partial`

### `Eloquent/Casts/ArrayObject.php` — `partial`
- **class `ArrayObject`** — `partial`
  - `collect()` — `partial`
  - `toArray()` — `partial`
  - `jsonSerialize()` — `partial`

### `Eloquent/Casts/AsArrayObject.php` — `partial`
- **class `AsArrayObject`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `serialize()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/AsBinary.php` — `partial`
- **class `AsBinary`** — `partial`
  - `castUsing()` — `partial`
  - `__construct()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `uuid()` — `partial`
  - `ulid()` — `partial`
  - `of()` — `partial`
- **class `to`** — `partial`

### `Eloquent/Casts/AsCollection.php` — `partial`
- **class `AsCollection`** — `partial`
  - `castUsing()` — `partial`
  - `__construct()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `of()` — `partial`
  - `using()` — `partial`
- **class `to`** — `partial`
- **class `must`** — `partial`

### `Eloquent/Casts/AsEncryptedArrayObject.php` — `partial`
- **class `AsEncryptedArrayObject`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `serialize()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/AsEncryptedCollection.php` — `partial`
- **class `AsEncryptedCollection`** — `partial`
  - `castUsing()` — `partial`
  - `__construct()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `of()` — `partial`
  - `using()` — `partial`
- **class `to`** — `partial`
- **class `must`** — `partial`

### `Eloquent/Casts/AsEnumArrayObject.php` — `partial`
- **class `AsEnumArrayObject`** — `partial`
  - `castUsing()` — `partial`
  - `__construct()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `serialize()` — `partial`
  - `of()` — `partial`
- **class `to`** — `partial`

### `Eloquent/Casts/AsEnumCollection.php` — `partial`
- **class `AsEnumCollection`** — `partial`
  - `castUsing()` — `partial`
  - `__construct()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `serialize()` — `partial`
  - `of()` — `partial`
- **class `to`** — `partial`

### `Eloquent/Casts/AsFluent.php` — `partial`
- **class `AsFluent`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/AsHtmlString.php` — `partial`
- **class `AsHtmlString`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/AsStringable.php` — `partial`
- **class `AsStringable`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/AsUri.php` — `partial`
- **class `AsUri`** — `partial`
  - `castUsing()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
- **class `to`** — `partial`
- **class `implements`** — `partial`

### `Eloquent/Casts/Attribute.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Casts/Attribute.py`.
- **class `Attribute`** — `partial`
  - `__construct()` — `partial`
  - `make()` — `partial`
  - `get()` — `partial`
  - `set()` — `partial`
  - `withoutObjectCaching()` — `partial`
  - `shouldCache()` — `partial`

### `Eloquent/Casts/Json.php` — `partial`
- **class `Json`** — `partial`
  - `encode()` — `partial`
  - `decode()` — `partial`
  - `encodeUsing()` — `partial`
  - `decodeUsing()` — `partial`

### `Eloquent/Collection.php` — `partial`
- **class `Collection`** — `partial`
  - `find()` — `partial`
  - `findOrFail()` — `partial`
  - `load()` — `partial`
  - `loadAggregate()` — `partial`
  - `loadCount()` — `partial`
  - `loadMax()` — `partial`
  - `loadMin()` — `partial`
  - `loadSum()` — `partial`
  - `loadAvg()` — `partial`
  - `loadExists()` — `partial`
  - `loadMissing()` — `partial`
  - `loadMissingRelationshipChain()` — `partial`
  - `loadMorph()` — `partial`
  - `loadMorphCount()` — `partial`
  - `contains()` — `partial`
  - `doesntContain()` — `partial`
  - `modelKeys()` — `partial`
  - `merge()` — `partial`
  - `map()` — `partial`
  - `mapWithKeys()` — `partial`
  - `fresh()` — `partial`
  - `diff()` — `partial`
  - `intersect()` — `partial`
  - `unique()` — `partial`
  - `only()` — `partial`
  - `except()` — `partial`
  - `makeHidden()` — `partial`
  - `mergeHidden()` — `partial`
  - `setHidden()` — `partial`
  - `makeVisible()` — `partial`
  - `mergeVisible()` — `partial`
  - `setVisible()` — `partial`
  - `append()` — `partial`
  - `setAppends()` — `partial`
  - `withoutAppends()` — `partial`
  - `getDictionary()` — `partial`
  - `countBy()` — `partial`
  - `collapse()` — `partial`
  - `flatten()` — `partial`
  - `flip()` — `partial`
  - `keys()` — `partial`
  - `pad()` — `partial`
  - `partition()` — `partial`
  - `pluck()` — `partial`
  - `zip()` — `partial`
  - `withRelationshipAutoloading()` — `partial`
  - `getQueueableClass()` — `partial`
  - `getQueueableIds()` — `partial`
  - `getQueueableRelations()` — `partial`
  - `getQueueableConnection()` — `partial`
  - `toQuery()` — `partial`
- **class `name`** — `partial`

### `Eloquent/Concerns/GuardsAttributes.php` — `partial`
- **class `GuardsAttributes`** — `partial`
  - `initializeGuardsAttributes()` — `partial`
  - `getFillable()` — `partial`
  - `fillable()` — `partial`
  - `mergeFillable()` — `partial`
  - `getGuarded()` — `partial`
  - `guard()` — `partial`
  - `mergeGuarded()` — `partial`
  - `unguard()` — `partial`
  - `reguard()` — `partial`
  - `isUnguarded()` — `partial`
  - `unguarded()` — `partial`
  - `isFillable()` — `partial`
- **public method `isGuarded()`** — `partial`
- **public method `totallyGuarded()`** — `partial`

### `Eloquent/Concerns/HasAttributes.php` — `partial`
- **class `HasAttributes`** — `partial`
  - `attributesToArray()` — `partial`
  - `relationsToArray()` — `partial`
  - `hasAttribute()` — `partial`
  - `getAttribute()` — `partial`
  - `getAttributeValue()` — `partial`
  - `getRelationValue()` — `partial`
  - `isRelation()` — `partial`
  - `hasGetMutator()` — `partial`
  - `hasAttributeMutator()` — `partial`
  - `hasAttributeGetMutator()` — `partial`
  - `hasAnyGetMutator()` — `partial`
  - `mergeCasts()` — `partial`
  - `setAttribute()` — `partial`
  - `hasSetMutator()` — `partial`
  - `hasAttributeSetMutator()` — `partial`
  - `fillJsonAttribute()` — `partial`
  - `fromJson()` — `partial`
  - `fromEncryptedString()` — `partial`
  - `encryptUsing()` — `partial`
  - `currentEncrypter()` — `partial`
  - `fromFloat()` — `partial`
  - `fromDateTime()` — `partial`
  - `getDates()` — `partial`
  - `getDateFormat()` — `partial`
  - `setDateFormat()` — `partial`
  - `hasCast()` — `partial`
  - `getCasts()` — `partial`
  - `getAttributes()` — `partial`
  - `setRawAttributes()` — `partial`
  - `getOriginal()` — `partial`
  - `getRawOriginal()` — `partial`
  - `only()` — `partial`
  - `except()` — `partial`
  - `syncOriginal()` — `partial`
  - `syncOriginalAttribute()` — `partial`
  - `syncOriginalAttributes()` — `partial`
  - `syncChanges()` — `partial`
  - `isDirty()` — `partial`
  - `isClean()` — `partial`
  - `discardChanges()` — `partial`
  - `wasChanged()` — `partial`
  - `getDirty()` — `partial`
  - `getChanges()` — `partial`
  - `getPrevious()` — `partial`
  - `originalIsEquivalent()` — `partial`
  - `append()` — `partial`
  - `getAppends()` — `partial`
  - `setAppends()` — `partial`
  - `mergeAppends()` — `partial`
  - `hasAppended()` — `partial`
  - `withoutAppends()` — `partial`
  - `getMutatedAttributes()` — `partial`
  - `cacheMutatedAttributes()` — `partial`
- **class `we`** — `partial`
- **class `itself`** — `partial`
- **class `castable`** — `partial`
- **class `and`** — `partial`
- **class `for`** — `partial`
- **class `and`** — `partial`
- **class `and`** — `partial`
- **class `attributes`** — `partial`
- **class `attribute`** — `partial`
- **class `attributes`** — `partial`
- **class `attribute`** — `partial`
- **class `caster`** — `partial`

### `Eloquent/Concerns/HasEvents.php` — `partial`
- **class `HasEvents`** — `partial`
  - `bootHasEvents()` — `partial`
  - `resolveObserveAttributes()` — `partial`
  - `observe()` — `partial`
  - `getObservableEvents()` — `partial`
  - `setObservableEvents()` — `partial`
  - `addObservableEvents()` — `partial`
  - `removeObservableEvents()` — `partial`
  - `retrieved()` — `partial`
  - `saving()` — `partial`
  - `saved()` — `partial`
  - `updating()` — `partial`
  - `updated()` — `partial`
  - `creating()` — `partial`
  - `created()` — `partial`
  - `replicating()` — `partial`
  - `deleting()` — `partial`
  - `deleted()` — `partial`
  - `flushEventListeners()` — `partial`
  - `dispatchesEvents()` — `partial`
  - `getEventDispatcher()` — `partial`
  - `setEventDispatcher()` — `partial`
  - `unsetEventDispatcher()` — `partial`
  - `withoutEvents()` — `partial`
- **class `for`** — `partial`
- **class `names`** — `partial`
- **class `name`** — `partial`

### `Eloquent/Concerns/HasGlobalScopes.php` — `partial`
- **class `HasGlobalScopes`** — `partial`
  - `bootHasGlobalScopes()` — `partial`
  - `resolveGlobalScopeAttributes()` — `partial`
  - `addGlobalScope()` — `partial`
  - `addGlobalScopes()` — `partial`
  - `hasGlobalScope()` — `partial`
  - `getGlobalScope()` — `partial`
  - `getAllGlobalScopes()` — `partial`
  - `setAllGlobalScopes()` — `partial`
  - `getGlobalScopes()` — `partial`
- **class `for`** — `partial`
- **class `names`** — `partial`
- **class `name`** — `partial`
- **class `extending`** — `partial`
- **class `instance`** — `partial`

### `Eloquent/Concerns/HasRelationships.php` — `partial`
- **class `HasRelationships`** — `partial`
  - `initializeHasRelationships()` — `partial`
  - `relationResolver()` — `partial`
  - `resolveRelationUsing()` — `partial`
  - `hasRelationAutoloadCallback()` — `partial`
  - `autoloadRelationsUsing()` — `partial`
  - `hasOne()` — `partial`
  - `hasOneThrough()` — `partial`
  - `morphOne()` — `partial`
  - `belongsTo()` — `partial`
  - `morphTo()` — `partial`
  - `getActualClassNameForMorph()` — `partial`
  - `through()` — `partial`
  - `hasMany()` — `partial`
  - `hasManyThrough()` — `partial`
  - `morphMany()` — `partial`
  - `belongsToMany()` — `partial`
  - `morphToMany()` — `partial`
  - `morphedByMany()` — `partial`
  - `joiningTable()` — `partial`
  - `joiningTableSegment()` — `partial`
  - `touches()` — `partial`
  - `touchOwners()` — `partial`
  - `getMorphClass()` — `partial`
  - `getRelations()` — `partial`
  - `getRelation()` — `partial`
  - `relationLoaded()` — `partial`
  - `setRelation()` — `partial`
  - `unsetRelation()` — `partial`
  - `setRelations()` — `partial`
  - `withRelationshipAutoloading()` — `partial`
  - `withoutRelations()` — `partial`
  - `withoutRelation()` — `partial`
  - `unsetRelations()` — `partial`
  - `getTouchedRelations()` — `partial`
  - `setTouchedRelations()` — `partial`
- **class `and`** — `partial`
- **class `name`** — `partial`
- **class `name`** — `partial`

### `Eloquent/Concerns/HasTimestamps.php` — `partial`
- **class `HasTimestamps`** — `partial`
  - `initializeHasTimestamps()` — `partial`
  - `touch()` — `partial`
  - `touchQuietly()` — `partial`
  - `updateTimestamps()` — `partial`
  - `setCreatedAt()` — `partial`
  - `setUpdatedAt()` — `partial`
  - `freshTimestamp()` — `partial`
  - `freshTimestampString()` — `partial`
  - `usesTimestamps()` — `partial`
  - `getCreatedAtColumn()` — `partial`
  - `getUpdatedAtColumn()` — `partial`
  - `getQualifiedCreatedAtColumn()` — `partial`
  - `getQualifiedUpdatedAtColumn()` — `partial`
  - `withoutTimestamps()` — `partial`
  - `withoutTimestampsOn()` — `partial`
  - `isIgnoringTimestamps()` — `partial`
- **class `during`** — `partial`

### `Eloquent/Concerns/HasUlids.php` — `partial`
- **class `HasUlids`** — `partial`
  - `newUniqueId()` — `partial`

### `Eloquent/Concerns/HasUniqueIds.php` — `partial`
- **class `HasUniqueIds`** — `partial`
  - `usesUniqueIds()` — `partial`
  - `setUniqueIds()` — `partial`
  - `newUniqueId()` — `partial`
  - `uniqueIds()` — `partial`

### `Eloquent/Concerns/HasUniqueStringIds.php` — `partial`
- **class `HasUniqueStringIds`** — `partial`
  - `initializeHasUniqueStringIds()` — `partial`
  - `uniqueIds()` — `partial`
  - `resolveRouteBindingQuery()` — `partial`
  - `getKeyType()` — `partial`
  - `getIncrementing()` — `partial`

### `Eloquent/Concerns/HasUuids.php` — `partial`
- **class `HasUuids`** — `partial`
  - `newUniqueId()` — `partial`

### `Eloquent/Concerns/HasVersion4Uuids.php` — `partial`
- **class `HasVersion4Uuids`** — `partial`
  - `newUniqueId()` — `partial`

### `Eloquent/Concerns/HidesAttributes.php` — `partial`
- **class `HidesAttributes`** — `partial`
  - `initializeHidesAttributes()` — `partial`
  - `getHidden()` — `partial`
  - `setHidden()` — `partial`
  - `mergeHidden()` — `partial`
  - `getVisible()` — `partial`
  - `setVisible()` — `partial`
  - `mergeVisible()` — `partial`
  - `makeVisible()` — `partial`
  - `makeVisibleIf()` — `partial`
  - `makeHidden()` — `partial`
  - `makeHiddenIf()` — `partial`

### `Eloquent/Concerns/PreventsCircularRecursion.php` — `partial`
- **class `PreventsCircularRecursion`** — `partial`

### `Eloquent/Concerns/QueriesRelationships.php` — `partial`
- **class `QueriesRelationships`** — `partial`
  - `has()` — `partial`
  - `orHas()` — `partial`
  - `doesntHave()` — `partial`
  - `orDoesntHave()` — `partial`
  - `whereHas()` — `partial`
  - `withWhereHas()` — `partial`
  - `orWhereHas()` — `partial`
  - `whereDoesntHave()` — `partial`
  - `orWhereDoesntHave()` — `partial`
  - `hasMorph()` — `partial`
  - `orHasMorph()` — `partial`
  - `doesntHaveMorph()` — `partial`
  - `orDoesntHaveMorph()` — `partial`
  - `whereHasMorph()` — `partial`
  - `orWhereHasMorph()` — `partial`
  - `whereDoesntHaveMorph()` — `partial`
  - `orWhereDoesntHaveMorph()` — `partial`
  - `whereRelation()` — `partial`
  - `withWhereRelation()` — `partial`
  - `orWhereRelation()` — `partial`
  - `whereDoesntHaveRelation()` — `partial`
  - `orWhereDoesntHaveRelation()` — `partial`
  - `whereMorphRelation()` — `partial`
  - `orWhereMorphRelation()` — `partial`
  - `whereMorphDoesntHaveRelation()` — `partial`
  - `orWhereMorphDoesntHaveRelation()` — `partial`
  - `whereMorphedTo()` — `partial`
  - `whereNotMorphedTo()` — `partial`
  - `orWhereMorphedTo()` — `partial`
  - `orWhereNotMorphedTo()` — `partial`
  - `whereBelongsTo()` — `partial`
  - `orWhereBelongsTo()` — `partial`
  - `whereAttachedTo()` — `partial`
  - `orWhereAttachedTo()` — `partial`
  - `withAggregate()` — `partial`
  - `withCount()` — `partial`
  - `withMax()` — `partial`
  - `withMin()` — `partial`
  - `withSum()` — `partial`
  - `withAvg()` — `partial`
  - `withExists()` — `partial`
  - `mergeConstraintsFrom()` — `partial`

### `Eloquent/Concerns/TransformsToResource.php` — `partial`
- **class `TransformsToResource`** — `partial`
  - `toResource()` — `partial`
  - `guessResourceName()` — `partial`
- **class `for`** — `partial`
- **class `for`** — `partial`
- **class `name`** — `partial`
- **class `from`** — `partial`
- **class `attribute`** — `partial`

### `Eloquent/Factories/Attributes/UseModel.php` — `partial`
- **class `UseModel`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Factories/BelongsToManyRelationship.php` — `partial`
- **class `BelongsToManyRelationship`** — `partial`
  - `__construct()` — `partial`
  - `createFor()` — `partial`
  - `recycle()` — `partial`

### `Eloquent/Factories/BelongsToRelationship.php` — `partial`
- **class `BelongsToRelationship`** — `partial`
  - `__construct()` — `partial`
  - `attributesFor()` — `partial`
  - `recycle()` — `partial`

### `Eloquent/Factories/CrossJoinSequence.php` — `partial`
- **class `CrossJoinSequence`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Factories/Factory.php` — `partial`
- **class `Factory`** — `partial`
  - `__construct()` — `partial`
  - `new()` — `partial`
  - `times()` — `partial`
  - `configure()` — `partial`
  - `raw()` — `partial`
  - `createOne()` — `partial`
  - `createOneQuietly()` — `partial`
  - `createMany()` — `partial`
  - `createManyQuietly()` — `partial`
  - `create()` — `partial`
  - `createQuietly()` — `partial`
  - `lazy()` — `partial`
  - `makeOne()` — `partial`
  - `make()` — `partial`
  - `makeMany()` — `partial`
  - `insert()` — `partial`
  - `state()` — `partial`
  - `prependState()` — `partial`
  - `set()` — `partial`
  - `sequence()` — `partial`
  - `forEachSequence()` — `partial`
  - `crossJoinSequence()` — `partial`
  - `has()` — `partial`
  - `hasAttached()` — `partial`
  - `for()` — `partial`
  - `recycle()` — `partial`
  - `getRandomRecycledModel()` — `partial`
  - `afterMaking()` — `partial`
  - `afterCreating()` — `partial`
  - `withoutAfterMaking()` — `partial`
  - `withoutAfterCreating()` — `partial`
  - `count()` — `partial`
  - `withoutParents()` — `partial`
  - `getConnectionName()` — `partial`
  - `connection()` — `partial`
  - `newModel()` — `partial`
  - `modelName()` — `partial`
  - `guessModelNamesUsing()` — `partial`
  - `useNamespace()` — `partial`
  - `factoryForModel()` — `partial`
  - `guessFactoryNamesUsing()` — `partial`
  - `expandRelationshipsByDefault()` — `partial`
  - `dontExpandRelationshipsByDefault()` — `partial`
  - `resolveFactoryName()` — `partial`
  - `flushState()` — `partial`
  - `__call()` — `partial`
- **class `names`** — `partial`

### `Eloquent/Factories/HasFactory.php` — `partial`
- **class `HasFactory`** — `partial`
  - `factory()` — `partial`
- **class `attribute`** — `partial`

### `Eloquent/Factories/Relationship.php` — `partial`
- **class `Relationship`** — `partial`
  - `__construct()` — `partial`
  - `createFor()` — `partial`
  - `recycle()` — `partial`

### `Eloquent/Factories/Sequence.php` — `partial`
- **class `Sequence`** — `partial`
  - `__construct()` — `partial`
  - `count()` — `partial`
  - `__invoke()` — `partial`

### `Eloquent/HasBuilder.php` — `partial`
- **class `HasBuilder`** — `partial`
  - `query()` — `partial`
  - `newEloquentBuilder()` — `partial`
  - `newQuery()` — `partial`
  - `newModelQuery()` — `partial`
  - `newQueryWithoutRelationships()` — `partial`
  - `newQueryWithoutScopes()` — `partial`
  - `newQueryWithoutScope()` — `partial`
  - `newQueryForRestoration()` — `partial`
  - `on()` — `partial`
  - `onWriteConnection()` — `partial`
  - `with()` — `partial`

### `Eloquent/HasCollection.php` — `partial`
- **class `HasCollection`** — `partial`
  - `newCollection()` — `partial`
  - `resolveCollectionFromAttribute()` — `partial`
- **class `names`** — `partial`
- **class `name`** — `partial`

### `Eloquent/HigherOrderBuilderProxy.php` — `partial`
- **class `HigherOrderBuilderProxy`** — `partial`
  - `__construct()` — `partial`
  - `__call()` — `partial`

### `Eloquent/InvalidCastException.php` — `partial`
- **class `InvalidCastException`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/JsonEncodingException.php` — `partial`
- **class `JsonEncodingException`** — `partial`
  - `forModel()` — `partial`
  - `forResource()` — `partial`
  - `forAttribute()` — `partial`

### `Eloquent/MassAssignmentException.php` — `partial`
- **class `MassAssignmentException`** — `partial`

### `Eloquent/MassPrunable.php` — `partial`
- **class `MassPrunable`** — `partial`
  - `pruneAll()` — `partial`
  - `prunable()` — `partial`

### `Eloquent/MissingAttributeException.php` — `partial`
- **class `MissingAttributeException`** — `partial`
  - `__construct()` — `partial`

### `Eloquent/Model.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Model.py`.
- **class `Model`** — `partial`
  - `__construct()` — `partial`
  - `initializeModelAttributes()` — `partial`
  - `clearBootedModels()` — `partial`
  - `withoutTouching()` — `partial`
  - `withoutTouchingOn()` — `partial`
  - `isIgnoringTouch()` — `partial`
  - `shouldBeStrict()` — `partial`
  - `preventLazyLoading()` — `partial`
  - `automaticallyEagerLoadRelationships()` — `partial`
  - `handleLazyLoadingViolationUsing()` — `partial`
  - `preventSilentlyDiscardingAttributes()` — `partial`
  - `handleDiscardedAttributeViolationUsing()` — `partial`
  - `preventAccessingMissingAttributes()` — `partial`
  - `handleMissingAttributeViolationUsing()` — `partial`
  - `withoutBroadcasting()` — `partial`
  - `fill()` — `partial`
  - `forceFill()` — `partial`
  - `qualifyColumn()` — `partial`
  - `qualifyColumns()` — `partial`
  - `newInstance()` — `partial`
  - `newFromBuilder()` — `partial`
  - `on()` — `partial`
  - `onWriteConnection()` — `partial`
  - `all()` — `partial`
  - `with()` — `partial`
  - `load()` — `partial`
  - `loadMorph()` — `partial`
  - `loadMissing()` — `partial`
  - `loadAggregate()` — `partial`
  - `loadCount()` — `partial`
  - `loadMax()` — `partial`
  - `loadMin()` — `partial`
  - `loadSum()` — `partial`
  - `loadAvg()` — `partial`
  - `loadExists()` — `partial`
  - `loadMorphAggregate()` — `partial`
  - `loadMorphCount()` — `partial`
  - `loadMorphMax()` — `partial`
  - `loadMorphMin()` — `partial`
  - `loadMorphSum()` — `partial`
  - `loadMorphAvg()` — `partial`
  - `update()` — `partial`
  - `updateOrFail()` — `partial`
  - `updateQuietly()` — `partial`
  - `push()` — `partial`
  - `pushQuietly()` — `partial`
  - `saveQuietly()` — `partial`
  - `save()` — `partial`
  - `saveOrIgnore()` — `partial`
  - `saveOrFail()` — `partial`
  - `destroy()` — `partial`
  - `delete()` — `partial`
  - `deleteQuietly()` — `partial`
  - `deleteOrFail()` — `partial`
  - `forceDelete()` — `partial`
  - `forceDestroy()` — `partial`
  - `query()` — `partial`
  - `newQuery()` — `partial`
  - `newModelQuery()` — `partial`
  - `newQueryWithoutRelationships()` — `partial`
  - `registerGlobalScopes()` — `partial`
  - `newQueryWithoutScopes()` — `partial`
  - `newQueryWithoutScope()` — `partial`
  - `newQueryForRestoration()` — `partial`
  - `newEloquentBuilder()` — `partial`
  - `newPivot()` — `partial`
  - `hasNamedScope()` — `partial`
  - `callNamedScope()` — `partial`
  - `toArray()` — `partial`
  - `toJson()` — `partial`
  - `toPrettyJson()` — `partial`
  - `jsonSerialize()` — `partial`
  - `fresh()` — `partial`
  - `refresh()` — `partial`
  - `refreshForUpdate()` — `partial`
  - `replicate()` — `partial`
  - `replicateQuietly()` — `partial`
  - `is()` — `partial`
  - `isNot()` — `partial`
  - `getConnection()` — `partial`
  - `getConnectionName()` — `partial`
  - `setConnection()` — `partial`
  - `resolveConnection()` — `partial`
  - `getConnectionResolver()` — `partial`
  - `setConnectionResolver()` — `partial`
  - `unsetConnectionResolver()` — `partial`
  - `getTable()` — `partial`
  - `setTable()` — `partial`
  - `getKeyName()` — `partial`
  - `setKeyName()` — `partial`
  - `getQualifiedKeyName()` — `partial`
  - `getKeyType()` — `partial`
  - `setKeyType()` — `partial`
  - `getIncrementing()` — `partial`
  - `setIncrementing()` — `partial`
  - `getKey()` — `partial`
  - `getQueueableId()` — `partial`
  - `getQueueableRelations()` — `partial`
  - `getQueueableConnection()` — `partial`
  - `getRouteKey()` — `partial`
  - `getRouteKeyName()` — `partial`
  - `resolveRouteBinding()` — `partial`
  - `resolveSoftDeletableRouteBinding()` — `partial`
  - `resolveChildRouteBinding()` — `partial`
  - `resolveSoftDeletableChildRouteBinding()` — `partial`
  - `resolveRouteBindingQuery()` — `partial`
  - `getForeignKey()` — `partial`
  - `getPerPage()` — `partial`
  - `setPerPage()` — `partial`
  - `isSoftDeletable()` — `partial`
  - `preventsLazyLoading()` — `partial`
  - `isAutomaticallyEagerLoadingRelationships()` — `partial`
  - `preventsSilentlyDiscardingAttributes()` — `partial`
  - `preventsAccessingMissingAttributes()` — `partial`
  - `broadcastChannelRoute()` — `partial`
  - `broadcastChannel()` — `partial`
  - `__get()` — `partial`
  - `__set()` — `partial`
  - `offsetExists()` — `partial`
  - `offsetGet()` — `partial`
  - `offsetSet()` — `partial`
  - `offsetUnset()` — `partial`
  - `__isset()` — `partial`
  - `__unset()` — `partial`
  - `__call()` — `partial`
  - `__callStatic()` — `partial`
  - `__toString()` — `partial`
  - `escapeWhenCastingToString()` — `partial`
  - `__sleep()` — `partial`
  - `__wakeup()` — `partial`
- **class `initializers`** — `partial`
- **class `to`** — `partial`
- **class `to`** — `partial`
- **class `attributes`** — `partial`
- **class `attributes`** — `partial`
- **class `during`** — `partial`
- **class `is`** — `partial`
- **class `is`** — `partial`
- **class `from`** — `partial`
- **class `attribute`** — `partial`

### `Eloquent/ModelInfo.php` — `partial`
- **class `ModelInfo`** — `partial`
  - `__construct()` — `partial`
  - `toArray()` — `partial`
  - `offsetExists()` — `partial`
  - `offsetGet()` — `partial`
  - `offsetSet()` — `partial`
  - `offsetUnset()` — `partial`
- **class `The`** — `partial`
- **class `that`** — `partial`
- **class `registered`** — `partial`

### `Eloquent/ModelInspector.php` — `partial`
- **class `ModelInspector`** — `partial`
  - `__construct()` — `partial`
  - `inspect()` — `partial`
- **class `being`** — `partial`
- **class `being`** — `partial`
- **class `used`** — `partial`
- **class `base`** — `partial`

### `Eloquent/ModelNotFoundException.php` — `partial`
- **class `ModelNotFoundException`** — `partial`
  - `setModel()` — `partial`
  - `getModel()` — `partial`
  - `getIds()` — `partial`

### `Eloquent/PendingHasThroughRelationship.php` — `partial`
- **class `PendingHasThroughRelationship`** — `partial`
  - `__construct()` — `partial`
  - `has()` — `partial`
  - `__call()` — `partial`

### `Eloquent/Prunable.php` — `partial`
- **class `Prunable`** — `partial`
  - `pruneAll()` — `partial`
  - `prunable()` — `partial`
  - `prune()` — `partial`

### `Eloquent/QueueEntityResolver.php` — `partial`
- **class `QueueEntityResolver`** — `partial`
  - `resolve()` — `partial`

### `Eloquent/RelationNotFoundException.php` — `partial`
- **class `RelationNotFoundException`** — `partial`
  - `make()` — `partial`

### `Eloquent/Relations/BelongsTo.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Relations/BelongsTo.py`.
- **class `BelongsTo`** — `partial`
  - `__construct()` — `partial`
  - `getResults()` — `partial`
  - `addConstraints()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `associate()` — `partial`
  - `dissociate()` — `partial`
  - `disassociate()` — `partial`
  - `touch()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `getRelationExistenceQueryForSelfRelation()` — `partial`
  - `getChild()` — `partial`
  - `getForeignKeyName()` — `partial`
  - `getQualifiedForeignKeyName()` — `partial`
  - `getParentKey()` — `partial`
  - `getOwnerKeyName()` — `partial`
  - `getQualifiedOwnerKeyName()` — `partial`
  - `getRelationName()` — `partial`

### `Eloquent/Relations/BelongsToMany.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Relations/BelongsToMany.py`.
- **class `BelongsToMany`** — `partial`
  - `__construct()` — `partial`
  - `addConstraints()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
- **class `name`** — `partial`
- **class `being`** — `partial`
  - `getPivotClass()` — `partial`
- **public method `using()`** — `partial`
- **public method `as()`** — `partial`
- **public method `wherePivot()`** — `partial`
- **public method `wherePivotBetween()`** — `partial`
- **public method `orWherePivotBetween()`** — `partial`
- **public method `wherePivotNotBetween()`** — `partial`
- **public method `orWherePivotNotBetween()`** — `partial`
- **public method `wherePivotIn()`** — `partial`
- **public method `orWherePivot()`** — `partial`
- **public method `withPivotValue()`** — `partial`
- **public method `orWherePivotIn()`** — `partial`
- **public method `wherePivotNotIn()`** — `partial`
- **public method `orWherePivotNotIn()`** — `partial`
- **public method `wherePivotNull()`** — `partial`
- **public method `wherePivotNotNull()`** — `partial`
- **public method `orWherePivotNull()`** — `partial`
- **public method `orWherePivotNotNull()`** — `partial`
- **public method `orderByPivot()`** — `partial`
- **public method `orderByPivotDesc()`** — `partial`
- **public method `findOrNew()`** — `partial`
- **public method `firstOrNew()`** — `partial`
- **public method `firstOrCreate()`** — `partial`
- **public method `createOrFirst()`** — `partial`
- **public method `updateOrCreate()`** — `partial`
- **public method `find()`** — `partial`
- **public method `findSole()`** — `partial`
- **public method `findMany()`** — `partial`
- **public method `findOrFail()`** — `partial`
- **public method `findOr()`** — `partial`
- **public method `firstWhere()`** — `partial`
- **public method `first()`** — `partial`
- **public method `firstOrFail()`** — `partial`
- **public method `firstOr()`** — `partial`
- **public method `getResults()`** — `partial`
- **public method `get()`** — `partial`
- **public method `paginate()`** — `partial`
- **public method `simplePaginate()`** — `partial`
- **public method `cursorPaginate()`** — `partial`
- **public method `chunk()`** — `partial`
- **public method `chunkById()`** — `partial`
- **public method `chunkByIdDesc()`** — `partial`
- **public method `eachById()`** — `partial`
- **public method `orderedChunkById()`** — `partial`
- **public method `each()`** — `partial`
- **public method `lazy()`** — `partial`
- **public method `lazyById()`** — `partial`
- **public method `lazyByIdDesc()`** — `partial`
- **public method `cursor()`** — `partial`
- **public method `touchIfTouching()`** — `partial`
- **public method `touch()`** — `partial`
- **public method `allRelatedIds()`** — `partial`
- **public method `save()`** — `partial`
- **public method `saveQuietly()`** — `partial`
- **public method `saveMany()`** — `partial`
- **public method `saveManyQuietly()`** — `partial`
- **public method `create()`** — `partial`
- **public method `createMany()`** — `partial`
- **public method `getRelationExistenceQuery()`** — `partial`
- **public method `getRelationExistenceQueryForSelfJoin()`** — `partial`
- **public method `take()`** — `partial`
- **public method `limit()`** — `partial`
- **public method `getExistenceCompareKey()`** — `partial`
- **public method `withTimestamps()`** — `partial`
- **public method `createdAt()`** — `partial`
- **public method `updatedAt()`** — `partial`
- **public method `getForeignPivotKeyName()`** — `partial`
- **public method `getQualifiedForeignPivotKeyName()`** — `partial`
- **public method `getRelatedPivotKeyName()`** — `partial`
- **public method `getQualifiedRelatedPivotKeyName()`** — `partial`
- **public method `getParentKeyName()`** — `partial`
- **public method `getQualifiedParentKeyName()`** — `partial`
- **public method `getRelatedKeyName()`** — `partial`
- **public method `getQualifiedRelatedKeyName()`** — `partial`
- **public method `getTable()`** — `partial`
- **public method `getRelationName()`** — `partial`
- **public method `getPivotAccessor()`** — `partial`
- **public method `getPivotColumns()`** — `partial`
- **public method `qualifyPivotColumn()`** — `partial`

### `Eloquent/Relations/Concerns/AsPivot.php` — `partial`
- **class `AsPivot`** — `partial`
  - `fromAttributes()` — `partial`
  - `fromRawAttributes()` — `partial`
  - `delete()` — `partial`
  - `getTable()` — `partial`
  - `getForeignKey()` — `partial`
  - `getRelatedKey()` — `partial`
  - `getOtherKey()` — `partial`
  - `setPivotKeys()` — `partial`
  - `setRelatedModel()` — `partial`
  - `hasTimestampAttributes()` — `partial`
  - `getCreatedAtColumn()` — `partial`
  - `getUpdatedAtColumn()` — `partial`
  - `getQueueableId()` — `partial`
  - `newQueryForRestoration()` — `partial`
  - `unsetRelations()` — `partial`

### `Eloquent/Relations/Concerns/CanBeOneOfMany.php` — `partial`
- **class `CanBeOneOfMany`** — `partial`
  - `ofMany()` — `partial`
  - `latestOfMany()` — `partial`
  - `oldestOfMany()` — `partial`
  - `getOneOfManySubQuery()` — `partial`
  - `qualifySubSelectColumn()` — `partial`
  - `isOneOfMany()` — `partial`
  - `getRelationName()` — `partial`

### `Eloquent/Relations/Concerns/ComparesRelatedModels.php` — `partial`
- **class `ComparesRelatedModels`** — `partial`
  - `is()` — `partial`
  - `isNot()` — `partial`

### `Eloquent/Relations/Concerns/InteractsWithDictionary.php` — `partial`
- **class `InteractsWithDictionary`** — `partial`

### `Eloquent/Relations/Concerns/InteractsWithPivotTable.php` — `partial`
- **class `InteractsWithPivotTable`** — `partial`
  - `toggle()` — `partial`
  - `toggleOrFail()` — `partial`
  - `syncWithoutDetaching()` — `partial`
  - `sync()` — `partial`
  - `syncOrFail()` — `partial`
  - `syncWithoutDetachingOrFail()` — `partial`
  - `syncWithPivotValues()` — `partial`
  - `syncWithPivotValuesOrFail()` — `partial`
- **public method `updateExistingPivot()`** — `partial`
- **public method `updateExistingPivotOrFail()`** — `partial`
- **public method `attach()`** — `partial`
- **public method `attachOrFail()`** — `partial`
- **public method `hasPivotColumn()`** — `partial`
- **public method `detach()`** — `partial`
- **public method `detachOrFail()`** — `partial`
- **public method `newPivot()`** — `partial`
- **public method `newExistingPivot()`** — `partial`
- **public method `newPivotStatement()`** — `partial`
- **public method `newPivotStatementForId()`** — `partial`
- **public method `newPivotQuery()`** — `partial`
- **public method `withPivot()`** — `partial`

### `Eloquent/Relations/Concerns/SupportsDefaultModels.php` — `partial`
- **class `SupportsDefaultModels`** — `partial`
  - `withDefault()` — `partial`

### `Eloquent/Relations/Concerns/SupportsInverseRelations.php` — `partial`
- **class `SupportsInverseRelations`** — `partial`
  - `inverse()` — `partial`
  - `chaperone()` — `partial`
  - `getInverseRelationship()` — `partial`
  - `withoutInverse()` — `partial`
  - `withoutChaperone()` — `partial`

### `Eloquent/Relations/HasMany.php` — `partial`
- **class `HasMany`** — `partial`
  - `one()` — `partial`
  - `getResults()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`

### `Eloquent/Relations/HasManyThrough.php` — `partial`
- **class `HasManyThrough`** — `partial`
  - `one()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `getResults()` — `partial`

### `Eloquent/Relations/HasOne.php` — `partial`
- **class `HasOne`** — `partial`
  - `getResults()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `addOneOfManySubQueryConstraints()` — `partial`
  - `getOneOfManySubQuerySelectColumns()` — `partial`
  - `addOneOfManyJoinSubQueryConstraints()` — `partial`
  - `newRelatedInstanceFor()` — `partial`

### `Eloquent/Relations/HasOneOrMany.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Relations/HasOneOrMany.py`.
- **class `HasOneOrMany`** — `partial`
  - `__construct()` — `partial`
  - `make()` — `partial`
  - `makeMany()` — `partial`
  - `addConstraints()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `matchOne()` — `partial`
  - `matchMany()` — `partial`
  - `findOrNew()` — `partial`
  - `firstOrNew()` — `partial`
  - `firstOrCreate()` — `partial`
  - `createOrFirst()` — `partial`
  - `updateOrCreate()` — `partial`
  - `upsert()` — `partial`
  - `save()` — `partial`
  - `saveQuietly()` — `partial`
  - `saveMany()` — `partial`
  - `saveManyQuietly()` — `partial`
  - `create()` — `partial`
  - `createQuietly()` — `partial`
  - `forceCreate()` — `partial`
  - `forceCreateQuietly()` — `partial`
  - `createMany()` — `partial`
  - `createManyQuietly()` — `partial`
  - `forceCreateMany()` — `partial`
  - `forceCreateManyQuietly()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `getRelationExistenceQueryForSelfRelation()` — `partial`
  - `take()` — `partial`
  - `limit()` — `partial`
  - `getExistenceCompareKey()` — `partial`
  - `getParentKey()` — `partial`
  - `getQualifiedParentKeyName()` — `partial`
  - `getForeignKeyName()` — `partial`
  - `getQualifiedForeignKeyName()` — `partial`
  - `getLocalKeyName()` — `partial`

### `Eloquent/Relations/HasOneOrManyThrough.php` — `partial`
- **class `HasOneOrManyThrough`** — `partial`
  - `__construct()` — `partial`
  - `addConstraints()` — `partial`
  - `getQualifiedParentKeyName()` — `partial`
  - `throughParentSoftDeletes()` — `partial`
  - `withTrashedParents()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `firstOrNew()` — `partial`
  - `firstOrCreate()` — `partial`
  - `createOrFirst()` — `partial`
  - `updateOrCreate()` — `partial`
  - `firstWhere()` — `partial`
  - `first()` — `partial`
  - `firstOrFail()` — `partial`
  - `firstOr()` — `partial`
  - `find()` — `partial`
  - `findSole()` — `partial`
  - `findMany()` — `partial`
  - `findOrFail()` — `partial`
  - `findOr()` — `partial`
  - `get()` — `partial`
  - `paginate()` — `partial`
  - `simplePaginate()` — `partial`
  - `cursorPaginate()` — `partial`
  - `chunk()` — `partial`
  - `chunkById()` — `partial`
  - `chunkByIdDesc()` — `partial`
  - `eachById()` — `partial`
  - `cursor()` — `partial`
  - `each()` — `partial`
  - `lazy()` — `partial`
  - `lazyById()` — `partial`
  - `lazyByIdDesc()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `getRelationExistenceQueryForSelfRelation()` — `partial`
  - `getRelationExistenceQueryForThroughSelfRelation()` — `partial`
  - `take()` — `partial`
  - `limit()` — `partial`
  - `getQualifiedFarKeyName()` — `partial`
  - `getFirstKeyName()` — `partial`
  - `getQualifiedFirstKeyName()` — `partial`
  - `getForeignKeyName()` — `partial`
  - `getQualifiedForeignKeyName()` — `partial`
  - `getLocalKeyName()` — `partial`
  - `getQualifiedLocalKeyName()` — `partial`
  - `getSecondLocalKeyName()` — `partial`

### `Eloquent/Relations/HasOneThrough.php` — `partial`
- **class `HasOneThrough`** — `partial`
  - `getResults()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `addOneOfManySubQueryConstraints()` — `partial`
  - `getOneOfManySubQuerySelectColumns()` — `partial`
  - `addOneOfManyJoinSubQueryConstraints()` — `partial`
  - `newRelatedInstanceFor()` — `partial`
  - `getParentKey()` — `partial`

### `Eloquent/Relations/MorphMany.php` — `partial`
- **class `MorphMany`** — `partial`
  - `one()` — `partial`
  - `getResults()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `forceCreate()` — `partial`

### `Eloquent/Relations/MorphOne.php` — `partial`
- **class `MorphOne`** — `partial`
  - `getResults()` — `partial`
  - `initRelation()` — `partial`
  - `match()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `addOneOfManySubQueryConstraints()` — `partial`
  - `getOneOfManySubQuerySelectColumns()` — `partial`
  - `addOneOfManyJoinSubQueryConstraints()` — `partial`
  - `newRelatedInstanceFor()` — `partial`

### `Eloquent/Relations/MorphOneOrMany.php` — `partial`
- **class `MorphOneOrMany`** — `partial`
  - `__construct()` — `partial`
  - `addConstraints()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `forceCreate()` — `partial`
  - `upsert()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `getQualifiedMorphType()` — `partial`
  - `getMorphType()` — `partial`
  - `getMorphClass()` — `partial`
- **class `of`** — `partial`
- **class `of`** — `partial`

### `Eloquent/Relations/MorphPivot.php` — `partial`
- **class `MorphPivot`** — `partial`
  - `delete()` — `partial`
  - `getMorphType()` — `partial`
  - `setMorphType()` — `partial`
  - `setMorphClass()` — `partial`
  - `getQueueableId()` — `partial`
  - `newQueryForRestoration()` — `partial`
- **class `for`** — `partial`

### `Eloquent/Relations/MorphTo.php` — `partial`
- **class `MorphTo`** — `partial`
  - `__construct()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `getEager()` — `partial`
  - `createModelByType()` — `partial`
  - `match()` — `partial`
  - `associate()` — `partial`
  - `dissociate()` — `partial`
  - `touch()` — `partial`
  - `getMorphType()` — `partial`
  - `getDictionary()` — `partial`
  - `morphWith()` — `partial`
  - `morphWithCount()` — `partial`
  - `constrain()` — `partial`
  - `withTrashed()` — `partial`
  - `withoutTrashed()` — `partial`
  - `onlyTrashed()` — `partial`
  - `getQualifiedOwnerKeyName()` — `partial`
  - `__call()` — `partial`

### `Eloquent/Relations/MorphToMany.php` — `partial`
- **class `MorphToMany`** — `partial`
  - `__construct()` — `partial`
  - `addEagerConstraints()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `newPivotQuery()` — `partial`
  - `newPivot()` — `partial`
  - `getMorphType()` — `partial`
  - `getQualifiedMorphTypeName()` — `partial`
  - `getMorphClass()` — `partial`
  - `getInverse()` — `partial`
- **class `of`** — `partial`
- **class `name`** — `partial`

### `Eloquent/Relations/Pivot.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Relations/Pivot.py`.
- **class `Pivot`** — `partial`

### `Eloquent/Relations/Relation.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/Relations/Relation.py`.
- **class `Relation`** — `partial`
  - `__construct()` — `partial`
  - `noConstraints()` — `partial`
  - `noConstraintsForRelation()` — `partial`
  - `withConstraints()` — `partial`
  - `withConstraintsForNestedRelation()` — `partial`
  - `getEager()` — `partial`
  - `sole()` — `partial`
  - `get()` — `partial`
  - `touch()` — `partial`
  - `rawUpdate()` — `partial`
  - `getRelationExistenceCountQuery()` — `partial`
  - `getRelationExistenceQuery()` — `partial`
  - `getRelationCountHash()` — `partial`
  - `getQuery()` — `partial`
  - `getBaseQuery()` — `partial`
  - `toBase()` — `partial`
  - `getParent()` — `partial`
  - `getQualifiedParentKeyName()` — `partial`
  - `getRelated()` — `partial`
  - `getRelatedClass()` — `partial`
  - `createdAt()` — `partial`
  - `updatedAt()` — `partial`
  - `relatedUpdatedAt()` — `partial`
  - `requireMorphMap()` — `partial`
  - `requiresMorphMap()` — `partial`
  - `enforceMorphMap()` — `partial`
  - `morphMap()` — `partial`
  - `getMorphedModel()` — `partial`
  - `getMorphAlias()` — `partial`
  - `__call()` — `partial`
  - `__clone()` — `partial`
- **class `names`** — `partial`
- **class `name`** — `partial`
- **class `names`** — `partial`

### `Eloquent/Scope.php` — `partial`
- **class `Scope`** — `partial`
  - `apply()` — `partial`

### `Eloquent/SoftDeletes.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Eloquent/SoftDeletes.py`.
- **class `SoftDeletes`** — `partial`
  - `bootSoftDeletes()` — `partial`
  - `initializeSoftDeletes()` — `partial`
  - `forceDelete()` — `partial`
  - `forceDeleteQuietly()` — `partial`
  - `forceDestroy()` — `partial`
  - `restore()` — `partial`
  - `restoreQuietly()` — `partial`
  - `trashed()` — `partial`
  - `softDeleted()` — `partial`
  - `restoring()` — `partial`
  - `restored()` — `partial`
  - `forceDeleting()` — `partial`
  - `forceDeleted()` — `partial`
  - `isForceDeleting()` — `partial`
  - `getDeletedAtColumn()` — `partial`
  - `getQualifiedDeletedAtColumn()` — `partial`
- **class `for`** — `partial`
- **class `for`** — `partial`

### `Eloquent/SoftDeletingScope.php` — `partial`
- **class `SoftDeletingScope`** — `partial`
  - `apply()` — `partial`
  - `extend()` — `partial`

### `Events/ConnectionEstablished.php` — `partial`
- **class `ConnectionEstablished`** — `partial`

### `Events/ConnectionEvent.php` — `partial`
- **class `ConnectionEvent`** — `partial`
  - `__construct()` — `partial`

### `Events/DatabaseBusy.php` — `partial`
- **class `DatabaseBusy`** — `partial`
  - `__construct()` — `partial`

### `Events/DatabaseRefreshed.php` — `partial`
- **class `DatabaseRefreshed`** — `partial`
  - `__construct()` — `partial`

### `Events/MigrationEnded.php` — `partial`
- **class `MigrationEnded`** — `partial`

### `Events/MigrationEvent.php` — `partial`
- **class `MigrationEvent`** — `partial`
  - `__construct()` — `partial`

### `Events/MigrationSkipped.php` — `partial`
- **class `MigrationSkipped`** — `partial`
  - `__construct()` — `partial`

### `Events/MigrationStarted.php` — `partial`
- **class `MigrationStarted`** — `partial`

### `Events/MigrationsEnded.php` — `partial`
- **class `MigrationsEnded`** — `partial`

### `Events/MigrationsEvent.php` — `partial`
- **class `MigrationsEvent`** — `partial`
  - `__construct()` — `partial`

### `Events/MigrationsPruned.php` — `partial`
- **class `MigrationsPruned`** — `partial`
  - `__construct()` — `partial`

### `Events/MigrationsStarted.php` — `partial`
- **class `MigrationsStarted`** — `partial`

### `Events/ModelPruningFinished.php` — `partial`
- **class `ModelPruningFinished`** — `partial`
  - `__construct()` — `partial`
- **class `names`** — `partial`

### `Events/ModelPruningStarting.php` — `partial`
- **class `ModelPruningStarting`** — `partial`
  - `__construct()` — `partial`
- **class `names`** — `partial`

### `Events/ModelsPruned.php` — `partial`
- **class `ModelsPruned`** — `partial`
  - `__construct()` — `partial`
- **class `name`** — `partial`

### `Events/NoPendingMigrations.php` — `partial`
- **class `NoPendingMigrations`** — `partial`
  - `__construct()` — `partial`

### `Events/QueryExecuted.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Events/QueryExecuted.py`.
- **class `QueryExecuted`** — `partial`
  - `__construct()` — `partial`
  - `toRawSql()` — `partial`

### `Events/SchemaDumped.php` — `partial`
- **class `SchemaDumped`** — `partial`
  - `__construct()` — `partial`

### `Events/SchemaLoaded.php` — `partial`
- **class `SchemaLoaded`** — `partial`
  - `__construct()` — `partial`

### `Events/StatementPrepared.php` — `partial`
- **class `StatementPrepared`** — `partial`
  - `__construct()` — `partial`

### `Events/TransactionBeginning.php` — `partial`
- **class `TransactionBeginning`** — `partial`

### `Events/TransactionCommitted.php` — `partial`
- **class `TransactionCommitted`** — `partial`

### `Events/TransactionCommitting.php` — `partial`
- **class `TransactionCommitting`** — `partial`

### `Events/TransactionRolledBack.php` — `partial`
- **class `TransactionRolledBack`** — `partial`

### `Grammar.php` — `partial`
- **class `Grammar`** — `partial`
  - `__construct()` — `partial`
  - `wrapArray()` — `partial`
  - `wrapTable()` — `partial`
  - `wrap()` — `partial`
  - `columnize()` — `partial`
  - `parameterize()` — `partial`
  - `parameter()` — `partial`
  - `quoteString()` — `partial`
  - `escape()` — `partial`
  - `isExpression()` — `partial`
  - `getValue()` — `partial`
  - `getDateFormat()` — `partial`
  - `getTablePrefix()` — `partial`
  - `setTablePrefix()` — `partial`

### `LazyLoadingViolationException.php` — `partial`
- **class `LazyLoadingViolationException`** — `partial`
  - `__construct()` — `partial`

### `LostConnectionDetector.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/LostConnectionDetector.py`.
- **class `LostConnectionDetector`** — `partial`
  - `causedByLostConnection()` — `partial`

### `LostConnectionException.php` — `partial`
- **class `LostConnectionException`** — `partial`

### `MariaDbConnection.php` — `partial`
- **class `MariaDbConnection`** — `partial`
  - `getDriverTitle()` — `partial`
  - `isMaria()` — `partial`
  - `getServerVersion()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `getSchemaState()` — `partial`

### `MigrationServiceProvider.php` — `partial`
- **class `MigrationServiceProvider`** — `partial`
  - `register()` — `partial`
  - `provides()` — `partial`

### `Migrations/DatabaseMigrationRepository.php` — `partial`
- **class `DatabaseMigrationRepository`** — `partial`
  - `__construct()` — `partial`
  - `getRan()` — `partial`
  - `getMigrations()` — `partial`
  - `getMigrationsByBatch()` — `partial`
  - `getLast()` — `partial`
  - `getMigrationBatches()` — `partial`
  - `log()` — `partial`
  - `delete()` — `partial`
  - `getNextBatchNumber()` — `partial`
  - `getLastBatchNumber()` — `partial`
  - `createRepository()` — `partial`
  - `repositoryExists()` — `partial`
  - `deleteRepository()` — `partial`
  - `getConnectionResolver()` — `partial`
  - `getConnection()` — `partial`
  - `setSource()` — `partial`

### `Migrations/Migration.php` — `partial`
- **class `Migration`** — `partial`
  - `getConnection()` — `partial`
  - `shouldRun()` — `partial`

### `Migrations/MigrationCreator.php` — `partial`
- **class `MigrationCreator`** — `partial`
  - `__construct()` — `partial`
  - `create()` — `partial`
  - `afterCreate()` — `partial`
  - `stubPath()` — `partial`
  - `getFilesystem()` — `partial`
- **class `already`** — `partial`
- **class `name`** — `partial`

### `Migrations/MigrationRepositoryInterface.php` — `partial`
- **class `MigrationRepositoryInterface`** — `partial`
  - `getRan()` — `partial`
  - `getMigrations()` — `partial`
  - `getMigrationsByBatch()` — `partial`
  - `getLast()` — `partial`
  - `getMigrationBatches()` — `partial`
  - `log()` — `partial`
  - `delete()` — `partial`
  - `getNextBatchNumber()` — `partial`
  - `createRepository()` — `partial`
  - `repositoryExists()` — `partial`
  - `deleteRepository()` — `partial`
  - `setSource()` — `partial`

### `Migrations/MigrationResult.php` — `partial`

### `Migrations/Migrator.php` — `partial`
- **class `Migrator`** — `partial`
  - `__construct()` — `partial`
  - `run()` — `partial`
  - `runPending()` — `partial`
  - `rollback()` — `partial`
  - `reset()` — `partial`
  - `resolve()` — `partial`
  - `getMigrationFiles()` — `partial`
  - `requireFiles()` — `partial`
  - `getMigrationName()` — `partial`
  - `path()` — `partial`
  - `paths()` — `partial`
  - `withoutMigrations()` — `partial`
  - `getConnection()` — `partial`
  - `usingConnection()` — `partial`
  - `setConnection()` — `partial`
  - `resolveConnection()` — `partial`
  - `resolveConnectionsUsing()` — `partial`
  - `getRepository()` — `partial`
  - `repositoryExists()` — `partial`
  - `hasRunAnyMigrations()` — `partial`
  - `deleteRepository()` — `partial`
  - `getFilesystem()` — `partial`
  - `setOutput()` — `partial`
  - `fireMigrationEvent()` — `partial`
- **class `implementation`** — `partial`
- **class `from`** — `partial`
- **class `name`** — `partial`

### `MultipleColumnsSelectedException.php` — `partial`
- **class `MultipleColumnsSelectedException`** — `partial`

### `MultipleRecordsFoundException.php` — `partial`
- **class `MultipleRecordsFoundException`** — `partial`
  - `__construct()` — `partial`
  - `getCount()` — `partial`

### `MySqlConnection.php` — `partial`
- **class `MySqlConnection`** — `partial`
  - `getDriverTitle()` — `partial`
  - `insert()` — `partial`
  - `getLastInsertId()` — `partial`
  - `isMaria()` — `partial`
  - `getServerVersion()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `getSchemaState()` — `partial`

### `PostgresConnection.php` — `partial`
- **class `PostgresConnection`** — `partial`
  - `getDriverTitle()` — `partial`
  - `prepareBindings()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `getSchemaState()` — `partial`

### `Query/Builder.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/QueryBuilder.py`.
- **class `Builder`** — `partial`
  - `__construct()` — `partial`
  - `select()` — `partial`
  - `selectSub()` — `partial`
  - `selectExpression()` — `partial`
  - `selectRaw()` — `partial`
  - `fromSub()` — `partial`
  - `fromRaw()` — `partial`
  - `addSelect()` — `partial`
  - `selectVectorDistance()` — `partial`
  - `distinct()` — `partial`
  - `from()` — `partial`
  - `useIndex()` — `partial`
  - `forceIndex()` — `partial`
  - `ignoreIndex()` — `partial`
  - `join()` — `partial`
  - `joinWhere()` — `partial`
  - `joinSub()` — `partial`
  - `joinLateral()` — `partial`
  - `leftJoinLateral()` — `partial`
  - `leftJoin()` — `partial`
  - `leftJoinWhere()` — `partial`
  - `leftJoinSub()` — `partial`
  - `rightJoin()` — `partial`
  - `rightJoinWhere()` — `partial`
  - `rightJoinSub()` — `partial`
  - `crossJoin()` — `partial`
  - `crossJoinSub()` — `partial`
  - `straightJoin()` — `partial`
  - `straightJoinWhere()` — `partial`
  - `straightJoinSub()` — `partial`
  - `mergeWheres()` — `partial`
  - `where()` — `partial`
  - `prepareValueAndOperator()` — `partial`
  - `orWhere()` — `partial`
  - `whereNot()` — `partial`
  - `orWhereNot()` — `partial`
  - `whereColumn()` — `partial`
  - `orWhereColumn()` — `partial`
  - `whereVectorSimilarTo()` — `partial`
  - `whereVectorDistanceLessThan()` — `partial`
  - `orWhereVectorDistanceLessThan()` — `partial`
  - `whereRaw()` — `partial`
  - `orWhereRaw()` — `partial`
  - `whereLike()` — `partial`
  - `orWhereLike()` — `partial`
  - `whereNotLike()` — `partial`
  - `orWhereNotLike()` — `partial`
  - `whereNullSafeEquals()` — `partial`
  - `orWhereNullSafeEquals()` — `partial`
  - `whereIn()` — `partial`
  - `orWhereIn()` — `partial`
  - `whereNotIn()` — `partial`
  - `orWhereNotIn()` — `partial`
  - `whereIntegerInRaw()` — `partial`
  - `orWhereIntegerInRaw()` — `partial`
  - `whereIntegerNotInRaw()` — `partial`
  - `orWhereIntegerNotInRaw()` — `partial`
  - `whereNull()` — `partial`
  - `orWhereNull()` — `partial`
  - `whereNotNull()` — `partial`
  - `whereBetween()` — `partial`
  - `whereBetweenColumns()` — `partial`
  - `orWhereBetween()` — `partial`
  - `orWhereBetweenColumns()` — `partial`
  - `whereNotBetween()` — `partial`
  - `whereNotBetweenColumns()` — `partial`
  - `orWhereNotBetween()` — `partial`
  - `orWhereNotBetweenColumns()` — `partial`
  - `whereValueBetween()` — `partial`
  - `orWhereValueBetween()` — `partial`
  - `whereValueNotBetween()` — `partial`
  - `orWhereValueNotBetween()` — `partial`
  - `orWhereNotNull()` — `partial`
  - `whereDate()` — `partial`
  - `orWhereDate()` — `partial`
  - `whereTime()` — `partial`
  - `orWhereTime()` — `partial`
  - `whereDay()` — `partial`
  - `orWhereDay()` — `partial`
  - `whereMonth()` — `partial`
  - `orWhereMonth()` — `partial`
  - `whereYear()` — `partial`
  - `orWhereYear()` — `partial`
  - `whereNested()` — `partial`
  - `forNestedWhere()` — `partial`
  - `addNestedWhereQuery()` — `partial`
  - `whereExists()` — `partial`
  - `orWhereExists()` — `partial`
  - `whereNotExists()` — `partial`
  - `orWhereNotExists()` — `partial`
  - `addWhereExistsQuery()` — `partial`
  - `whereRowValues()` — `partial`
  - `orWhereRowValues()` — `partial`
  - `whereJsonContains()` — `partial`
  - `orWhereJsonContains()` — `partial`
  - `whereJsonDoesntContain()` — `partial`
  - `orWhereJsonDoesntContain()` — `partial`
  - `whereJsonOverlaps()` — `blocked`
  - `orWhereJsonOverlaps()` — `blocked`
  - `whereJsonDoesntOverlap()` — `blocked`
  - `orWhereJsonDoesntOverlap()` — `blocked`
  - `whereJsonContainsKey()` — `partial`
  - `orWhereJsonContainsKey()` — `partial`
  - `whereJsonDoesntContainKey()` — `partial`
  - `orWhereJsonDoesntContainKey()` — `partial`
  - `whereJsonLength()` — `partial`
  - `orWhereJsonLength()` — `partial`
  - `dynamicWhere()` — `partial`
  - `whereFullText()` — `partial`
  - `orWhereFullText()` — `partial`
  - `whereAll()` — `partial`
  - `orWhereAll()` — `partial`
  - `whereAny()` — `partial`
  - `orWhereAny()` — `partial`
  - `whereNone()` — `partial`
  - `orWhereNone()` — `partial`
  - `groupBy()` — `partial`
  - `groupByRaw()` — `partial`
  - `having()` — `partial`
  - `orHaving()` — `partial`
  - `havingNested()` — `partial`
  - `addNestedHavingQuery()` — `partial`
  - `havingNull()` — `partial`
  - `orHavingNull()` — `partial`
  - `havingNotNull()` — `partial`
  - `orHavingNotNull()` — `partial`
  - `havingBetween()` — `partial`
  - `havingNotBetween()` — `partial`
  - `orHavingBetween()` — `partial`
  - `orHavingNotBetween()` — `partial`
  - `havingRaw()` — `partial`
  - `orHavingRaw()` — `partial`
  - `orderBy()` — `partial`
  - `orderByDesc()` — `partial`
  - `latest()` — `partial`
  - `oldest()` — `partial`
  - `orderByVectorDistance()` — `partial`
  - `inRandomOrder()` — `partial`
  - `inOrderOf()` — `partial`
  - `orderByRaw()` — `partial`
  - `skip()` — `partial`
  - `offset()` — `partial`
  - `take()` — `partial`
  - `limit()` — `partial`
  - `groupLimit()` — `partial`
  - `forPage()` — `partial`
  - `forPageBeforeId()` — `partial`
  - `forPageAfterId()` — `partial`
  - `reorder()` — `partial`
  - `reorderDesc()` — `partial`
  - `union()` — `partial`
  - `unionAll()` — `partial`
  - `lock()` — `partial`
  - `lockForUpdate()` — `partial`
  - `sharedLock()` — `partial`
  - `timeout()` — `partial`
  - `beforeQuery()` — `partial`
  - `applyBeforeQueryCallbacks()` — `partial`
  - `afterQuery()` — `partial`
  - `applyAfterQueryCallbacks()` — `partial`
  - `toSql()` — `partial`
  - `toRawSql()` — `partial`
  - `find()` — `partial`
  - `findOr()` — `partial`
  - `value()` — `partial`
  - `rawValue()` — `partial`
  - `soleValue()` — `partial`
  - `get()` — `partial`
  - `paginate()` — `partial`
  - `simplePaginate()` — `partial`
  - `cursorPaginate()` — `partial`
  - `getCountForPagination()` — `partial`
  - `cursor()` — `partial`
  - `pluck()` — `partial`
  - `implode()` — `partial`
  - `exists()` — `partial`
  - `doesntExist()` — `partial`
  - `existsOr()` — `partial`
  - `doesntExistOr()` — `partial`
  - `count()` — `partial`
  - `min()` — `partial`
  - `max()` — `partial`
  - `sum()` — `partial`
  - `avg()` — `partial`
  - `average()` — `partial`
  - `aggregate()` — `partial`
  - `numericAggregate()` — `partial`
  - `insert()` — `partial`
  - `insertOrIgnore()` — `partial`
  - `insertOrIgnoreReturning()` — `partial`
  - `insertGetId()` — `partial`
  - `insertUsing()` — `partial`
  - `insertOrIgnoreUsing()` — `partial`
  - `update()` — `partial`
  - `updateFrom()` — `partial`
  - `updateOrInsert()` — `partial`
  - `upsert()` — `partial`
  - `increment()` — `partial`
  - `incrementEach()` — `partial`
  - `decrement()` — `partial`
  - `decrementEach()` — `partial`
  - `delete()` — `partial`
  - `truncate()` — `partial`
  - `newQuery()` — `partial`
  - `getColumns()` — `partial`
  - `raw()` — `partial`
  - `getLimit()` — `partial`
  - `getOffset()` — `partial`
  - `getBindings()` — `partial`
  - `getRawBindings()` — `partial`
  - `setBindings()` — `partial`
  - `addBinding()` — `partial`
  - `castBinding()` — `partial`
  - `mergeBindings()` — `partial`
  - `cleanBindings()` — `partial`
  - `getConnection()` — `partial`
  - `getProcessor()` — `partial`
  - `getGrammar()` — `partial`
  - `useWritePdo()` — `partial`
  - `fetchUsing()` — `partial`
  - `clone()` — `partial`
  - `cloneWithout()` — `partial`
  - `cloneWithoutBindings()` — `partial`
  - `dump()` — `partial`
  - `dumpRawSql()` — `partial`
  - `dd()` — `partial`
  - `ddRawSql()` — `partial`
  - `__call()` — `partial`

### `Query/Expression.php` — `partial`
- **class `Expression`** — `partial`
  - `__construct()` — `partial`
  - `getValue()` — `partial`

### `Query/Grammars/Grammar.php` — `partial`
- **class `Grammar`** — `partial`
  - `compileSelect()` — `partial`
  - `compileJoinLateral()` — `partial`
  - `compileWheres()` — `partial`
  - `prepareBindingForJsonContains()` — `partial`
  - `compileJsonValueCast()` — `partial`
  - `whereFullText()` — `partial`
  - `whereExpression()` — `partial`
  - `compileRandom()` — `partial`
  - `compileExists()` — `partial`
  - `compileInsert()` — `partial`
  - `compileInsertOrIgnore()` — `partial`
  - `compileInsertOrIgnoreReturning()` — `partial`
  - `compileInsertGetId()` — `partial`
  - `compileInsertUsing()` — `partial`
  - `compileInsertOrIgnoreUsing()` — `partial`
  - `compileUpdate()` — `partial`
  - `compileUpsert()` — `partial`
  - `prepareBindingsForUpdate()` — `partial`
  - `compileDelete()` — `partial`
  - `prepareBindingsForDelete()` — `partial`
  - `compileTruncate()` — `partial`
  - `compileThreadCount()` — `partial`
  - `supportsSavepoints()` — `partial`
  - `compileSavepoint()` — `partial`
  - `compileSavepointRollBack()` — `partial`
  - `substituteBindingsIntoRawSql()` — `partial`
  - `getOperators()` — `partial`
  - `getBitwiseOperators()` — `partial`

### `Query/Grammars/MariaDbGrammar.php` — `partial`
- **class `MariaDbGrammar`** — `partial`
  - `compileJoinLateral()` — `partial`
  - `compileJsonValueCast()` — `partial`
  - `compileThreadCount()` — `partial`
  - `useLegacyGroupLimit()` — `partial`

### `Query/Grammars/MySqlGrammar.php` — `partial`
- **class `MySqlGrammar`** — `partial`
  - `compileSelect()` — `partial`
  - `whereFullText()` — `partial`
  - `useLegacyGroupLimit()` — `partial`
  - `compileInsertOrIgnore()` — `partial`
  - `compileInsertOrIgnoreUsing()` — `partial`
  - `compileJsonValueCast()` — `partial`
  - `compileRandom()` — `partial`
  - `compileInsert()` — `partial`
  - `compileUpsert()` — `partial`
  - `compileJoinLateral()` — `partial`
  - `prepareBindingsForUpdate()` — `partial`
  - `compileThreadCount()` — `partial`

### `Query/Grammars/PostgresGrammar.php` — `partial`
- **class `PostgresGrammar`** — `partial`
  - `whereFullText()` — `partial`
  - `compileInsertOrIgnore()` — `partial`
  - `compileInsertOrIgnoreReturning()` — `partial`
  - `compileInsertOrIgnoreUsing()` — `partial`
  - `compileInsertGetId()` — `partial`
  - `compileUpdate()` — `partial`
  - `compileUpsert()` — `partial`
  - `compileJoinLateral()` — `partial`
  - `compileUpdateFrom()` — `partial`
  - `prepareBindingsForUpdateFrom()` — `partial`
  - `prepareBindingsForUpdate()` — `partial`
  - `compileDelete()` — `partial`
  - `compileTruncate()` — `partial`
  - `compileThreadCount()` — `partial`
  - `substituteBindingsIntoRawSql()` — `partial`
  - `getOperators()` — `partial`
  - `customOperators()` — `partial`
  - `cascadeOnTruncate()` — `partial`
  - `cascadeOnTrucate()` — `partial`

### `Query/Grammars/SQLiteGrammar.php` — `partial`
- **class `SQLiteGrammar`** — `partial`
  - `prepareWhereLikeBinding()` — `partial`
  - `prepareBindingForJsonContains()` — `partial`
  - `compileUpdate()` — `partial`
  - `compileInsertOrIgnore()` — `partial`
  - `compileInsertOrIgnoreReturning()` — `partial`
  - `compileInsertOrIgnoreUsing()` — `partial`
  - `compileUpsert()` — `partial`
  - `prepareBindingsForUpdate()` — `partial`
  - `compileDelete()` — `partial`
  - `compileTruncate()` — `partial`

### `Query/Grammars/SqlServerGrammar.php` — `partial`
- **class `SqlServerGrammar`** — `partial`
  - `compileSelect()` — `partial`
  - `prepareBindingForJsonContains()` — `partial`
  - `compileJsonValueCast()` — `partial`
  - `compileRandom()` — `partial`
  - `compileExists()` — `partial`
  - `compileUpsert()` — `partial`
  - `prepareBindingsForUpdate()` — `partial`
  - `compileJoinLateral()` — `partial`
  - `compileSavepoint()` — `partial`
  - `compileSavepointRollBack()` — `partial`
  - `compileThreadCount()` — `partial`
  - `getDateFormat()` — `partial`
  - `wrapTable()` — `partial`

### `Query/IndexHint.php` — `partial`
- **class `IndexHint`** — `partial`
  - `__construct()` — `partial`

### `Query/JoinClause.php` — `partial`
- **class `JoinClause`** — `partial`
  - `__construct()` — `partial`
  - `on()` — `partial`
  - `orOn()` — `partial`
  - `newQuery()` — `partial`
- **class `name`** — `partial`

### `Query/JoinLateralClause.php` — `partial`
- **class `JoinLateralClause`** — `partial`

### `Query/Processors/MariaDbProcessor.php` — `partial`
- **class `MariaDbProcessor`** — `partial`

### `Query/Processors/MySqlProcessor.php` — `partial`
- **class `MySqlProcessor`** — `partial`
  - `processColumnListing()` — `partial`
  - `processInsertGetId()` — `partial`
  - `processColumns()` — `partial`
  - `processIndexes()` — `partial`
  - `processForeignKeys()` — `partial`

### `Query/Processors/PostgresProcessor.php` — `partial`
- **class `PostgresProcessor`** — `partial`
  - `processInsertGetId()` — `partial`
  - `processTypes()` — `partial`
  - `processColumns()` — `partial`
  - `processIndexes()` — `partial`
  - `processForeignKeys()` — `partial`

### `Query/Processors/Processor.php` — `partial`
- **class `Processor`** — `partial`
  - `processSelect()` — `partial`
  - `processInsertGetId()` — `partial`
  - `processSchemas()` — `partial`
  - `processTables()` — `partial`
  - `processViews()` — `partial`
  - `processTypes()` — `partial`
  - `processColumns()` — `partial`
  - `processIndexes()` — `partial`
  - `processForeignKeys()` — `partial`

### `Query/Processors/SQLiteProcessor.php` — `partial`
- **class `SQLiteProcessor`** — `partial`
  - `processColumns()` — `partial`
  - `processIndexes()` — `partial`
  - `processForeignKeys()` — `partial`

### `Query/Processors/SqlServerProcessor.php` — `partial`
- **class `SqlServerProcessor`** — `partial`
  - `processInsertGetId()` — `partial`
  - `processColumns()` — `partial`
  - `processIndexes()` — `partial`
  - `processForeignKeys()` — `partial`

### `QueryException.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/QueryException.py`.
- **class `QueryException`** — `partial`
  - `__construct()` — `partial`
  - `getConnectionName()` — `partial`
  - `getSql()` — `partial`
  - `getRawSql()` — `partial`
  - `getBindings()` — `partial`
  - `getConnectionDetails()` — `partial`

### `RecordNotFoundException.php` — `partial`
- **class `RecordNotFoundException`** — `partial`

### `RecordsNotFoundException.php` — `partial`
- **class `RecordsNotFoundException`** — `partial`

### `SQLiteConnection.php` — `partial`
- **class `SQLiteConnection`** — `partial`
  - `getDriverTitle()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `getSchemaState()` — `partial`

### `SQLiteDatabaseDoesNotExistException.php` — `partial`
- **class `SQLiteDatabaseDoesNotExistException`** — `partial`
  - `__construct()` — `partial`

### `Schema/Blueprint.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Schema/Blueprint.py`.
- **class `Blueprint`** — `partial`
  - `__construct()` — `partial`
  - `build()` — `partial`
  - `toSql()` — `partial`
  - `addFluentCommands()` — `partial`
  - `addAlterCommands()` — `partial`
  - `creating()` — `partial`
  - `create()` — `partial`
  - `engine()` — `partial`
  - `innoDb()` — `partial`
  - `charset()` — `partial`
  - `collation()` — `partial`
  - `temporary()` — `partial`
  - `drop()` — `partial`
  - `dropIfExists()` — `partial`
  - `dropColumn()` — `partial`
  - `renameColumn()` — `partial`
  - `dropPrimary()` — `partial`
  - `dropUnique()` — `partial`
  - `dropIndex()` — `partial`
  - `dropFullText()` — `partial`
  - `dropSpatialIndex()` — `partial`
  - `dropForeign()` — `partial`
  - `dropConstrainedForeignId()` — `partial`
  - `dropForeignIdFor()` — `partial`
  - `dropConstrainedForeignIdFor()` — `partial`
  - `renameIndex()` — `partial`
  - `dropTimestamps()` — `partial`
  - `dropTimestampsTz()` — `partial`
  - `dropSoftDeletes()` — `partial`
  - `dropSoftDeletesTz()` — `partial`
  - `dropRememberToken()` — `partial`
  - `dropMorphs()` — `partial`
  - `rename()` — `partial`
  - `primary()` — `partial`
  - `unique()` — `partial`
  - `index()` — `partial`
  - `fullText()` — `partial`
  - `spatialIndex()` — `partial`
  - `vectorIndex()` — `partial`
  - `rawIndex()` — `partial`
  - `foreign()` — `partial`
  - `id()` — `partial`
  - `increments()` — `partial`
  - `integerIncrements()` — `partial`
  - `tinyIncrements()` — `partial`
  - `smallIncrements()` — `partial`
  - `mediumIncrements()` — `partial`
  - `bigIncrements()` — `partial`
  - `char()` — `partial`
  - `string()` — `partial`
  - `tinyText()` — `partial`
  - `text()` — `partial`
  - `mediumText()` — `partial`
  - `longText()` — `partial`
  - `integer()` — `partial`
  - `tinyInteger()` — `partial`
  - `smallInteger()` — `partial`
  - `mediumInteger()` — `partial`
  - `bigInteger()` — `partial`
  - `unsignedInteger()` — `partial`
  - `unsignedTinyInteger()` — `partial`
  - `unsignedSmallInteger()` — `partial`
  - `unsignedMediumInteger()` — `partial`
  - `unsignedBigInteger()` — `partial`
  - `foreignId()` — `partial`
  - `foreignIdFor()` — `partial`
  - `foreignUuidFor()` — `partial`
  - `foreignUlidFor()` — `partial`
  - `float()` — `partial`
  - `double()` — `partial`
  - `decimal()` — `partial`
  - `boolean()` — `partial`
  - `enum()` — `partial`
  - `set()` — `partial`
  - `json()` — `partial`
  - `jsonb()` — `partial`
  - `date()` — `partial`
  - `dateTime()` — `partial`
  - `dateTimeTz()` — `partial`
  - `time()` — `partial`
  - `timeTz()` — `partial`
  - `timestamp()` — `partial`
  - `timestampTz()` — `partial`
  - `timestamps()` — `partial`
  - `nullableTimestamps()` — `partial`
  - `timestampsTz()` — `partial`
  - `nullableTimestampsTz()` — `partial`
  - `datetimes()` — `partial`
  - `softDeletes()` — `partial`
  - `softDeletesTz()` — `partial`
  - `softDeletesDatetime()` — `partial`
  - `year()` — `partial`
  - `binary()` — `partial`
  - `uuid()` — `partial`
  - `foreignUuid()` — `partial`
  - `ulid()` — `partial`
  - `foreignUlid()` — `partial`
  - `ipAddress()` — `partial`
  - `macAddress()` — `partial`
  - `geometry()` — `partial`
  - `geography()` — `partial`
  - `computed()` — `partial`
  - `vector()` — `partial`
  - `tsvector()` — `partial`
  - `morphs()` — `partial`
  - `nullableMorphs()` — `partial`
  - `numericMorphs()` — `partial`
  - `nullableNumericMorphs()` — `partial`
  - `uuidMorphs()` — `partial`
  - `nullableUuidMorphs()` — `partial`
  - `ulidMorphs()` — `partial`
  - `nullableUlidMorphs()` — `partial`
  - `rememberToken()` — `partial`
  - `rawColumn()` — `partial`
  - `comment()` — `partial`
  - `addColumn()` — `partial`
  - `after()` — `partial`
  - `removeColumn()` — `partial`
  - `getTable()` — `partial`
  - `getPrefix()` — `partial`
  - `getColumns()` — `partial`
  - `getCommands()` — `partial`
  - `getState()` — `partial`
  - `getAddedColumns()` — `partial`
  - `getChangedColumns()` — `partial`

### `Schema/BlueprintState.php` — `partial`
- **class `BlueprintState`** — `partial`
  - `__construct()` — `partial`
  - `getPrimaryKey()` — `partial`
  - `getColumns()` — `partial`
  - `getIndexes()` — `partial`
  - `getForeignKeys()` — `partial`
  - `update()` — `partial`

### `Schema/Builder.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/Schema/Builder.py`.
- **class `Builder`** — `partial`
  - `__construct()` — `partial`
  - `defaultStringLength()` — `partial`
  - `defaultTimePrecision()` — `partial`
  - `defaultMorphKeyType()` — `partial`
  - `morphUsingUuids()` — `partial`
  - `morphUsingUlids()` — `partial`
  - `createDatabase()` — `partial`
  - `dropDatabaseIfExists()` — `partial`
  - `getSchemas()` — `partial`
  - `hasTable()` — `partial`
  - `hasView()` — `partial`
  - `getTables()` — `partial`
  - `getTableListing()` — `partial`
  - `getViews()` — `partial`
  - `getTypes()` — `partial`
  - `hasColumn()` — `partial`
  - `hasColumns()` — `partial`
  - `whenTableHasColumn()` — `partial`
  - `whenTableDoesntHaveColumn()` — `partial`
  - `whenTableHasIndex()` — `partial`
  - `whenTableDoesntHaveIndex()` — `partial`
  - `getColumnType()` — `partial`
  - `getColumnListing()` — `partial`
  - `getColumns()` — `partial`
  - `getIndexes()` — `partial`
  - `getIndexListing()` — `partial`
  - `hasIndex()` — `partial`
  - `hasForeignKey()` — `partial`
  - `getForeignKeys()` — `partial`
  - `table()` — `partial`
  - `create()` — `partial`
  - `drop()` — `partial`
  - `dropIfExists()` — `partial`
  - `dropColumns()` — `partial`
  - `dropAllTables()` — `partial`
  - `dropAllViews()` — `partial`
  - `dropAllTypes()` — `partial`
  - `rename()` — `partial`
  - `enableForeignKeyConstraints()` — `partial`
  - `disableForeignKeyConstraints()` — `partial`
  - `withoutForeignKeyConstraints()` — `partial`
  - `ensureVectorExtensionExists()` — `partial`
  - `ensureExtensionExists()` — `partial`
  - `getCurrentSchemaListing()` — `partial`
  - `getCurrentSchemaName()` — `partial`
  - `parseSchemaAndTable()` — `partial`
  - `getConnection()` — `partial`
  - `blueprintResolver()` — `partial`

### `Schema/ColumnDefinition.php` — `partial`
- **class `ColumnDefinition`** — `partial`

### `Schema/ForeignIdColumnDefinition.php` — `partial`
- **class `ForeignIdColumnDefinition`** — `partial`
  - `__construct()` — `partial`
  - `constrained()` — `partial`
  - `references()` — `partial`

### `Schema/ForeignKeyDefinition.php` — `partial`
- **class `ForeignKeyDefinition`** — `partial`
  - `cascadeOnUpdate()` — `partial`
  - `restrictOnUpdate()` — `partial`
  - `nullOnUpdate()` — `partial`
  - `noActionOnUpdate()` — `partial`
  - `cascadeOnDelete()` — `partial`
  - `restrictOnDelete()` — `partial`
  - `nullOnDelete()` — `partial`
  - `noActionOnDelete()` — `partial`

### `Schema/Grammars/Grammar.php` — `partial`
- **class `Grammar`** — `partial`
  - `compileCreateDatabase()` — `partial`
  - `compileDropDatabaseIfExists()` — `partial`
  - `compileSchemas()` — `partial`
  - `compileTableExists()` — `partial`
  - `compileTables()` — `partial`
  - `compileViews()` — `partial`
  - `compileTypes()` — `partial`
  - `compileColumns()` — `partial`
  - `compileIndexes()` — `partial`
  - `compileVectorIndex()` — `partial`
  - `compileForeignKeys()` — `partial`
  - `compileRenameColumn()` — `partial`
  - `compileChange()` — `partial`
  - `compileFulltext()` — `partial`
  - `compileDropFullText()` — `partial`
  - `compileForeign()` — `partial`
  - `compileDropForeign()` — `partial`
- **public method `prefixArray()`** — `partial`
- **public method `wrapTable()`** — `partial`
- **public method `wrap()`** — `partial`
- **public method `getFluentCommands()`** — `partial`
- **public method `supportsSchemaTransactions()`** — `partial`

### `Schema/Grammars/MariaDbGrammar.php` — `partial`
- **class `MariaDbGrammar`** — `partial`
  - `compileRenameColumn()` — `partial`
  - `compileVectorIndex()` — `partial`

### `Schema/Grammars/MySqlGrammar.php` — `partial`
- **class `MySqlGrammar`** — `partial`
  - `compileCreateDatabase()` — `partial`
  - `compileSchemas()` — `partial`
  - `compileTableExists()` — `partial`
  - `compileTables()` — `partial`
  - `compileViews()` — `partial`
  - `compileColumns()` — `partial`
  - `compileIndexes()` — `partial`
  - `compileForeignKeys()` — `partial`
  - `compileCreate()` — `partial`
  - `compileAdd()` — `partial`
  - `compileAutoIncrementStartingValues()` — `partial`
  - `compileRenameColumn()` — `partial`
  - `compileChange()` — `partial`
  - `compilePrimary()` — `partial`
  - `compileUnique()` — `partial`
  - `compileIndex()` — `partial`
  - `compileFullText()` — `partial`
  - `compileSpatialIndex()` — `partial`
  - `compileDrop()` — `partial`
  - `compileDropIfExists()` — `partial`
  - `compileDropColumn()` — `partial`
  - `compileDropPrimary()` — `partial`
  - `compileDropUnique()` — `partial`
  - `compileDropIndex()` — `partial`
  - `compileDropFullText()` — `partial`
  - `compileDropSpatialIndex()` — `partial`
  - `compileForeign()` — `partial`
  - `compileDropForeign()` — `partial`
  - `compileRename()` — `partial`
  - `compileRenameIndex()` — `partial`
  - `compileDropAllTables()` — `partial`
  - `compileDropAllViews()` — `partial`
  - `compileEnableForeignKeyConstraints()` — `partial`
  - `compileDisableForeignKeyConstraints()` — `partial`
  - `compileTableComment()` — `partial`
  - `escapeNames()` — `partial`

### `Schema/Grammars/PostgresGrammar.php` — `partial`
- **class `PostgresGrammar`** — `partial`
  - `compileCreateDatabase()` — `partial`
  - `compileSchemas()` — `partial`
  - `compileTableExists()` — `partial`
  - `compileTables()` — `partial`
  - `compileViews()` — `partial`
  - `compileTypes()` — `partial`
  - `compileColumns()` — `partial`
  - `compileIndexes()` — `partial`
  - `compileForeignKeys()` — `partial`
  - `compileCreate()` — `partial`
  - `compileAdd()` — `partial`
  - `compileAutoIncrementStartingValues()` — `partial`
  - `compileChange()` — `partial`
  - `compilePrimary()` — `partial`
  - `compileUnique()` — `partial`
  - `compileIndex()` — `partial`
  - `compileFulltext()` — `partial`
  - `compileSpatialIndex()` — `partial`
  - `compileVectorIndex()` — `partial`
  - `compileForeign()` — `partial`
  - `compileDrop()` — `partial`
  - `compileDropIfExists()` — `partial`
  - `compileDropAllTables()` — `partial`
  - `compileDropAllViews()` — `partial`
  - `compileDropAllTypes()` — `partial`
  - `compileDropAllDomains()` — `partial`
  - `compileDropColumn()` — `partial`
  - `compileDropPrimary()` — `partial`
  - `compileDropUnique()` — `partial`
  - `compileDropIndex()` — `partial`
  - `compileDropFullText()` — `partial`
  - `compileDropSpatialIndex()` — `partial`
  - `compileDropForeign()` — `partial`
  - `compileRename()` — `partial`
  - `compileRenameIndex()` — `partial`
  - `compileEnableForeignKeyConstraints()` — `partial`
  - `compileDisableForeignKeyConstraints()` — `partial`
  - `compileComment()` — `partial`
  - `compileTableComment()` — `partial`
  - `escapeNames()` — `partial`
- **class `key`** — `partial`

### `Schema/Grammars/SQLiteGrammar.php` — `partial`
- **class `SQLiteGrammar`** — `partial`
  - `getAlterCommands()` — `partial`
  - `compileSqlCreateStatement()` — `partial`
  - `compileDbstatExists()` — `partial`
  - `compileSchemas()` — `partial`
  - `compileTableExists()` — `partial`
  - `compileTables()` — `partial`
  - `compileLegacyTables()` — `partial`
  - `compileViews()` — `partial`
  - `compileColumns()` — `partial`
  - `compileIndexes()` — `partial`
  - `compileForeignKeys()` — `partial`
  - `compileCreate()` — `partial`
  - `compileAdd()` — `partial`
  - `compileAlter()` — `partial`
  - `compileChange()` — `partial`
  - `compilePrimary()` — `partial`
  - `compileUnique()` — `partial`
  - `compileIndex()` — `partial`
  - `compileSpatialIndex()` — `partial`
  - `compileForeign()` — `partial`
  - `compileDrop()` — `partial`
  - `compileDropIfExists()` — `partial`
  - `compileDropAllTables()` — `partial`
  - `compileDropAllViews()` — `partial`
  - `compileRebuild()` — `partial`
  - `compileDropColumn()` — `partial`
  - `compileDropPrimary()` — `partial`
  - `compileDropUnique()` — `partial`
  - `compileDropIndex()` — `partial`
  - `compileDropSpatialIndex()` — `partial`
  - `compileDropForeign()` — `partial`
  - `compileRename()` — `partial`
  - `compileRenameIndex()` — `partial`
  - `compileEnableForeignKeyConstraints()` — `partial`
  - `compileDisableForeignKeyConstraints()` — `partial`
  - `pragma()` — `partial`
- **class `set`** — `partial`

### `Schema/Grammars/SqlServerGrammar.php` — `partial`
- **class `SqlServerGrammar`** — `partial`
  - `compileSchemas()` — `partial`
  - `compileTableExists()` — `partial`
  - `compileTables()` — `partial`
  - `compileViews()` — `partial`
  - `compileColumns()` — `partial`
  - `compileIndexes()` — `partial`
  - `compileForeignKeys()` — `partial`
  - `compileCreate()` — `partial`
  - `compileAdd()` — `partial`
  - `compileRenameColumn()` — `partial`
  - `compileChange()` — `partial`
  - `compilePrimary()` — `partial`
  - `compileUnique()` — `partial`
  - `compileIndex()` — `partial`
  - `compileSpatialIndex()` — `partial`
  - `compileDefault()` — `partial`
  - `compileDrop()` — `partial`
  - `compileDropIfExists()` — `partial`
  - `compileDropAllTables()` — `partial`
  - `compileDropColumn()` — `partial`
  - `compileDropDefaultConstraint()` — `partial`
  - `compileDropPrimary()` — `partial`
  - `compileDropUnique()` — `partial`
  - `compileDropIndex()` — `partial`
  - `compileDropSpatialIndex()` — `partial`
  - `compileDropForeign()` — `partial`
  - `compileRename()` — `partial`
  - `compileRenameIndex()` — `partial`
  - `compileEnableForeignKeyConstraints()` — `partial`
  - `compileDisableForeignKeyConstraints()` — `partial`
  - `compileDropAllForeignKeys()` — `partial`
  - `compileDropAllViews()` — `partial`
  - `quoteString()` — `partial`

### `Schema/IndexDefinition.php` — `partial`
- **class `IndexDefinition`** — `partial`

### `Schema/MariaDbBuilder.php` — `partial`
- **class `MariaDbBuilder`** — `partial`

### `Schema/MariaDbSchemaState.php` — `partial`
- **class `MariaDbSchemaState`** — `partial`
  - `load()` — `partial`

### `Schema/MySqlBuilder.php` — `partial`
- **class `MySqlBuilder`** — `partial`
  - `dropAllTables()` — `partial`
  - `dropAllViews()` — `partial`
  - `getCurrentSchemaListing()` — `partial`

### `Schema/MySqlSchemaState.php` — `partial`
- **class `MySqlSchemaState`** — `partial`
  - `dump()` — `partial`
  - `load()` — `partial`

### `Schema/PostgresBuilder.php` — `partial`
- **class `PostgresBuilder`** — `partial`
  - `dropAllTables()` — `partial`
  - `dropAllViews()` — `partial`
  - `dropAllTypes()` — `partial`
  - `getCurrentSchemaListing()` — `partial`

### `Schema/PostgresSchemaState.php` — `partial`
- **class `PostgresSchemaState`** — `partial`
  - `dump()` — `partial`
  - `load()` — `partial`

### `Schema/SQLiteBuilder.php` — `partial`
- **class `SQLiteBuilder`** — `partial`
  - `createDatabase()` — `partial`
  - `dropDatabaseIfExists()` — `partial`
  - `getTables()` — `partial`
  - `getViews()` — `partial`
  - `getColumns()` — `partial`
  - `dropAllTables()` — `partial`
  - `dropAllViews()` — `partial`
  - `pragma()` — `partial`
  - `refreshDatabaseFile()` — `partial`
  - `getCurrentSchemaListing()` — `partial`

### `Schema/SchemaState.php` — `partial`
- **class `SchemaState`** — `partial`
  - `__construct()` — `partial`
  - `makeProcess()` — `partial`
  - `hasMigrationTable()` — `partial`
  - `withMigrationTable()` — `partial`
  - `handleOutputUsing()` — `partial`

### `Schema/SqlServerBuilder.php` — `partial`
- **class `SqlServerBuilder`** — `partial`
  - `dropAllTables()` — `partial`
  - `dropAllViews()` — `partial`
  - `getCurrentSchemaName()` — `partial`

### `Schema/SqliteSchemaState.php` — `partial`
- **class `SqliteSchemaState`** — `partial`
  - `dump()` — `partial`
  - `load()` — `partial`

### `Seeder.php` — `partial`
- **class `Seeder`** — `partial`
  - `call()` — `partial`
  - `callWith()` — `partial`
  - `callSilent()` — `partial`
  - `callOnce()` — `partial`
  - `setContainer()` — `partial`
  - `setCommand()` — `partial`
  - `__invoke()` — `partial`
- **class `once`** — `partial`

### `SqlServerConnection.php` — `partial`
- **class `SqlServerConnection`** — `partial`
  - `getDriverTitle()` — `partial`
  - `transaction()` — `partial`
  - `getSchemaBuilder()` — `partial`
  - `getSchemaState()` — `partial`

### `UniqueConstraintViolationException.php` — `partial`
- Candidate PyJinx counterpart: `framework/Illuminate/Database/UniqueConstraintViolationException.py`.
- **class `UniqueConstraintViolationException`** — `partial`
  - `setIndex()` — `partial`
  - `setColumns()` — `partial`

## PyJinx implementation inventory

The following files are the current implementation surface to reconcile against the Laravel checklist.

### `framework/Illuminate/Database/DatabaseManager.py`
- class `_TransactionCallbacks`
  - `run_after_commit()`
  - `run_after_rollback()`
  - `parse_connection_name()`
  - `connection()`
  - `build()`
  - `calculate_dynamic_connection_name()`
  - `connect_using()`
  - `listen()`
  - `extend()`
  - `forget_extension()`
  - `get_pdo()`
  - `get_raw_pdo()`
  - `get_read_pdo()`
  - `get_name()`
  - `get_config()`
  - `get_driver_name()`
  - `get_database_name()`
  - `supported_drivers()`
  - `available_drivers()`
  - `get_name_with_read_write_type()`
  - `get_table_prefix()`
  - `prefixed_table_name()`
  - `disconnect()`
  - `purge()`
  - `reconnect()`
  - `using_connection()`
  - `get_default_connection()`
  - `set_default_connection()`
  - `get_connections()`
  - `set_application()`
  - `table()`
  - `session()`
  - `transaction()`
  - `begin_transaction()`
  - `commit()`
  - `roll_back()`
  - `transaction_level()`
  - `after_commit()`
  - `after_rollback()`
  - `dispose()`
- class `_TransactionCallbackFailure`
  - `run_after_commit()`
  - `run_after_rollback()`
  - `parse_connection_name()`
  - `connection()`
  - `build()`
  - `calculate_dynamic_connection_name()`
  - `connect_using()`
  - `listen()`
  - `extend()`
  - `forget_extension()`
  - `get_pdo()`
  - `get_raw_pdo()`
  - `get_read_pdo()`
  - `get_name()`
  - `get_config()`
  - `get_driver_name()`
  - `get_database_name()`
  - `supported_drivers()`
  - `available_drivers()`
  - `get_name_with_read_write_type()`
  - `get_table_prefix()`
  - `prefixed_table_name()`
  - `disconnect()`
  - `purge()`
  - `reconnect()`
  - `using_connection()`
  - `get_default_connection()`
  - `set_default_connection()`
  - `get_connections()`
  - `set_application()`
  - `table()`
  - `session()`
  - `transaction()`
  - `begin_transaction()`
  - `commit()`
  - `roll_back()`
  - `transaction_level()`
  - `after_commit()`
  - `after_rollback()`
  - `dispose()`
- class `_ManualRollback`
  - `run_after_commit()`
  - `run_after_rollback()`
  - `parse_connection_name()`
  - `connection()`
  - `build()`
  - `calculate_dynamic_connection_name()`
  - `connect_using()`
  - `listen()`
  - `extend()`
  - `forget_extension()`
  - `get_pdo()`
  - `get_raw_pdo()`
  - `get_read_pdo()`
  - `get_name()`
  - `get_config()`
  - `get_driver_name()`
  - `get_database_name()`
  - `supported_drivers()`
  - `available_drivers()`
  - `get_name_with_read_write_type()`
  - `get_table_prefix()`
  - `prefixed_table_name()`
  - `disconnect()`
  - `purge()`
  - `reconnect()`
  - `using_connection()`
  - `get_default_connection()`
  - `set_default_connection()`
  - `get_connections()`
  - `set_application()`
  - `table()`
  - `session()`
  - `transaction()`
  - `begin_transaction()`
  - `commit()`
  - `roll_back()`
  - `transaction_level()`
  - `after_commit()`
  - `after_rollback()`
  - `dispose()`
- class `DatabaseManager`
  - `run_after_commit()`
  - `run_after_rollback()`
  - `parse_connection_name()`
  - `connection()`
  - `build()`
  - `calculate_dynamic_connection_name()`
  - `connect_using()`
  - `listen()`
  - `extend()`
  - `forget_extension()`
  - `get_pdo()`
  - `get_raw_pdo()`
  - `get_read_pdo()`
  - `get_name()`
  - `get_config()`
  - `get_driver_name()`
  - `get_database_name()`
  - `supported_drivers()`
  - `available_drivers()`
  - `get_name_with_read_write_type()`
  - `get_table_prefix()`
  - `prefixed_table_name()`
  - `disconnect()`
  - `purge()`
  - `reconnect()`
  - `using_connection()`
  - `get_default_connection()`
  - `set_default_connection()`
  - `get_connections()`
  - `set_application()`
  - `table()`
  - `session()`
  - `transaction()`
  - `begin_transaction()`
  - `commit()`
  - `roll_back()`
  - `transaction_level()`
  - `after_commit()`
  - `after_rollback()`
  - `dispose()`

### `framework/Illuminate/Database/DatabaseServiceProvider.py`
- class `DatabaseServiceProvider`
  - `register()`
  - `boot()`

### `framework/Illuminate/Database/DeadlockException.py`
- class `DeadlockException`

### `framework/Illuminate/Database/Eloquent/Builder.py`
- class `Builder`
  - `where()`
  - `or_where()`
  - `where_raw()`
  - `or_where_raw()`
  - `select_raw()`
  - `from_sub()`
  - `order_by_raw()`
  - `group_by_raw()`
  - `having_raw()`
  - `or_having_raw()`
  - `where_null_safe_equals()`
  - `or_where_null_safe_equals()`
  - `where_not()`
  - `or_where_not()`
  - `where_integer_in_raw()`
  - `or_where_integer_in_raw()`
  - `where_integer_not_in_raw()`
  - `or_where_integer_not_in_raw()`
  - `where_exists()`
  - `or_where_exists()`
  - `where_not_exists()`
  - `or_where_not_exists()`
  - `where_like()`
  - `or_where_like()`
  - `where_not_like()`
  - `or_where_not_like()`
  - `where_all()`
  - `or_where_all()`
  - `where_any()`
  - `or_where_any()`
  - `where_none()`
  - `or_where_none()`
  - `chunk()`
  - `each()`
  - `cursor()`
  - `with_()`
  - `where_has()`
  - `select()`
  - `add_select()`
  - `add_select_aliased()`
  - `join()`
  - `left_join()`
  - `where_in()`
  - `where_not_in()`
  - `where_null()`
  - `where_not_null()`
  - `where_between()`
  - `where_not_between()`
  - `order_by()`
  - `order_by_desc()`
  - `latest()`
  - `oldest()`
  - `limit()`
  - `offset()`
  - `skip()`
  - `take()`
  - `for_page()`
  - `get()`
  - `first()`
  - `first_or_new()`
  - `first_or_create()`
  - `create_or_first()`
  - `update_or_create()`
  - `increment_or_create()`
  - `first_or_fail()`
  - `value()`
  - `pluck()`
  - `exists()`
  - `doesnt_exist()`
  - `count()`
  - `sum()`
  - `avg()`
  - `min()`
  - `max()`
  - `create()`
  - `create_quietly()`
  - `force_create()`
  - `force_create_quietly()`
  - `increment()`
  - `decrement()`
  - `update()`
  - `with_trashed()`
  - `without_trashed()`
  - `only_trashed()`
  - `restore()`
  - `delete()`

### `framework/Illuminate/Database/Eloquent/Casts/Attribute.py`
- class `Attribute`
  - `make()`
  - `get()`
  - `set()`
  - `without_object_caching()`
  - `should_cache()`

### `framework/Illuminate/Database/Eloquent/Model.py`
- class `Model`
  - `on()`
  - `without_events()`
  - `saving()`
  - `saved()`
  - `creating()`
  - `created()`
  - `updating()`
  - `updated()`
  - `deleting()`
  - `deleted()`
  - `retrieved()`
  - `query()`
  - `find()`
  - `all()`
  - `where()`
  - `find_or_fail()`
  - `get_key_name()`
  - `set_key_name()`
  - `get_key_type()`
  - `set_key_type()`
  - `get_incrementing()`
  - `set_incrementing()`
  - `get_table()`
  - `set_table()`
  - `get_connection_name()`
  - `set_connection()`
  - `qualify_column()`
  - `get_qualified_key_name()`
  - `get_created_at_column()`
  - `get_updated_at_column()`
  - `set_created_at()`
  - `set_updated_at()`
  - `get_date_format()`
  - `set_date_format()`
  - `from_date_time()`
  - `get_key()`
  - `get_auth_identifier_name()`
  - `get_auth_identifier()`
  - `get_auth_password_name()`
  - `get_auth_password()`
  - `get_remember_token_name()`
  - `get_remember_token()`
  - `set_remember_token()`
  - `get_route_key()`
  - `get_route_key_name()`
  - `resolve_route_binding()`
  - `resolve_soft_deletable_route_binding()`
  - `has_many()`
  - `has_one()`
  - `belongs_to()`
  - `belongs_to_many()`
  - `create()`
  - `fill()`
  - `force_fill()`
  - `create_quietly()`
  - `force_create()`
  - `force_create_quietly()`
  - `save()`
  - `save_quietly()`
  - `update()`
  - `update_quietly()`
  - `delete()`
  - `delete_quietly()`
  - `increment()`
  - `decrement()`
  - `fresh()`
  - `refresh()`
  - `refresh_for_update()`
  - `replicate()`
  - `replicate_quietly()`
  - `is_()`
  - `is_not()`
  - `get_arrayable_items()`
  - `get_arrayable_attributes()`
  - `get_arrayable_appends()`
  - `get_arrayable_relations()`
  - `attributes_to_dict()`
  - `relations_to_dict()`
  - `to_dict()`
  - `json_serialize()`
  - `get_hidden()`
  - `set_hidden()`
  - `merge_hidden()`
  - `get_visible()`
  - `set_visible()`
  - `merge_visible()`
  - `make_visible()`
  - `make_visible_if()`
  - `make_hidden()`
  - `make_hidden_if()`
  - `append()`
  - `get_appends()`
  - `set_appends()`
  - `merge_appends()`
  - `has_appended()`
  - `without_appends()`
  - `load()`
  - `get_relation_value()`
  - `is_dirty()`
  - `get_dirty()`
  - `get_original()`
  - `get_raw_original()`
  - `sync_original()`
  - `sync_original_attribute()`
  - `sync_original_attributes()`
  - `sync_changes()`
  - `is_clean()`
  - `get_changes()`
  - `was_changed()`

### `framework/Illuminate/Database/Eloquent/ModelNotFoundException.py`
- class `ModelNotFoundException`

### `framework/Illuminate/Database/Eloquent/Relations/BelongsTo.py`
- class `BelongsTo`
  - `add_constraints()`
  - `get_results()`
  - `associate()`
  - `dissociate()`

### `framework/Illuminate/Database/Eloquent/Relations/BelongsToMany.py`
- class `BelongsToMany`
  - `add_constraints()`
  - `perform_join()`
  - `add_where_constraints()`
  - `get_results()`
  - `get()`
  - `first()`
  - `as_()`
  - `with_pivot()`
  - `with_timestamps()`
  - `where_pivot()`
  - `order_by_pivot()`
  - `all_related_ids()`
  - `attach()`
  - `detach()`
  - `sync()`
  - `sync_without_detaching()`
  - `toggle()`

### `framework/Illuminate/Database/Eloquent/Relations/HasOneOrMany.py`
- class `HasOneOrMany`
  - `add_constraints()`
  - `save()`
  - `create()`
  - `get_parent_key()`
  - `get_results()`
  - `get_results()`
- class `HasOne`
  - `add_constraints()`
  - `save()`
  - `create()`
  - `get_parent_key()`
  - `get_results()`
  - `get_results()`
- class `HasMany`
  - `add_constraints()`
  - `save()`
  - `create()`
  - `get_parent_key()`
  - `get_results()`
  - `get_results()`

### `framework/Illuminate/Database/Eloquent/Relations/Pivot.py`
- class `Pivot`

### `framework/Illuminate/Database/Eloquent/Relations/Relation.py`
- class `Relation`
  - `add_constraints()`
  - `get_results()`
  - `get()`
  - `match()`

### `framework/Illuminate/Database/Eloquent/SoftDeletes.py`
- class `SoftDeletes`
  - `trashed()`
  - `restore()`
  - `force_delete()`
  - `restoring()`
  - `restored()`

### `framework/Illuminate/Database/Eloquent/__init__.py`

### `framework/Illuminate/Database/Events/QueryExecuted.py`
- class `QueryExecuted`

### `framework/Illuminate/Database/Events/__init__.py`

### `framework/Illuminate/Database/LostConnectionDetector.py`
- class `LostConnectionDetector`
  - `caused_by_lost_connection()`

### `framework/Illuminate/Database/QueryBuilder.py`
- class `QueryBuilder`
  - `select()`
  - `select_raw()`
  - `select_sub()`
  - `from_()`
  - `from_sub()`
  - `add_select()`
  - `add_select_aliased()`
  - `distinct()`
  - `join()`
  - `left_join()`
  - `where()`
  - `or_where()`
  - `where_raw()`
  - `or_where_raw()`
  - `where_null_safe_equals()`
  - `or_where_null_safe_equals()`
  - `where_not()`
  - `or_where_not()`
  - `where_like()`
  - `or_where_like()`
  - `where_not_like()`
  - `or_where_not_like()`
  - `where_exists()`
  - `or_where_exists()`
  - `where_not_exists()`
  - `or_where_not_exists()`
  - `where_all()`
  - `or_where_all()`
  - `where_any()`
  - `or_where_any()`
  - `where_none()`
  - `or_where_none()`
  - `where_column()`
  - `or_where_column()`
  - `where_between_columns()`
  - `or_where_between_columns()`
  - `where_not_between_columns()`
  - `or_where_not_between_columns()`
  - `where_date()`
  - `or_where_date()`
  - `where_time()`
  - `or_where_time()`
  - `where_day()`
  - `or_where_day()`
  - `where_month()`
  - `or_where_month()`
  - `where_year()`
  - `or_where_year()`
  - `where_json_contains()`
  - `or_where_json_contains()`
  - `where_json_doesnt_contain()`
  - `or_where_json_doesnt_contain()`
  - `where_json_contains_key()`
  - `or_where_json_contains_key()`
  - `where_json_doesnt_contain_key()`
  - `or_where_json_doesnt_contain_key()`
  - `where_json_length()`
  - `or_where_json_length()`
  - `where_row_values()`
  - `or_where_row_values()`
  - `where_in()`
  - `or_where_in()`
  - `where_not_in()`
  - `or_where_not_in()`
  - `where_integer_in_raw()`
  - `or_where_integer_in_raw()`
  - `where_integer_not_in_raw()`
  - `or_where_integer_not_in_raw()`
  - `where_null()`
  - `or_where_null()`
  - `where_not_null()`
  - `or_where_not_null()`
  - `where_between()`
  - `or_where_between()`
  - `where_not_between()`
  - `order_by()`
  - `order_by_raw()`
  - `order_by_desc()`
  - `latest()`
  - `oldest()`
  - `group_by()`
  - `group_by_raw()`
  - `having()`
  - `having_raw()`
  - `or_having_raw()`
  - `limit()`
  - `offset()`
  - `skip()`
  - `take()`
  - `for_page()`
  - `chunk()`
  - `each()`
  - `cursor()`
  - `insert()`
  - `insert_get_id()`
  - `upsert()`
  - `lock()`
  - `lock_for_update()`
  - `shared_lock()`
  - `update()`
  - `delete()`
  - `truncate()`
  - `increment()`
  - `decrement()`
  - `get()`
  - `first()`
  - `value()`
  - `pluck()`
  - `exists()`
  - `doesnt_exist()`
  - `count()`
  - `sum()`
  - `avg()`
  - `min()`
  - `max()`
  - `to_sql()`
  - `get_bindings()`

### `framework/Illuminate/Database/QueryException.py`
- class `QueryException`
  - `get_connection_name()`
  - `get_sql()`
  - `get_raw_sql()`
  - `get_bindings()`
  - `get_connection_details()`

### `framework/Illuminate/Database/Schema/Blueprint.py`
- class `ForeignKeyDefinition`
  - `references()`
  - `on()`
  - `register_referenced_table()`
  - `on_delete()`
  - `on_update()`
  - `cascade_on_delete()`
  - `restrict_on_delete()`
  - `null_on_delete()`
  - `no_action_on_delete()`
  - `cascade_on_update()`
  - `restrict_on_update()`
  - `null_on_update()`
  - `no_action_on_update()`
  - `as_constraint()`
  - `nullable()`
  - `default()`
  - `unique()`
  - `index()`
  - `primary()`
  - `nullable()`
  - `default()`
  - `constrained()`
  - `references()`
  - `constraints()`
  - `id()`
  - `string()`
  - `text()`
  - `integer()`
  - `big_integer()`
  - `boolean()`
  - `float()`
  - `timestamp()`
  - `foreign_id()`
  - `timestamps()`
  - `remember_token()`
  - `nullable()`
  - `default()`
  - `primary()`
  - `unique()`
  - `index()`
  - `drop_column()`
  - `rename_column()`
  - `foreign()`
- class `ColumnDefinition`
  - `references()`
  - `on()`
  - `register_referenced_table()`
  - `on_delete()`
  - `on_update()`
  - `cascade_on_delete()`
  - `restrict_on_delete()`
  - `null_on_delete()`
  - `no_action_on_delete()`
  - `cascade_on_update()`
  - `restrict_on_update()`
  - `null_on_update()`
  - `no_action_on_update()`
  - `as_constraint()`
  - `nullable()`
  - `default()`
  - `unique()`
  - `index()`
  - `primary()`
  - `nullable()`
  - `default()`
  - `constrained()`
  - `references()`
  - `constraints()`
  - `id()`
  - `string()`
  - `text()`
  - `integer()`
  - `big_integer()`
  - `boolean()`
  - `float()`
  - `timestamp()`
  - `foreign_id()`
  - `timestamps()`
  - `remember_token()`
  - `nullable()`
  - `default()`
  - `primary()`
  - `unique()`
  - `index()`
  - `drop_column()`
  - `rename_column()`
  - `foreign()`
- class `ForeignIdColumnDefinition`
  - `references()`
  - `on()`
  - `register_referenced_table()`
  - `on_delete()`
  - `on_update()`
  - `cascade_on_delete()`
  - `restrict_on_delete()`
  - `null_on_delete()`
  - `no_action_on_delete()`
  - `cascade_on_update()`
  - `restrict_on_update()`
  - `null_on_update()`
  - `no_action_on_update()`
  - `as_constraint()`
  - `nullable()`
  - `default()`
  - `unique()`
  - `index()`
  - `primary()`
  - `nullable()`
  - `default()`
  - `constrained()`
  - `references()`
  - `constraints()`
  - `id()`
  - `string()`
  - `text()`
  - `integer()`
  - `big_integer()`
  - `boolean()`
  - `float()`
  - `timestamp()`
  - `foreign_id()`
  - `timestamps()`
  - `remember_token()`
  - `nullable()`
  - `default()`
  - `primary()`
  - `unique()`
  - `index()`
  - `drop_column()`
  - `rename_column()`
  - `foreign()`
- class `Blueprint`
  - `references()`
  - `on()`
  - `register_referenced_table()`
  - `on_delete()`
  - `on_update()`
  - `cascade_on_delete()`
  - `restrict_on_delete()`
  - `null_on_delete()`
  - `no_action_on_delete()`
  - `cascade_on_update()`
  - `restrict_on_update()`
  - `null_on_update()`
  - `no_action_on_update()`
  - `as_constraint()`
  - `nullable()`
  - `default()`
  - `unique()`
  - `index()`
  - `primary()`
  - `nullable()`
  - `default()`
  - `constrained()`
  - `references()`
  - `constraints()`
  - `id()`
  - `string()`
  - `text()`
  - `integer()`
  - `big_integer()`
  - `boolean()`
  - `float()`
  - `timestamp()`
  - `foreign_id()`
  - `timestamps()`
  - `remember_token()`
  - `nullable()`
  - `default()`
  - `primary()`
  - `unique()`
  - `index()`
  - `drop_column()`
  - `rename_column()`
  - `foreign()`

### `framework/Illuminate/Database/Schema/Builder.py`
- class `SchemaBuilder`
  - `connection()`
  - `has_table()`
  - `has_column()`
  - `has_columns()`
  - `get_columns()`
  - `get_indexes()`
  - `get_foreign_keys()`
  - `has_view()`
  - `get_tables()`
  - `get_views()`
  - `get_types()`
  - `create()`
  - `drop()`
  - `table()`
  - `drop_columns()`
  - `drop_if_exists()`
  - `rename()`

### `framework/Illuminate/Database/Serializable.py`
- class `Serializable`

### `framework/Illuminate/Database/UniqueConstraintViolationException.py`
- class `UniqueConstraintViolationException`
  - `set_index()`
  - `set_columns()`

### `framework/Illuminate/Database/__init__.py`

### `framework/Illuminate/Database/Connection.py`
- class `Connection`
  - `url()`
  - `listen()`
  - `before_executing()`
  - `connect()`
  - `begin()`
  - `raw_connection()`
  - `get_pdo()`
  - `select()`
  - `select_one()`
  - `scalar()`
  - `select_from_write_connection()`
  - `insert()`
  - `update()`
  - `delete()`
  - `statement()`
  - `affecting_statement()`
  - `unprepared()`
  - `get_raw_pdo()`
  - `get_read_pdo()`
  - `get_raw_read_pdo()`
  - `get_direct_pdo()`
  - `get_raw_direct_pdo()`
  - `set_read_pdo()`
  - `set_read_pdo_config()`
  - `set_direct_pdo()`
  - `set_direct_pdo_config()`
  - `get_direct_pdo_config()`
  - `has_direct_connection()`
  - `get_name()`
  - `set_read_write_type()`
  - `get_name_with_read_write_type()`
  - `get_config()`
  - `get_driver_name()`
  - `get_driver_title()`
  - `get_server_version()`
  - `get_database_name()`
  - `get_table_prefix()`
  - `set_table_prefix()`
  - `set_reconnector()`
  - `reconnect()`
  - `disconnect()`
  - `purge()`
  - `dispose()`

### `framework/Illuminate/Database/ConnectionResolver.py`
- class `ConnectionResolver`
  - `connection()`
  - `add_connection()`
  - `has_connection()`
  - `get_default_connection()`
  - `set_default_connection()`

## Immediate inventory follow-up

1. Review every `missing` and `partial` row against Laravel source before implementation.
2. Keep SQLite JSON-overlap rows `blocked` while the pinned SQLite grammar lacks `compileJsonOverlaps`.
3. Convert each selected method group into a strict red-green-refactor slice with focused tests.
4. Update `framework/docs/LARAVEL_FEATURE_PARITY_TODO.md` after each evidenced slice.
