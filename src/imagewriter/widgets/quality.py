from typing import Self

import ipywidgets as widgets  # type: ignore

from imagewriter.base.quality import Quality

QUALITIES: dict[str, Quality] = {
    "Correspondence": Quality.CORRESPONDENCE,
    "Draft": Quality.DRAFT,
    "NLQ": Quality.NEAR_LETTER_QUALITY,
}

QUALITY_NAMES: dict[Quality, str] = {
    quality: name for name, quality in QUALITIES.items()
}


class QualityWidget(widgets.Dropdown):
    def __init__(self: Self, quality: Quality) -> None:
        super().__init__(
            options=list(QUALITIES.keys()),
            value=QUALITY_NAMES[quality],
            description="Quality:",
            disabled=False,
        )

    @property
    def quality(self: Self) -> Quality:
        value: str = self.value if self.value else "Draft"
        return QUALITIES[value]

    @quality.setter
    def quality(self: Self, quality: Quality) -> None:
        self.value = QUALITY_NAMES[quality]
