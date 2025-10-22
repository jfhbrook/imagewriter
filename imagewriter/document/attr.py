from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str
    classes: List[str]
    pairs: List[Tuple[str, str]]
