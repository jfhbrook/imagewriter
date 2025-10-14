from imagewriter.encoding.base import esc, format_number


def repeat(char: str, n: int) -> bytes:
    """
    Repeat a character n times, as per page 83 of the ImageWriter II Technical
    Reference Manual.
    """

    assert len(char) == 1, "Can only repeat one character"

    return esc("R", format_number(n, 3), char)
