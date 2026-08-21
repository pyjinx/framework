from typing import Any, Self


class ValidationResponse:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__initial_data = data
        self.__validated_data: dict = {}
        self.__validation_errors: dict = {}
        self.__validated = False

    @property
    def validated(self) -> bool:
        return self.__validated

    @property
    def data(self) -> dict[str, Any]:
        return self.__validated_data

    @property
    def errors(self) -> dict[str, list[str]]:
        return self.__validation_errors

    def set_error(self, field, value) -> None:
        field_errors = self.__validation_errors.setdefault(field, [])

        field_errors.append(value)

    def execute(self) -> Self:
        self.__validated = len(self.errors.keys()) == 0

        if self.__validated:
            self.__validated_data = self.__initial_data

        return self
