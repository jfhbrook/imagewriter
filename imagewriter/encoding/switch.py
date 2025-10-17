from abc import ABC
import dataclasses
from typing import Any, List, Self, Set, Tuple

from imagewriter.encoding.base import Command, esc
from imagewriter.switch import SoftwareSwitch, SoftwareSwitchSettings


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


def update_software_switch_settings(
    settings: SoftwareSwitchSettings, **changes: Any
) -> Tuple[SoftwareSwitchSettings, List[Command]]:
    """
    Update software switch settings, under the assumption that the current
    settings are accurate.
    """

    replaced = dataclasses.replace(settings, **changes)

    closed_before = settings.switches()
    open_before = SoftwareSwitch.difference(closed_before)
    closed_after = replaced.switches()
    open_after = SoftwareSwitch.difference(closed_after)

    to_open = open_after - open_before
    to_close = closed_after - closed_before

    commands: List[Command] = list()

    if to_open:
        commands.append(OpenSoftwareSwitches(to_open))
    if to_close:
        commands.append(CloseSoftwareSwitches(to_close))

    return (replaced, commands)


def force_software_switch_settings(settings: SoftwareSwitchSettings) -> List[Command]:
    """
    Fully write out software switch settings, regardless of their prior state.
    """

    to_close = settings.switches()
    to_open = SoftwareSwitch.difference(to_close)

    return [OpenSoftwareSwitches(to_open), CloseSoftwareSwitches(to_close)]
