from typing import List

from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.language import Language
from imagewriter.switch import SoftwareSwitch


def set_language(language: Language) -> List[Command]:
    """
    Set the language, irrespective of current software switch or language
    settings.
    """

    return [
        OpenSoftwareSwitches(SoftwareSwitch.open_language_switches(language)),
        CloseSoftwareSwitches(SoftwareSwitch.language_switches(language)),
    ]
