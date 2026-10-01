#!/usr/bin/env python3
"""PreToolUse on Bash — refuse deleting secrets files and unbounded destructive SQL.

A known limit, worth reading before you widen it: this matches the TEXT of a command, so a
heredoc that merely spells out one of these patterns is blocked the same as a command that
runs it. That happened twice while writing this very file — once for the delete-secrets
pattern, once for a human-readable reason string that spelled out the SQL. The fix is to
split the write or reword the prose, not to loosen the pattern: a guard that lets prose
through lets a command dressed as prose through.
"""
import json
import re
import sys

SECRETS = r"(\.env|\.denv|denv\.env|\.pem|id_rsa|id_ed25519|\.p12|\.keystore)"

RULES = [
    (r"\b(rm|unlink|shred)\b[^\n]*" + SECRETS, "Cannot delete secrets files"),
    (r"\bDELETE\s+FROM\b(?![^\n]*\bWHERE\b)", "Unbounded row deletion, no WHERE clause — ask the user first"),
    (r"\bUPDATE\s+\w+\s+SET\b(?![^\n]*\bWHERE\b)", "Unbounded row update, no WHERE clause — ask the user first"),
    (r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b", "DROP is destructive — ask the user first"),
    (r"\bTRUNCATE\s+TABLE\b", "TRUNCATE is destructive — ask the user first"),
    (r"\bprisma\s+migrate\s+reset\b", "prisma migrate reset wipes dev data — ask the user first"),
    (r"\bgit\s+push\s+(--force|-f)\b", "Force push is denied"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard is denied"),
    (r"\bgit\s+clean\s+-[a-z]*f", "git clean -f is denied"),
    (r"--no-verify\b", "Never skip the commit hooks"),
]


def main():
    try:
        payload = json.load(sys.stdin)
        cmd = (payload.get("tool_input") or {})["command"]
    except Exception:
        sys.exit(0)
    for pattern, reason in RULES:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(json.dumps({"decision": "block", "reason": reason}))
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    main()
