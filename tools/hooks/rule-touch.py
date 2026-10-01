#!/usr/bin/env python3
"""PostToolUse hook: you just edited a file that a shared rule lives in — say where the
other copies are, before the copy nobody looks at is the one that goes wrong.

Silent unless the edited file appears in the shared-rules manifest.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

try:
    import _lib
except Exception:
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    edited = (payload.get("tool_input") or {}).get("file_path")
    if not edited:
        sys.exit(0)

    root = _lib.project_root()
    cfg = _lib.load_config(root)
    manifest = os.path.join(root, cfg["sharedRulesFile"])
    if not os.path.exists(manifest):
        sys.exit(0)
    try:
        rules = json.loads(_lib.read(manifest)).get("rules", [])
    except ValueError:
        sys.exit(0)

    try:
        rel = os.path.relpath(os.path.abspath(edited), root).replace(os.sep, "/")
    except ValueError:
        sys.exit(0)

    lines = []
    for rule in rules:
        files = rule.get("files") or []
        if rel not in files:
            continue
        others = [f for f in files if f != rel]
        lines.append("- %s: %s" % (rule.get("id", "?"), rule.get("statement", "")))
        if others:
            lines.append("  same rule also written in: %s" % ", ".join(others))
        lines.append("  check with: tools/run shared-rules --rule %s" % rule.get("id", "?"))

    if lines:
        note = ("This file carries a rule that is written by hand elsewhere too:\n"
                + "\n".join(lines))
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": note,
        }}))
    sys.exit(0)


if __name__ == "__main__":
    main()
