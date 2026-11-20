#!/usr/bin/env python3
"""Write the 20 November 2026 poster to /output/entry.png.

The poster bytes live in image.b64 next to this file, so the entry
program needs nothing but the Python standard library: it reads the
base64 text, decodes it, and writes the PNG out. No network, no clock,
no randomness -- the same input always produces the same output bytes.
"""
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "image.b64"
DEST = Path("/output/entry.png")


def main() -> Path:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(base64.b64decode(SOURCE.read_text(encoding="ascii")))
    return DEST


if __name__ == "__main__":
    main()
