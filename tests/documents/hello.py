from typing import List

from imagewriter.encoding import CharacterEncoder, Command, CR, LF

encoder: CharacterEncoder = CharacterEncoder()

HELLO_WORLD: List[Command] = encoder.encode("Hello world!") + [CR, LF]
