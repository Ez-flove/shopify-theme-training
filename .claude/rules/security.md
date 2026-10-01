# Agent Security Rules

What the agent must never do. For code-level standards see `code-security.md`.

## 1. Secrets & environment files

- **Never read, edit, write, or delete environment files** — `.env` and its variants, `.denv`, or anything
  the project treats as a secrets file
- **Never read system secrets** — `/etc/shadow`, `/etc/passwd`, `~/.ssh/`, `~/.aws/`, `~/.gnupg/`
- **Never log, print, or expose secrets** — API keys, tokens, passwords, service credentials
- **Never commit secrets** — check `.gitignore` before staging, and warn if a credentials or key
  file is about to be committed
- **Never hardcode secrets in source** — read them through the project's config layer

## 2. File system boundaries

- **Never write outside the project directory** — every edit and write stays inside the repo root or
  `~/.claude/`. If a file genuinely belongs elsewhere, say so and get agreement first
- **Never modify generated files** — anything a generator owns, plus lockfiles
- **Never modify the directories the project conventions mark immutable** during feature work

## 3. Dependency security

- **Pin exact versions** — no `^`, no `~`, no `latest`
- **No unnecessary packages** — add one only when there is no reasonable alternative
- **Verify authority before installing** — confirm the official org, the exact package name, not a
  typosquat or an abandoned fork; check advisories
- **Install from the app directory that owns the dependency**, never from the repo root by habit

## 4. Database safety

- **Never delete rows without a WHERE clause, and never without asking first**
- **Never reset a migration state** without explicit approval — dev data has been lost that way
- **Never accept a destructive migration.** If the tool warns about data loss — a dropped column, a
  type change, a table reset — stop. Use the non-destructive path: add a default, make it nullable
  first, split it into multiple steps
- **Patch the SQL for constraint migrations** — backfill defaults and clean orphaned rows before
  adding NOT NULL, unique, or foreign-key constraints

## 5. Git safety

- **Never force push. Never hard reset. Never `git clean -f`.**
- **Never commit unless explicitly asked. Never push unless explicitly asked.**
- **Read `.gitignore` before committing** — avoid staging ignored or sensitive files
- **Never skip the commit hooks** (`--no-verify`)

## 6. Privilege & infrastructure

- **Never use `sudo` or `su`**
- **Never inspect the network** with sniffing tools
- **Never recursively force-delete**
- Reach containers through the project's documented path, not host-level service manipulation

---

## Enforcement layers

These rules are not only written down. Three layers actually stop the action:

| Layer | Where | What it does |
|---|---|---|
| Permission deny list | `.claude/settings.json` → `permissions.deny` | Rejected before execution, no hook needed |
| PreToolUse hooks | `tools/hooks/guard-paths.py`, `guard-read.py`, `guard-bash.py` | Inspect the tool input and block: secrets files, writes outside the project, reads of system secrets, unbounded destructive SQL, force push, hard reset, `--no-verify` |
| Written rules | this file | Everything a pattern cannot decide — package authority, migration judgement, "ask first" |

**Two things worth knowing about the hook layer, both learned the hard way.**

A path in a hook config that points at a script which does not exist fails **every time the hook
fires**, and unless the command ends in `|| true` the failure is silent noise nobody reads. After
moving or deleting a hook script, check every `settings.json` that names it.

The Bash guard matches the **text** of a command, so a heredoc that merely spells out one of its
patterns is blocked exactly like a command that runs it. This is a false positive with a real
reason: a guard that lets prose through lets a command dressed as prose through. Split the write or
reword the prose — do not loosen the pattern.
