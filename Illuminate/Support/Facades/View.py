from typing import TYPE_CHECKING

from Illuminate.Support.Facades.Facade import Facade

if TYPE_CHECKING:
    from Illuminate.View.ViewFactory import ViewFactory


class View(metaclass=Facade):
    @classmethod
    def get_facade_accessor(cls):
        return "view"

    if TYPE_CHECKING:

        @classmethod
        def make(cls, file: str, args: dict | None = None) -> "ViewFactory": ...
