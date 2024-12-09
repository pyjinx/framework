from Illuminate.Foundation.Support.Providers.RouteServiceProvider import (
    RouteServiceProvider as ServiceProvider,
)
from Illuminate.View.ViewFactory import ViewFactory
from Illuminate.Foundation.Application import Application


class ViewServiceProvider(ServiceProvider):
    def __init__(self, app: Application) -> None:
        self.__app = app

    def register(self):
        def register_view_factory(app: Application):
            return ViewFactory(app)

        self.__app.singleton("view", register_view_factory)

    def boot(self):
        pass
