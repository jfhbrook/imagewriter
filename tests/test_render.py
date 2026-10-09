from imagewriter.test import TestPage as _TestPage


def test_render(test_page: _TestPage, snapshot) -> None:
    assert test_page.full_monty() == snapshot
