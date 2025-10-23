import importlib.resources

from imagewriter.pandoc import parse_document


def test_pandoc_markdown(snapshot) -> None:
    markdown = importlib.resources.read_text(__name__, "documents/test_pandoc.md")

    doc = parse_document(markdown, "markdown")

    assert doc == snapshot
