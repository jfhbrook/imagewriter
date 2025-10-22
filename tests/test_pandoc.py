from imagewriter.pandoc import parse


def test_pandoc_markdown(snapshot) -> None:
    with open("./tests/documents/test.md", "r") as f:
        markdown = f.read()

    doc = parse(markdown, "markdown")

    assert doc == snapshot
