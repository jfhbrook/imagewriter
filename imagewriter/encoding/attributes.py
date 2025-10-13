from imagewriter.encoding.base import ctrl, esc

START_DOUBLE_WIDTH: bytes = ctrl("N")
STOP_DOUBLE_WIDTH: bytes = ctrl("O")
START_UNDERLINE: bytes = esc("X")
STOP_UNDERLINE: bytes = esc("Y")
START_BOLDFACE: bytes = esc("!")
STOP_BOLDFACE: bytes = esc('"')
START_HALF_HEIGHT: bytes = esc("w")
STOP_HALF_HEIGHT: bytes = esc("W")
START_SUPERSCRIPT: bytes = esc("x")
STOP_SUPERSCRIPT: bytes = esc("z")
START_SUBSCRIPT: bytes = esc("y")
STOP_SUBSCRIPT: bytes = STOP_SUPERSCRIPT
