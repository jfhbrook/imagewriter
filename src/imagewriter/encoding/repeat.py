from imagewriter.encoding.base import Bytes, Command, esc, number


def repeat(char: str, n: int) -> Command:
    """
    Repeat a character n times, as per page 83 of the ImageWriter II Technical
    Reference Manual.
    """

    assert len(char) == 1, "Can only repeat one character"

    return Bytes(esc("R") + number(n, 3) + char.encode(encoding="ascii"))
