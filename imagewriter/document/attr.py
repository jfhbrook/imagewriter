from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str = ""
    classes: List[str] = field(default_factory=list)
    pairs: List[Tuple[str, str]] = field(default_factory=list)
