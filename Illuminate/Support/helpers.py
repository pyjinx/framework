import inspect
import operator
from collections.abc import Callable
from typing import Any, TypeVar

from Illuminate.Support.HigherOrderTapProxy import HigherOrderTapProxy

T = TypeVar("T")
R = TypeVar("R")


def safe_eval_compare(key, oper, value):
    compare_ops = {
        "==": operator.eq,
        "!=": operator.ne,
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
    }

    if oper in compare_ops:
        return compare_ops[oper](key, value)
    else:
        raise ValueError("Invalid operator")


def tap(value: T, callback: Callable[[T], R] | None = None):
    if not callback:
        return HigherOrderTapProxy(value)

    callback(value)

    return value


def transform(
    value: T,
    callback: Callable[[T], R] | None = None,
    default: Callable[[T], R] | None = None,
):
    if value:
        return callback(value)

    if callable(default):
        return default(value)

    return default


def with_(value: T, callback: Callable[[T], R] | None = None) -> T:
    if not callback:
        return value

    return callback(value)


def is_class(obj: Any):
    return inspect.isclass(obj)


def is_class_instance(obj: Any):
    if is_class(obj):
        return False

    return isinstance(obj, obj.__class__)
