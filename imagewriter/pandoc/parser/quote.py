from typing import Any

from imagewriter.document import QuoteType


def parse_quote_type(contents: Any) -> QuoteType:
    return contents["t"]
