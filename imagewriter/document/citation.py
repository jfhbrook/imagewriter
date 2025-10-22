from dataclasses import dataclass
from typing import List, Literal

from imagewriter.document.base import Inline


class Citation:
    pass


@dataclass
class CitationId(Citation):
    id: str


@dataclass
class CitationPrefix(Citation):
    prefix: List[Inline]


@dataclass
class CitationSuffix(Citation):
    suffix: List[Inline]


CitationModeType = (
    Literal["AuthorInText"] | Literal["SuppressAuthor"] | Literal["NormalCitation"]
)

AUTHOR_IN_TEXT: CitationModeType = "AuthorInText"
SUPPRESS_AUTHOR: CitationModeType = "SuppressAuthor"
NORMAL_CITATION: CitationModeType = "NormalCitation"


@dataclass
class CitationMode(Citation):
    mode: CitationModeType


@dataclass
class CitationNoteNum(Citation):
    number: int


@dataclass
class CitationHash(Citation):
    hash: int
