from parsy import Parser  # type: ignore

from imagewriter.decoding.base import State, esc, number
from imagewriter.encoding.boundaries import SetLeftMargin, SetPageLength


def set_left_margin(state: State) -> Parser:
    def map(n: int) -> SetLeftMargin:
        return SetLeftMargin(n, state.pitch)

    return esc("L") >> number(3).map(map)


set_page_length = esc("H") >> number(4).map(SetPageLength)
