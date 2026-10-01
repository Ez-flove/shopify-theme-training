#!/usr/bin/env python3
# Description: check business rules that live in more than one file (compare + discover)
"""
A rule written by hand in two places drifts, and the copy nobody looks at is the one that
goes wrong. Declare the rule once in the manifest and this makes two passes:

  compare   the rule is declared in N files and they disagree
  discover  some file uses the rule's symbol and is NOT in the manifest at all

Discover is the half that finds what nobody knew about. Its ceiling, stated plainly: it
finds new uses of a rule ALREADY declared. It cannot find a rule nobody has declared.

    tools/run shared-rules                    both passes
    tools/run shared-rules --mode discover    just the second
    tools/run shared-rules --rule <id>        one rule
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib  # noqa: E402

# A mustMatch naming a VALUE is not a check — it is a substring search over the whole file,
# so a bare 'MULTIPLE' is satisfied by an unrelated array 300 lines away. Match the SHAPE
# the value sits in. A key pinning the value (btnLabel: 'Mojarib Survey') has a ':' and is fine.
STRUCTURAL = set("><=!()[]{}:?&|+*\\^$")

DECLARATION = "(?:export\\s+)?(?:default\\s+)?(?:const|let|var|enum|type|interface|class|function|def|abstract\\s+class)\\s+%s\\b"


def load_manifest(root, cfg, rep):
    rel = cfg["sharedRulesFile"]
    path = os.path.join(root, rel)
    if not os.path.exists(path):
        rep.fail(rel, "manifest missing. Create it with {\"rules\": []} and add a row per\n"
                      "rule that is written by hand in more than one file.")
        return None, rel
    try:
        data = json.loads(_lib.read(path))
    except ValueError as exc:
        rep.fail(rel, "not valid JSON: %s" % exc)
        return None, rel
    return data.get("rules", []), rel


def validate_rule(rule, rep):
    rid = rule.get("id") or "<rule with no id>"
    ok = True
    if not rule.get("statement"):
        rep.fail(rid, "no 'statement'. Write the rule as a sentence — the next reader needs to\n"
                      "know what is being protected, not only which regex to keep green.")
        ok = False
    files = rule.get("files") or []
    if not files:
        rep.fail(rid, "no 'files'. A rule with no homes protects nothing.")
        ok = False
    elif len(files) < 2 and not rule.get("singleHome"):
        rep.fail(rid, "only one file listed. Either the second copy has not been found yet, or\n"
                      "the rule really does live in one place — say \"singleHome\": true if so.")
        ok = False
    for pattern in rule.get("mustMatch") or []:
        stripped = pattern.strip()
        if not any(ch in STRUCTURAL for ch in stripped):
            rep.fail("%s / mustMatch %r" % (rid, pattern),
                     "this pattern names a VALUE, not a shape. It is a substring search over the\n"
                     "whole file, so an unrelated line elsewhere satisfies it and deleting the rule\n"
                     "from the function it guards changes nothing. Match the expression instead —\n"
                     "  bad:  'MULTIPLE'\n"
                     "  good: totalOptions\\s*>\\s*DROPDOWN_MIN_OPTIONS")
            ok = False
        try:
            re.compile(pattern)
        except re.error as exc:
            rep.fail("%s / mustMatch %r" % (rid, pattern), "not a valid regex: %s" % exc)
            ok = False
    kind = (rule.get("discover") or {}).get("kind", "mention")
    if kind not in ("mention", "declaration"):
        rep.fail(rid, "discover.kind must be 'mention' or 'declaration', got %r.\n"
                      "A declaration is a copy; a use is a consumer. When a symbol has many honest\n"
                      "consumers, say 'declaration' so the pass names only the files that redeclare it."
                 % kind)
        ok = False
    return ok


def compare(root, cfg, rules, rep):
    for rule in rules:
        rid = rule["id"]
        patterns = rule.get("mustMatch") or []
        for rel in rule.get("files") or []:
            path = os.path.join(root, rel)
            if not os.path.exists(path):
                rep.fail("%s / %s" % (rid, rel),
                         "listed in the manifest but not on disk. Moved or deleted — update the row.")
                continue
            if not patterns:
                continue
            body = _lib.strip_comments(_lib.read(path))
            for pattern in patterns:
                if not re.search(pattern, body):
                    rep.fail("%s / %s" % (rid, rel),
                             "does not match  %s\nrule: %s" % (pattern, rule.get("statement", "")))


def discover(root, cfg, rules, rep):
    corpus = _lib.walk_files(root, cfg)
    if not corpus:
        rep.fail("discover", "no source files matched sourceGlobs %s — the pass would be green\n"
                             "because it had nowhere to look, which is not the same as clean."
                 % cfg["sourceGlobs"])
        return
    rep.note("discover read %d source file(s)" % len(corpus))
    cache = {}
    for rule in rules:
        rid = rule["id"]
        spec = rule.get("discover") or {}
        symbols = spec.get("symbols") or []
        if not symbols:
            continue
        kind = spec.get("kind", "mention")
        known = set(rule.get("files") or []) | set(spec.get("allowedElsewhere") or [])
        for symbol in symbols:
            needle = (DECLARATION % re.escape(symbol)) if kind == "declaration" else r"\b%s\b" % re.escape(symbol)
            probe = re.compile(needle)
            hits = []
            for rel in corpus:
                if rel in known:
                    continue
                body = cache.get(rel)
                if body is None:
                    body = _lib.strip_comments(_lib.read(os.path.join(root, rel)))
                    cache[rel] = body
                if probe.search(body):
                    hits.append(rel)
            for rel in hits:
                verb = "declares" if kind == "declaration" else "names"
                rep.fail("%s / %s %s %s" % (rid, rel, verb, symbol),
                         "not in the manifest. Either it is a legitimate consumer — add it to\n"
                         "discover.allowedElsewhere — or it is a third copy of the rule, which is\n"
                         "the case this pass exists to find.\nrule: %s" % rule.get("statement", ""))


def main():
    argv = sys.argv[1:]
    mode = "both"
    only = None
    if "--mode" in argv:
        mode = argv[argv.index("--mode") + 1]
    if "--rule" in argv:
        only = argv[argv.index("--rule") + 1]
    if mode not in ("both", "compare", "discover"):
        _lib.die("--mode must be both, compare or discover")

    root = _lib.project_root()
    cfg = _lib.load_config(root)
    rep = _lib.Reporter("shared-rules")

    rules, rel = load_manifest(root, cfg, rep)
    if rules is None:
        sys.exit(rep.finish())
    if only:
        rules = [r for r in rules if r.get("id") == only]
        if not rules:
            _lib.die("no rule with id %r in %s" % (only, rel))

    usable = [r for r in rules if r.get("id") and validate_rule(r, rep)]
    if mode in ("both", "compare"):
        compare(root, cfg, usable, rep)
    if mode in ("both", "discover"):
        discover(root, cfg, usable, rep)

    rep.note("%d rule(s) in %s" % (len(rules), rel))
    sys.exit(rep.finish())


if __name__ == "__main__":
    main()
