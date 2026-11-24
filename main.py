#!/usr/bin/env python3
"""Copy the shipped entry.png to the grader output directory.

Standard library only: no Pillow, no fonts, no network.
Deterministic: the output is a byte-for-byte copy of the shipped image.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "acb89b67815e0d82c5f8caa2d96976f7df5a86dda7fc0b678c70e5abdad0046b"
EXPECTED_SIZE = 132850


def main():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if not bot_dir:
        bot_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(bot_dir, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    shutil.copyfile(src, dst)

    digest = hashlib.sha256()
    size = 0
    with open(dst, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            size += len(chunk)
            digest.update(chunk)
    sha = digest.hexdigest()

    if size != EXPECTED_SIZE or sha != EXPECTED_SHA256:
        print(
            "mismatch: copied %d bytes sha256=%s, expected %d bytes sha256=%s"
            % (size, sha, EXPECTED_SIZE, EXPECTED_SHA256),
            file=sys.stderr,
        )
        return 1

    print("wrote %s (%d bytes, sha256=%s)" % (dst, size, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
