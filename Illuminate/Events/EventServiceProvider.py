from Illuminate.Events.Dispatcher import Dispatcher
from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.Contracts.Foundation.Application import Application


class EventServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        def lambda_function(app: Application):
            return Dispatcher(self.__app)

        self.__app.singleton("events", lambda_function)

    def boot(self):
        pass
