from typing import List

from imagewriter.encoding import Command


def test_attributes(attributes: List[Command], snapshot) -> None:
    assert attributes == snapshot
