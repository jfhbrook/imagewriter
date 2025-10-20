from typing import List, Self

from imagewriter.encoding import apply_settings, Command, CR
from imagewriter.settings import Settings


class Job:
    """
    A print job.
    """

    def __init__(self: Self, settings: Settings) -> None:
        self._commands: List[Command] = [*apply_settings(settings), CR]

    def write(self: Self, commands: List[Command]) -> None:
        """
        Write raw commands.
        """

        self._commands += commands

    @property
    def commands(self: Self) -> List[Command]:
        """
        Commands to write to the printer to complete the job.
        """

        return self._commands + [CR]
