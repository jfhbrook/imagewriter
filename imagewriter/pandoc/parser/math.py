from typing import Any

from imagewriter.document import MathType


def parse_math_type(contents: Any) -> MathType:
    return contents["t"]
