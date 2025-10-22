from dataclasses import dataclass
from typing import List, Tuple

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


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str
    classes: List[str]
    pairs: List[Tuple[str, str]]
