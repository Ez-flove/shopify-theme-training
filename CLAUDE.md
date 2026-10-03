# CLAUDE.md

Guidance for Claude Code in this repository.

## What this is

A workspace for practising Shopify theme development. The theme is **Dawn v16.0.0**, copied
without history from `github.com/Shopify/dawn` tag `v16.0.0` on 2026-10-01; `docs/dawn-README.md`
is Dawn's own README, including its theme code principles. Each training exercise is a change to
this theme and goes through the claude-flow-kit lifecycle: brief → spec → plan → build → guard →
verify.

This is a learning repo. When a plan or a change uses a Shopify concept that is not obvious — a
Liquid object, a schema setting type, the Section Rendering API, a theme editor event — say in
one sentence why it is the right tool and link the shopify.dev page.

## Workspace

```
layout/ sections/ blocks/ snippets/   the theme — Dawn v16.0.0
templates/ config/ locales/ assets/
docs/exercises/<EX-ID>/               the trainer's brief (verbatim) and design, per exercise
docs/specs/features/                  one spec per exercise
docs/plans/                           one plan per change
docs/architecture/                    change-guards.json, shared-rules.json
tests/guards/                         guards, on Node's built-in test runner
tools/                                tools/run <tool>
```

Shopify CLI uploads only the theme folders, so `docs/`, `tests/` and `tools/` never reach the
store. The kit's source (the `flow` plugin and the template) lives outside this repo, at
`~/Desktop/claude-flow-kit`.

## Stack

| Part | Stack |
|---|---|
| Theme | Liquid · JSON templates and section groups · vanilla JS custom elements · CSS — no build, no package.json |
| Tooling | Shopify CLI 4.8.3 · Theme Check · Node 22 (`node --test`, `node --check`) · Python 3.8 (kit tools) |

## Commands

Every command is declared in **`flow.config.json`** → `commands`; the workflows read it from there.

```bash
shopify theme dev --store ngocmx-training  # dev theme on the store + preview at http://127.0.0.1:9292
                                           # runs until stopped; asks for the storefront password
                                           # --theme-editor-sync: not on the first run against a new
                                           # dev theme — it pulled the store's empty settings_schema.json
                                           # over the local one (docs/plans/2026-10-01-training-setup.md)
shopify theme check --fail-level error     # lint. Dawn v16 baseline: 0 errors, 9 warnings. "Files
                                           # inspected" also counts JSON outside the theme folders
                                           # (flow.config.json, docs/), so it is not a baseline
tools/run js-syntax                        # node --check over assets/*.js
node --test 'tests/guards/*.test.js' 'tests/unit/*.test.js'   # guards + unit tests of assets/*.js
tools/run change-guards [--check]          # regenerate / check docs/architecture/change-guards.json
tools/run shared-rules                     # a rule written in two files that no longer agree
tools/run mutate <file> --sub 'OLD=>NEW' -- node --test tests/guards/<guard>.test.js
tools/run fetch-shot "<text with links>"   # prnt.sc links or image URLs → .local/shoot/<id>.<ext>
```

