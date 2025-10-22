from typing import Any

from imagewriter.document import Document
from imagewriter.pandoc.parser.block import parse_block_list


def parse_document(contents: Any) -> Document:
    return Document(
        pandoc_api_version=contents.get("pandoc-api-version"),
        meta=contents.get("meta"),
        blocks=parse_block_list(contents["blocks"]),
    )
