#!/usr/bin/env python3
"""Ship the 21 November 2026 news image.

The graded artefact is entry.png beside this file: a one-page summary
of Saturday 21 November 2026, drawn beforehand by generate.py from
stories.json. Running this program places an exact copy of that PNG
at $MAKEFUN_OUTPUT_DIR/entry.png (falling back to /output), so every
run produces identical bytes. Standard library only.
"""

import os
import shutil

IMAGE_NAME = "entry.png"


def output_folder():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(folder, IMAGE_NAME)
    destination_dir = output_folder()
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, IMAGE_NAME)
    shutil.copyfile(source, destination)
    print("copied", source, "->", destination,
          os.path.getsize(destination), "bytes")


if __name__ == "__main__":
    main()
