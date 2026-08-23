from __future__ import annotations

import json
from urllib.parse import parse_qs, unquote, urlparse


class ConfigurationUrlParser:
    """Parse Laravel database configuration URLs into connection options."""

    _driver_aliases = {
        "mssql": "sqlsrv",
        "mysql2": "mysql",
        "postgres": "pgsql",
        "postgresql": "pgsql",
        "sqlite3": "sqlite",
    }

    @classmethod
    def get_driver_aliases(cls) -> dict[str, str]:
        return dict(cls._driver_aliases)

    @classmethod
    def add_driver_alias(cls, alias: str, driver: str) -> None:
        cls._driver_aliases[alias] = driver

    def parse_configuration(self, config: dict | str) -> dict:
        if isinstance(config, str):
            config = {"url": config}
        else:
            config = dict(config)

        url = config.pop("url", None)
        if not url:
            return config

        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc and not parsed.path:
            raise ValueError("The database configuration URL is malformed.")

        components = self._primary_options(parsed)
        components.update(self._query_options(parsed.query))
        return {**config, **components}

    def _primary_options(self, parsed) -> dict:
        driver = self._driver_aliases.get(parsed.scheme, parsed.scheme or None)
        options = {"driver": driver} if driver else {}

        if parsed.username is not None:
            options["username"] = unquote(parsed.username)
        if parsed.password is not None:
            options["password"] = unquote(parsed.password)
        if parsed.hostname and parsed.hostname != "null":
            options["host"] = unquote(parsed.hostname)
        if parsed.port is not None:
            options["port"] = parsed.port

        path = unquote(parsed.path)
        if path and path != "/":
            if driver == "sqlite":
                if path == "/:memory:":
                    path = ":memory:"
                elif path.startswith("//"):
                    path = path[1:]
                else:
                    path = path.lstrip("/")
            else:
                path = path.lstrip("/")
            options["database"] = path

        return {key: value for key, value in options.items() if value is not None}

    def _query_options(self, query: str) -> dict:
        if not query:
            return {}

        options = {}
        for key, values in parse_qs(query, keep_blank_values=True).items():
            normalized_key = key[:-2] if key.endswith("[]") else key
            parsed_values = [self._native(unquote(value)) for value in values]
            options[normalized_key] = parsed_values if key.endswith("[]") else parsed_values[-1]
        return options

    @staticmethod
    def _native(value: str):
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value
