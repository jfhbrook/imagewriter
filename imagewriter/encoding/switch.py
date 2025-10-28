from abc import ABC
from typing import List, Self, Set

from imagewriter.encoding.base import Command, esc
from imagewriter.switch import SoftwareSwitch, SoftwareSwitches


def fmt_switch_position(closed: bool) -> str:
    return "CLOSE" if closed else "OPEN"


def fmt_switch_banks(banks: bytes) -> str:
    return f"[0b{banks[0]:08b}, 0b{banks[1]:08b}]"


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

    def __repr__(self: Self) -> str:
        packed = self.pack()

        return f"SetSoftwareSwitches({self.closed}, {fmt_switch_banks(packed)})"


class OpenSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(False, switches)

    def __repr__(self: Self) -> str:
        packed = self.pack()

        return f"OpenSoftwareSwitches({fmt_switch_banks(packed)})"


class CloseSoftwareSwitches(SetSoftwareSwitches):
    def __init__(self: Self, switches: Set[SoftwareSwitch]) -> None:
        return super().__init__(True, switches)

    def __repr__(self: Self) -> str:
        packed = self.pack()

        return f"CloseSoftwareSwitches({fmt_switch_banks(packed)})"


def apply_software_switches(switches: SoftwareSwitches) -> List[Command]:
    """
    Apply current software switches, resolving any drift.
    """

    commands: List[Command] = list()
    to_close = switches.switches()
    to_open = SoftwareSwitch.difference(to_close)

    if to_open:
        commands.append(OpenSoftwareSwitches(to_open))

    if to_close:
        commands.append(CloseSoftwareSwitches(to_close))

    return commands
