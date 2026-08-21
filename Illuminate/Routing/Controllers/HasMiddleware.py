from abc import ABC
from typing import Self


class Middleware:
    def __init__(
        self, name: str, only: list[str] = [], exclude: list[str] = []
    ) -> None:
        self.__name = name
        self.__only = only
        self.__exclude = exclude

    @property
    def name(self):
        return self.__name

    @property
    def only(self):
        return self.__only

    @property
    def exclude(self):
        return self.__exclude

    def set_only(self, only: str | list[str] = []) -> Self:
        self.__only = only if isinstance(only, list) else [only]

        return self

    def set_exclude(self, exclude: str | list[str] = []) -> Self:
        self.__exclude = exclude if isinstance(exclude, list) else [exclude]

        return self

    def filter(self, method) -> bool:
        if self.__only:
            return method in self.__only
        elif self.__exclude:
            return method not in self.__exclude

        return True


class HasMiddleware(ABC):
    @classmethod
    def middleware(cls) -> list[str | Middleware]:
        raise NotImplementedError("Must implement middleware method")
