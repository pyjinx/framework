from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Validation.Factory import Factory


class ValidationServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        def register_factory(app: Application):
            return Factory(app)

        self.__app.singleton("validator", register_factory)

    def boot(self):
        pass
