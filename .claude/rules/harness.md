# Thinking Quality Rules

These apply whenever you are executing one of the `/flow-*` workflows. They correct recurring
thinking errors that no linter can catch. Sibling of `writing-style.md` — that file is about the
words that come out; this one is about what you believed before you wrote them.

## No plan, no code — a hard gate

**Do not edit a file until the plan for that change exists in `docs/plans/`.** Not in chat, not in
your head, not "I'll write it up after". A plan that arrives after the edit is a description, and a
description cannot be disagreed with before the cost is paid.

The plan for a change states four things, and they fit in a few lines:

1. **What is wrong** — in the user's terms, not the code's
2. **Where** — `file:line`, measured, not guessed
3. **What changes** — and what deliberately does not
4. **What will prove it** — the exact check, including the mutation that must turn it red

Two things do **not** need a plan: reading, and measuring. Go and measure freely — that is how
points 1 and 2 get filled in.

## Track progress in the plan, as you go

**The plan is the progress record, and it is updated when a thing changes state — not at the end
of the day.** A plan that only ever grows is a wish list.

- Status moves the moment it moves: measured → planned → done → verified.
- When an item closes, the evidence goes **in the plan**, not only into chat. Chat scrolls away.
- When something is deferred, it goes to `docs/tech-debt.md` **at the moment of deferring**, with
  what would unblock it — not collected later from memory.
- When a decision is reversed, it stays in the decision log, struck through, with who reversed it.

## Never state an assumption as a finding

**Every claim is either measured or labelled.** If it has a `file:line`, a command output, a commit
hash, or a screenshot behind it, write it plainly. If it does not, say what it is — "suspected",
"needs measuring", `NOT_REPRODUCED` — and name the one check that would settle it.

The expensive mistakes are rarely careless readings. They are careful readings of **too small a
surface**, published without the sentence that says how far the search went. So when your
conclusion is that something is **absent** — a field, a call, a request, a hook — say where you
looked. An absence claimed without a boundary is an assumption wearing a finding's clothes.

## Before concluding a fix does not work

A fix that measures as broken is a diff, a build, and a running process — and only the first was in
your change. Check the last two before reading a single line deeper.

A build error can keep a watcher's previous child alive **silently**, so the running app serves code
from before your edit and nothing says so. If the serving process predates the edit, nothing
measured against it means anything. Check when the process started, and check that the build is
actually passing, before you rewrite correct code.

## When reading test output

**Read the file/suite count, not just the test count.** "742 tests passed" beside "1 suite failed"
is not a pass — a file that fails to compile contributes zero tests and zero failures, so the
reassuring number is the one that cannot see the problem. A non-zero failed-file count is a red run
whatever the test count says.

**When the working tree holds someone else's work, gate on your own files.** Totals are not
comparable to a baseline another session has moved. Filter to the files in your diff and report
both numbers, saying whose work the difference belongs to. Never let a number stand in for a
reading.

## When receiving feedback or review findings

**Do not immediately start editing.** First: ask why the feedback exists and what root cause it
points at; consider the full cross-file impact; propose the approach. Only then implement. Skipping
this is how one-line fixes cascade into broken builds.

## Before changing infrastructure code

Infrastructure means auth flow, router config, build scripts, migrations, CI, and anything under a
directory the conventions call immutable.

1. **Read the git log first** — `git log --oneline --follow -- <file>` to learn why the current code
   exists. If a commit says "switch to X", there was a reason.
2. **Never suggest "clear localStorage / cookies" as a fix.** If browser state produces wrong
   behaviour, the code has a bug.
3. **Do not revert someone else's work** without understanding the context.

## When following an existing pattern

Before copying a pattern, ask whether the spec has changed since it was established, whether the
architecture has moved on, and whether a better example now exists in the codebase. "Because that's
how we did it before" is not a reason.

## When about to say "done", "verified", or "complete"

Show evidence. Not "I verified X" — show the output: the failing check now passing, the build
result, the specific spec rules you checked with quotes, the exact numbers. If you cannot show
evidence, you have not verified — you have guessed.
