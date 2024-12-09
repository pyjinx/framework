from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Exceptions.Handler import Handler


class HandleExceptions:
    def bootstrap(self, app: Application) -> None:
        self.__app = app

        def register_exception_handler(app: Application):
            return Handler(app)

        self.__app.singleton("exception_handler", register_exception_handler)
