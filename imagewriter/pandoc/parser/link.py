from typing import Any

from imagewriter.document import Target


def parse_target(contents: Any) -> Target:
    return Target(contents[0], contents[1])
