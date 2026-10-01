# A change has to reach every end

When you add a field or a rule, the question is not "did I write it" but **which ends have to
know**. Nearly every recurring defect is an end that did not: a payload field one branch of a
create-path forgot, a column a duplication routine never copied, a guard fixed in one app and left
in the other.

The tools for this exist in `tools/`. What is usually missing is the step where you decide which one
applies. That is what this page is.

---

## The four tools, and when each applies

**The compiler can see both ends → make it ask.** When both ends are typed against the same
contract, an exhaustive `Record<keyof Contract, …>` turns a forgotten field into a build error.
Declare `copy` or `{ rebuild: reason }` for every key — a deliberate skip and an oversight are the
same empty space otherwise.

**One value means two things → split the type, don't add a flag.** A `save()` that returns `true`
for both "written" and "nothing to write" makes every call site say "saved successfully" for both.
Three names force every caller to choose:

```ts
type SaveOutcome = 'saved' | 'nothing-to-save' | 'invalid'
```

A flag someone forgets to read fails silently; a type does not.

**Both ends are hand-written → a test reads the source.** A store's field literal against the schema
columns, a mapper against a DTO, one app's guard against the other's. Compare the field sets and
name every deliberate exclusion **with its reason**, so "absent" is always a decision. These live
under the paths in `flow.config.json` → `guardGlobs`.

**You do not know where the copies are → declare the rule once and go looking.** The three tools
above all assume somebody already knows the rule lives in two places. The expensive failures are the
ones where nobody knew — a threshold written a second time with `>=` where the rule says `>`,
surviving for months because the only screen that obeys it is one nobody demos.

Declare it in `docs/architecture/shared-rules.json` and `tools/run shared-rules` makes two passes:

| | catches |
|---|---|
| **compare** | the rule is declared in N files and they disagree |
| **discover** | some file uses the rule's symbol and is **not in the manifest at all** |

**Discover asks one of two questions, and picking the wrong one makes it useless** —
`discover.kind`:

| | asks | right for |
|---|---|---|
| `mention` (default) | which file **names** the symbol | a rule with few legitimate mentions — a threshold, a tab order |
| `declaration` | which file **declares** it | an enum that many consumers import |

Under `mention`, a widely-imported enum returns twenty files, nineteen of them correct consumers.
The tempting fix — nineteen `allowedElsewhere` rows — is the failure this page warns about below:
the manifest fills with rows that protect nothing. Asking who *declares* it narrows the answer to
the files that really hold a copy. **A declaration is a copy; a use is a consumer.**

**Its ceiling, stated plainly.** Discover finds new uses of a rule **already declared**. It cannot
find a rule nobody has declared — which is exactly the state the drifting threshold was in before
its first row existed. It narrows the hole; it does not close it. Closing it means the rule stops
being hand-copied at all: generate it from one source.

---

## Four things the manifest teaches, all worth not rediscovering

- **A `mustMatch` that names a VALUE is not a check; match the SHAPE the value sits in.** It is a
  substring search over the whole file, so a bare `'MULTIPLE'` is satisfied by an unrelated array
  three hundred lines away, and deleting the rule from the function it guards changes nothing.
  `tools/run shared-rules` refuses a bare quoted pattern outright. A key that pins the value
  (`btnLabel: 'Start survey'`) has structure and is fine.
- **A docblock naming the rule is documentation, not a second copy.** The tool strips comments
  before searching. The wrong reaction to a red run is an exception per docblock: the manifest fills
  with rows that protect nothing, and the next reader learns that red means "add an exception".
- **A negative-case mutation must stay GREEN.** `tools/run mutate` only knows one direction, so it
  reports green as "does not measure this". A field declared as deliberately different has to
  survive being changed — run it with `--expect green`. Otherwise the exclusion map is decoration.
- **A guard asserting an ABSENCE is green for two different reasons: nothing is wrong, or there was
  nowhere to look.** Same colour, and the guard cannot tell them apart unless it proves it is
  looking at the right thing — *in the same test case*, because cases run independently and a
  neighbouring assertion can be deleted as redundant. The reliable fix is structural: build the
  bad-list from a **known-non-empty constant** rather than from the corpus, so an empty corpus fails
  loudly instead of passing quietly. Where that is impossible, assert the corpus is real before
  concluding.
- **A comment warning about a trap does not stop the trap.** If three files carry a docblock
  explaining a hazard, the fourth will do it anyway. Write the guard.

---

## And when you find the second copy: where to move the rule is itself a decision

The four tools above all *detect* a rule that has been written twice. Closing it is a separate
choice, and "add an exception to the manifest" is not one of them. Move the rule to where both ends
must go through it: inside a module, its own domain layer; across modules, a shared contract plus an
adapter, with the rule in the base rather than only in the signature. **A guard that reads source is
the last net for what the compiler cannot see — not the place the rule lives.**

---

## In this theme, the ends are listed

`shopify-theme.md` §1 names every end for a section setting, a block type, a storefront string, a
snippet parameter, a global setting, a variant-dependent element, a metafield and a cart change.
Start there; the TypeScript examples above show the mechanism, not this stack.

---

## Before you add a field, read the list

**`docs/architecture/change-guards.json`** — every guard, what it protects, and what to extend when
your field is new. Generated by `tools/run change-guards` from each guard's own docblock, so it
cannot drift from the guards themselves. Read it before writing the field, not after.

A guard declares itself in its top docblock:

```ts
/**
 * @guard watches: what falls through if this is not extended
 * @guard extend:  what to change when your field or rule is new
 * @guard caught:  (optional) a real defect this caught, with a date
 */
```

Everything else — path, app, the names of its exclusion maps, the files it reads — is derived, which
is the half that used to go stale. `tools/run change-guards --check` fails when the list is behind.

## What a new guard owes you

- **Prove it fails, with `tools/run mutate`.** Break the thing it covers and watch it go red. A
  guard that has never failed measures nothing, and is indistinguishable from one that works. Use
  the tool rather than doing it by hand: it refuses to report anything unless the file actually
  changed, because a mutation that did not land produces a green run that means neither "safe" nor
  "has a gap".
- **One mutation per condition.** Two mutations failing *different* cases prove the conditions are
  pinned apart. If a single mutation reddens every case, the cases are one case written five ways.
- **Name what is missing, don't count it.** Assert the list of missing fields is empty, so the
  failure says *which* field fell through. A count says only that you are unhappy.
- **Say what it cannot catch.** Asking the DOM whether an element exists does not ask the layout, so
  a field hidden by CSS still counts as present. A limit stated is a limit the next reader can work
  around; a limit discovered is another round trip.
