from contextlib import contextmanager
from typing import Generator, List, Optional, Self, Sequence

from imagewriter.character import Text
from imagewriter.color import Color
from imagewriter.document import (
    BlockQuote,
    BlockVisitor,
    BulletList,
    Cite,
    Code,
    CodeBlock,
    DefinitionList,
    Div,
    Document,
    Emph,
    Figure,
    Header,
    HorizontalRule,
    Image,
    InlineVisitor,
    LineBlock,
    LineBreak,
    Link,
    Math,
    Note,
    OrderedList,
    Para,
    Plain,
    Quoted,
    RawBlock,
    RawInline,
    SmallCaps,
    SoftBreak,
    Space,
    Span,
    Str,
    Strikeout,
    Strong,
    Subscript,
    Superscript,
    Table,
    Underline,
)
from imagewriter.encoding import (
    apply_settings,
    BACKSPACE,
    BackspaceLengthError,
    CarriageReturnLengthError,
    CharacterEncoder,
    Command,
    CR,
    LF,
    LineFeedLengthError,
    Print,
    reset_tabs,
    SetColor,
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
    TAB,
    TabLengthError,
    to_tab_stops,
)
from imagewriter.pitch import Pitch
from imagewriter.settings import Settings
from imagewriter.units import Length


class DocumentVisitor(BlockVisitor[None], InlineVisitor[None]):
    def __init__(self: Self, renderer: "DocumentRenderer") -> None:
        self.renderer: "DocumentRenderer" = renderer

    def visit_str(self: Self, element: Str) -> None:
        self.renderer.text(element.contents)

    def visit_emph(self: Self, element: Emph) -> None:
        with self.renderer.boldface():
            for el in element.contents:
                el.accept(self)

    def visit_underline(self: Self, element: Underline) -> None:
        with self.renderer.underline():
            for el in element.contents:
                el.accept(self)

    def visit_strong(self: Self, element: Strong) -> None:
        with self.renderer.double_width():
            with self.renderer.boldface():
                for el in element.contents:
                    el.accept(self)

    def visit_strikeout(self: Self, element: Strikeout) -> None:
        with self.renderer.strikeout():
            for el in element.contents:
                el.accept(self)

    def visit_subscript(self: Self, element: Subscript) -> None:
        with self.renderer.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_superscript(self: Self, element: Superscript) -> None:
        with self.renderer.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_small_caps(self: Self, element: SmallCaps) -> None:
        raise NotImplementedError("visit_small_caps")

    def visit_quoted(self: Self, element: Quoted) -> None:
        raise NotImplementedError("visit_quoted")

    def visit_cite(self: Self, element: Cite) -> None:
        raise NotImplementedError("visit_cite")

    def visit_code(self: Self, element: Code) -> None:
        self.renderer.code(element.contents)

    def visit_space(self: Self, element: Space) -> None:
        self.renderer.text(" ")

    def visit_soft_break(self: Self, element: SoftBreak) -> None:
        # TODO: What is a soft break?
        self.renderer.write([CR, LF])

    def visit_line_break(self: Self, element: LineBreak) -> None:
        self.renderer.write([CR, LF])

    def visit_math(self: Self, element: Math) -> None:
        raise NotImplementedError("visit_math")

    def visit_raw_inline(self: Self, element: RawInline) -> None:
        raise NotImplementedError("visit_raw_inline")

    def visit_link(self: Self, element: Link) -> None:
        # TODO: What attributes may a link have?
        with self.renderer.color(Color.PURPLE):
            for el in element.alt_text:
                el.accept(self)

    def visit_image(self: Self, element: Image) -> None:
        raise NotImplementedError("visit_image")

    def visit_note(self: Self, element: Note) -> None:
        raise NotImplementedError("visit_note")

    def visit_span(self: Self, element: Span) -> None:
        # TODO: What attributes may a span have?
        for el in element.contents:
            el.accept(self)

    def visit_plain(self: Self, element: Plain) -> None:
        for el in element.contents:
            el.accept(self)

    def visit_para(self: Self, element: Para) -> None:
        for el in element.contents:
            el.accept(self)

        self.renderer.write([CR, LF, CR, LF])

    def visit_line_block(self: Self, element: LineBlock) -> None:
        for line in element.contents:
            for el in line:
                el.accept(self)
            self.renderer.write([CR, LF])

    def visit_code_block(self: Self, element: CodeBlock) -> None:
        with self.renderer.code_block():
            self.renderer.text(element.contents)

    def visit_raw_block(self: Self, element: RawBlock) -> None:
        raise NotImplementedError("visit_raw_block")

    def visit_block_quote(self: Self, element: BlockQuote) -> None:
        # TODO: Implement context manager block quote
        raise NotImplementedError("visit_block_quote")

    def visit_ordered_list(self: Self, element: OrderedList) -> None:
        raise NotImplementedError("visit_ordered_list")

    def visit_bullet_list(self: Self, element: BulletList) -> None:
        raise NotImplementedError("visit_bullet_list")

    def visit_definition_list(self: Self, element: DefinitionList) -> None:
        raise NotImplementedError("visit_definition_list")

    def visit_header(self: Self, element: Header) -> None:
        raise NotImplementedError("visit_header")

    def visit_horizontal_rule(self: Self, element: HorizontalRule) -> None:
        # TODO: Something nicer
        self.renderer.write([CR, LF, CR, LF])
        self.renderer.text("---")
        self.renderer.write([CR, LF, CR, LF])

    def visit_table(self: Self, element: Table) -> None:
        raise NotImplementedError("visit_table")

    def visit_figure(self: Self, element: Figure) -> None:
        raise NotImplementedError("visit_figure")

    def visit_div(self: Self, element: Div) -> None:
        # TODO: What attrs can a div have?
        for el in element.contents:
            el.accept(self)


