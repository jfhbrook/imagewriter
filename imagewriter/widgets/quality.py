from typing import Dict, Self

import ipywidgets as widgets

from imagewriter.quality import Quality

QUALITIES: Dict[str, Quality] = {
    "Correspondence": Quality.CORRESPONDENCE,
    "Draft": Quality.DRAFT,
    "NLQ": Quality.NEAR_LETTER_QUALITY,
}

QUALITY_NAMES: Dict[Quality, str] = {
    quality: name for name, quality in QUALITIES.items()
}


class QualityWidget(widgets.Dropdown):
    def __init__(self: Self, quality: Quality) -> None:
        super().__init__(
            options=list(QUALITIES.keys()),
            value=self._start_value(quality),
            description="Quality:",
            disabled=False,
        )

    def _start_value(self: Self, quality: Quality) -> str:
        return QUALITY_NAMES[quality]

    @property
    def quality(self: Self) -> Quality:
        value: str = self.value if self.value else "Draft"
        return QUALITIES[value]
