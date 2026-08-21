from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class Gate(ABC):
    @abstractmethod
    def check(self, ability: str, arguments: list[Any] = []) -> bool:
        pass

    @abstractmethod
    def define(self, ability: str, callback: Callable[[Any], Any]) -> None:
        pass
