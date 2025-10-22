from typing import Self

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
        raise NotImplementedError("visit_strikeout")

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
        raise NotImplementedError("visit_code")

    def visit_space(self: Self, element: Space) -> None:
        self.job.text(" ")

    def visit_soft_break(self: Self, element: SoftBreak) -> None:
        self.job.text("\r\n")

    def visit_line_break(self: Self, element: LineBreak) -> None:
        self.job.text("\r\n")

    def visit_math(self: Self, element: Math) -> None:
        raise NotImplementedError("visit_math")

    def visit_raw_inline(self: Self, element: RawInline) -> None:
        raise NotImplementedError("visit_raw_inline")

    def visit_link(self: Self, element: Link) -> None:
        raise NotImplementedError("visit_link")

    def visit_image(self: Self, element: Image) -> None:
        raise NotImplementedError("visit_image")

    def visit_note(self: Self, element: Note) -> None:
        raise NotImplementedError("visit_note")

    def visit_span(self: Self, element: Span) -> None:
        # TODO: What attributes may a span have?
        for el in element.contents:
            el.accept(self)

    def visit_plain(self: Self, element: Plain) -> None:
        pass

    def visit_para(self: Self, element: Para) -> None:
        pass

    def visit_line_block(self: Self, element: LineBlock) -> None:
        pass

    def visit_code_block(self: Self, element: CodeBlock) -> None:
        pass

    def visit_raw_block(self: Self, element: RawBlock) -> None:
        pass

    def visit_block_quote(self: Self, element: BlockQuote) -> None:
        pass

    def visit_ordered_list(self: Self, element: OrderedList) -> None:
        pass

    def visit_bullet_list(self: Self, element: BulletList) -> None:
        pass

    def visit_definition_list(self: Self, element: DefinitionList) -> None:
        pass

    def visit_header(self: Self, element: Header) -> None:
        pass

    def visit_horizontal_rule(self: Self, element: HorizontalRule) -> None:
        pass

    def visit_table(self: Self, element: Table) -> None:
        pass

    def visit_figure(self: Self, element: Figure) -> None:
        pass

    def visit_div(self: Self, element: Div) -> None:
        pass
