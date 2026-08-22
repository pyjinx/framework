from __future__ import annotations

import html
import traceback
from typing import Any


class DevelopmentDiagnostics:
    """Minimal, opt-in debug details; not an Ignition-compatible renderer."""

    @staticmethod
    def json_payload(exception: BaseException) -> dict[str, Any]:
        return {
            "message": str(exception),
            "exception": f"{type(exception).__module__}.{type(exception).__qualname__}",
            "trace": traceback.format_exception(exception),
        }

    @staticmethod
    def html_details(exception: BaseException) -> str:
        trace = "".join(traceback.format_exception(exception))
        return f"<pre>{html.escape(trace)}</pre>"
