"""
A code point, represented as either an int; or as a string or byte character.
"""

from imagewriter.base.character.ascii import assert_ascii

CodePoint = str | bytes | int


def is_single_byte(point: bytes) -> bool:
    """
    Check that a code point is a single byte.
    """

    return len(point) == 1


def from_code_point(point: CodePoint) -> int:
    """
    Convert a code point to an integer value.
    """

    buffer: bytes = b""
    result: int = -1

    if isinstance(point, str):
        buffer = point.encode(encoding="ascii")
    elif isinstance(point, bytes):
        buffer = point
    else:
        result = point

    if buffer:
        assert is_single_byte(buffer)
        result = buffer[0]

    assert_ascii(result)

    return result
