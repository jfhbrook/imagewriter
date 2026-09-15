from typing import List, Self

from imagewriter.color import Color
from imagewriter.document import (
    Block,
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
from imagewriter.encoding import Command, cr_lf
from imagewriter.render.text import RichTextBuilder
from imagewriter.settings import Settings


class DocumentRenderer(BlockVisitor[None], InlineVisitor[None]):
    def __init__(self: Self, settings: Settings) -> None:
        self.builder: RichTextBuilder = RichTextBuilder(settings)

    def render(self: Self, document: Document) -> List[Command]:
        for block in document.blocks:
            block.accept(self)

        self.trim(document.blocks)

        return self.builder.commands

    def trim(self: Self, blocks: List[Block]) -> None:
        for block in reversed(blocks):
            if isinstance(block, Space):
                self.builder.trim_space()
            elif isinstance(block, LineBreak) or isinstance(block, SoftBreak):
                self.builder.trim_cr_lf()
            elif isinstance(block, Para) or isinstance(block, HorizontalRule):
                self.builder.trim_cr_lf(2)
            else:
                break

    def visit_str(self: Self, element: Str) -> None:
        self.builder.text(element.contents)

    def visit_emph(self: Self, element: Emph) -> None:
        with self.builder.boldface():
            for el in element.contents:
                el.accept(self)

    def visit_underline(self: Self, element: Underline) -> None:
        with self.builder.underline():
            for el in element.contents:
                el.accept(self)

    def visit_strong(self: Self, element: Strong) -> None:
        with self.builder.double_width():
            with self.builder.boldface():
                for el in element.contents:
                    el.accept(self)

    def visit_strikeout(self: Self, element: Strikeout) -> None:
        with self.builder.strikeout():
            for el in element.contents:
                el.accept(self)

    def visit_subscript(self: Self, element: Subscript) -> None:
        with self.builder.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_superscript(self: Self, element: Superscript) -> None:
        with self.builder.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_small_caps(self: Self, element: SmallCaps) -> None:
        raise NotImplementedError("visit_small_caps")

    def visit_quoted(self: Self, element: Quoted) -> None:
        raise NotImplementedError("visit_quoted")

    def visit_cite(self: Self, element: Cite) -> None:
        raise NotImplementedError("visit_cite")

    def visit_code(self: Self, element: Code) -> None:
        self.builder.code(element.contents)

    def visit_space(self: Self, element: Space) -> None:
        self.builder.space()

    def visit_soft_break(self: Self, element: SoftBreak) -> None:
        # TODO: What is a soft break?
        self.builder.cr_lf()

    def visit_line_break(self: Self, element: LineBreak) -> None:
        self.builder.cr_lf()

    def visit_math(self: Self, element: Math) -> None:
        raise NotImplementedError("visit_math")

    def visit_raw_inline(self: Self, element: RawInline) -> None:
        raise NotImplementedError("visit_raw_inline")

    def visit_link(self: Self, element: Link) -> None:
        # TODO: What attributes may a link have?
        with self.builder.color(Color.PURPLE):
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

        self.builder.write(cr_lf(2))

    def visit_line_block(self: Self, element: LineBlock) -> None:
        for line in element.contents:
            for el in line:
                el.accept(self)
            self.builder.write(cr_lf())

    def visit_code_block(self: Self, element: CodeBlock) -> None:
        with self.builder.code_block():
            self.builder.text(element.contents)

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
        if element.level == 1:
            self._header_1(element)
        elif element.level == 2:
            self._header_2(element)
        elif element.level == 3:
            self._header_3(element)
        elif element.level == 4:
            self._header_4(element)
        else:
            raise NotImplementedError(f"Headers at level {element.level}")

    def _header_1(self: Self, element: Header) -> None:
        with self.builder.boldface():
            with self.builder.double_width():
                self.builder.text("#")
                self.builder.space()
                for el in element.contents:
                    el.accept(self)
        self.builder.cr_lf(2)

    def _header_2(self: Self, element: Header) -> None:
        with self.builder.boldface():
            self.builder.text("##")
            self.builder.space()
            for el in element.contents:
                el.accept(self)
        self.builder.cr_lf(2)

    def _header_3(self: Self, element: Header) -> None:
        self.builder.text("###")
        self.builder.space()
        for el in element.contents:
            el.accept(self)
        self.builder.cr_lf(2)

    def _header_4(self: Self, element: Header) -> None:
        self.builder.text("####")
        self.builder.space()
        for el in element.contents:
            el.accept(self)
        self.builder.cr_lf(2)

    def visit_horizontal_rule(self: Self, element: HorizontalRule) -> None:
        # TODO: Something nicer
        self.builder.write(cr_lf(2))
        self.builder.text("---")
        self.builder.write(cr_lf(2))

    def visit_table(self: Self, element: Table) -> None:
        raise NotImplementedError("visit_table")

    def visit_figure(self: Self, element: Figure) -> None:
        raise NotImplementedError("visit_figure")

    def visit_div(self: Self, element: Div) -> None:
        # TODO: What attrs can a div have?
        for el in element.contents:
            el.accept(self)
