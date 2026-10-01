#!/usr/bin/env python3
# Description: break what a guard protects, run the guard, prove it goes red — then restore
"""
A guard that has never failed is a guard that measures nothing, and it is indistinguishable
from one that works. This applies the mutation, runs the test, restores the file, and says
which of the two you have.

It refuses to report anything unless the file actually changed — a mutation that did not land
produces a green run that means neither "safe" nor "has a gap".

    tools/run mutate <file> --sub 'OLD=>NEW' -- yarn test path/to/guard.spec.ts
    tools/run mutate <file> --drop 'a line substring' -- yarn test ...
    tools/run mutate <file> --sub '>=>>=' --expect green -- yarn test ...
    tools/run mutate <file> --sub 'A=>B' --dry-run

--expect red (default) is the normal direction: the guard must notice.
--expect green is for a NEGATIVE case — a field declared as deliberately different has to
survive being changed, otherwise the exclusion map is decoration. This tool only knows one
direction, so a green run on the default expectation is reported as "does not measure this".
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import _lib  # noqa: E402

USAGE = __doc__.strip()


def parse_args(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)
    target = argv[0]
    rest = argv[1:]
    cmd = None
    if "--" in rest:
        idx = rest.index("--")
        cmd = " ".join(rest[idx + 1:]).strip()
        rest = rest[:idx]
    opts = {"expect": "red", "dry_run": False, "sub": None, "drop": None}
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--sub":
            opts["sub"] = rest[i + 1]; i += 2
        elif arg == "--drop":
            opts["drop"] = rest[i + 1]; i += 2
        elif arg == "--expect":
            opts["expect"] = rest[i + 1]; i += 2
        elif arg == "--dry-run":
            opts["dry_run"] = True; i += 1
        else:
            _lib.die("unknown option %r\n\n%s" % (arg, USAGE))
    if opts["expect"] not in ("red", "green"):
        _lib.die("--expect must be red or green")
    if not opts["sub"] and not opts["drop"]:
        _lib.die("give a mutation: --sub 'OLD=>NEW' or --drop 'substring of the line'")
    if opts["sub"] and "=>" not in opts["sub"]:
        _lib.die("--sub takes 'OLD=>NEW' (literal text, not a regex)")
    if not cmd and not opts["dry_run"]:
        _lib.die("give the guard to run after --  (e.g. -- yarn test path/to/guard.spec.ts)")
    return target, opts, cmd


def mutate(text, opts):
    if opts["sub"]:
        old, new = opts["sub"].split("=>", 1)
        if old not in text:
            return None, "the file does not contain %r, so there is nothing to mutate" % old
        return text.replace(old, new, 1), None
    needle = opts["drop"]
    lines = text.split("\n")
    kept = [ln for ln in lines if needle not in ln]
    if len(kept) == len(lines):
        return None, "no line contains %r, so there is nothing to drop" % needle
    return "\n".join(kept), None


def main():
    root = _lib.project_root()
    target, opts, cmd = parse_args(sys.argv[1:])
    path = target if os.path.isabs(target) else os.path.join(root, target)
    if not os.path.exists(path):
        _lib.die("no such file: %s" % target)

    original = _lib.read(path)
    changed, why = mutate(original, opts)
    if changed is None:
        _lib.die("mutation did not land — %s.\nNothing was run and nothing is reported: a green\n"
                 "run from a mutation that never applied means neither safe nor broken." % why)
    if changed == original:
        _lib.die("mutation produced an identical file. Nothing run, nothing reported.")

    if opts["dry_run"]:
        import difflib
        diff = difflib.unified_diff(
            original.split("\n"), changed.split("\n"),
            fromfile=target, tofile=target + " (mutated)", lineterm="", n=2,
        )
        print("\n".join(diff))
        sys.exit(0)

    backup = tempfile.NamedTemporaryFile(prefix="mutate-", suffix=".bak", delete=False)
    backup.write(original.encode("utf-8"))
    backup.close()
    restored = False

    def restore():
        if not restored:
            shutil.copyfile(backup.name, path)
        os.unlink(backup.name)

    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(changed)
        print("mutate: %s" % target)
        print("  mutation  %s" % (opts["sub"] or ("drop lines containing %r" % opts["drop"])))
        print("  running   %s" % cmd)
        print("")
        # Flush before handing stdout to the child, or our header lands after its output
        # and the report reads as though the guard ran first.
        sys.stdout.flush()
        proc = subprocess.run(cmd, shell=True, cwd=root)
        code = proc.returncode
    finally:
        restore()
        restored = True

    print("")
    print("  file restored; guard exited %d" % code)
    went_red = code != 0
    if opts["expect"] == "red":
        if went_red:
            print("  RESULT  guard measures this — mutation applied, guard went red")
            sys.exit(0)
        print("  RESULT  guard does NOT measure this — the mutation landed and the guard stayed")
        print("          green. Either the assertion never reaches this code, or it asserts an")
        print("          absence over a corpus that had nowhere to look.")
        sys.exit(1)
    if went_red:
        print("  RESULT  negative case FAILS — a deliberate difference must survive being")
        print("          changed. As written, the exclusion is decoration.")
        sys.exit(1)
    print("  RESULT  negative case holds — the deliberate difference survived")
    sys.exit(0)


if __name__ == "__main__":
    main()
