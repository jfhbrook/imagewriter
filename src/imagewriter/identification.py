from dataclasses import dataclass
from typing import Self, Set

Feature = str
FEAT_COLOR_RIBBON: Feature = "C"
FEAT_SHEET_FEEDER: Feature = "F"


@dataclass
class Identification:
    model: str
    carriage_width: int
    features: Set[Feature]

    @property
    def color_ribbon(self: Self) -> bool:
        """
        True if a color ribbon is installed.
        """
        return FEAT_COLOR_RIBBON in self.features

    @property
    def sheet_feeder(self: Self) -> bool:
        """
        True if a SheetFeeder is installed.
        """

        return FEAT_SHEET_FEEDER in self.features


def parse_id_response(res: bytes) -> Identification:
    """
    Parse a response to the self-identify command, as per page 89 of the
    ImageWriter II Technical Reference Manual.

    Note that the response is of variable length, but is sent at the maximum
    baud rate. The intent is that the host device checks for received bytes at
    exactly the configured baud rate with no wait and stops when no byte is
    received. The reference manual recommends doing this at a low level with
    assembly.
    """

    model: str = res[0:2].decode(encoding="ascii")
    carriage_width: int = int(res[2:4].decode(encoding="ascii"))
    features: Set[Feature] = set(res[4:].decode(encoding="ascii").split(""))

    return Identification(
        model=model,
        carriage_width=carriage_width,
        features=features,
    )
