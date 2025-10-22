import json
import subprocess

from imagewriter.document import Document, Format
import imagewriter.pandoc.parser as parser


def parse_document(document: str, format: Format = "markdown") -> Document:
    process = subprocess.run(
        ["pandoc", "-r", format, "-w", "json"],
        input=document,
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return parser.parse_document(json.loads(process.stdout))
