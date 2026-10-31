from collections.abc import Callable

from imagewriter.encoding import CR, LF, Command


def test_hello_world(
    hello_world: str, encoded_text: Callable[[str], list[Command]]
) -> None:
    assert hello_world == encoded_text("Hello world!") + [CR, LF]
