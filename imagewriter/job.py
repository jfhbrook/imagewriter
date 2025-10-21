from typing import List, Self

from imagewriter.encoding import (
    apply_settings,
    Command,
    CR,
    reset_tabs,
    SetPitch,
    to_tab_stops,
)
from imagewriter.pitch import Pitch
from imagewriter.settings import Settings
from imagewriter.units import Length


class Job:
    """
    A print job.
    """

    def __init__(self: Self, settings: Settings) -> None:
        self._settings: Settings = settings
        self._has_header: bool = False
        self._commands: List[Command] = list()

    def _write_header(self: Self) -> None:
        if not self._has_header:
            self._commands += [*apply_settings(self._settings), CR]
            self._has_header = True

    def write(self: Self, commands: List[Command]) -> Self:
        """
        Write raw commands.
        """

        self._write_header()
        self._commands += commands

        return self

    @property
    def commands(self: Self) -> List[Command]:
        """
        Commands to write to the printer to complete the job.
        """

        self._write_header()
        self._commands.append(CR)

        return self._commands

    def pitch(self: Self, pitch: Pitch) -> Self:
        """
        Set the current pitch.
        """

        self._settings = Settings.replace(self._settings, pitch=pitch)
        if self._has_header:
            self._commands += [
                SetPitch(pitch),
                *reset_tabs(to_tab_stops(self._settings.tab_stops, pitch)),
            ]

        return self

    def tab_stops(self: Self, tab_stops: List[Length]) -> Self:
        """
        Set the current tab stops.
        """

        self._settings = Settings.replace(self._settings, tab_stops=tab_stops)

        if self._has_header:
            self._commands += reset_tabs(to_tab_stops(tab_stops, self._settings.pitch))
        return self
