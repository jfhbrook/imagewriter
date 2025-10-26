from imagewriter.pandoc import parse_document


def test_pandoc_markdown(pandoc_markdown, snapshot) -> None:
    doc = parse_document(pandoc_markdown, "markdown")

    assert doc == snapshot
