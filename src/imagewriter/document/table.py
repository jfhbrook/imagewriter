from dataclasses import dataclass
from typing import Literal

Alignment = Literal["AlignLeft", "AlignRight", "AlignCenter", "AlignDefault"]


@dataclass
class ColSpec:
    """
    The specification for a single table column.
    """

    alignment: Alignment
    width: float | None
