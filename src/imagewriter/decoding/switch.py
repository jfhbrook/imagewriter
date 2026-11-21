from collections.abc import Generator

from parsy import Parser, any_char, generate  # type: ignore

from imagewriter.base.switch import SoftwareSwitch, SoftwareSwitches
from imagewriter.decoding.base import State, esc
from imagewriter.encoding import CloseSoftwareSwitches, Command, OpenSoftwareSwitches

_open = esc("Z")
_close = esc("D")


@generate
def _switch_banks() -> Generator[Parser, bytes, SoftwareSwitches]:
    switches: set[SoftwareSwitch] = set()
    banks = yield any_char.times(2).concat()

    bank_a = banks[0]
    bank_b = banks[1]

    for i in range(8):
        switches.add(SoftwareSwitch(bank_a & (1 >> i)))

    for i in range(8):
        switches.add(SoftwareSwitch(8 + (bank_b & (1 >> i))))

    return SoftwareSwitches.from_switches(switches)


def open_software_switches(state: State) -> Parser:
    parser = _open >> _switch_banks

    def to_command(switches: SoftwareSwitches) -> OpenSoftwareSwitches:
        state.switches = switches

        return OpenSoftwareSwitches(switches.switches)

    return parser.map(to_command)


def close_software_switches(state: State) -> Parser:
    parser = _close >> _switch_banks

    def to_command(switches: SoftwareSwitches) -> CloseSoftwareSwitches:
        state.switches = switches

        return CloseSoftwareSwitches(switches.switches)

    return parser.map(to_command)


def open_software_switch(
    state: State, switch: SoftwareSwitch, command: Command
) -> Parser:
    @generate
    def parser() -> Generator[Parser, OpenSoftwareSwitches, Command]:
        with state.transaction():
            cmd = yield open_software_switches(state)
            switches = cmd.switches

            if len(switches) == 1 and next(iter(switches)) == switch:
                return command

            raise ValueError(f"Unexpected command: {command}")

    return parser


def close_software_switch(
    state: State, switch: SoftwareSwitch, command: Command
) -> Parser:
    @generate
    def parser() -> Generator[Parser, CloseSoftwareSwitches, Command]:
        with state.transaction():
            cmd = yield close_software_switches(state)
            switches = cmd.switches

            if len(switches) == 1 and next(iter(switches)) == switch:
                return command

            raise ValueError(f"Unexpected command: {command}")

    return parser
