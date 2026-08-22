from contextlib import contextmanager
from pathlib import Path
from weakref import WeakSet

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseManager:
    def __init__(self, app, config) -> None:
        self.app = app
        self.config = config
        self._engines: dict[str, Engine] = {}
        self._engine_fingerprints: dict[str, tuple[str, bool]] = {}
        self._session_factories: dict[str, sessionmaker] = {}
        self._active_sessions: dict[str, WeakSet[Session]] = {}

    def connection(self, name: str | None = None) -> Engine:
        name = name or self.get_default_connection()
        if name in self._engines:
            return self._engines[name]

        connection = self._configuration(name)
        url = self._url(connection)
        engine = create_engine(url, future=True)
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
        self.connection(name)
        session = self._session_factories[name]()
        self._active_sessions.setdefault(name, WeakSet()).add(session)
        return session

    @contextmanager
    def transaction(self, name: str | None = None):
        name = name or self.get_default_connection()
        session = self.session(name)
        try:
            with session.begin():
                yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            self._active_sessions.get(name, WeakSet()).discard(session)

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
        return cleanup_error

    def _configuration(self, name: str) -> dict:
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
