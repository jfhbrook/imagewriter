from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

Format = str


class Inline:
    """
    Inline element.
    """

    pass


class Block:
    """
    Block element.
    """

    pass


# TODO: Is this a union type, like captions?
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
