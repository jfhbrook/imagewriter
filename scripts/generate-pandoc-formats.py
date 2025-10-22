import subprocess
from typing import List


def pandoc_formats() -> List[str]:
    process = subprocess.run(
        ["pandoc", "--list-input-formats"],
        check=True,
        capture_output=True,
        encoding="utf8",
    )

    return [format for format in process.stdout.split("\n") if format]


HEAD = """from typing import Literal

Format = (
"""

FOOT = """)
"""


def main() -> None:
    formats = pandoc_formats()

    template = 'Literal["{}"]'

    with open("./imagewriter/document/format.py", "w") as f:
        f.write(HEAD)
        f.write(f"    {template.format(formats.pop(0))}\n")

        for format in formats:
            f.write(f"    | {template.format(format)}\n")

        f.write(FOOT)


if __name__ == "__main__":
    main()
