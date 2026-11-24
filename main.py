#!/usr/bin/env python3
"""news-image-20261124 — copy the shipped entry.png to the output directory.

Render: map pins 3 (Cikande, centred on Java) and 13 (Wellington, on the
New Zealand sliver) sit on their islands, each with a 1px leader line to
its true spot. The other 10 pins are at their true or cluster-offset spots.

Standard library only (the grader container has no third-party packages).
Reads the output directory from MAKEFUN_OUTPUT_DIR and falls back to
/output when that variable is absent. Verifies the copied file's SHA-256
against the hash baked in below and exits non-zero on any mismatch.
"""

import hashlib
import os
import shutil
import sys

# SHA-256 of the shipped entry.png (1024x1024, 224932 bytes).
EXPECTED_SHA256 = "1bf3ababcb5694ac658184d934cc4ec63f04df691580ae00243fca248a41e334"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: shipped entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir and "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            out_dir = sys.argv[idx + 1]
    if not out_dir:
        out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    digest = hashlib.sha256()
    with open(dst, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    actual = digest.hexdigest()
    if actual != EXPECTED_SHA256:
        print("error: SHA-256 mismatch for %s" % dst, file=sys.stderr)
        print("  expected %s" % EXPECTED_SHA256, file=sys.stderr)
        print("  actual   %s" % actual, file=sys.stderr)
        return 1
    print("wrote %s sha256=%s" % (dst, actual))
    return 0


if __name__ == "__main__":
    sys.exit(main())