**When the user sends screenshot links, fetch them before answering:** `tools/run fetch-shot`
with the whole message (it picks out every link), then Read each saved file. A prnt.sc link is an
HTML page — reasoning from the URL alone means reasoning without the screenshot. A link it refuses
(removed, unknown id, another site's page) is reported to the user as such, not guessed around.
`.local/shoot/index.tsv` maps each file back to its link; `.local/` is git-ignored, so a screenshot
that must be kept as an exercise's design goes to `docs/exercises/<EX-ID>/design/` via `--out`.

There is no build and no typecheck in the usual sense; `build` is empty on purpose. A change is
proven only by rendering it — `.claude/rules/shopify-theme.md` §3 is the checklist.

## How it fits together

Work flows top to bottom. **Each layer links down only; a fact lives in exactly one place.**

```
ENTRY      /flow-feature  /flow-fix-bug  /flow-enhance
           /flow-review   /flow-review-pr
           /flow-guard    /flow-commit
             │  pick one; it tells you the process
RULES      .claude/rules/*   hard constraints, and why each exists:
             │   harness ................. thinking quality, the no-plan-no-code gate
             │   business-logic-analysis .. root cause, source-of-truth order, finding tags
             │   change-reaches-every-end . which ends must know when you add a field
             │   shopify-theme ........... those ends in a theme, theme flaw classes, browser verify
             │   code-security ........... the theme security checklist
             │   security ................ what the agent must never do
             │   writing-style ........... how to word anything a person reads
KNOWLEDGE  this file + docs/
EXECUTION  tools/run <tool>   ·   flow.config.json holds everything project-specific
```

## Non-negotiables

- **No plan, no code.** A change gets a plan in `docs/plans/` before the first edit. Reading and
  measuring need no plan — go and measure freely.
- **Every exercise starts with its brief and a spec.** The brief goes into
  `docs/exercises/<EX-ID>/brief.md` verbatim; the spec in `docs/specs/features/` quotes it and
  lists every ambiguity as an OPEN QUESTION. The spec is approved before code.
- **Never publish, delete, or push to the live theme.** Work through `shopify theme dev`.
- **Done means seen in the browser and the theme editor**, not only a clean Theme Check.
- **Never commit or push unless explicitly asked.**
- **Before you add a setting, a block or a string, read `docs/architecture/change-guards.json`
  and `.claude/rules/shopify-theme.md` §1** — they name what already watches, and every end.
- **Evidence, not assertion.** "Done" needs the actual command output and the screenshots.

## Superpowers alongside the flow kit

The `superpowers` plugin is enabled for this project. Its own `using-superpowers` skill ranks
CLAUDE.md above its skills, so the rules below win wherever a skill says otherwise.

**The `/flow-*` commands own the lifecycle; superpowers skills are techniques used inside it.**

| Flow phase | Superpowers skill that fits |
|---|---|
| `/flow-feature` Gate 1 — spec | `brainstorming`: one clarifying question at a time; anything unanswered becomes an OPEN QUESTION in the spec |
| `/flow-feature` Gate 2 — plan | `writing-plans`: bite-sized tasks with exact files, inside the kit's plan format (the four points, the ends that must know, the status table) |
| Build | `executing-plans`, or `subagent-driven-development` for a plan with independent tasks |
| `/flow-fix-bug` Phases 1–2 | `systematic-debugging` |
| Before saying done | `verification-before-completion`, plus `.claude/rules/shopify-theme.md` §3 |
| `/flow-review` | `requesting-code-review` / `receiving-code-review` |

**Where files go — overrides the skills' defaults.** Specs go to `docs/specs/features/`, plans to
`docs/plans/`, named as `docs/WORKFLOW.md` says. Never `docs/superpowers/`: the Stop hook and every
`/flow-*` command read only the kit's paths, so a plan there counts as no plan.

**No commit as a step of a skill.** Brainstorming's "write the design doc and commit", writing-plans'
"frequent commits", the worktree skill's "add to .gitignore and commit", and finishing a branch
with a push all wait for the user to ask, like every other commit here.

**What "a failing test first" means in this theme.** Liquid cannot be rendered locally, so TDD
takes the form that can actually fail:

- A rule a source-reading guard can see (a schema/render mismatch, a missing translation key, a
  hardcoded route) → write or extend the guard in `tests/guards/` first, run it red, then the change.
- Logic in `assets/*.js` that can run outside the browser → a `node --test` case first.
- Markup, styling and theme-editor behaviour → the failing check is the browser checklist: show the
  page **without** the behaviour on the `shopify theme dev` preview (screenshot or page text in the
  plan) before the change, and with it after.

Never write a test that only asserts the new Liquid text exists in the file — it cannot fail for
the reason the exercise exists.

**Worktrees are off by default.** Each one would need its own `shopify theme dev` development
theme. Use one only when the user asks; it goes in `.worktrees/`, which is already ignored.

## Want to… → start here

| Goal | Entry |
|---|---|
| Do an exercise | `/flow-feature EX-<nn>` |
| Fix a bug | `/flow-fix-bug` |
| Change existing behaviour | `/flow-enhance` |
| Review a scope | `/flow-review` · a PR → `/flow-review-pr` |
| Add or audit a guard | `/flow-guard` |
| Commit | `/flow-commit` |

## Commit convention

```
<Type>(<Scope>): <short description>

<what changed and why — the mechanism, in prose>
```

Types: `Feature` · `Fix` · `Refactor` · `Foundation` · `Docs` · `Guard`. Scope is the exercise id
(`EX-01`) or the area (`setup`, `guards`). Messages in English.
