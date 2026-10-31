from dataclasses import dataclass, field


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str = ""
    classes: list[str] = field(default_factory=list)
    pairs: list[tuple[str, str]] = field(default_factory=list)
