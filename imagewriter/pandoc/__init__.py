import json
import subprocess
from typing import List

from imagewriter.document import Document
import imagewriter.pandoc.parser as parser


def pandoc_formats() -> List[str]:
    process = subprocess.run(
        ["pandoc", "--list-input-formats"],
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return [format for format in process.stdout.split("\n") if format]


def parse_document(document: str, format: str = "markdown") -> Document:
    process = subprocess.run(
        ["pandoc", "-r", format, "-w", "json"],
        input=document,
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return parser.parse_document(json.loads(process.stdout))
