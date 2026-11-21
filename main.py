#!/usr/bin/env python3
"""Copy the front-page image to the output directory.

Standard library only. The image itself is drawn by generate.py at
build time and committed as entry.png; this program only copies it to
/output/entry.png so both grader runs write the same bytes.
Deterministic by construction: no network, no clock, no randomness.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
