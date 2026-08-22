from __future__ import annotations

from typing import Any, Callable

from Illuminate.Exceptions.Handler import ExceptionResponse, Handler


class Exceptions:
    """Laravel-shaped forwarding configuration for the bounded core handler."""

    def __init__(self, handler: Handler) -> None:
        self.handler = handler

    def report(self, callback: Callable[..., Any]) -> Callable[..., Any]:
        return self.handler.reportable(callback)

    def reportable(self, callback: Callable[..., Any]) -> Callable[..., Any]:
        return self.handler.reportable(callback)

    def render(self, callback: Callable[..., Any]) -> Exceptions:
        self.handler.renderable(callback)
        return self

    def renderable(self, callback: Callable[..., Any]) -> Exceptions:
        self.handler.renderable(callback)
        return self

    def respond(
        self,
        callback: Callable[[ExceptionResponse, BaseException, Any], ExceptionResponse],
    ) -> Exceptions:
        self.handler.respond_using(callback)
        return self

    def level(self, exception_type: type[BaseException], level: int) -> Exceptions:
        self.handler.level(exception_type, level)
        return self

    def context(
        self,
        callback: Callable[[BaseException, dict[str, Any]], dict[str, Any]],
    ) -> Exceptions:
        self.handler.build_context_using(callback)
        return self

    def dont_report(
        self, exceptions: type[BaseException] | list[type[BaseException]]
    ) -> Exceptions:
        self.handler.dont_report(exceptions)
        return self

    def dont_report_duplicates(self) -> Exceptions:
        self.handler.dont_report_duplicates()
        return self

    def should_render_json_when(
        self, callback: Callable[[Any, BaseException], bool]
    ) -> Exceptions:
        self.handler.should_render_json_when(callback)
        return self
