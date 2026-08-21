from collections.abc import Callable
from typing import Any, Generic, Self, TypeVar

from Illuminate.Contracts.Collections.Collection import Collection as CollectionContract
from Illuminate.Helpers.Util import Util

T = TypeVar("T")


class Conditionable(Generic[T], CollectionContract):
    def when(
        self,
        value=None,
        callback: Callable[..., Any] | None = None,
        default: Callable[..., Any] | None = None,
    ) -> Self:
        value = value(self) if callable(value) else value

        if value:
            return (
                Util.callback_with_dynamic_args(callback, [self, value])
                if callable(callback)
                else self
            )
        else:
            return (
                Util.callback_with_dynamic_args(default, [self, value])
                if callable(default)
                else self
            )
