from typing import Dict, Self

import ipywidgets as widgets

from imagewriter.pitch import Pitch

PITCHES: Dict[str, Pitch] = {pitch.value: pitch for pitch in Pitch}


class PitchWidget(widgets.Dropdown):
    def __init__(self: Self, pitch: Pitch) -> None:
        super().__init__(
            options=list(PITCHES.keys()),
            value=pitch.value,
            description="Pitch:",
            disabled=False,
        )

    @property
    def pitch(self: Self) -> Pitch:
        value: str = self.value if self.value else "Elite"
        return PITCHES[value]

    @pitch.setter
    def pitch(self: Self, pitch: Pitch) -> None:
        self.value = pitch.value
