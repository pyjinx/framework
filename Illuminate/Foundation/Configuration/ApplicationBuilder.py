from __future__ import annotations

from Illuminate.Contracts.Foundation.Application import Application
from Illuminate.Contracts.Foundation.Console.Kernel import (
    Kernel as ConsoleKernelContract,
)
from Illuminate.Contracts.Http.Kernel import Kernel as HttpKernelContract
from Illuminate.Foundation.Bootstrap.RegisterProviders import RegisterProviders
from Illuminate.Foundation.Console.Kernel import Kernel as ConsoleKernel
from Illuminate.Foundation.Http.Kernel import Kernel as HttpKernel
from collections.abc import Callable

from Illuminate.Exceptions.Handler import Handler
from Illuminate.Foundation.Configuration.Exceptions import Exceptions



class ApplicationBuilder:
    def __init__(self, application: Application):
        self.__application = application

    def with_routing(self):
        return self

    def with_middleware(self):
        return self

    def with_exceptions(
        self, using: Callable[[Exceptions], object] | None = None
    ) -> ApplicationBuilder:
        self.__application.singleton("exception_handler", lambda app: Handler(app))

        if using is not None:
            self.__application.after_resolving(
                "exception_handler",
                lambda handler: using(Exceptions(handler)),
            )

        return self

    def with_kernels(self):
        self.__application.singleton(HttpKernelContract, HttpKernel)
        self.__application.singleton(ConsoleKernelContract, ConsoleKernel)

        return self

    def with_events(self):
        return self

    def with_commands(self):
        return self

    def with_providers(self, providers=[]):
        RegisterProviders.merge(providers)

        return self

    def create(self):
        return self.__application
