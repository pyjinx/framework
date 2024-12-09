from Illuminate.Log.LogManager import LogManager
from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Contracts.Foundation.Application import Application


class LogServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        def register_log_manager(app: Application):
            return LogManager(app)

        self.__app.singleton("log", register_log_manager)

    def boot(self):
        pass
