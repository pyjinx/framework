from __future__ import annotations


class DatabaseTransactionRecord:
    def __init__(self, connection, level: int, parent=None) -> None:
        self.connection = connection
        self.level = level
        self.parent = parent
        self._callbacks = []
        self._rollback_callbacks = []

    def add_callback(self, callback) -> None:
        self._callbacks.append(callback)

    def add_callback_for_rollback(self, callback) -> None:
        self._rollback_callbacks.append(callback)

    def execute_callbacks(self) -> None:
        if self.parent is not None:
            self.parent.execute_callbacks()
        for callback in tuple(self._callbacks):
            callback()

    def execute_callbacks_for_rollback(self) -> None:
        if self.parent is not None:
            self.parent.execute_callbacks_for_rollback()
        for callback in tuple(self._rollback_callbacks):
            callback()

    def get_callbacks(self) -> list:
        return list(self._callbacks)

    def get_callbacks_for_rollback(self) -> list:
        return list(self._rollback_callbacks)
