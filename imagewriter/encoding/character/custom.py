from typing import List, Self


class CustomCharacter:
    def __init__(self: Self, point: int) -> None:
        assert (32 <= point <= 126) or (
            160 <= point <= 239
        ), "Point must be within either low or high ASCII"
        self.point: int = point


CustomCharacters = CustomCharacter | List[CustomCharacter]
