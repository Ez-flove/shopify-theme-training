#!/usr/bin/env python3
"""Stop hook — the "no plan, no code" gate, as a reminder rather than a block.

If the working tree has source changes and nothing under docs/plans/ was touched, then the
plan arrived after the edit, which makes it a description — and a description cannot be
disagreed with before the cost is paid.

Deliberately non-blocking, and deliberately silent whenever it cannot tell: a gate that
guesses loudly gets switched off, and then it guards nothing.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

try:
    import _lib
except Exception:
    sys.exit(0)


def changed_paths(root):
    try:
        out = subprocess.check_output(
            # --untracked-files=all matters: without it git collapses a new directory to
            # "src/", which no source glob matches, and the gate goes quiet for the wrong
            # reason — silent because it had nowhere to look, not because nothing changed.
            ["git", "-C", root, "status", "--porcelain", "--untracked-files=all"],
            text=True, stderr=subprocess.DEVNULL,
        )
    except Exception:
        return None
    paths = []
    for line in out.split("\n"):
        if not line.strip():
            continue
        entry = line[3:].strip().strip('"')
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        paths.append(entry)
    return paths


def main():
    root = _lib.project_root()
    cfg = _lib.load_config(root)
    paths = changed_paths(root)
    if not paths:
        sys.exit(0)

    touched_plan = any(p.startswith("docs/plans/") for p in paths)
    source = [
        p for p in paths
        if not p.startswith("docs/")
        and any(_lib.match_glob(p, pat) for pat in cfg["sourceGlobs"])
    ]
    if touched_plan or not source:
        sys.exit(0)

    shown = source[:6]
    more = "" if len(source) <= 6 else "\n  ... and %d more" % (len(source) - 6)
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "Stop",
        "additionalContext": (
            "No plan, no code — this tree has source changes and nothing under docs/plans/:\n  "
            + "\n  ".join(shown) + more
            + "\nIf that was a real change rather than reading or measuring, the plan owes four\n"
              "lines: what is wrong in the user's terms, where (file:line, measured not guessed),\n"
              "what changes and what deliberately does not, and the exact check that will prove\n"
              "it — including the mutation that must turn it red."
        ),
    }}))


if __name__ == "__main__":
    main()
