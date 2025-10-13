def ctrl(character: str) -> bytes:
    """
    Generate a control character, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    point: int = ord(character)

    if not (64 <= point <= 95):
        raise ValueError(f"{character} ({point}) must be between 64 and 95 inclusive")

    return bytes(chr(point - 64), encoding="ascii")


ESC = bytes([27])


def esc(*sequence: str | int | bytes) -> bytes:
    """
    Generate an escape sequence, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    seq: bytes = b""

    for s in sequence:
        if isinstance(s, str):
            seq += bytes(s, encoding="ascii")
        elif isinstance(s, int):
            seq += bytes([s])
        else:
            seq += s

    return ESC + seq
