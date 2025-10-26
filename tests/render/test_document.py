from imagewriter.pandoc import parse_document
from imagewriter.render import DocumentRenderer
from imagewriter.settings import Settings


def test_render_document(settings: Settings, simple_markdown: str, snapshot) -> None:
    doc = parse_document(simple_markdown, "markdown")

    renderer = DocumentRenderer(settings)

    assert renderer.render(doc) == snapshot