class DocumentRenderer:
    def __init__(self: Self, settings: Settings) -> None:
        self._settings: Settings = settings
        self._character_encoder = CharacterEncoder(
            settings.language,
            map_mousetext=not settings.include_eighth_data_bit,
            map_custom=not settings.include_eighth_data_bit,
        )
        self._has_header: bool = False
        self._commands: List[Command] = list()
        self._tab_size: Optional[int] = None

    def render(self: Self, document: Document) -> List[Command]:
        visitor = DocumentVisitor(self)
        for block in document.blocks:
            block.accept(visitor)

        return self.commands

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

    def write(self: Self, commands: Command | str | List[Command]) -> Self:
        """
        Write raw commands.
        """

        self._write_header()
        if isinstance(commands, Command):
            self._commands.append(commands)
        elif isinstance(commands, str):
            for c in commands.encode(encoding="ascii"):
                self._commands.append(Print(c.to_bytes(byteorder="big")))
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
            self._commands.append(SetPitch(pitch))

            if self._tab_size:
                self.tab_size(self._tab_size)
            else:
                self.tab_stops(self.settings.tab_stops)

        return self

    def tab_stops(self: Self, tab_stops: Sequence[Length]) -> Self:
        """
        Set the current tab stops.
        """
        self._tab_size = None

        self._settings = Settings.replace(self._settings, tab_stops=tab_stops)

        if self._has_header:
            self._commands += reset_tabs(to_tab_stops(tab_stops, self._settings.pitch))
        return self

    def tab_size(self: Self, size: int) -> Self:
        tab_stops = list(range(0, self.settings.pitch.max_character_position, size))
        self.tab_stops(tab_stops)
        self._tab_size = size
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
                raise
            except (LineFeedLengthError, CarriageReturnLengthError) as exc:
                raise NotImplementedError(
                    "Strikeout is not implement across lines"
                ) from exc

        self._commands += [BACKSPACE for _ in range(0, backspace_ct)]

        for cmd in self._commands[start:]:
            try:
                self._commands.append(Print(b"-" * len(cmd)))
            except BackspaceLengthError:
                pass
            except TabLengthError:
                self._commands.append(TAB)

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
