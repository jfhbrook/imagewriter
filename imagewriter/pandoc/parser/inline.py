from typing import Any, Callable, Dict, List

from imagewriter.document import (  # Note,
    Cite,
    Code,
    Emph,
    Image,
    Inline,
    LineBreak,
    Link,
    Math,
    Quoted,
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
    Underline,
)
from imagewriter.pandoc.parser.base import parse_attr
from imagewriter.pandoc.parser.citation import parse_citation
from imagewriter.pandoc.parser.link import parse_target
from imagewriter.pandoc.parser.math import parse_math_type
from imagewriter.pandoc.parser.quote import parse_quote_type

InlineParser = Callable[[Any], Inline]


def parse_cite(contents: Any) -> Inline:
    return Cite(
        [parse_citation(cont) for cont in contents[0]], parse_inline_list(contents[1])
    )


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


def parse_image(contents: Any) -> Inline:
    return Image(
        parse_attr(contents[0]),
        parse_inline_list(contents[1]),
        parse_target(contents[2]),
    )


def parse_math(contents: Any) -> Inline:
    return Math(parse_math_type(contents[0]), contents[1])


def parse_note(contents: Any) -> Inline:
    # return Note(parse_block_list(contents))
    raise NotImplementedError("Note")


def parse_quoted(contents: Any) -> Inline:
    return Quoted(parse_quote_type(contents[0]), parse_inline_list(contents[1]))


def parse_span(contents: Any) -> Inline:
    return Span(parse_attr(contents[0]), parse_inline_list(contents[1]))


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
