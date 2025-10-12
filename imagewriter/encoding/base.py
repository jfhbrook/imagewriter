def ctrl(character: str) -> str:
    """
    Generate a control character, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    point: int = ord(character)

    if not (64 <= point <= 95):
        raise ValueError(f"{character} ({point}) must be between 64 and 95 inclusive")

    return chr(point - 64)


ESC = bytes([27])


def esc(*sequence: str | int | bytes) -> bytes:
    """
    Generate an escape sequence, as per page 5 of the ImageWriter II Technical
    Reference Manual.
    """

    seq: bytes = b""

    for s in sequence:
        if type(s) is str:
            seq += bytes(s, encoding="ascii")
        elif type(s) is int:
            seq += bytes([s])
        elif type(s) is bytes:
            seq += s
        else:
            raise ValueError(f"Unable to convert {s} to bytes")

    return ESC + seq
