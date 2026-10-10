import pytest

from imagewriter.test import TestPage as _TestPage


@pytest.mark.parametrize(
    "method",
    [
        "full_monty",
        "languages",
        "pitch",
        "quality",
        "attributes",
        "mousetext",
        "markdown",
    ],
)
def test_render(method: str, test_page: _TestPage, snapshot) -> None:
    assert getattr(test_page, method)() == snapshot
