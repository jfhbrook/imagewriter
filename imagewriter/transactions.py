from typing import Callable, Dict, Self, Sequence

from imagewriter.encoding.base import Command
from imagewriter.state import State

RevertFn = Callable[[State]]


class TransactionManager:
    def __init__(self: Self, state: State) -> None:
        self.state: State = state
        self._transactions: Dict[Command, RevertFn] = dict()

    def start_command(self: Self, command: Command, revert: RevertFn) -> None:
        self._transactions[command] = revert

    def complete_command(self: Self, command: Command) -> None:
        del self._transactions[command]

    def rollback(self: Self, commands: Sequence[Command]) -> None:
        for command in commands:
            if command in self._transactions:
                self._transactions[command](self.state)

        self._transactions = dict()
