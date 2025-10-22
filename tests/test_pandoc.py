from imagewriter.pandoc import parse_document


def test_pandoc_markdown(snapshot) -> None:
    with open("./tests/documents/test.md", "r") as f:
        markdown = f.read()

    doc = parse_document(markdown, "markdown")

    assert doc == snapshot
