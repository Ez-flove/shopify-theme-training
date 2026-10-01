#!/usr/bin/env python3
# Description: generate docs/architecture/change-guards.json from each guard's @guard docblock
"""
Every guard declares itself in its own top docblock:

    /**
     * @guard watches: what falls through if this is not extended
     * @guard extend:  what to change when your field or rule is new
     * @guard caught:  (optional) a defect this actually caught, with a date
     */

Everything else in the output — path, app, the names of its exclusion maps, the files it
reads — is derived from the source, which is the half that used to go stale.

    tools/run change-guards            regenerate the list
    tools/run change-guards --check    fail if the list is out of date (for CI / verify)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib  # noqa: E402

DOCBLOCK = re.compile(r"/\*\*(.*?)\*/", re.S)
TAG = re.compile(r"@guard\s+(watches|extend|caught)\s*:\s*(.*?)(?=(?:\n\s*\*\s*@guard\s)|\Z)", re.S)
# The prefix is optional: a map is just as often called ALLOWED_MISSING as NAV_ALLOWED.
# Requiring a prefix meant every name that STARTS with the keyword went undetected — found by
# the probe fixture on the first run, which is the whole argument for running the probe.
EXCLUSION_NAME = re.compile(
    r"(?:const|let|var)\s+((?:[A-Z][A-Z0-9_]*_)?(?:ALLOWED|EXCLUDED|EXCLUSIONS|SKIP|SKIPPED|"
    r"EXPECTED|DELIBERATE|KNOWN|EXEMPT|IGNORED)[A-Z0-9_]*)\b"
)
PATHISH = re.compile(r"""['"`]((?:\.{0,2}/)?[\w.@-]+(?:/[\w.@-]+)+\.(?:ts|tsx|js|jsx|py|prisma|json|sql|go|php|rb))['"`]""")


def clean_tag(text):
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"^\s*\*\s?", "", line).strip()
        if line:
            lines.append(line)
    return " ".join(lines).strip()


def app_of(rel, cfg):
    for app in cfg.get("apps") or []:
        if rel == app or rel.startswith(app.rstrip("/") + "/"):
            return app.rstrip("/")
    head = rel.split("/")[0]
    return head if "/" in rel else "."


def guard_id(rel):
    name = os.path.basename(rel)
    for suffix in (".spec.ts", ".spec.tsx", ".test.ts", ".test.tsx", ".spec.js", ".test.js", ".spec.py"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return os.path.splitext(name)[0]


def collect(root, cfg):
    guards = []
    missing_block = []
    required = cfg.get("guardRequiredGlobs") or []
    for rel in _lib.walk_files(root, cfg, cfg["guardGlobs"]):
        text = _lib.read(os.path.join(root, rel))
        block = None
        for candidate in DOCBLOCK.findall(text):
            if "@guard" in candidate:
                block = candidate
                break
        if block is None:
            if any(_lib.match_glob(rel, pat) for pat in required):
                missing_block.append(rel)
            continue
        tags = {}
        for key, value in TAG.findall(block):
            tags.setdefault(key, clean_tag(value))
        if "watches" not in tags or "extend" not in tags:
            missing_block.append(rel + "  (has @guard but not both watches: and extend:)")
            continue
        body = text[text.index(block) + len(block):] if block in text else text
        entry = {
            "id": guard_id(rel),
            "app": app_of(rel, cfg),
            "path": rel,
            "watches": tags["watches"],
            "extend": tags["extend"],
        }
        if tags.get("caught"):
            entry["caught"] = tags["caught"]
        exclusions = sorted(set(EXCLUSION_NAME.findall(body)))
        if exclusions:
            entry["exclusionMaps"] = exclusions
        reads = sorted(set(PATHISH.findall(body)))
        if reads:
            entry["reads"] = reads
        guards.append(entry)
    guards.sort(key=lambda g: (g["app"], g["id"]))
    return guards, missing_block


def duplicate_ids(guards):
    seen = {}
    for g in guards:
        seen.setdefault(g["id"], []).append(g["path"])
    return {k: v for k, v in seen.items() if len(v) > 1}


def main():
    check = "--check" in sys.argv
    root = _lib.project_root()
    cfg = _lib.load_config(root)
    out_rel = cfg["guardsOutput"]
    out_path = os.path.join(root, out_rel)

    guards, missing_block = collect(root, cfg)
    payload = {"count": len(guards), "guards": guards}
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    rep = _lib.Reporter("change-guards")
    for rel in missing_block:
        rep.fail(rel, "no @guard block. Every guard states what falls through without it\n"
                      "and what to extend when your field is new. Add:\n"
                      "  * @guard watches: ...\n  * @guard extend: ...")
    dupes = duplicate_ids(guards)
    for gid, paths in sorted(dupes.items()):
        rep.fail("duplicate guard id '%s'" % gid, "\n".join(paths))

    if check:
        existing = _lib.read(out_path) if os.path.exists(out_path) else ""
        if existing != rendered:
            old_ids = set()
            try:
                old_ids = set(g["id"] for g in json.loads(existing or "{}").get("guards", []))
            except ValueError:
                pass
            new_ids = set(g["id"] for g in guards)
            detail = ["%s is out of date. Run: tools/run change-guards" % out_rel]
            for gid in sorted(new_ids - old_ids):
                detail.append("  + %s (guard exists, list does not know it)" % gid)
            for gid in sorted(old_ids - new_ids):
                detail.append("  - %s (listed, guard gone or renamed)" % gid)
            if not (new_ids ^ old_ids):
                detail.append("  same guards, changed content (watches/extend/reads/exclusions)")
            rep.fail("stale list", "\n".join(detail))
        rep.note("%d guard(s) declared" % len(guards))
        sys.exit(rep.finish())

    if rep.findings:
        sys.exit(rep.finish())

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(rendered)
    print("change-guards: wrote %d guard(s) to %s" % (len(guards), out_rel))
    by_app = {}
    for g in guards:
        by_app[g["app"]] = by_app.get(g["app"], 0) + 1
    for app in sorted(by_app):
        print("  %-12s %d" % (app, by_app[app]))
    sys.exit(0)


if __name__ == "__main__":
    main()
