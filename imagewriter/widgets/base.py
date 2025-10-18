from typing import Any, Self

import ipywidgets as widgets


class Label(widgets.Label):
    def __init__(self: Self, value: str, **kwargs: Any) -> None:
        kwargs["style"] = kwargs.get("style", dict())
        kwargs["style"]["font_weight"] = kwargs["style"].get("font_weight", "bold")

        super().__init__(value, **kwargs)


def header(value: str, level: int = 4) -> widgets.HTML:
    return widgets.HTML(value=f"<h{level}>{value}</h{level}>")
