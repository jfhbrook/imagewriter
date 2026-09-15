"""
Abstractions for rendering documents to the ImageWriter II's coded format:

- `RichTextBuilder` allows for building rich text documents
- `DocumentRenderer` renders document models from `imagewriter.document` using
  `RichTextBuilder`
- `PandocRenderer` renders Markdown and other document formats using `pandoc` and
  `DocumentRenderer`
"""

from typing import List

from imagewriter.render.document import DocumentRenderer
from imagewriter.render.pandoc import PandocRenderer
from imagewriter.render.text import RichTextBuilder

__all__: List[str] = [
    "DocumentRenderer",
    "PandocRenderer",
    "RichTextBuilder",
]
