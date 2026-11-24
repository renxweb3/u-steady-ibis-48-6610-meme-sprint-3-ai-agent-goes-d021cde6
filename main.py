#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — writes entry.png.

Copies the captioned meme this repository holds (built by make_meme.py)
to the output directory. No network, no randomness: every run writes the
same bytes.
"""
import os
import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    size = target.stat().st_size
    assert size <= 1_048_576, f"entry.png too big: {size} bytes"
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    main()
