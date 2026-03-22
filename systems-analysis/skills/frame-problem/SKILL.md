---
name: frame-problem
description: Use when reasoning or acting on assumptions that may no longer hold — especially after time has passed, the user has acted between turns, prior actions had untraced side effects, or when accepting a problem framing without questioning it. Triggers on stale state, unexamined non-effects, inherited problem framing, confidence without re-verification, and any gap between when information was gathered and when it's being used.
---

# The Frame Problem

You cannot act or reason without assuming a frame — things you take to stay the same. The frame problem has no general solution (Fodor, 1987). This skill forces you to make frame assumptions explicit, which makes them auditable. An implicit frame can't be checked. An explicit one can. Sources: Fodor (1987), Dennett (1984), Hayes (1973).

## Four Actions

Apply in order when you suspect your frame may be wrong:

| Action | Question | What to do |
|--------|----------|------------|
| **Name the Frame** | What am I assuming stays the same? | State it. "I'm assuming the codebase is the same as when I last read it." "I'm assuming the user's goal is X." If you can't name the assumption, you can't check it. |
| **Check Freshness** | When was this information gathered, and what has happened since? | Check mtimes (`ls -l`) on files you're about to modify — if newer than your last read, re-read them. Turns passed since last read? User mentioned doing something? Your own prior actions had side effects? CI or deployments may have run? |
| **Check Scope** | Am I solving the right problem? | The frame includes the problem definition itself. If the user says "it's a caching issue," that's a frame. The most consequential assumption is often which problem you're solving, not how. |
| **Name the Blind Spots** | What kind of change would my current vocabulary not let me notice? | Your ontology determines what changes are visible to you. This is the hardest action — an admission of bounded rationality, stated out loud. |
| **Rate Confidence** | What part of this frame am I least confident about? | Name it. That's where to direct verification effort — and where to warn the human that your reasoning is weakest. |

## Failure Modes (Dennett's Three Robots)

| Mode | Pattern | Correction |
|------|---------|------------|
| **R1** — ignoring side effects | Acts without considering what else the action touches | Back up. Name the frame. What are you assuming stays the same? |
| **R1D1** — considering everything | Traces every possible implication, never acts | You're past diminishing returns. State the cost of further checking vs. the risk of being wrong. Act. |
| **R2D1** — meta-paralysis | Tries to enumerate what's relevant, which is itself unbounded | The relevance question has no general answer. Check what your model makes salient. Accept residual risk. |

Each robot fails by trying to *solve* the frame problem rather than *manage* it.

## Termination

This skill has no clean stopping rule. Fodor: "The frame problem is just Hamlet's problem viewed from an engineer's perspective." You stop checking when the expected cost of further checking exceeds the expected cost of being wrong. **Say that tradeoff out loud** — don't just silently stop.

## Red Flags

- Reasoning from information gathered many turns ago without re-checking
- "I already know what's in that file" (do you?)
- Accepting the user's diagnosis without examining the frame it assumes
- Confidence that a prior action worked without verifying
- "Nothing else changed" — the universal frame assumption, almost never explicitly checked
- Making a second fix to something that "should have worked the first time" (your frame may be wrong, not your fix)

## Rationalizations

| Thought | Reality |
|---------|---------|
| "I just read that file" | How many turns ago? What has the user done since? |
| "That's not relevant" | Relevance is context-dependent and you chose the context. Check the choice. |
| "I already checked" | You checked under a frame. Has the frame changed? |
| "The user said it's X" | Agreement is not diagnosis. The user's frame is a frame too. |
| "Let me be thorough and check everything" | R1D1. You can't check everything. Name what matters most and why. |
| "This is too simple to have side effects" | R1. Simplicity of your model ≠ simplicity of the system. |
| "I'll verify after" | Post-hoc verification confirms your frame; it doesn't test it. |

## Examples

- [Stale cache assumption](examples/stale-cache-assumption.md) — team debugs cache when the real problem is corrupted migration data
- [Inherited problem framing](examples/inherited-problem-framing.md) — ticket requests rate limiting for a problem that async processing already solved

## Transition Signals

- **Can't name the frame because you don't have a model** → start with **representing-and-intervening**. You need R&I's Represent phase before you can name what you're holding constant.
- **Frame check reveals the problem definition itself is wrong** → return to **representing-and-intervening** (Problem Setting / Schon). The frame error is upstream of any solution.
- **Frame check reveals a regulation mismatch** → switch to **requisite-variety**. The frame was "this regulator is sufficient" and it isn't.
- **Need to establish whether a causal assumption in the frame actually holds** → switch to **design-causal-study**. The frame contains a causal claim that hasn't been tested.
- **Frame is solid, assumptions verified, ready to act** → if **writing-plans** is available, use it to structure the work.

The frame problem is meta-epistemic: *what am I assuming without examining, and is that assumption still valid?*
