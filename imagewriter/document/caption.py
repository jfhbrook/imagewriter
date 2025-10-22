from dataclasses import dataclass
from typing import List, Optional

from imagewriter.document.base import Block, Inline


@dataclass
class Caption:
    """
    The caption of a table or figure.
    """

    short: Optional[List[Inline]]
    contents: List[Block]
