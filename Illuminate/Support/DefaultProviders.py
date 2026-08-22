from __future__ import annotations

from typing import Iterable, Self


class DefaultProviders:
    """Laravel-shaped default framework provider collection."""

    def __init__(self, providers: Iterable[type] | None = None):
        self.providers = list(providers) if providers is not None else self._defaults()

    @staticmethod
    def _defaults() -> list[type]:
        from Illuminate.Auth.AuthServiceProvider import AuthServiceProvider
        from Illuminate.Database.DatabaseServiceProvider import DatabaseServiceProvider
        from Illuminate.Events.EventServiceProvider import EventServiceProvider
        from Illuminate.Foundation.Providers.CommanderServiceProvider import (
            CommanderServiceProvider,
        )
        from Illuminate.Routing.RoutingServiceProvider import RoutingServiceProvider
        from Illuminate.Validation.ValidationServiceProvider import (
            ValidationServiceProvider,
        )
        from Illuminate.View.ViewServiceProvider import ViewServiceProvider

        return [
            AuthServiceProvider,
            EventServiceProvider,
            DatabaseServiceProvider,
            RoutingServiceProvider,
            ValidationServiceProvider,
            CommanderServiceProvider,
            ViewServiceProvider,
        ]

    def merge(self, providers: Iterable[type]) -> Self:
        return type(self)([*self.providers, *providers])

    def replace(self, replacements: dict[type, type]) -> Self:
        return type(self)(
            [replacements.get(provider, provider) for provider in self.providers]
        )

    def except_(self, providers: Iterable[type]) -> Self:
        excluded = set(providers)
        return type(self)(provider for provider in self.providers if provider not in excluded)

    def to_array(self) -> list[type]:
        return list(self.providers)
