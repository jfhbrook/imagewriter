from typing import Self

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
from imagewriter.encoding import CR, LF
from imagewriter.job import Job


class DocumentRenderer(BlockVisitor[None], InlineVisitor[None]):
    def __self__(self: Self, job: Job) -> None:
        self.job: Job = job

    def visit_str(self: Self, element: Str) -> None:
        self.job.text(element.contents)

    def visit_emph(self: Self, element: Emph) -> None:
        with self.job.boldface():
            for el in element.contents:
                el.accept(self)

    def visit_underline(self: Self, element: Underline) -> None:
        with self.job.underline():
            for el in element.contents:
                el.accept(self)

    def visit_strong(self: Self, element: Strong) -> None:
        with self.job.double_width():
            with self.job.boldface():
                for el in element.contents:
                    el.accept(self)

    def visit_strikeout(self: Self, element: Strikeout) -> None:
        with self.job.strikeout():
            for el in element.contents:
                el.accept(self)

    def visit_subscript(self: Self, element: Subscript) -> None:
        with self.job.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_superscript(self: Self, element: Superscript) -> None:
        with self.job.subscript():
            for el in element.contents:
                el.accept(self)

    def visit_small_caps(self: Self, element: SmallCaps) -> None:
        raise NotImplementedError("visit_small_caps")

    def visit_quoted(self: Self, element: Quoted) -> None:
        raise NotImplementedError("visit_quoted")

    def visit_cite(self: Self, element: Cite) -> None:
        raise NotImplementedError("visit_cite")

    def visit_code(self: Self, element: Code) -> None:
        self.job.code(element.contents)

    def visit_space(self: Self, element: Space) -> None:
        self.job.text(" ")

    def visit_soft_break(self: Self, element: SoftBreak) -> None:
        # TODO: What is a soft break?
        self.job.write([CR, LF])

    def visit_line_break(self: Self, element: LineBreak) -> None:
        self.job.write([CR, LF])

    def visit_math(self: Self, element: Math) -> None:
        raise NotImplementedError("visit_math")

    def visit_raw_inline(self: Self, element: RawInline) -> None:
        raise NotImplementedError("visit_raw_inline")

    def visit_link(self: Self, element: Link) -> None:
        # TODO: What attributes may a link have?
        with self.job.color(Color.PURPLE):
            self.job.text(element.target.title)

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

        self.job.write([CR, LF, CR, LF])

    def visit_line_block(self: Self, element: LineBlock) -> None:
        for line in element.contents:
            for el in line:
                el.accept(self)
            self.job.write([CR, LF])

    def visit_code_block(self: Self, element: CodeBlock) -> None:
        with self.job.code_block():
            self.job.text(element.contents)

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
        self.job.write([CR, LF, CR, LF])
        self.job.text("---")
        self.job.write([CR, LF, CR, LF])

    def visit_table(self: Self, element: Table) -> None:
        raise NotImplementedError("visit_table")

    def visit_figure(self: Self, element: Figure) -> None:
        raise NotImplementedError("visit_figure")

    def visit_div(self: Self, element: Div) -> None:
        # TODO: What attrs can a div have?
        for el in element.contents:
            el.accept(self)
