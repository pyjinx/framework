from typing import TYPE_CHECKING

from Illuminate.Support.ServiceProvider import ServiceProvider
from Illuminate.View.ViewFactory import ViewFactory

if TYPE_CHECKING:
    from Illuminate.Foundation.Application import Application


class ViewServiceProvider(ServiceProvider):
    def __init__(self, app: "Application") -> None:
        self.__app = app

    def register(self):
        def register_view_factory(app: "Application"):
            return ViewFactory(app)

        self.__app.singleton("view", register_view_factory)

    def boot(self):
        pass
