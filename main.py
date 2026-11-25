"""Entrypoint: copy the pre-drawn entry.png to the grader's output dir.

The image is drawn by generate.py (same directory) and committed to the
repository; this program only places it at /output/entry.png, using the
MAKEFUN_OUTPUT_DIR environment variable when the grader sets it.
"""

import os
import shutil

# The image itself is drawn by generate.py and committed; this entrypoint
# only places the committed bytes where the grader expects them.
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
