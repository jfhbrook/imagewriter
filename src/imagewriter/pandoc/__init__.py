"""
Use Pandoc to parse documents, such as Markdown, into a document model (which can then
be rendered into commands). This enables printing Markdown-like documents as rich text.
"""

import json
import subprocess
from typing import List

from imagewriter.document import Document, PANDOC_FORMATS, PandocFormat
import imagewriter.pandoc.parser as parser


def parse_document(document: str, format: PandocFormat = "markdown") -> Document:
    assert format in PANDOC_FORMATS, f"{format} is not supported by Pandoc."

    process = subprocess.run(
        ["pandoc", "-r", format, "-w", "json"],
        input=document,
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return parser.parse_document(json.loads(process.stdout))


__all__: List[str] = ["parse_document"]
