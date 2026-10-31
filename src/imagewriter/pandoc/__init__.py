"""
Use Pandoc to parse documents, such as Markdown, into a document model (which can then
be rendered into commands). This enables printing Markdown-like documents as rich text.
"""

import json
import subprocess

from imagewriter.document import PANDOC_FORMATS, Document, PandocFormat
from imagewriter.pandoc import parser


def parse_document(document: str, format: PandocFormat = "markdown") -> Document:
    """
    Parse a text document using a Pandoc supported format, such as markdown.

    Args:
        document: A text document in string format
        format: A format supported by Pandoc
    """

    assert format in PANDOC_FORMATS, f"{format} is not supported by Pandoc."

    process = subprocess.run(
        ["pandoc", "-r", format, "-w", "json"],
        input=document,
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return parser.parse_document(json.loads(process.stdout))
