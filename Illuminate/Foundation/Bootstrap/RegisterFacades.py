from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Support.Facades.Facade import Facade


class RegisterFacades:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        Facade.set_facade_application(self.__app)
