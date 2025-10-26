from typing import Callable, List

from imagewriter.encoding import Command, CR, LF


def test_hello_world(
    hello_world: str, encoded_text: Callable[[str], List[Command]]
) -> None:
    assert hello_world == encoded_text("Hello world!") + [CR, LF]
