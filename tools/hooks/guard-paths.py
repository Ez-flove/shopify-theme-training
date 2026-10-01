#!/usr/bin/env python3
"""PreToolUse on Edit|Write — refuse secrets files and any write outside the project.

Mojarib carried this as a 900-character one-liner inside settings.json, which nobody could
read and nobody could test. Same teeth, in a file you can run.
"""
import json
import os
import subprocess
import sys

SECRET_PREFIXES = (".env", ".denv")
SECRET_NAMES = ("denv.env", "secrets.json", "credentials.json")


def block(reason):
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
        path = (payload.get("tool_input") or {})["file_path"]
    except Exception:
        sys.exit(0)

    base = os.path.basename(path)
    if base.startswith(SECRET_PREFIXES) or base in SECRET_NAMES:
        block("Cannot edit or write secrets files (%s)" % base)

    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.DEVNULL
        ).strip()
        above = subprocess.check_output(
            ["git", "rev-parse", "--show-superproject-working-tree"],
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        root = above or root
    except Exception:
        sys.exit(0)

    allowed = [root + os.sep, os.path.expanduser("~/.claude/")]
    target = os.path.abspath(path)
    if any(target.startswith(prefix) for prefix in allowed):
        sys.exit(0)
    block(
        "Cannot write outside the project (%s).\n"
        "If you genuinely need a file elsewhere, say so and use Bash — this guard exists so\n"
        "stray writes never happen by accident." % target
    )


if __name__ == "__main__":
    main()
