from collections.abc import Generator
from typing import Any

from parsy import Parser, alt, any_char, generate  # type: ignore

from imagewriter.decoding.base import esc, number
from imagewriter.encoding.graphics import PrintGraphicsData

_start_uint64_data = esc("g") >> number(3).map(lambda n: n * 8)
_start_bytes_data = esc("G") >> number(4)


@generate
def print_graphics_data() -> Generator[Parser, Any, PrintGraphicsData]:
    count: int = yield alt(_start_uint64_data, _start_bytes_data)
    data: bytes = yield any_char.times(count).concat()

    return PrintGraphicsData(data)
