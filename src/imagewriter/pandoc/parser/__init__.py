from typing import Any, Callable, Dict, List, Optional, Self

from imagewriter.document import (
    Alignment,
    Block,
    BlockQuote,
    BulletList,
    Caption,
    Cell,
    Cite,
    Code,
    CodeBlock,
    ColSpec,
    DefinitionList,
    DefinitionListItem,
    Div,
    Document,
    Emph,
    Figure,
    Header,
    HorizontalRule,
    Image,
    Inline,
    LineBlock,
    LineBreak,
    Link,
    ListAttributes,
    Math,
    Note,
    OrderedList,
    Para,
    Plain,
    Quoted,
    RawBlock,
    RawInline,
    Row,
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
    TableBody,
    TableFoot,
    TableHead,
    Underline,
)
from imagewriter.pandoc.parser.attr import parse_attr
from imagewriter.pandoc.parser.citation import parse_citation
from imagewriter.pandoc.parser.link import parse_target
from imagewriter.pandoc.parser.math import parse_math_type
from imagewriter.pandoc.parser.quote import parse_quote_type

BlockParser = Callable[[Any], Block]
InlineParser = Callable[[Any], Inline]

# Caption


def parse_caption(contents: Any) -> Caption:
    return Caption(
        short=parse_inline_list(contents[0]) if contents[0] is not None else None,
        contents=parse_block_list(contents[1]),
    )


# Inline


def parse_cite(contents: Any) -> Inline:
    return Cite(
        citations=[parse_citation(cont) for cont in contents[0]],
        contents=parse_inline_list(contents[1]),
    )


def parse_code(contents: Any) -> Inline:
    return Code(attr=parse_attr(contents[0]), contents=contents[1])


def parse_emph(contents: Any) -> Inline:
    return Emph(contents=parse_inline_list(contents))


def parse_line_break(contents: Any) -> Inline:
    return LineBreak()


def parse_link(contents: Any) -> Inline:
    return Link(
        attr=parse_attr(contents[0]),
        alt_text=parse_inline_list(contents[1]),
        target=parse_target(contents[2]),
    )


def parse_raw_inline(contents: Any) -> Inline:
    return RawInline(format=contents[0], contents=contents[1])


def parse_small_caps(contents: Any) -> Inline:
    return SmallCaps(contents=parse_inline_list(contents))


def parse_soft_break(contents: Any) -> Inline:
    return SoftBreak()


def parse_space(contents: Any) -> Inline:
    return Space()


def parse_str(contents: Any) -> Inline:
    return Str(contents=contents)


def parse_strikeout(contents: Any) -> Inline:
    return Strikeout(contents=parse_inline_list(contents))


def parse_strong(contents: Any) -> Inline:
    return Strong(contents=parse_inline_list(contents))


def parse_superscript(contents: Any) -> Inline:
    return Superscript(contents=parse_inline_list(contents))


def parse_subscript(contents: Any) -> Inline:
    return Subscript(contents=parse_inline_list(contents))


def parse_underline(contents: Any) -> Inline:
    return Underline(contents=parse_inline_list(contents))


def parse_image(contents: Any) -> Inline:
    return Image(
        attr=parse_attr(contents[0]),
        alt_text=parse_inline_list(contents[1]),
        target=parse_target(contents[2]),
    )


def parse_math(contents: Any) -> Inline:
    return Math(math_type=parse_math_type(contents[0]), contents=contents[1])


def parse_note(contents: Any) -> Inline:
    return Note(contents=parse_block_list(contents))


def parse_quoted(contents: Any) -> Inline:
    return Quoted(
        quote_type=parse_quote_type(contents[0]),
        contents=parse_inline_list(contents[1]),
    )


def parse_span(contents: Any) -> Inline:
    return Span(attr=parse_attr(contents[0]), contents=parse_inline_list(contents[1]))


INLINE_PARSERS: Dict[str, InlineParser] = {
    "Cite": parse_cite,
    "Code": parse_code,
    "Emph": parse_emph,
    "Image": parse_image,
    "LineBreak": parse_line_break,
    "Link": parse_link,
    "Math": parse_math,
    "Note": parse_note,
    "Quoted": parse_quoted,
    "RawInline": parse_raw_inline,
    "SmallCaps": parse_small_caps,
    "SoftBreak": parse_soft_break,
    "Space": parse_space,
    "Span": parse_span,
    "Str": parse_str,
    "Strikeout": parse_strikeout,
    "Strong": parse_strong,
    "Subscript": parse_subscript,
    "Superscript": parse_superscript,
    "Underline": parse_underline,
}


def parse_inline(contents: Any) -> Inline:
    return INLINE_PARSERS[contents["t"]](contents.get("c", None))


def parse_inline_list(contents: List[Any]) -> List[Inline]:
    return [parse_inline(inline) for inline in contents]


# Block


def parse_plain(contents: Any) -> Block:
    return Plain(contents=parse_inline_list(contents))


def parse_para(contents: Any) -> Block:
    return Para(contents=parse_inline_list(contents))


