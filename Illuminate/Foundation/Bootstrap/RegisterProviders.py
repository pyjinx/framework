from Illuminate.Contracts.Foundation.Application import Application


class RegisterProviders:
    _merge: list = []

    def bootstrap(self, app: Application) -> None:
        self._merge_additional_providers(app)
        app.register_configured_providers()

    def _merge_additional_providers(self, app: Application) -> None:
        config = app.make("config")
        configured = list(config.get("app.providers", []) or [])
        additional = list(type(self)._merge)
        type(self)._merge = []

        providers = []
        for provider in [*configured, *additional]:
            if provider not in providers:
                providers.append(provider)
        config.set("app.providers", providers)

    @classmethod
    def merge(cls, providers) -> None:
        for provider in providers:
            if provider not in cls._merge:
                cls._merge.append(provider)
