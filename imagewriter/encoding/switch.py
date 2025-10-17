from abc import ABC
from typing import List, Self, Set

from imagewriter.encoding.base import Command, esc
from imagewriter.switch import SoftwareSwitch


class SetSoftwareSwitches(Command, ABC):
    def __init__(self: Self, closed: bool, switches: Set[SoftwareSwitch]) -> None:
        self._closed: bool = closed
        self.switches: Set[SoftwareSwitch] = switches

    @property
    def open(self: Self) -> bool:
        return not self._closed

    @property
    def closed(self: Self) -> bool:
        return self._closed

    def pack(self: Self) -> bytes:
        bank_a = 0
        bank_b = 0

        # Collect the bits into a short
        short = 0

        for sw in sorted(self.switches, key=lambda s: s.value):
            short |= sw.value

        # Store data in two little endian bytes
        for i in range(0, 16):
            if short & (1 << i):
                if i < 8:
                    bank_a |= 0x80 >> i
                else:
                    bank_b |= 0x8000 >> i

        return bytes([bank_a, bank_b])

    def __bytes__(self: Self) -> bytes:
        code: bytes = esc("D") if self.closed else esc("Z")

        return code + self.pack()


class OpenSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(False, switches)


class CloseSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(True, switches)


def set_software_switches(switches: Set[SoftwareSwitch]) -> List[Command]:
    """
    Close the software switches provided, and open all other software
    switches.
    """

    return [
        OpenSoftwareSwitches(SoftwareSwitch.difference(*switches)),
        CloseSoftwareSwitches(switches),
    ]
