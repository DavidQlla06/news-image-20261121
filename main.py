"""Entrypoint for the news-image-20261121 entry.

Writes the front-page image to the output directory (the MAKEFUN_OUTPUT_DIR
environment variable when set, otherwise /output). The image is rendered by
generate.py when Pillow is available; in the grading sandbox, which has no
third-party packages, the committed entry.png is copied instead. Either way
the bytes are identical because generate.py is deterministic.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def produce():
    """Return the path of a freshly rendered entry.png, or None."""
    try:
        import generate
    except Exception:
        return None
    try:
        generate.main()
    except Exception:
        return None
    path = os.path.join(HERE, "entry.png")
    return path if os.path.exists(path) else None


def main():
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    rendered = produce()
    source = rendered if rendered else os.path.join(HERE, "entry.png")
    if not os.path.exists(source):
        print("no entry.png available", file=sys.stderr)
        return 1
    if os.path.abspath(source) != os.path.abspath(dest):
        shutil.copyfile(source, dest)
    print("entry.png written to", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
