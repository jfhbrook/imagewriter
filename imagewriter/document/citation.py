from dataclasses import dataclass
from enum import Enum
from typing import List

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


class CitationMode(Enum, Citation):
    AUTHOR_IN_TEXT = 0
    SUPPRESS_AUTHOR = 1
    NORMAL = 2


@dataclass
class CitationNoteNum(Citation):
    number: int


@dataclass
class CitationHash(Citation):
    hash: int
