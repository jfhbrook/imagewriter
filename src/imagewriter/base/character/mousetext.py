"""
MouseText is a special character font included in the ImageWriter II. It is generally
accessible in high ASCII, but can be mapped from low ASCII with a special mode.

Mousetext is documented in the ImageWriter II Technical Reference Manual starting at
page 40.
"""

from enum import Enum


class MouseTextCharacter(Enum):
    """
    A MouseText character.

    Many of these characters are included in the Symbols for Legacy Computing
    Unicode block:

    <https://www.unicode.org/charts/PDF/U1FB00.pdf>

    However, some of them suffer from false unification issues:

    <https://www.unicode.org/L2/L2025/25037-legacy-box-drawing-disunification.pdf>
    """

    DARK_APPLE = 192
    LIGHT_APPLE = 193
    ARROWHEAD_SHAPED_POINTER = 194
    HOURGLASS = 195
    CHECK_MARK = 196
    INVERSE_CHECK_MARK = 197
    DOWNWARDS_ARROW_WITH_TIP_LEFTWARDS = 198
    # As in the UI element on a classic Mac - Referred to as HORIZONTAL ONE EIGHTH
    # BLOCK in Unicode
    TITLE_BAR = 199
    LEFTWARDS_ARROW = 200
    ELLIPSIS = 201
    DOWNWARDS_ARROW = 202
    UPWARDS_ARROW = 203
    UPPER_RIGHT_ONE_EIGHT_BLOCK = 204
    CARRIAGE_RETURN = 205
    FULL_BLOCK = 206  # In "block characters" unicode block
    LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK = 207
    RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK = 208
    DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK = 209
    UPWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK = 210
    UPPER_ONE_EIGHT_BLOCK = 211
    LEFT_AND_LOWER_ONE_EIGHT_BLOCK = 212
    RIGHTWARDS_ARROW = 213
    MEDIUM_SHADE = 214
    DARK_SHADE = 215
    LEFT_HALF_FOLDER = 216  # Paired with RIGHT_HALF_FOLDER
    RIGHT_HALF_FOLDER = 217  # Paired with LEFT_HALF_FOLDER
    RIGHT_ONE_EIGHT_BLOCK = 218
    BLACK_DIAMOND = 219
    LOWER_ONE_EIGHT_BLOCK = 220
    VOIDED_GREEK_CROSS = 221
    RIGHT_OPEN_SQUARED_DOT = 222
    LEFT_ONE_EIGHT_BLOCK = 223
