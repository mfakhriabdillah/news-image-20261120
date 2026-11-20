#!/usr/bin/env python3
"""news-image-20261120 entry.

Writes the pre-built 2D front-page image (entry.png, in the repo root)
to /output/entry.png, byte-for-byte, with no network access.

The image sums up Friday 20 November 2026 world news in one picture:
  1. Trump, Xi and Putin meet in Shenzhen
  2. ICJ: Myanmar guilty of Rohingya genocide
  3. Tanker hit by mine in Strait of Hormuz
  4. Ukraine peace talks continue
  5. Anthropic shares jump 17% on Nasdaq debut

Deterministic: the same input bytes always produce the same output bytes.
"""

import os
import shutil
import sys


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(repo_root, "entry.png")
    out_dir = "/output"
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print(f"missing input: {src}", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    # Validate the deliverable before finishing: PNG, 1024x1024, <= 1 MiB.
    size = os.path.getsize(dst)
    if size > 1024 * 1024:
        print(f"output too large: {size} bytes", file=sys.stderr)
        return 1
    with open(dst, "rb") as f:
        header = f.read(33)
    if not header.startswith(b"\x89PNG\r\n\x1a\n"):
        print("output is not a PNG", file=sys.stderr)
        return 1
    # PNG IHDR: width and height are bytes 16..24 (big-endian uint32s).
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"unexpected dimensions: {width}x{height}", file=sys.stderr)
        return 1

    print(f"wrote {dst} ({size} bytes, {width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
