"""Shared helpers for the flow tools. Python 3.8 compatible on purpose."""
import fnmatch
import json
import os
import re
import subprocess
import sys

DEFAULT_CONFIG = {
    "projectName": "project",
    "sourceGlobs": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"],
    "ignoreDirs": [
        "node_modules", ".git", "dist", "build", "coverage", ".next",
        ".turbo", ".cache", "vendor", "__pycache__", ".venv",
    ],
    "ignoreFileGlobs": ["*.generated.ts", "*.gen.ts", "*.d.ts", "*.min.js"],
    "guardGlobs": ["**/__tests__/architecture/*.spec.ts", "**/*.guard.test.ts"],
    "guardRequiredGlobs": ["**/__tests__/architecture/*.spec.ts"],
    "guardsOutput": "docs/architecture/change-guards.json",
    "sharedRulesFile": "docs/architecture/shared-rules.json",
    "apps": [],
    "commands": {
        "test": "yarn test",
        "testFile": "yarn test --",
        "lint": "yarn lint",
        "build": "yarn build",
        "typecheck": "npx tsc --noEmit",
    },
}


def project_root():
    env = os.environ.get("PROJECT_ROOT")
    if env:
        return os.path.abspath(env)
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def load_config(root=None):
    root = root or project_root()
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))
    path = os.path.join(root, "flow.config.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            user = json.load(fh)
        for key, value in user.items():
            if isinstance(value, dict) and isinstance(cfg.get(key), dict):
                merged = dict(cfg[key])
                merged.update(value)
                cfg[key] = merged
            else:
                cfg[key] = value
    return cfg


def walk_files(root, cfg, globs=None):
    """Every tracked-looking source file under root that the config does not exclude."""
    globs = globs or cfg["sourceGlobs"]
    ignore_dirs = set(cfg["ignoreDirs"])
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith(".git")]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if any(fnmatch.fnmatch(name, pat) for pat in cfg["ignoreFileGlobs"]):
                continue
            if not any(match_glob(rel, pat) for pat in globs):
                continue
            out.append(rel)
    return sorted(out)


def match_glob(rel, pattern):
    """fnmatch with ** meaning "any depth", which plain fnmatch does not give us."""
    if "**/" in pattern:
        tail = pattern.split("**/", 1)[1]
        if fnmatch.fnmatch(rel, tail) or fnmatch.fnmatch(os.path.basename(rel), tail):
            return True
        return fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(rel, "*/" + tail)
    return fnmatch.fnmatch(rel, pattern)


BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
LINE_COMMENT = re.compile(r"(?<![:\"'\w])//[^\n]*")
HASH_COMMENT = re.compile(r"(?m)^\s*#[^\n]*$")


def strip_comments(text):
    """A docblock naming a rule is documentation, not a second copy of it."""
    text = BLOCK_COMMENT.sub("", text)
    text = LINE_COMMENT.sub("", text)
    return HASH_COMMENT.sub("", text)


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def git_tracked(root):
    try:
        out = subprocess.check_output(
            ["git", "-C", root, "ls-files"], text=True, stderr=subprocess.DEVNULL
        )
        return set(out.split("\n"))
    except Exception:
        return None


class Reporter:
    """Findings are named, never counted — a count says only that you are unhappy."""

    def __init__(self, title):
        self.title = title
        self.findings = []
        self.notes = []

    def fail(self, subject, detail):
        self.findings.append((subject, detail))

    def note(self, text):
        self.notes.append(text)

    def finish(self):
        for text in self.notes:
            print("  " + text)
        if not self.findings:
            print("%s: clean" % self.title)
            return 0
        print("")
        print("%s: %d finding(s)" % (self.title, len(self.findings)))
        for subject, detail in self.findings:
            print("")
            print("  %s" % subject)
            for line in str(detail).split("\n"):
                print("    %s" % line)
        print("")
        return 1


def die(message):
    sys.stderr.write("error: %s\n" % message)
    sys.exit(2)
