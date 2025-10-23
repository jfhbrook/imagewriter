import importlib.resources

from imagewriter.job import Job
from imagewriter.pandoc import parse_document
from imagewriter.render import DocumentRenderer
from imagewriter.settings import Settings


def test_render_document(settings: Settings, snapshot) -> None:
    markdown = importlib.resources.read_text(
        __name__, "../documents/test_render_document.md"
    )

    doc = parse_document(markdown, "markdown")

    job = Job(settings)

    renderer = DocumentRenderer(job)

    assert renderer.render(doc).commands == snapshot
