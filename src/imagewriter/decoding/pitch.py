from collections.abc import Callable

from parsy import Parser, alt  # type: ignore

from imagewriter.base.pitch import Pitch
from imagewriter.decoding.base import State, esc, number
from imagewriter.encoding.pitch import PITCH_CODES, InsertSpaces, SetPitch


def _map_pitch(state: State, pitch: Pitch) -> Callable[[bytes], SetPitch]:
    def _map(_: bytes) -> SetPitch:
        command = SetPitch(pitch)
        state.pitch = pitch

        return command

    return _map


def set_pitch(state: State) -> Parser:
    return alt(
        *[
            esc(code).map(_map_pitch(state, pitch))
            for pitch, code in PITCH_CODES.items()
        ]
    )


def _map_insert_spaces(state: State, spaces: int) -> Callable[[bytes], InsertSpaces]:
    def _map(_: bytes) -> InsertSpaces:
        return InsertSpaces(state.pitch, spaces)

    return _map


def insert_spaces(state: State) -> Parser:
    return alt(*[esc(str(n)).map(_map_insert_spaces(state, n)) for n in range(1, 7)])


def set_spacing(state: State) -> Parser:
    return esc("m") >> number(1).map(lambda n: InsertSpaces(state.pitch, n))
