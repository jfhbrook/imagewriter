from dataclasses import dataclass
from typing import List

from imagewriter.document.base import (
    Attr,
    Block,
    Format,
    Inline,
    MathType,
    QuoteType,
)
from imagewriter.document.citation import Citation
from imagewriter.document.link import Target


@dataclass
class Str(Inline):
    """
    str.
    """

    contents: str


@dataclass
class Emph(Inline):
    """
    Emphasized text.
    """

    contents: List[Inline]


@dataclass
class Underline(Inline):
    """
    Underlined text.
    """

    contents: List[Inline]


@dataclass
class Strong(Inline):
    """
    Strongly emphasized text.
    """

    contents: List[Inline]


@dataclass
class Strikeout(Inline):
    """
    Strikeout text.
    """

    contents: List[Inline]


@dataclass
class Subscript(Inline):
    """
    Subscripted text.
    """

    contents: List[Inline]


@dataclass
class Superscript(Inline):
    """
    Superscripted text.
    """

    contents: List[Inline]


@dataclass
class SmallCaps(Inline):
    """
    Small caps text.
    """

    contents: List[Inline]


@dataclass
class Quoted(Inline):
    """
    Quoted text.
    """

    quote_type: QuoteType
    contents: List[Inline]


@dataclass
class Cite(Inline):
    """
    Citation.
    """

    citation: Citation
    contents: List[Inline]


@dataclass
class Code(Inline):
    """
    Inline code.
    """

    attr: Attr
    contents: str


@dataclass
class Space(Inline):
    """
    Inter-word space.
    """

    pass


@dataclass
class SoftBreak(Inline):
    """
    Soft line break.
    """

    pass


@dataclass
class LineBreak(Inline):
    """
    Hard line break.
    """

    pass


@dataclass
class Math(Inline):
    """
    TeX math (literal).
    """

    math_type: MathType
    contents: str


@dataclass
class RawInline(Inline):
    """
    Raw inline.
    """

    format: Format
    contents: str


@dataclass
class Link(Inline):
    """
    Hyperlink.
    """

    attr: Attr
    alt_text: List[Inline]
    target: Target


@dataclass
class Image(Inline):
    """
    Image.
    """

    attr: Attr
    alt_text: List[Inline]
    target: Target


@dataclass
class Note(Inline):
    """
    Footnote or endnote.
    """

    contents: List[Block]
