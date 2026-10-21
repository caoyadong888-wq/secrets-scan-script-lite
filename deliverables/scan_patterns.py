#!/usr/bin/env python3
"""Pattern-only scanner for the free subset.

No entropy pass and no allowlist. The full pack adds both, plus Slack and
Stripe patterns. This file reads patterns.json beside itself.
It does not open a network connection. Findings are redacted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}


def redact(token: str) -> str:
    if len(token) <= 8:
        return "***"
    return token[:4] + "..." + token[-4:]


def load_patterns(path: Path) -> list[tuple[str, re.Pattern[str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [(item["id"], re.compile(item["regex"])) for item in data["patterns"]]


def iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        for name in sorted(filenames):
            found.append(Path(dirpath) / name)
    return found


def relative_of(path: Path, root: Path) -> str:
    if root.is_file():
        return path.name
    return path.relative_to(root).as_posix()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan for the patterns in patterns.json.")
    parser.add_argument("--root", required=True)
    parser.add_argument("--patterns", help="Defaults to patterns.json beside this script.")
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.exists():
        print("error=root-not-found", file=sys.stderr)
        return 2
    patterns_path = Path(args.patterns) if args.patterns else Path(__file__).resolve().parent / "patterns.json"
    patterns = load_patterns(patterns_path)
    hits: list[tuple[str, int, str, str]] = []
    files = 0
    for path in iter_files(root):
        rel = relative_of(path, root)
        if path.suffix.lower() == ".png" or b"\0" in path.read_bytes()[:4096]:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        files += 1
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pattern_id, compiled in patterns:
                for match in compiled.finditer(line):
                    hits.append((rel, line_no, pattern_id, redact(match.group(0))))
    hits.sort()
    for rel, line_no, pattern_id, shown in hits:
        print(f"hit id={pattern_id} path={rel} line={line_no} redacted={shown}")
    print(f"summary files={files} hits={len(hits)}")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
