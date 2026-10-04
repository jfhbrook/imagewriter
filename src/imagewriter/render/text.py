from collections.abc import Callable
from contextlib import AbstractContextManager, contextmanager
from typing import Generator, Self, Sequence

from imagewriter.base.character import Text
from imagewriter.base.color import Color
from imagewriter.base.language import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.quality import Quality
from imagewriter.base.settings import Settings
from imagewriter.base.units import Length
from imagewriter.encoding import (
    apply_settings,
    BACKSPACE,
    BackspaceLengthError,
    CarriageReturn,
    CarriageReturnLengthError,
    CharacterEncoder,
    CLEAR_ALL_TABS,
    Command,
    CR,
    cr_lf,
    LineFeed,
    LineFeedLengthError,
    Print,
    PRINT_SLASHED_ZERO,
    PRINT_UNSLASHED_ZERO,
    reset_tabs,
    set_language,
    SetColor,
    SetPitch,
    SetQuality,
    Space,
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
    TAB,
    TabLengthError,
    to_tab_stops,
)


class RichTextBuilder:
    """
    A builder for creating simple rich text documents.
    """

    def __init__(self: Self, settings: Settings) -> None:
        self._settings: Settings = settings
        self._character_encoder = CharacterEncoder(
            settings.language,
            map_mousetext=not settings.include_eighth_data_bit,
            map_custom=not settings.include_eighth_data_bit,
        )

        self._commands: list[Command] = list()

        # A header is a series of commands at the top of the document that
        # configures all settings. In cases where the header is already set,
        # we often write more targeted commands.
        self._has_header: bool = False

        # The ImageWriter II uses individual tab stops internally. But the renderer
        # supports setting those tab stops based on a consistent tab size. This field is
        self._tab_size: int | None = None

    #
    # Settings related functionality.
    #

    @property
    def settings(self: Self) -> Settings:
        """
        Print settings.
        """

        return self._settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        # Update and apply settings.
        self._update_settings(settings)
        self._apply_settings()

    def _update_settings(self: Self, settings: Settings) -> None:
        # Update internal settings and the character encoder accordingly.
        self._settings = settings
        self._character_encoder = CharacterEncoder(
            settings.language,
            map_mousetext=not settings.include_eighth_data_bit,
            map_custom=not settings.include_eighth_data_bit,
        )

    def _apply_settings(self: Self) -> None:
        # Write settings to commands.
        self._commands += [*apply_settings(self._settings), CR]

        # Applying settings implies a header.
        if not self._has_header:
            self._has_header = True

    def _write_header(self: Self) -> None:
        # Write the settings header, if it hasn't been written already.
        if not self._has_header:
            self._apply_settings()

    #
    # Tab settings.
    #

    def tab_stops(self: Self, tab_stops: Sequence[Length]) -> Self:
        """
        Set tab stops.
        """

        self._settings = Settings.replace(self._settings, tab_stops=tab_stops)

        if not self._has_header:
            # Tab stops are included in the header.
            self._write_header()
        else:
            # Otherwise, we just reset the tabs.
            self._commands += reset_tabs(to_tab_stops(tab_stops, self._settings.pitch))

        return self

    def tab_size(self: Self, size: int | None) -> Self:
        """
        Set the tab size by setting appropriate tab stops.
        """

        self._tab_size = size

        if size is None:
            # If no size is set, clear all tabs - this is the default behavior.
            self._commands.append(CLEAR_ALL_TABS)
        else:
            # If there is a size, generate tab stops and set them.
            tab_stops = list(range(0, self.settings.pitch.max_character_position, size))
            self.tab_stops(tab_stops)

        return self

    #
    # The basics.
    #

    def __len__(self: Self) -> int:
        """
        The number of staged commands.
        """

        return len(self._commands)

    def write(self: Self, commands: Command | str | list[Command]) -> Self:
        """
        Write raw commands.
        """

        # Write the header, if it hasn't already been written
        self._write_header()

        if isinstance(commands, Command):
            # Just a command!
            self._commands.append(commands)
        elif isinstance(commands, str):
            # Raw text!
            for c in commands.encode(encoding="ascii"):
                self._commands.append(Print(c.to_bytes(byteorder="big")))
        else:
            # A list of commands!
            self._commands += commands

        return self

    @property
    def commands(self: Self) -> list[Command]:
        """
        Rendered commands.
        """

        # Make sure the header has been written
        self._write_header()

        # Add a CR so the document flushes correctly
        self._commands.append(CR)

        commands = self._commands

        # Reset the commands, allowing the renderer to be reused.
        self._commands = list()

        return commands

    #
    # Language, pitch and quality.
    #

    @contextmanager
    def language(self: Self, language: Language) -> Generator[None, None, None]:
        """
        Use a given language.
        """

        self.write(set_language(language))

        yield

        self.write(set_language(self.settings.language))

    @contextmanager
    def pitch(self: Self, pitch: Pitch) -> Generator[None, None, None]:
        """
        Use a given pitch.
        """

        self.write(SetPitch(pitch))
        self.tab_size(self._tab_size)

        yield

        self.write(SetPitch(self.settings.pitch))
        self.tab_size(self._tab_size)

    @contextmanager
    def quality(self: Self, quality: Quality) -> Generator[None, None, None]:
        """
        Print at a given quality.
        """

        original_quality = self.settings.quality

        self.write(SetQuality(quality))

        yield

        self.write(SetQuality(original_quality))

    #
    # Whitespace management.
    #

    def trim(self: Self, count: int) -> Self:
        """
        Remove the last count commands.
        """

        self._write_header()

        self._commands = self._commands[:-count]
        return self

    def cr_lf(self: Self, count: int = 1) -> Self:
        """
        Write a CR and an LF.
        """

        self.write(cr_lf(count))
        return self

    def trim_cr_lf(self: Self, count: int = 1) -> Self:
        """
        Trim tailing CRFLs.
        """

        self._write_header()

        for _ in range(0, count):
            cr = self._commands[-1]
            lf = self._commands[-2]

            assert isinstance(cr, CarriageReturn)
            assert isinstance(lf, LineFeed)
            assert lf.lines == 1

            self.trim(2)

        return self

    def space(self: Self) -> Self:
        """
        Write a space.
        """
        self.write(Space())
        return self

    def trim_space(self: Self) -> Self:
        """
        Trim spaces.
        """

        self._write_header()

        assert isinstance(self._commands[-1], Space)
        self.trim(1)
        return self

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

        self.write(SetColor(color))

        yield

        self.write(SetColor(Color.BLACK))

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
        backspace_ct = 0

        for cmd in reversed(self._commands[start:]):
            try:
                backspace_ct += len(cmd)
            except BackspaceLengthError:
                backspace_ct -= 1
            except TabLengthError:
                if self._tab_size:
                    backspace_ct += self._tab_size
                else:
                    raise
            except (LineFeedLengthError, CarriageReturnLengthError) as exc:
                raise NotImplementedError(
                    "Strikeout is not implement across lines"
                ) from exc

        self._commands += [BACKSPACE for _ in range(0, backspace_ct)]

        for cmd in self._commands[start:]:
            try:
                self.write(Print(b"-" * len(cmd)))
            except BackspaceLengthError:
                pass
            except TabLengthError:
                self.write(TAB)

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

    @contextmanager
    def slashed_zero(self: Self) -> Generator[None, None, None]:
        """
        Print slashed zeroes.
        """

        slashed_zero = self.settings.slashed_zero

        if not slashed_zero:
            self._commands.append(PRINT_SLASHED_ZERO)

        yield

        if not slashed_zero:
            self._commands.append(PRINT_UNSLASHED_ZERO)

    @contextmanager
    def unslashed_zero(self: Self) -> Generator[None, None, None]:
        """
        Print unslashed zeroes.
        """

        slashed_zero = self.settings.slashed_zero

        if slashed_zero:
            self._commands.append(PRINT_UNSLASHED_ZERO)

        yield

        if slashed_zero:
            self._commands.append(PRINT_SLASHED_ZERO)

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

    @contextmanager
    def header(self: Self, level: int) -> Generator[None, None, None]:
        """
        Write a header.
        """

        header_methods = {1: self._header_1, 2: self._header_2}
        header_default = self._header_default(level)

        with header_methods.get(level, header_default)():
            yield

    def _header_default(
        self: Self, level: int
    ) -> Callable[[], AbstractContextManager[None]]:
        # A default header, if no specific header style is specified.
        @contextmanager
        def _default() -> Generator[None, None, None]:
            self.text("#" * level)
            self.space()

            yield

            self.cr_lf(2)

        return _default

    @contextmanager
    def _header_1(self: Self) -> Generator[None, None, None]:
        # A level 1 header. Printed in boldface and double width.
        with self.boldface():
            with self.double_width():
                self.text("#")
                self.space()

                yield

        self.cr_lf(2)

    @contextmanager
    def _header_2(self: Self) -> Generator[None, None, None]:
        # A level 2 header. Printed in boldface.
        with self.boldface():
            self.text("##")
            self.space()

            yield

        self.cr_lf(2)
