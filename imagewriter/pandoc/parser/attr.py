from typing import Any

from imagewriter.document import Attr


def parse_attr(contents: Any) -> Attr:
    return Attr(contents[0], contents[1], [(t[0], t[1]) for t in contents[2]])
