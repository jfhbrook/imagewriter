from typing import Self

from imagewriter.base.settings import Settings
from imagewriter.document import PandocFormat
from imagewriter.encoding import Command
from imagewriter.pandoc import parse_document
from imagewriter.render.document import DocumentRenderer
from imagewriter.render.text import RichTextBuilder


class PandocRenderer:
    """
    Render a document format, such as Markdown, using pandoc.
    """

    def __init__(self: Self, settings: Settings) -> None:
        self._renderer = DocumentRenderer(settings)

    @property
    def builder(self: Self) -> RichTextBuilder:
        return self._renderer.builder

    @property
    def settings(self: Self) -> Settings:
        return self.builder.settings

    @settings.setter
    def settings(self: Self, settings: Settings) -> None:
        self.builder.settings = settings

    def render(
        self: Self,
        document: str,
        format: PandocFormat = "markdown",
        standalone: bool = False,
    ) -> list[Command]:
        doc = parse_document(document, format)
        return self._renderer.render(doc, standalone=standalone)
