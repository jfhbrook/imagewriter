from typing import List

from imagewriter.encoding import Command


def test_render(test_page: List[Command], snapshot) -> None:
    assert test_page == snapshot
