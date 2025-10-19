from typing import Callable, List

import pytest

from imagewriter.encoding.base import Bytes, Command


@pytest.fixture
def encoded_text() -> Callable[[str | bytes], List[Command]]:
    def encoded_text(text: str | bytes) -> List[Command]:
        buffer = text if isinstance(text, bytes) else text.encode(encoding="ascii")
        return [Bytes(byte.to_bytes(byteorder="big")) for byte in buffer]

    return encoded_text