def parse_line_block(contents: Any) -> Block:
    return LineBlock(contents=[parse_inline_list(inlines) for inlines in contents])


def parse_code_block(contents: Any) -> Block:
    return CodeBlock(attr=parse_attr(contents[0]), contents=contents[1])


def parse_raw_block(contents: Any) -> Block:
    return RawBlock(format=contents[0], contents=contents[1])


def parse_block_quote(contents: Any) -> Block:
    return BlockQuote(contents=parse_block_list(contents))


def parse_list_attributes(contents: Any) -> ListAttributes:
    return ListAttributes(
        start=contents[0], style=contents[1]["t"], delimiter=contents[2]["t"]
    )


def parse_ordered_list(contents: Any) -> Block:
    return OrderedList(
        attrs=parse_list_attributes(contents[0]),
        items=[parse_block_list(block_list) for block_list in contents[1]],
    )


def parse_bullet_list(contents: Any) -> Block:
    return BulletList(items=[parse_block_list(item) for item in contents])


class DefinitionListParser:
    def __call__(self: Self, contents: Any) -> Block:
        return DefinitionList(items=[self.item(cont) for cont in contents])

    def item(self: Self, contents: Any) -> DefinitionListItem:
        return DefinitionListItem(
            term=parse_inline_list(contents[0]),
            definitions=[parse_block_list(cont) for cont in contents[1]],
        )


parse_definition_list = DefinitionListParser()


def parse_header(contents: Any) -> Block:
    return Header(
        level=contents[0],
        attr=parse_attr(contents[1]),
        contents=parse_inline_list(contents[2]),
    )


def parse_horizontal_rule(contents: Any) -> Block:
    return HorizontalRule()


class TableParser:
    def __call__(self: Self, contents: Any) -> Block:
        return Table(
            attr=parse_attr(contents[0]),
            caption=parse_caption(contents[1]),
            columns=[self.col_spec(cont) for cont in contents[2]],
            header=self.header(contents[3]),
            body=[self.body(cont) for cont in contents[4]],
            footer=self.footer(contents[5]),
        )

    def alignment(self: Self, contents: Any) -> Alignment:
        return contents["t"]

    def col_width(self: Self, contents: Any) -> Optional[float]:
        if contents["t"] == "ColWidth":
            return contents["c"]
        return None

    def col_spec(self: Self, contents: Any) -> ColSpec:
        return ColSpec(
            alignment=self.alignment(contents[0]), width=self.col_width(contents[1])
        )

    def cell(self: Self, contents: Any) -> Cell:
        return Cell(
            attr=parse_attr(contents[0]),
            alignment=self.alignment(contents[1]),
            row_span=contents[2],
            column_span=contents[3],
            contents=parse_block_list(contents[4]),
        )

    def row(self: Self, contents: Any) -> Row:
        return Row(
            attr=parse_attr(contents[0]),
            contents=[self.cell(cont) for cont in contents[1]],
        )

    def header(self: Self, contents: Any) -> TableHead:
        return TableHead(
            attr=parse_attr(contents[0]), rows=[self.row(cont) for cont in contents[1]]
        )

    def body(self: Self, contents: Any) -> TableBody:
        return TableBody(
            attr=parse_attr(contents[0]),
            row_header_columns=contents[1],
            row_header=[self.row(cont) for cont in contents[2]],
            body=[self.row(cont) for cont in contents[3]],
        )

    def footer(self: Self, contents: Any) -> TableFoot:
        return TableFoot(
            attr=parse_attr(contents[0]), rows=[self.row(cont) for cont in contents[1]]
        )


parse_table = TableParser()


def parse_figure(contents: Any) -> Figure:
    return Figure(
        attr=parse_attr(contents[0]),
        caption=parse_caption(contents[1]),
        contents=parse_block_list(contents[2]),
    )


def parse_div(contents: Any) -> Block:
    return Div(attr=parse_attr(contents[0]), contents=parse_block_list(contents[1]))


BLOCK_PARSERS: Dict[str, BlockParser] = {
    "Plain": parse_plain,
    "Para": parse_para,
    "LineBlock": parse_line_block,
    "CodeBlock": parse_code_block,
    "RawBlock": parse_raw_block,
    "BlockQuote": parse_block_quote,
    "OrderedList": parse_ordered_list,
    "BulletList": parse_bullet_list,
    "DefinitionList": parse_definition_list,
    "Header": parse_header,
    "HorizontalRule": parse_horizontal_rule,
    "Table": parse_table,
    "Figure": parse_figure,
    "Div": parse_div,
}


def parse_block(contents: Any) -> Block:
    return BLOCK_PARSERS[contents["t"]](contents.get("c", None))


def parse_block_list(contents: List[Any]) -> List[Block]:
    return [parse_block(block) for block in contents]


def parse_document(contents: Any) -> Document:
    return Document(
        pandoc_api_version=contents.get("pandoc-api-version"),
        meta=contents.get("meta"),
        blocks=parse_block_list(contents["blocks"]),
    )
