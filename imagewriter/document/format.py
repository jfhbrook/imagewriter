from typing import Literal, Set

#
# Formats supported by Pandoc. This file is generated with
# ./scripts/generate-pandoc-formats.py and includes all formats supported by
# the currently installed version of pandoc.
#

NativeFormat = Literal["imagewriter"]

PandocFormat = (
    Literal["biblatex"]
    | Literal["bibtex"]
    | Literal["bits"]
    | Literal["commonmark"]
    | Literal["commonmark_x"]
    | Literal["creole"]
    | Literal["csljson"]
    | Literal["csv"]
    | Literal["djot"]
    | Literal["docbook"]
    | Literal["docx"]
    | Literal["dokuwiki"]
    | Literal["endnotexml"]
    | Literal["epub"]
    | Literal["fb2"]
    | Literal["gfm"]
    | Literal["haddock"]
    | Literal["html"]
    | Literal["ipynb"]
    | Literal["jats"]
    | Literal["jira"]
    | Literal["json"]
    | Literal["latex"]
    | Literal["man"]
    | Literal["markdown"]
    | Literal["markdown_github"]
    | Literal["markdown_mmd"]
    | Literal["markdown_phpextra"]
    | Literal["markdown_strict"]
    | Literal["mdoc"]
    | Literal["mediawiki"]
    | Literal["muse"]
    | Literal["native"]
    | Literal["odt"]
    | Literal["opml"]
    | Literal["org"]
    | Literal["pod"]
    | Literal["ris"]
    | Literal["rst"]
    | Literal["rtf"]
    | Literal["t2t"]
    | Literal["textile"]
    | Literal["tikiwiki"]
    | Literal["tsv"]
    | Literal["twiki"]
    | Literal["typst"]
    | Literal["vimwiki"]
    | Literal["xml"]
)

Format = NativeFormat | PandocFormat

NATIVE_FORMATS: Set[Format] = {
    "imagewriter",
}

PANDOC_FORMATS: Set[Format] = {
    "biblatex",
    "bibtex",
    "bits",
    "commonmark",
    "commonmark_x",
    "creole",
    "csljson",
    "csv",
    "djot",
    "docbook",
    "docx",
    "dokuwiki",
    "endnotexml",
    "epub",
    "fb2",
    "gfm",
    "haddock",
    "html",
    "ipynb",
    "jats",
    "jira",
    "json",
    "latex",
    "man",
    "markdown",
    "markdown_github",
    "markdown_mmd",
    "markdown_phpextra",
    "markdown_strict",
    "mdoc",
    "mediawiki",
    "muse",
    "native",
    "odt",
    "opml",
    "org",
    "pod",
    "ris",
    "rst",
    "rtf",
    "t2t",
    "textile",
    "tikiwiki",
    "tsv",
    "twiki",
    "typst",
    "vimwiki",
    "xml",
}

FORMATS: Set[Format] = NATIVE_FORMATS | PANDOC_FORMATS
