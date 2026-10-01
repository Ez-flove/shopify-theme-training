# Business-Logic Analysis Mindset

The root-cause discipline shared by every workflow that **changes or judges behaviour** —
`/flow-fix-bug`, `/flow-enhance`, `/flow-review`, `/flow-review-pr`. Sibling of `harness.md`: that
file holds general workflow thinking rules, this one holds the specific analysis mindset.

The **trigger** is whatever kicked the work off — a failing test, a bug report, a ticket assertion,
an enhancement request, a "this is slow" complaint.

---

## 1. Correctness rules (non-negotiable)

**Correctness comes from the sources named in `flow.config.json` → `sourcesOfTruth`, in that
order.** Nothing else decides: not a test-case sheet's wording, not a bug report, not a ticket, not
a plan, not a code comment, not prior memory, not convention.

- **No assumptions — go and read.** On any ambiguity, re-open the source before judging or fixing.
  If every source is silent, or they contradict each other in a way the order does not settle, raise
  it as an **OPEN QUESTION** tagged `SPEC_GAP`. Do not guess, and do not "fix" to match the
  trigger's wording.
- **A more recent source wins over an older one of the same rank.** Feedback recorded against a
  build post-dates the document it comments on.
- **The trigger is a CLAIM, not a fact.** Verify it is real — trace the code path, or reproduce it
  (a UI step, an API round-trip, a measurement) — and confirm the behaviour actually contradicts the
  spec, **before** planning a fix. Record it as a concrete failure scenario: *concrete inputs →
  observed wrong output vs spec-expected output.* If it does not reproduce, or the trigger
  contradicts the spec, do not plan a code fix — tag it `NOT_REPRODUCED` / `SPEC_GAP` and surface
  it.

### When a prototype is one of the sources

A clickable prototype or design bundle with no backend is authoritative only as far as the wire.

**It decides** what the user sees and can do: layout and states, which control appears under which
condition, gating by status, ordering, seeded defaults, copy for labels and errors, client-side
validation messages, interaction rules.

**It cannot decide** persistence, server validation, data lifecycle, permissions, or entitlements.
Where it fakes those — a timer standing in for a save, a toast instead of a request, a hardcoded
status — that is the prototype having no server, not a specification.

The test: if a behaviour needs a database or an API call to be real, the prototype's version of it
carries no authority. **An absence is especially weak evidence** — a prototype omits server concerns
by construction, so "the design doesn't validate this" almost always means "the design couldn't",
not "it shouldn't be validated".

---

## 2. Root cause via the flaw-class lens

Don't stop at the surface symptom. A UI symptom is often a contract or transaction defect. Walk this
list, find the *mechanism* that is broken, and **fix the mechanism, not the symptom.**

In this theme, walk `shopify-theme.md` §2 as well — editor lifecycle, variant change, blank values
and the rest have no row here.

| Class | What to look for |
|---|---|
| **Missing / wrong status check** | A guard absent, or one status where the spec means two. Map the spec's per-status rule to the actual condition. |
| **Missing UI** | The element or interaction was never implemented. |
| **Contract drift** | Client payload type vs server DTO — single vs array, required vs optional, field names. Regenerate the generated contract after any server-side change. |
| **ID lifecycle** | New entities carry client-side temporary ids until save. Are they remapped everywhere they are referenced? Orphans mean dropped or mis-keyed rows. |
| **Transaction order** | Dependent steps in the wrong order — entities must exist before anything referencing their real ids. |
| **Sequence / counter drift** | Human-friendly ids from a counter that can fall behind rows inserted out of band, then collide. Should be self-correcting. |
| **Uniqueness / dedupe** | Before a batch insert, are duplicate keys possible after remapping or merging? Dedupe first. |
| **State races** | Reading state on the same tick after an async update → stale value, dropped edits, spurious validation. Needs a ref or a restructure. |
| **Cache invalidation** | After a mutation, do dependent queries actually refetch? Prefix match vs exact key match. |
| **Save-model consistency** | An immediate per-field write that breaks a "nothing persists until Save" model — it should fold into the batch. |
| **Graceful degradation** | One invalid sub-item must **skip**, not roll back the whole save. A failed submit must **preserve** the user's draft. |
| **Cross-audience divergence** | The same flow behaving differently in two apps — different endpoints, verbs, DTOs, save models, or one app missing a rule the other enforces. Where parity is intended, reconcile both. |
| **Server-side gap** | The endpoint, field, or logic is missing entirely. |

---

## 3. Think before patching

- **Consider the full cross-file impact before editing.** Does the fix touch other DTOs, mappers,
  forms, the generated contract, the other app, or tests? Fix them together — never leave the change
  half applied. `change-reaches-every-end.md` is the checklist for deciding which ends must know.
- **Fix the mechanism, not the symptom.** No band-aids. A UI symptom whose cause is a contract
  defect is fixed at that layer.
- **Keep the change scoped to the defect.** Don't opportunistically refactor unrelated code — but do
  fix the actual mechanism even when that is more than one line.
- **Auto-fix only clear correctness defects.** For product choices, or anything tagged `SPEC_GAP`,
  present the options and **wait** for a decision before changing code.

---

## 4. Classify each finding

Tag every finding so the plan and the summary are traceable:

- `DEFERRED` — explicitly deferred or not yet built
- `WRONG_CONDITION` — the logic exists but the condition is incorrect
- `MISSING_CHECK` — a status, permission, or visibility check is absent
- `MISSING_UI` — the element or interaction is not implemented
- `MISSING_BACKEND` — server endpoint, field, or logic missing
- `DATA_MISMATCH` — client/server contract mismatch
- `REGRESSION` — previously working, broken by a later change
- `SPEC_GAP` — the spec does not cover this, or is ambiguous (raise as an OPEN QUESTION)
- `SPEC_MISSED` — the spec covers it and the implementation misread it
- `NOT_REPRODUCED` — it did not reproduce, or the trigger contradicts the spec (no code fix)

---

## 5. Verify with evidence

Per `harness.md`, no "done" without evidence — **show the actual command output.**

- Run the project's build, lint and test commands (from `flow.config.json` → `commands`) for every
  app touched. Call out **pre-existing** failures separately from ones your change introduced; never
  claim a clean run you did not get.
- **Reproduce broken → passing.** Re-run the exact failure scenario from §1 and confirm it now
  matches the spec-expected result.
- After any contract change, regenerate the contract for every app that consumes it, and prove a
  shared fix for **both** audiences, not one.
- A finding is only FIXED once you can show the evidence. Otherwise it stays `DEFERRED`,
  `NOT_REPRODUCED`, or needs-decision in the summary.
