from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Self, Tuple

Format = str


class Inline(ABC):
    """
    Inline element.
    """

    # TODO: This typing is loose to decouple these types from their
    # definitions. If we combine block and inline into __init__, we should be
    # able to tighten these types significantly.
    @abstractmethod
    def accept(self: Self, visitor: Any) -> Any:
        pass


class Block(ABC):
    """
    Block element.
    """

    @abstractmethod
    def accept(self: Self, visitor: Any) -> Any:
        pass


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str
    classes: List[str]
    pairs: List[Tuple[str, str]]


@dataclass
class Document:
    blocks: List[Block]
    pandoc_api_version: Optional[List[int]] = None
    meta: Optional[Dict[str, Any]] = None
