from imagewriter.pandoc import parse_document


def test_pandoc_markdown(pandoc_markdown, snapshot) -> None:
    doc = parse_document(pandoc_markdown, "markdown")

    # Allow for different versions of pandoc in tests
    doc.pandoc_api_version = []

    assert doc == snapshot
