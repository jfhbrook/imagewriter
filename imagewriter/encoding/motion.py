from imagewriter.encoding.base import ctrl, esc

CR = "\r"
LF = "\n"
BACKSPACE = ctrl("H")


def set_unidirectional_printing(is_unidirectional: bool) -> bytes:
    """
    Configure unidirectional printing, as per page 63 of the ImageWriter II
    Technical Reference Manual.
    """

    if is_unidirectional:
        return esc(">")
    return esc("<")
