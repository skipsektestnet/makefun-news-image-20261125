#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 v3 entry.

Copies the pre-rendered entry.png (produced by generate.py) to the output
directory the harness provides. Standard library only, no network, fully
deterministic: the bytes written are exactly the bytes of entry.png.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    # The harness sets MAKEFUN_OUTPUT_DIR; fall back to /output, then argv[1].
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if len(sys.argv) < 2 else sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
