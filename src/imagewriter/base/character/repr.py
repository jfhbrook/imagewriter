def repr_code_point(point: int) -> str:
    """
    A representation of a code point.
    """

    character = ""

    try:
        character = chr(point)
    except ValueError:
        return f"{point}"
    else:
        return f"{point} ({character!r})"
