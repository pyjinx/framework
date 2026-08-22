from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Exceptions.Handler import Handler


class HandleExceptions:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        if "exception_handler" not in self.__app.get_bindings():
            self.__app.singleton(
                "exception_handler",
                lambda application: Handler(application),
            )
