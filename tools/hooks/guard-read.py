#!/usr/bin/env python3
"""PreToolUse on Read — refuse system secrets outside the project."""
import json
import os
import re
import subprocess
import sys

BLOCKED = [
    r"/etc/shadow", r"/etc/passwd", r"/\.ssh/", r"/\.aws/",
    r"/\.gnupg/", r"/\.docker/config\.json",
]


def main():
    try:
        payload = json.load(sys.stdin)
        path = (payload.get("tool_input") or {})["file_path"]
    except Exception:
        sys.exit(0)

    if not any(re.search(pat, path) for pat in BLOCKED):
        sys.exit(0)
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        root = None
    if root and os.path.abspath(path).startswith(root + os.sep):
        sys.exit(0)
    print(json.dumps({
        "decision": "block",
        "reason": "Cannot read system secrets outside the project",
    }))


if __name__ == "__main__":
    main()
