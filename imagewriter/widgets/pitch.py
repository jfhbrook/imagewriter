from typing import Dict, Self

import ipywidgets as widgets

from imagewriter.pitch import Pitch

PITCHES: Dict[str, Pitch] = {pitch.value: pitch for pitch in Pitch}


class PitchWidget(widgets.Dropdown):
    def __init__(self: Self, pitch: Pitch) -> None:
        super().__init__(
            options=list(PITCHES.keys()),
            value=self._start_value(pitch),
            description="Pitch:",
            disabled=False,
        )

    def _start_value(self: Self, pitch: Pitch) -> str:
        return pitch.value

    @property
    def language(self: Self) -> Pitch:
        value: str = self.value if self.value else "Elite"
        return PITCHES[value]
