from dataclasses import dataclass
from typing import Literal

ListNumberStyle = (
    Literal["DefaultStyle"]
    | Literal["Example"]
    | Literal["Decimal"]
    | Literal["LowerRoman"]
    | Literal["UpperRoman"]
    | Literal["LowerAlpha"]
    | Literal["UpperAlpha"]
)

DEFAULT_STYLE: ListNumberStyle = "DefaultStyle"
EXAMPLE: ListNumberStyle = "Example"
DECIMAL: ListNumberStyle = "Decimal"
LOWER_ROMAN: ListNumberStyle = "LowerRoman"
UPPER_ROMAN: ListNumberStyle = "UpperRoman"
LOWER_ALPHA: ListNumberStyle = "LowerAlpha"
UPPER_ALPHA: ListNumberStyle = "UpperAlpha"

ListNumberDelim = (
    Literal["DefaultDelim"]
    | Literal["Period"]
    | Literal["OneParen"]
    | Literal["TwoParens"]
)

DEFAULT_DELIM: ListNumberDelim = "DefaultDelim"
PERIOD: ListNumberDelim = "Period"
ONE_PAREN: ListNumberDelim = "OneParen"
TWO_PARENS: ListNumberDelim = "TwoParens"


@dataclass
class ListAttributes:
    """
    List attributes.
    """

    start: int
    style: ListNumberStyle
    delimiter: ListNumberDelim
