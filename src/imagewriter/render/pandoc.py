from typing import List, Self

from imagewriter.document import PandocFormat
from imagewriter.encoding import Command
from imagewriter.pandoc import parse_document
from imagewriter.render.document import DocumentRenderer
from imagewriter.settings import Settings


class PandocRenderer:
    def __init__(self: Self, settings: Settings) -> None:
        self._renderer = DocumentRenderer(settings)

    def render(
        self: Self, document: str, format: PandocFormat = "markdown"
    ) -> List[Command]:
        doc = parse_document(document, format)
        return self._renderer.render(doc)
