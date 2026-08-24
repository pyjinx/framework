from __future__ import annotations

from Illuminate.Database.DatabaseTransactionRecord import DatabaseTransactionRecord


class DatabaseTransactionsManager:
    def __init__(self) -> None:
        self.pending_transactions: list[DatabaseTransactionRecord] = []
        self.committed_transactions: list[DatabaseTransactionRecord] = []

    def begin(self, connection, level: int) -> DatabaseTransactionRecord:
        parent = next(
            (
                record
                for record in reversed(self.pending_transactions)
                if record.connection == connection
            ),
            None,
        )
        record = DatabaseTransactionRecord(connection, level, parent)
        self.pending_transactions.append(record)
        return record

    def commit(self, connection, level_being_committed: int, new_transaction_level: int):
        self.stage_transactions(connection, level_being_committed)
        if self.after_commit_callbacks_should_be_executed(new_transaction_level):
            for record in tuple(self.committed_transactions):
                if record.connection == connection:
                    record.execute_callbacks()
        return self

    def stage_transactions(self, connection, level_being_committed: int) -> None:
        staged = [
            record
            for record in self.pending_transactions
            if record.connection == connection and record.level >= level_being_committed
        ]
        self.pending_transactions = [
            record for record in self.pending_transactions if record not in staged
        ]
        self.committed_transactions.extend(staged)

    def rollback(self, connection, new_transaction_level: int) -> None:
        rolled_back = [
            record
            for record in self.pending_transactions
            if record.connection == connection and record.level >= new_transaction_level
        ]
        self.pending_transactions = [
            record for record in self.pending_transactions if record not in rolled_back
        ]
        for record in rolled_back:
            record.execute_callbacks_for_rollback()

    def add_callback(self, callback) -> None:
        current = self.callback_applicable_transactions()[-1:] 
        if current:
            current[0].add_callback(callback)

    def add_callback_for_rollback(self, callback) -> None:
        current = self.callback_applicable_transactions()[-1:]
        if current:
            current[0].add_callback_for_rollback(callback)

    def callback_applicable_transactions(self) -> list[DatabaseTransactionRecord]:
        return self.pending_transactions

    def after_commit_callbacks_should_be_executed(self, level: int) -> bool:
        return level == 0

    def get_pending_transactions(self) -> list[DatabaseTransactionRecord]:
        return list(self.pending_transactions)

    def get_committed_transactions(self) -> list[DatabaseTransactionRecord]:
        return list(self.committed_transactions)
