from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseManager:
    def __init__(self, app, config) -> None:
        self.app = app
        self.config = config
        self._engines: dict[str, Engine] = {}
        self._session_factories: dict[str, sessionmaker] = {}

    def connection(self, name: str | None = None) -> Engine:
        name = name or self.config.get("database.default", "sqlite")
        if name in self._engines:
            return self._engines[name]

        connection = self.config.get(f"database.connections.{name}")
        if connection is None:
            raise ValueError(f"Database connection [{name}] is not configured.")

        engine = create_engine(self._url(name, connection), future=True)
        if name == "sqlite" and connection.get("foreign_keys", True):
            self._enable_sqlite_foreign_keys(engine)

        self._engines[name] = engine
        self._session_factories[name] = sessionmaker(
            bind=engine,
            autoflush=True,
            expire_on_commit=False,
        )
        return engine

    def session(self, name: str | None = None) -> Session:
        name = name or self.config.get("database.default", "sqlite")
        self.connection(name)
        return self._session_factories[name]()

    @contextmanager
    def transaction(self, name: str | None = None):
        session = self.session(name)
        try:
            with session.begin():
                yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self) -> None:
        for engine in self._engines.values():
            engine.dispose()
        self._engines.clear()
        self._session_factories.clear()

    def _url(self, name, connection):
        url = connection.get("url")
        if url:
            return url
        if name != "sqlite":
            raise ValueError(f"Database driver [{name}] is not implemented.")

        database = Path(connection.get("database", ":memory:"))
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
