from dataclasses import dataclass


@dataclass
class Target:
    """
    Link target.
    """

    url: str
    title: str
