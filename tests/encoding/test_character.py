from tests.documents.hello import HELLO_WORLD

from imagewriter.encoding import CR, LF


def test_hello_world(encoded_text) -> None:
    assert HELLO_WORLD == encoded_text("Hello world!") + [CR, LF]
