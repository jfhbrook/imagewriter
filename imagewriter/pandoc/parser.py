from typing import Any, Callable, Dict, List

from imagewriter.document import (
    Attr,
    Block,
    BlockQuote,
    BulletList,
    Code,
    CodeBlock,
    Document,
    Emph,
    Header,
    HorizontalRule,
    Inline,
    LineBlock,
    LineBreak,
    Link,
    ListAttributes,
    OrderedList,
    Para,
    Plain,
    RawBlock,
    RawInline,
    SmallCaps,
    SoftBreak,
    Space,
    Str,
    Strikeout,
    Strong,
    Subscript,
    Superscript,
    Target,
    Underline,
)


def parse_attr(contents: Any) -> Attr:
    return Attr(contents[0], contents[1], [(t[0], t[1]) for t in contents[2]])


def parse_target(contents: Any) -> Target:
    return Target(contents[0], contents[1])


InlineParser = Callable[[Any], Inline]


def unimplemented_inline_parser(name: str) -> InlineParser:
    def parser(contents: Any) -> Inline:
        raise NotImplementedError(name)

    return parser


def parse_code(contents: Any) -> Inline:
    return Code(parse_attr(contents[0]), contents[1])


def parse_emph(contents: Any) -> Inline:
    return Emph(parse_inline_list(contents))


def parse_line_break(contents: Any) -> Inline:
    return LineBreak()


def parse_link(contents: Any) -> Inline:
    return Link(
        parse_attr(contents[0]),
        parse_inline_list(contents[1]),
        parse_target(contents[2]),
    )


def parse_raw_inline(contents: Any) -> Inline:
    return RawInline(contents[0], contents[1])


def parse_small_caps(contents: Any) -> Inline:
    return SmallCaps(parse_inline_list(contents))


def parse_soft_break(contents: Any) -> Inline:
    return SoftBreak()


def parse_space(contents: Any) -> Inline:
    return Space()


def parse_str(contents: Any) -> Inline:
    return Str(contents)


def parse_strikeout(contents: Any) -> Inline:
    return Strikeout(parse_inline_list(contents))


def parse_strong(contents: Any) -> Inline:
    return Strong(parse_inline_list(contents))


def parse_superscript(contents: Any) -> Inline:
    return Superscript(parse_inline_list(contents))


def parse_subscript(contents: Any) -> Inline:
    return Subscript(parse_inline_list(contents))


def parse_underline(contents: Any) -> Inline:
    return Underline(parse_inline_list(contents))


INLINE_PARSERS: Dict[str, InlineParser] = {
    "Cite": unimplemented_inline_parser("Cite"),
    "Code": parse_code,
    "Emph": parse_emph,
    "Image": unimplemented_inline_parser("Image"),
    "LineBreak": parse_line_break,
    "Link": parse_link,
    "Math": unimplemented_inline_parser("Math"),
    "Note": unimplemented_inline_parser("Note"),
    "Quoted": unimplemented_inline_parser("Quoted"),
    "RawInline": parse_raw_inline,
    "SmallCaps": parse_small_caps,
    "SoftBreak": parse_soft_break,
    "Space": parse_space,
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


BlockParser = Callable[[Any], Block]


def unimplemented_block_parser(name: str) -> BlockParser:
    def parser(contents: Any) -> Block:
        raise NotImplementedError(name)

    return parser


def parse_plain(contents: Any) -> Block:
    return Plain(parse_inline_list(contents))


def parse_para(contents: Any) -> Block:
    return Para(parse_inline_list(contents))


def parse_line_block(contents: Any) -> Block:
    return LineBlock([parse_inline_list(inlines) for inlines in contents])


def parse_code_block(contents: Any) -> Block:
    return CodeBlock(parse_attr(contents[0]), contents[1])


def parse_raw_block(contents: Any) -> Block:
    return RawBlock(contents[0], contents[1])


def parse_block_quote(contents: Any) -> Block:
    return BlockQuote(parse_block_list(contents))


def parse_list_attributes(contents: Any) -> ListAttributes:
    return ListAttributes(contents[0], contents[1]["t"], contents[2]["t"])


def parse_ordered_list(contents: Any) -> Block:
    return OrderedList(
        parse_list_attributes(contents[0]),
        [parse_block_list(block_list) for block_list in contents[1]],
    )


def parse_bullet_list(contents: Any) -> Block:
    return BulletList([parse_block_list(item) for item in contents])


def parse_header(contents: Any) -> Block:
    return Header(contents[0], parse_attr(contents[1]), parse_inline_list(contents[2]))


def parse_horizontal_rule(contents: Any) -> Block:
    return HorizontalRule()


BLOCK_PARSERS: Dict[str, BlockParser] = {
    "Plain": parse_plain,
    "Para": parse_para,
    "LineBlock": parse_line_block,
    "CodeBlock": parse_code_block,
    "RawBlock": parse_raw_block,
    "BlockQuote": parse_block_quote,
    "OrderedList": parse_ordered_list,
    "BulletList": parse_bullet_list,
    "DefinitionList": unimplemented_block_parser("DefinitionList"),
    "Header": parse_header,
    "HorizontalRule": parse_horizontal_rule,
    "Table": unimplemented_block_parser("Table"),
    "Figure": unimplemented_block_parser("Figure"),
    "Div": unimplemented_block_parser("Div"),
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
