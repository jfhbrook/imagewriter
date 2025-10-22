import subprocess
from typing import IO, List

#
# Formats not supported by Pandoc, but supported by imagewriter.
#

NATIVE_FORMATS = ["imagewriter"]


def pandoc_formats() -> List[str]:
    process = subprocess.run(
        ["pandoc", "--list-input-formats"],
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return [format for format in process.stdout.split("\n") if format]




HEAD = """from typing import Literal, Set

#
# Formats supported by Pandoc. This file is generated with
# ./scripts/generate-pandoc-formats.py and includes all formats supported by
# the currently installed version of pandoc.
#

"""

BEGIN_NATIVE_TYPE = """NativeFormat = (
"""

BEGIN_PANDOC_TYPE = """PandocFormat = (
"""

END_TYPE = """)

"""

COMBINED_TYPE = """Format = NativeFormat | PandocFormat

"""

BEGIN_NATIVE_SET = """NATIVE_FORMATS: Set[Format] = {
"""

BEGIN_PANDOC_SET = """PANDOC_FORMATS: Set[Format] = {
"""

END_SET = """}

"""

COMBINED_SET = """FORMATS: Set[Format] = NATIVE_FORMATS | PANDOC_FORMATS
"""


def write_type_elements(f: IO, formats: List[str]) -> None:
    f.write(f'    Literal["{formats[0]}"]\n')

    for format in formats[1:]:
        f.write(f'    | Literal["{format}"]\n')


def write_native_type(f: IO) -> None:
    f.write(BEGIN_NATIVE_TYPE)
    write_type_elements(f, NATIVE_FORMATS)
    f.write(END_TYPE)


def write_pandoc_type(f: IO, formats: List[str]) -> None:
    f.write(BEGIN_PANDOC_TYPE)
    write_type_elements(f, formats)
    f.write(END_TYPE)


def write_set_elements(f: IO, formats: List[str]) -> None:
    for format in formats:
        f.write(f'    "{format}",\n')


def write_native_set(f: IO) -> None:
    f.write(BEGIN_NATIVE_SET)
    write_set_elements(f, NATIVE_FORMATS)
    f.write(END_SET)


def write_pandoc_set(f: IO, formats: List[str]) -> None:
    f.write(BEGIN_PANDOC_SET)
    write_set_elements(f, formats)
    f.write(END_SET)


def main() -> None:
    formats = pandoc_formats()

    with open("./imagewriter/document/format.py", "w") as f:
        f.write(HEAD)
        write_native_type(f)
        write_pandoc_type(f, formats)
        f.write(COMBINED_TYPE)
        write_native_set(f)
        write_pandoc_set(f, formats)
        f.write(COMBINED_SET)



if __name__ == "__main__":
    main()
