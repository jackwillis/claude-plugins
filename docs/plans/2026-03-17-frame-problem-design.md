# Frame Problem Skill Design

## Goal

A skill that forces an AI agent to make its frame assumptions explicit — what it's assuming stays the same — so those assumptions become auditable rather than silently held.

## Core Insight

You cannot act or reason without assuming a frame: things you take to stay the same. The frame problem has no general solution (Fodor, 1987). The skill doesn't try to solve it. It forces the agent to name its frame, which makes the frame checkable. An implicit frame can't be checked. An explicit one can.

## Sources

- **Fodor (1987)** "Modules, Frames, Fridgeons, Sleeping Dogs, and the Music of the Spheres" — the frame problem is Hamlet's problem (when to stop thinking), the sleeping dog strategy is empty without the right ontology, fridgeons show that "most events leave most facts unchanged" is ontology-dependent
- **Dennett (1984)** "Cognitive Wheels" — R1/R1D1/R2D1 thought experiment, each attempted solution generates a new variant of the problem
- **Hayes (1973)** "The Frame Problem and Related Problems in AI" — original formulation, frame axioms grow as M actions x N properties, stability of the world is what motivates the search for a general solution

## Skill Identity

- **Name:** `frame-problem`
- **Type:** Pattern (way of thinking about assumptions)
- **Location:** `systems-analysis/skills/frame-problem/SKILL.md`
- **Description:** Use when reasoning or acting on assumptions that may no longer hold — especially after time has passed, the user has acted between turns, prior actions had untraced side effects, or when accepting a problem framing without questioning it. Triggers on stale state, unexamined non-effects, inherited problem framing, confidence without re-verification, and any gap between when information was gathered and when it's being used.

## Four Actions

Applied in order when the skill fires:

### 1. Name the Frame

State what you're assuming stays the same. If you can't name your frame assumptions, you can't check them. Fodor: the sleeping dog strategy is empty unless you say what counts as a sleeping dog.

### 2. Check Freshness

Has anything happened — user action, time passing, your own prior actions — that could have invalidated the frame? The question is: when was this information gathered, and what has happened since?

Concrete triggers:
- Turns have passed since you last read a file
- The user mentioned doing something ("I pushed," "I switched branches," "I edited that file")
- You made changes that could have side effects you didn't trace
- CI, deployments, or other automated processes may have run

### 3. Check Scope

Are you solving the right problem? The frame includes not just facts about the world but the problem definition itself. If the user says "I think it's a caching issue," that's a frame. The most consequential assumption is often which problem you're solving, not how you're solving it. (Schon's problem-setting, generalized.)

### 4. Name the Blind Spots

What kind of change would your current vocabulary not let you notice? Fodor's fridgeons: the issue isn't tracking every conceivable property, but recognizing that your ontology determines what changes are even visible to you. This is the hardest action and the most honest — an admission of bounded rationality, stated out loud.

## Failure Modes (Dennett's Three Robots)

| Mode | Pattern | Example | Correction |
|------|---------|---------|------------|
| **R1** — ignoring side effects | Acts on plan without considering what else it touches | Refactoring a function without checking its callers | Back up. Name the frame. What are you assuming stays the same? |
| **R1D1** — considering everything | Traces every possible implication, never acts | "Let me also check whether this affects the build, the docs, the deployment, the..." | You're past diminishing returns. State the cost of further checking vs. the risk of being wrong. Act. |
| **R2D1** — meta-paralysis | Tries to enumerate what's relevant before acting, which is itself unbounded | Spending more time deciding what to check than it would take to just check the likely things | The relevance question has no general answer (Fodor). Check what your model makes salient. Accept residual risk. |

Each robot fails because it tries to solve the frame problem rather than manage it.

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

## Termination

The skill explicitly acknowledges it has no clean stopping rule. Fodor: "The frame problem is just Hamlet's problem viewed from an engineer's perspective." You stop checking when the expected cost of further checking exceeds the expected cost of being wrong. Say that tradeoff out loud — don't just silently stop.

## Transition Signals

- **Can't name the frame because you don't have a model** → start with **representing-and-intervening**. You need R&I's Represent phase before you can name what you're holding constant.
- **Frame check reveals the problem definition itself is wrong** → return to **representing-and-intervening** (Problem Setting / Schon). The frame error is upstream of any solution.
- **Frame check reveals a regulation mismatch** → switch to **requisite-variety**. The frame was "this regulator is sufficient" and it isn't.
- **Need to establish whether a causal assumption in the frame actually holds** → switch to **design-causal-study**. The frame contains a causal claim that hasn't been tested.
- **Frame is solid, assumptions verified, ready to act** → if **writing-plans** is available, use it to structure the work.

## Relationship to Existing Skills

R&I's Problem Setting section (Schon) is one species of frame error — accepting the wrong problem frame. This skill generalizes: every assumption is a frame, not just the problem definition. R&I keeps its Schon section; this skill cross-references it.

- **R&I** is epistemic: how does this work, and what will happen if I change it?
- **Frame Problem** is meta-epistemic: what am I assuming without examining, and is that assumption still valid?

## Design Decisions

1. **Pattern, not technique.** No fixed steps to follow mechanically. Fodor's whole point is that there can't be a general algorithm for relevance determination. The skill forces explicitness, not completeness.
2. **Broadest scope.** Covers any case where an agent's frame is wrong: stale state, wrong problem framing, untraced side effects, ontological blind spots. Not limited to the narrow logical frame problem.
3. **Dennett's robots as failure modes, not as the structure.** The R1/R1D1/R2D1 progression is memorable but descriptive, not prescriptive. The four actions (Name/Freshness/Scope/Blind Spots) are the prescriptive core.
4. **Explicit termination acknowledgment.** The skill states that it has no clean stopping rule, and requires the agent to state the tradeoff when it stops checking. This is intellectually honest and practically useful.
5. **Cross-references R&I rather than absorbing it.** R&I's Schon section stays in R&I. This skill references it as one instance of frame error.
