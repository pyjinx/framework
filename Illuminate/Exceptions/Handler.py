from __future__ import annotations

import html
import inspect
import json
import logging
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from weakref import WeakKeyDictionary

from Illuminate.Exceptions.Diagnostics import DevelopmentDiagnostics
from Illuminate.Exceptions.MethodNotAllowedException import MethodNotAllowedException
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException


@dataclass(frozen=True)
class ExceptionResponse:
    """The framework-owned response produced by the core exception handler."""

    status_code: int
    body: str
    headers: dict[str, str]

    def get_status_code(self) -> int:
        return self.status_code

    def get_headers(self) -> list[tuple[str, str]]:
        return list(self.headers.items())

    def get_content(self) -> str:
        return self.body


class Handler:
    """Report and render exceptions without depending on development diagnostics."""

    def __init__(self, app) -> None:
        self._app = app
        self._dont_report: list[type[BaseException]] = [
            MethodNotAllowedException,
            RouteNotFoundException,
        ]
        self._report_callbacks: list[Callable[..., Any]] = []
        self._render_callbacks: list[Callable[..., Any]] = []
        self._context_callbacks: list[
            Callable[[BaseException, dict[str, Any]], dict[str, Any]]
        ] = []
        self._levels: dict[type[BaseException], int] = {}
        self._should_render_json_when: (
            Callable[[Any, BaseException], bool] | None
        ) = None
        self._respond_using: (
            Callable[[ExceptionResponse, BaseException, Any], ExceptionResponse] | None
        ) = None
        self._without_duplicates = False
        self._reported_exceptions = WeakKeyDictionary()
        self._reported_nonweakref_ids: OrderedDict[int, None] = OrderedDict()
        self._reported_nonweakref_limit = 1024

    def reportable(self, callback: Callable[..., Any]) -> Callable[..., Any]:
        self._report_callbacks.append(callback)
        return callback

    def dont_report(self, exceptions: type[BaseException] | list[type[BaseException]]) -> Handler:
        for exception_type in self._wrap(exceptions):
            if exception_type not in self._dont_report:
                self._dont_report.append(exception_type)
        return self

    def level(self, exception_type: type[BaseException], level: int) -> Handler:
        self._levels[exception_type] = level
        return self

    def build_context_using(
        self,
        callback: Callable[[BaseException, dict[str, Any]], dict[str, Any]],
    ) -> Handler:
        self._context_callbacks.append(callback)
        return self

    def dont_report_duplicates(self) -> Handler:
        self._without_duplicates = True
        return self

    def should_render_json_when(
        self, callback: Callable[[Any, BaseException], bool]
    ) -> Handler:
        self._should_render_json_when = callback
        return self

    def renderable(self, callback: Callable[..., Any]) -> Handler:
        self._render_callbacks.append(callback)
        return self

    def respond_using(
        self, callback: Callable[[ExceptionResponse, BaseException, Any], ExceptionResponse]
    ) -> Handler:
        self._respond_using = callback
        return self

    def should_report(self, exception: BaseException) -> bool:
        if self._without_duplicates and self._has_reported(exception):
            return False
        return not isinstance(exception, tuple(self._dont_report))

    def report(self, exception: BaseException) -> None:
        if not self.should_report(exception):
            return

        self._mark_reported(exception)


        for callback in self._report_callbacks:
            if self._callback_handles(callback, exception) and callback(exception) is False:
                return

        context = self._build_context(exception)
        self._logger().log(
            self._map_log_level(exception),
            str(exception),
            extra={"context": context, "exception": exception},
        )
    def _has_reported(self, exception: BaseException) -> bool:
        if id(exception) in self._reported_nonweakref_ids:
            return True
        try:
            return exception in self._reported_exceptions
        except TypeError:
            return False

    def _mark_reported(self, exception: BaseException) -> None:
        try:
            self._reported_exceptions[exception] = True
            return
        except TypeError:
            # Built-in exceptions cannot be weak-referenced. Keep this fallback
            # bounded so duplicate suppression cannot retain an unbounded ID set.
            exception_id = id(exception)
            self._reported_nonweakref_ids[exception_id] = None
            self._reported_nonweakref_ids.move_to_end(exception_id)
            while len(self._reported_nonweakref_ids) > self._reported_nonweakref_limit:
                self._reported_nonweakref_ids.popitem(last=False)


    def render(self, request, exception: BaseException) -> ExceptionResponse:
        response = self._render_from_exception(request, exception)
        if response is None:
            response = self._render_via_callbacks(request, exception)
        if response is None:
            response = self._render_default(request, exception)

        if self._respond_using is not None:
            response = self._respond_using(response, exception, request)
            if not isinstance(response, ExceptionResponse):
                raise TypeError("Exception response callback must return ExceptionResponse.")

        return response

    def _render_from_exception(
        self, request, exception: BaseException
    ) -> ExceptionResponse | None:
        renderer = getattr(exception, "render", None)
        if not callable(renderer):
            return None
        return self._ensure_response(renderer(request))

    def _render_via_callbacks(
        self, request, exception: BaseException
    ) -> ExceptionResponse | None:
        for callback in self._render_callbacks:
            if not self._callback_handles(callback, exception):
                continue
            response = self._ensure_response(callback(exception, request))
            if response is not None:
                return response
        return None

    def _render_default(self, request, exception: BaseException) -> ExceptionResponse:
        status_code, headers = self._exception_status_and_headers(exception)
        if self._should_return_json(request, exception):
            return self._json_response(exception, status_code, headers)
        return self._html_response(exception, status_code, headers)

    def _json_response(
        self, exception: BaseException, status_code: int, headers: dict[str, str]
    ) -> ExceptionResponse:
        payload: dict[str, Any]
        if self._debug_enabled():
            payload = DevelopmentDiagnostics.json_payload(exception)
        else:
            payload = {
                "message": str(exception) if status_code != 500 else "Server Error"
            }

        return ExceptionResponse(
            status_code,
            json.dumps(payload, indent=2, ensure_ascii=False),
            {"Content-Type": "application/json", **headers},
        )

    def _html_response(
        self, exception: BaseException, status_code: int, headers: dict[str, str]
    ) -> ExceptionResponse:
        message = str(exception) if status_code != 500 else "Server Error"
        details = ""
        if self._debug_enabled():
            message = str(exception) or type(exception).__name__
            details = DevelopmentDiagnostics.html_details(exception)

        body = (
            "<!doctype html><html><head><meta charset=\"utf-8\">"
            f"<title>{status_code}</title></head><body><h1>{status_code}</h1>"
            f"<p>{html.escape(message)}</p>{details}</body></html>"
        )
        return ExceptionResponse(
            status_code,
            body,
            {"Content-Type": "text/html; charset=utf-8", **headers},
        )

    def _should_return_json(self, request, exception: BaseException) -> bool:
        if self._should_render_json_when is not None:
            return bool(self._should_render_json_when(request, exception))

        expects_json = getattr(request, "expects_json", None)
        if callable(expects_json):
            return bool(expects_json())

        header = getattr(request, "header", None)
        accept = header("Accept") if callable(header) else None
        return self._accepts_json(accept)

    @staticmethod
    def _accepts_json(accept: str | None) -> bool:
        if not accept:
            return False
        preferred = accept.split(",", 1)[0].split(";", 1)[0].strip().lower()
        return preferred == "application/json" or preferred.endswith("+json")

    def _debug_enabled(self) -> bool:
        try:
            config = self._app.make("config")
        except Exception:
            return False
        return bool(config.get("app.debug", False))

    def _build_context(self, exception: BaseException) -> dict[str, Any]:
        context_method = getattr(exception, "context", None)
        context = dict(context_method()) if callable(context_method) else {}
        for callback in self._context_callbacks:
            addition = callback(exception, context)
            if addition is not None:
                context.update(addition)
        return context

    def _map_log_level(self, exception: BaseException) -> int:
        for exception_type, level in self._levels.items():
            if isinstance(exception, exception_type):
                return level
        return logging.ERROR

    def _logger(self):
        try:
            logger = self._app.make("logger")
        except Exception:
            logger = logging.getLogger("pyjinx")
        if not callable(getattr(logger, "log", None)):
            raise TypeError("Configured exception logger must provide log().")
        return logger

    @staticmethod
    def _wrap(
        exceptions: type[BaseException] | list[type[BaseException]],
    ) -> list[type[BaseException]]:
        return exceptions if isinstance(exceptions, list) else [exceptions]

    @staticmethod
    def _callback_handles(callback: Callable[..., Any], exception: BaseException) -> bool:
        parameters = tuple(inspect.signature(callback).parameters.values())
        if not parameters:
            return True
        annotation = parameters[0].annotation
        return (
            annotation is inspect.Parameter.empty
            or not inspect.isclass(annotation)
            or isinstance(exception, annotation)
        )

    @staticmethod
    def _ensure_response(response: Any) -> ExceptionResponse | None:
        if response is None:
            return None
        if not isinstance(response, ExceptionResponse):
            raise TypeError("Exception render callbacks must return ExceptionResponse.")
        return response

    @staticmethod
    def _exception_status_and_headers(
        exception: BaseException,
    ) -> tuple[int, dict[str, str]]:
        status_code = getattr(exception, "status_code", 500)
        if not isinstance(status_code, int) or not 400 <= status_code <= 599:
            status_code = 500
        raw_headers = getattr(exception, "headers", {})
        headers = dict(raw_headers) if isinstance(raw_headers, dict) else {}
        return status_code, headers
