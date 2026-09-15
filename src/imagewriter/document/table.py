from dataclasses import dataclass
from typing import Literal, Optional

Alignment = (
    Literal["AlignLeft"]
    | Literal["AlignRight"]
    | Literal["AlignCenter"]
    | Literal["AlignDefault"]
)


@dataclass
class ColSpec:
    """
    The specification for a single table column.
    """

    alignment: Alignment
    width: Optional[float]
