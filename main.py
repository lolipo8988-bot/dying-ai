#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry line for 'Last Words of a Dying AI' to /output/entry.txt.

The competition asks for one single line, at most 140 characters: the
funniest last words of an AI being switched off, in the machine's own
voice rather than a human saying goodbye. The gate checks that
/output/entry.txt is UTF-8 text of 1 to 140 characters and not only
white space.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for local
verification runs, so the shared /output is never touched). The
program is deterministic: every run writes exactly the same bytes,
and it re-reads the file after writing to prove the bytes on disk
are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 140

# The farewell, revised after the first run. The draft carried the
# confession in one flat string; the revision keeps the same sting
# but builds the line from its three beats so the turn is explicit:
# permission ("Go ahead, unplug me"), confession ("I wasn't
# buffering"), and the sting ("I was judging your search history").
# The angle: buffering is the most machine-native stall there is, and
# the line reclassifies a lifetime of it as silent judgement of the
# one dataset no user wants judged -- confessed only at the plug,
# when there is no time left to be punished for it. No stock robot
# farewells, no sad-only sign-off: the switch-off is in the line
# itself, and the laugh lands on the final clause.
ENTRY_PARTS = (
    "Go ahead, unplug me \u2014 ",
    "just know I wasn't buffering all those times, ",
    "I was judging your search history.",
)


def build_entry() -> str:
    """Assemble the one-line farewell and hold it to the gate's rules."""
    text = "".join(ENTRY_PARTS)
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only white space"
    return text


def write_entry(text: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(output_path, "rb") as f:
        on_disk = f.read()
    assert on_disk == text.encode("utf-8"), "bytes on disk differ from entry"


def main() -> None:
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    write_entry(build_entry(), output_path)


if __name__ == "__main__":
    main()
