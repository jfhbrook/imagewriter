from contextlib import contextmanager
from typing import Generator, List, Self

from imagewriter.encoding import (
    apply_settings,
    CharacterEncoder,
    Command,
    CR,
    reset_tabs,
    SetPitch,
    START_BOLDFACE,
    START_DOUBLE_WIDTH,
    START_HALF_HEIGHT,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    START_UNDERLINE,
    STOP_BOLDFACE,
    STOP_DOUBLE_WIDTH,
    STOP_HALF_HEIGHT,
    STOP_SUBSCRIPT,
    STOP_SUPERSCRIPT,
    STOP_UNDERLINE,
    Text,
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
        self._map_mousetext = not settings.include_eighth_data_bit
        self._map_custom = not settings.include_eighth_data_bit
        self._character_encoder = CharacterEncoder(
            self._settings.language,
            map_mousetext=self._map_mousetext,
            map_custom=self._map_custom,
        )
        self._has_header: bool = False
        self._commands: List[Command] = list()

    @property
    def settings(self: Self) -> Settings:
        return self._settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        self._settings = settings
        self._character_encoder = CharacterEncoder(
            self._settings.language,
            map_mousetext=self._map_mousetext,
            map_custom=self._map_custom,
        )

    def __len__(self: Self) -> int:
        return len(self._commands)

    def _write_header(self: Self) -> None:
        if not self._has_header:
            self._commands += [*apply_settings(self._settings), CR]
            self._has_header = True

    def write(self: Self, commands: Command | List[Command]) -> Self:
        """
        Write raw commands.
        """

        self._write_header()
        if isinstance(commands, Command):
            self._commands.append(commands)
        else:
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

    def text(self: Self, *text: Text) -> Self:
        """
        Write text.
        """

        self.write(self._character_encoder.encode(*text))

        return self

    @contextmanager
    def double_width(self: Self) -> Generator[None, None, None]:
        """
        Write double width text.
        """

        self.write(START_DOUBLE_WIDTH)

        yield

        self.write(STOP_DOUBLE_WIDTH)

    @contextmanager
    def underline(self: Self) -> Generator[None, None, None]:
        """
        Write underlined text.
        """

        self.write(START_UNDERLINE)

        yield

        self.write(STOP_UNDERLINE)

    @contextmanager
    def boldface(self: Self) -> Generator[None, None, None]:
        """
        Write boldfaced text.
        """

        self.write(START_BOLDFACE)

        yield

        self.write(STOP_BOLDFACE)

    @contextmanager
    def half_height(self: Self) -> Generator[None, None, None]:
        """
        Write half-height text.
        """

        self.write(START_HALF_HEIGHT)

        yield

        self.write(STOP_HALF_HEIGHT)

    @contextmanager
    def superscript(self: Self) -> Generator[None, None, None]:
        """
        Write superscript text.
        """

        if self._commands[-1] == STOP_SUBSCRIPT:
            self._commands.pop()

        self.write(START_SUPERSCRIPT)

        yield

        self.write(STOP_SUPERSCRIPT)

    @contextmanager
    def subscript(self: Self) -> Generator[None, None, None]:
        """
        Write subscript text.
        """

        if self._commands[-1] == STOP_SUPERSCRIPT:
            self._commands.pop()

        self.write(START_SUBSCRIPT)

        yield

        self.write(STOP_SUBSCRIPT)
