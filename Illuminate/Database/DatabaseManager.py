from collections.abc import Callable
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
from pathlib import Path
from time import perf_counter
from weakref import WeakSet

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from Illuminate.Database.Events.QueryExecuted import QueryExecuted


class _TransactionCallbacks:
    def __init__(self) -> None:
        self.after_commit = []
        self.after_rollback = []
        self.committed_children = []

    def run_after_commit(self) -> None:
        for child in self.committed_children:
            child.run_after_commit()
        for callback in self.after_commit:
            callback()

    def run_after_rollback(self) -> None:
        for child in self.committed_children:
            child.run_after_rollback()
        for callback in self.after_rollback:
            callback()


class _TransactionCallbackFailure(Exception):
    def __init__(self, original):
        self.original = original
        super().__init__(str(original))


class _ManualRollback(Exception):
    pass


class DatabaseManager:
    def __init__(self, app, config) -> None:
        self.app = app
        self.config = config
        self._engines: dict[str, Engine] = {}
        self._dynamic_connection_configurations: dict[str, dict] = {}
        self._extensions: dict[str, Callable] = {}
        self._engine_fingerprints: dict[str, tuple[str, bool]] = {}
        self._session_factories: dict[str, sessionmaker] = {}
        self._active_sessions: dict[str, WeakSet[Session]] = {}
        self._transaction_sessions: ContextVar[
            dict[str, tuple[Session, ...]] | None
        ] = ContextVar("database_manager_transaction_sessions", default=None)
        self._transaction_callbacks: ContextVar[
            dict[str, tuple[_TransactionCallbacks, ...]] | None
        ] = ContextVar("database_manager_transaction_callbacks", default=None)
        self._manual_transaction_contexts: ContextVar[
            dict[str, tuple[object, ...]] | None
        ] = ContextVar("database_manager_manual_transaction_contexts", default=None)
        self._query_listeners: list[Callable[[QueryExecuted], object]] = []

    @staticmethod
    def parse_connection_name(name: str) -> tuple[str, str | None]:
        for connection_type in ("read", "write", "direct"):
            suffix = f"::{connection_type}"
            if name.endswith(suffix):
                return name[: -len(suffix)], connection_type
        return name, None

    def connection(self, name: str | None = None) -> Engine:
        name = name or self.get_default_connection()
        database_name, _ = self.parse_connection_name(name)
        name = database_name
        if database_name in self._engines:
            return self._engines[database_name]

        connection = self._configuration(database_name)
        resolver = self._extensions.get(database_name) or self._extensions.get(
            connection.get("driver")
        )
        url = self._url(connection)
        engine = (
            resolver(connection, database_name)
            if resolver is not None
            else create_engine(url, future=True)
        )
        event.listen(engine, "before_cursor_execute", self._before_cursor_execute)
        event.listen(
            engine,
            "after_cursor_execute",
            lambda connection, cursor, statement, parameters, context, executemany: (
                self._after_cursor_execute(
                    name,
                    connection,
                    cursor,
                    statement,
                    parameters,
                    context,
                    executemany,
                )
            ),
        )
        if connection["driver"] == "sqlite" and connection.get("foreign_keys", True):
            self._enable_sqlite_foreign_keys(engine)

        self._engines[name] = engine
        self._engine_fingerprints[name] = (
            url,
            bool(connection.get("foreign_keys", True)),
        )
        self._session_factories[name] = sessionmaker(
            bind=engine,
            autoflush=True,
            expire_on_commit=False,
            close_resets_only=False,
        )
        self._active_sessions.setdefault(name, WeakSet())
        return engine

    def build(self, config: dict) -> Engine:
        """Build and cache a SQLite connection from dynamic configuration."""
        config = dict(config)
        name = config.get("name") or self.calculate_dynamic_connection_name(config)
        return self.connect_using(name, config, force=True)

    @staticmethod
    def calculate_dynamic_connection_name(config: dict) -> str:
        identity = "".join(
            f"{key}{value}"
            for key, value in config.items()
            if isinstance(value, (str, int)) and not isinstance(value, bool)
        )
        return f"dynamic_{hashlib.md5(identity.encode()).hexdigest()}"

    def connect_using(self, name: str, config: dict, force: bool = False) -> Engine:
        if force:
            self.purge(name)
        elif name in self._engines:
            raise RuntimeError(
                f"Cannot establish connection [{name}] because another "
                "connection with that name already exists."
            )

        self._dynamic_connection_configurations[name] = dict(config)
        return self.connection(name)

    def listen(self, callback: Callable[[QueryExecuted], object]) -> None:
        self._query_listeners.append(callback)

    def extend(self, name: str, resolver: Callable) -> None:
        self._extensions[name] = resolver

    def forget_extension(self, name: str) -> None:
        self._extensions.pop(name, None)

    @staticmethod
    def _before_cursor_execute(
        connection, cursor, statement, parameters, context, executemany
    ) -> None:
        context._pyjinx_query_started_at = perf_counter()

    def _after_cursor_execute(
        self,
        name: str,
        connection,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ) -> None:
        started_at = getattr(context, "_pyjinx_query_started_at", None)
        elapsed = 0.0 if started_at is None else (perf_counter() - started_at) * 1000
        bindings = self._query_bindings(parameters, executemany)
        query = QueryExecuted(
            str(statement),
            bindings,
            elapsed,
            self._engines[name],
            name,
        )
        for callback in tuple(self._query_listeners):
            callback(query)

    @staticmethod
    def _query_bindings(parameters, executemany: bool) -> list:
        if parameters is None:
            return []
        if isinstance(parameters, dict):
            return list(parameters.values())
        if executemany:
            return [value for row in parameters for value in row]
        if isinstance(parameters, (tuple, list)):
            return list(parameters)
        return [parameters]

    def get_pdo(self, name: str | None = None):
        """Return SQLAlchemy's pooled DBAPI connection boundary."""
        return self.connection(name).raw_connection()

    def get_raw_pdo(self, name: str | None = None):
        return self.get_pdo(name)

    def get_read_pdo(self, name: str | None = None):
        return self.get_pdo(name)

    def get_name(self, name: str | None = None) -> str:
        requested = name or self.get_default_connection()
        database_name, _ = self.parse_connection_name(requested)
        return database_name

    def get_config(self, name: str | None = None, option: str | None = None):
        requested = name or self.get_default_connection()
        database_name, _ = self.parse_connection_name(requested)
        config = dict(self._configuration(database_name))
        if option is None:
            return config

        value = config
        for segment in option.split("."):
            if not isinstance(value, dict) or segment not in value:
                return None
            value = value[segment]
        return value

    def get_driver_name(self, name: str | None = None) -> str | None:
        return self.get_config(name, "driver")

    def get_database_name(self, name: str | None = None):
        return self.get_config(name, "database")

    @staticmethod
    def supported_drivers() -> list[str]:
        return ["mysql", "mariadb", "pgsql", "sqlite", "sqlsrv"]

    @staticmethod
    def available_drivers() -> list[str]:
        return ["sqlite"]

    def get_name_with_read_write_type(self, name: str | None = None) -> str:
        requested = name or self.get_default_connection()
        database_name, connection_type = self.parse_connection_name(requested)
        return (
            f"{database_name}::{connection_type}" if connection_type else database_name
        )

    def get_table_prefix(self, name: str | None = None) -> str:
        requested = name or self.get_default_connection()
        database_name, _ = self.parse_connection_name(requested)
        return str(self._configuration(database_name).get("prefix", ""))

    def prefixed_table_name(self, table_name: str, name: str | None = None) -> str:
        return f"{self.get_table_prefix(name)}{table_name}"

    def disconnect(self, name: str | None = None) -> None:
        name = name or self.get_default_connection()
        cleanup_error = self._close_sessions(name)
        dispose_error = None
        if engine := self._engines.get(name):
            try:
                engine.dispose()
            except Exception as error:
                dispose_error = error

        if cleanup_error is not None:
            if dispose_error is not None:
                raise cleanup_error from dispose_error
            raise cleanup_error
        if dispose_error is not None:
            raise dispose_error

    def purge(self, name: str | None = None) -> None:
        name = name or self.get_default_connection()
        cleanup_error = None
        try:
            self.disconnect(name)
        except Exception as error:
            cleanup_error = error
        finally:
            self._engines.pop(name, None)
            self._engine_fingerprints.pop(name, None)
            self._session_factories.pop(name, None)
            self._active_sessions.pop(name, None)

        if cleanup_error is not None:
            raise cleanup_error

    def reconnect(self, name: str | None = None) -> Engine:
        name = name or self.get_default_connection()
        if name not in self._engines:
            return self.connection(name)

        try:
            connection = self._configuration(name)
            configured_fingerprint = (
                self._url(connection),
                bool(connection.get("foreign_keys", True)),
            )
        except Exception as configuration_error:
            try:
                self.purge(name)
            except Exception as cleanup_error:
                raise configuration_error from cleanup_error
            raise

        if self._engine_fingerprints.get(name) != configured_fingerprint:
            self.purge(name)
            return self.connection(name)

        self.disconnect(name)
        return self._engines[name]

    def using_connection(self, name: str, callback):
        previous_name = self.get_default_connection()
        self.set_default_connection(name)

        try:
            return callback()
        finally:
            self.set_default_connection(previous_name)

    def get_default_connection(self) -> str:
        return self.config.get("database.default", "sqlite")

    def set_default_connection(self, name: str) -> None:
        self.config.set("database.default", name)

    def get_connections(self) -> dict[str, Engine]:
        return dict(self._engines)

    def table(self, table_name: str, connection_name: str | None = None):
        from Illuminate.Database.QueryBuilder import QueryBuilder

        return QueryBuilder(self, table_name, connection_name)

    def session(self, name: str | None = None) -> Session:
        name = name or self.get_default_connection()
        sessions = (self._transaction_sessions.get() or {}).get(name, ())
        if sessions:
            return sessions[-1]

        self.connection(name)
        session = self._session_factories[name]()
        self._active_sessions.setdefault(name, WeakSet()).add(session)
        return session

    @contextmanager
    def _query_connection(self, name: str | None = None, write: bool = False):
        name = name or self.get_default_connection()
        sessions = (self._transaction_sessions.get() or {}).get(name, ())
        if sessions:
            yield sessions[-1].connection()
            return

        engine = self.connection(name)
        if write:
            with engine.begin() as connection:
                yield connection
        else:
            with engine.connect() as connection:
                yield connection

    def _query_bind(self, name: str | None = None):
        name = name or self.get_default_connection()
        sessions = (self._transaction_sessions.get() or {}).get(name, ())
        return sessions[-1].connection() if sessions else self.connection(name)

    def transaction(self, callback=None, attempts: int = 1, name: str | None = None):
        if callable(callback):
            return self._run_transaction(callback, attempts, name)

        if callback is not None:
            if not isinstance(callback, str) or name is not None:
                raise TypeError("Transaction callback must be callable.")
            name = callback

        return self._transaction_context(name)

    def begin_transaction(self, name: str | None = None) -> None:
        """Start a transaction that is completed by commit or roll_back."""
        name = name or self.get_default_connection()
        context = self._transaction_context(name)
        context.__enter__()

        contexts = dict(self._manual_transaction_contexts.get() or {})
        contexts[name] = (
            *contexts.get(name, ()),
            context,
        )
        self._manual_transaction_contexts.set(contexts)

    def commit(self, name: str | None = None) -> None:
        """Commit the active direct transaction."""
        name = name or self.get_default_connection()
        contexts = dict(self._manual_transaction_contexts.get() or {})
        stack = contexts.get(name, ())
        if not stack:
            return

        context = stack[-1]
        try:
            context.__exit__(None, None, None)
        finally:
            contexts[name] = stack[:-1]
            self._manual_transaction_contexts.set(contexts)

    def roll_back(self, to_level: int | None = None, name: str | None = None) -> None:
        """Roll back direct transactions through the requested level."""
        name = name or self.get_default_connection()
        contexts = dict(self._manual_transaction_contexts.get() or {})
        stack = contexts.get(name, ())
        if not stack:
            return

        target = len(stack) - 1 if to_level is None else to_level
        if target < 0 or target >= len(stack):
            return

        while len(stack) > target:
            context = stack[-1]
            rollback = _ManualRollback()
            try:
                context.__exit__(_ManualRollback, rollback, rollback.__traceback__)
            except _ManualRollback as error:
                if error is not rollback:
                    raise
            finally:
                stack = stack[:-1]
                contexts[name] = stack
                self._manual_transaction_contexts.set(contexts)

    @contextmanager
    def _transaction_context(self, name: str | None):
        name = name or self.get_default_connection()
        sessions = (self._transaction_sessions.get() or {}).get(name, ())
        session = sessions[-1] if sessions else self.session(name)
        try:
            transaction = session.begin_nested() if sessions else session.begin()
        except Exception:
            if not sessions:
                self._close_transaction_session(name, session)
            raise

        session_stacks = dict(self._transaction_sessions.get() or {})
        session_stacks[name] = (*sessions, session)
        session_token = self._transaction_sessions.set(session_stacks)
        callbacks = (self._transaction_callbacks.get() or {}).get(name, ())
        callback_stacks = dict(self._transaction_callbacks.get() or {})
        transaction_callbacks = _TransactionCallbacks()
        callback_stacks[name] = (*callbacks, transaction_callbacks)
        callback_token = self._transaction_callbacks.set(callback_stacks)

        body_error = None
        body_raised = False
        rollback_failed = False
        try:
            try:
                with transaction:
                    try:
                        yield session
                    except BaseException as error:
                        body_raised = True
                        body_error = error
                        raise
            except BaseException as error:
                rollback_failed = body_error is not None and error is not body_error
                body_error = error

            if body_error is None and callbacks:
                callbacks[-1].committed_children.append(transaction_callbacks)
        finally:
            self._transaction_callbacks.reset(callback_token)
            self._transaction_sessions.reset(session_token)
            if not sessions:
                self._close_transaction_session(name, session)
        if body_error is not None:
            if body_raised and not rollback_failed:
                try:
                    transaction_callbacks.run_after_rollback()
                except Exception as callback_error:
                    raise _TransactionCallbackFailure(callback_error) from body_error
            raise body_error

        if not callbacks:
            try:
                transaction_callbacks.run_after_commit()
            except Exception as callback_error:
                raise _TransactionCallbackFailure(callback_error) from None

    def _run_transaction(self, callback, attempts: int, name: str | None):
        name = name or self.get_default_connection()
        for current_attempt in range(1, attempts + 1):
            is_nested = self.transaction_level(name) > 0
            try:
                with self._transaction_context(name) as session:
                    result = callback(session)
            except _TransactionCallbackFailure as error:
                raise error.original from error
            except Exception as error:
                if (
                    not is_nested
                    and current_attempt < attempts
                    and self._caused_by_concurrency_error(error)
                ):
                    continue
                raise
            return result

        return None

    def transaction_level(self, name: str | None = None) -> int:
        name = name or self.get_default_connection()
        return len((self._transaction_sessions.get() or {}).get(name, ()))

    def after_commit(self, callback, name: str | None = None) -> None:
        name = name or self.get_default_connection()
        callbacks = (self._transaction_callbacks.get() or {}).get(name, ())
        if callbacks:
            callbacks[-1].after_commit.append(callback)
        else:
            callback()

    def after_rollback(self, callback, name: str | None = None) -> None:
        name = name or self.get_default_connection()
        callbacks = (self._transaction_callbacks.get() or {}).get(name, ())
        if callbacks:
            callbacks[-1].after_rollback.append(callback)

    def _close_transaction_session(self, name: str, session: Session) -> None:
        try:
            session.close()
        finally:
            self._active_sessions.get(name, WeakSet()).discard(session)

    @staticmethod
    def _caused_by_concurrency_error(error: Exception) -> bool:
        messages = (
            "Deadlock found when trying to get lock",
            "deadlock detected",
            "The database file is locked",
            "database is locked",
            "database table is locked",
            "A table in the database is locked",
            "has been chosen as the deadlock victim",
            "Lock wait timeout exceeded; try restarting transaction",
            "WSREP detected deadlock/conflict and aborted the transaction. Try restarting the transaction",
            "Record has changed since last read in table",
        )
        current = error
        seen = set()
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            if (
                str(getattr(current, "code", "")) == "40001"
                or str(getattr(current, "sqlstate", "")) == "40001"
            ):
                return True
            if any(message in str(current) for message in messages):
                return True
            current = getattr(current, "orig", None) or getattr(
                current, "__cause__", None
            )

        return False

    def dispose(self) -> None:
        cleanup_error = None
        for name in list(self._engines):
            error = self._close_sessions(name)
            cleanup_error = cleanup_error or error

        for engine in self._engines.values():
            try:
                engine.dispose()
            except Exception as error:
                cleanup_error = cleanup_error or error

        self._engines.clear()
        self._engine_fingerprints.clear()
        self._session_factories.clear()
        self._active_sessions.clear()

        if cleanup_error is not None:
            raise cleanup_error

    def _close_sessions(self, name: str):
        sessions = self._active_sessions.get(name)
        if sessions is None:
            return None

        cleanup_error = None
        for session in list(sessions):
            try:
                session.rollback()
            except Exception as error:
                cleanup_error = cleanup_error or error
            finally:
                try:
                    session.close()
                except Exception as error:
                    cleanup_error = cleanup_error or error
        sessions.clear()

    def _configuration(self, name: str) -> dict:
        connection = self._dynamic_connection_configurations.get(name)
        if connection is None:
            connection = self.config.get(f"database.connections.{name}")
        if connection is None:
            raise ValueError(f"Database connection [{name}] is not configured.")
        return connection

    def _url(self, connection: dict) -> str:
        driver = connection.get("driver")
        if driver is None:
            raise ValueError("A driver must be specified.")
        if driver != "sqlite":
            raise ValueError(f"Unsupported driver [{driver}].")

        url = connection.get("url")
        if url:
            return url

        database = connection.get("database", ":memory:")
        if database == ":memory:":
            return "sqlite:///:memory:"

        database = Path(database)
        if not database.is_absolute():
            database = Path(self.app.base_path()) / database
        database.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{database}"

    @staticmethod
    def _enable_sqlite_foreign_keys(engine):
        @event.listens_for(engine, "connect")
        def set_foreign_keys(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
