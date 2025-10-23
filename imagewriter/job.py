from contextlib import contextmanager
from typing import Generator, List, Self, Sequence

from imagewriter.character import Text
from imagewriter.color import Color
from imagewriter.encoding import (
    apply_settings,
    BACKSPACE,
    CharacterEncoder,
    Command,
    CR,
    reset_tabs,
    set_color,
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
        self._character_encoder = CharacterEncoder(
            settings.language,
            map_mousetext=not settings.include_eighth_data_bit,
            map_custom=not settings.include_eighth_data_bit,
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
            settings.language,
            map_mousetext=not settings.include_eighth_data_bit,
            map_custom=not settings.include_eighth_data_bit,
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

        self.settings = Settings.replace(self.settings, pitch=pitch)
        if self._has_header:
            self._commands += [
                SetPitch(pitch),
                *reset_tabs(to_tab_stops(self.settings.tab_stops, pitch)),
            ]

        return self

    def tab_stops(self: Self, tab_stops: Sequence[Length]) -> Self:
        """
        Set the current tab stops.
        """

        self._settings = Settings.replace(self._settings, tab_stops=tab_stops)

        if self._has_header:
            self._commands += reset_tabs(to_tab_stops(tab_stops, self._settings.pitch))
        return self

    def tab_size(self: Self, size: int) -> Self:
        tab_stops = list(range(0, self.settings.pitch.max_character_position, size))
        return self.tab_stops(tab_stops)

    def text(self: Self, *text: Text) -> Self:
        """
        Write text.
        """

        self.write(self._character_encoder.encode(*text))

        return self

    @contextmanager
    def color(self: Self, color: Color) -> Generator[None, None, None]:
        """
        Write colored text.
        """

        self.write(set_color(color))

        yield

        self.write(set_color(Color.BLACK))

    @contextmanager
    def monospace(self: Self) -> Generator[None, None, None]:
        """
        Temporarily use a monospace (non-proportional) pitch.
        """

        pitch = self.settings.pitch

        monospace = {
            Pitch.PICA_PROPORTIONAL: Pitch.PICA,
            Pitch.ELITE_PROPORTIONAL: Pitch.ELITE,
        }.get(pitch, pitch)

        if monospace != pitch:
            self.pitch(monospace)

        yield

        if monospace != pitch:
            self.pitch(pitch)

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
    def strikeout(self: Self) -> Generator[None, None, None]:
        """
        Strike out text.
        """

        start = len(self)

        with self.monospace():
            yield

            self._strikeout(start)

    def _strikeout(self: Self, start: int) -> None:
        chars = 0
        for cmd in self._commands[start:]:
            chars += self._printable_characters(cmd)

        self._commands = [
            *(BACKSPACE for _ in range(0, chars)),
            *self._character_encoder.encode(" " * chars),
        ]

    def _printable_characters(self: Self, command: Command) -> int:
        raise NotImplementedError("Job._printable_characters")

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

    def code(self: Self, *text: Text) -> Self:
        """
        Write inline code.
        """

        with self.monospace():
            with self.color(Color.GREEN):
                self.text(*text)

        return self

    @contextmanager
    def code_block(self: Self) -> Generator[None, None, None]:
        """
        Write a code block.
        """

        with self.monospace():
            with self.color(Color.GREEN):
                yield
