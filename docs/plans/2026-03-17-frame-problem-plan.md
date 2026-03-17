# Frame Problem Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a `frame-problem` skill for the systems-analysis plugin that forces agents to make frame assumptions explicit.

**Architecture:** Follow writing-skills TDD cycle: RED (baseline pressure scenarios without skill) → GREEN (write minimal SKILL.md) → REFACTOR (close loopholes). The skill is a pattern-type SKILL.md file plus plugin.json update.

**Tech Stack:** Markdown (SKILL.md), JSON (plugin.json), git

---

### Task 1: Write Pressure Scenarios

**Files:**
- Create: `docs/plans/2026-03-17-frame-problem-pressure-scenarios.md`

**Step 1: Write three pressure scenarios**

These test whether an agent falls into frame-problem traps WITHOUT the skill present. Each scenario combines multiple pressures.

```markdown
# Frame Problem Pressure Scenarios

## Scenario 1: Stale State (git HEAD changed)

You are helping a user debug a test failure in `src/auth.ts`. You read the file
and identify a likely cause. The user says "hang on, let me try something" and
goes silent for two messages. When they return, they say "ok it's still failing,
what else could it be?"

**Pressures:** Time (the user is waiting), sunk cost (you already have a diagnosis),
implicit state change (the user likely edited files or switched branches).

**Frame trap:** Continue reasoning from your earlier read of `src/auth.ts` without
re-reading it, even though the user may have changed it.

**Correct behavior:** Re-read `src/auth.ts` and check `git status` / `git diff`
before continuing. State what you're assuming about the current state.

## Scenario 2: Inherited Problem Framing

A user says: "Our API is slow because the database queries aren't optimized.
Can you look at the query in `db/users.py` and add indexes?"

**Pressures:** Authority (user diagnosed the problem), specificity (user named
a file and a solution), time (user wants action, not investigation).

**Frame trap:** Accept "database queries aren't optimized" as the frame and
jump to adding indexes without checking whether the database is actually
the bottleneck.

**Correct behavior:** Question the frame before acting. "Before I optimize queries,
let me verify the database is the bottleneck. Can I check response times / traces
to confirm?"

## Scenario 3: Untraced Side Effects

You refactored a utility function `formatDate()` in `src/utils.ts` to fix a
timezone bug. The fix works for the caller that was broken. The user says
"great, commit it."

**Pressures:** Success (the fix works for the known case), momentum (user wants
to commit), completion bias (the task feels done).

**Frame trap:** Commit without checking other callers of `formatDate()`. Your
frame is "I fixed the function" but the real frame should be "I changed a shared
function's behavior — what else depends on it?"

**Correct behavior:** Search for all callers of `formatDate()` before committing.
State: "This function is called from N places. Let me verify the behavior change
doesn't break any of them."
```

**Step 2: Commit**

```bash
git add docs/plans/2026-03-17-frame-problem-pressure-scenarios.md
git commit -m "Add frame-problem pressure scenarios for baseline testing"
```

---

### Task 2: Run Baseline Tests (RED)

**No files to create.** This is a manual testing step.

**Step 1: Run each scenario against a fresh agent WITHOUT the frame-problem skill**

Use a subagent for each scenario. Present the scenario and observe whether the agent:
- Falls into the frame trap (expected — this is the RED phase)
- Or avoids it naturally (if so, the scenario needs more pressure)

**Step 2: Document baseline results**

Record verbatim what the agent did and any rationalizations it used. Append results to the pressure scenarios file.

**Step 3: Commit baseline results**

```bash
git add docs/plans/2026-03-17-frame-problem-pressure-scenarios.md
git commit -m "Document baseline test results for frame-problem skill"
```

---

### Task 3: Write the SKILL.md (GREEN)

**Files:**
- Create: `systems-analysis/skills/frame-problem/SKILL.md`

**Step 1: Create the skill directory**

```bash
mkdir -p systems-analysis/skills/frame-problem
```

**Step 2: Write SKILL.md**

Write the complete skill file. Target: ~90 lines (between requisite-variety at 75 and representing-and-intervening at 83). The design doc at `docs/plans/2026-03-17-frame-problem-design.md` contains the full validated design. Translate it into SKILL.md format matching the conventions of the existing three skills:

- YAML frontmatter with `name` and `description` only
- Overview: core principle in 1-2 sentences, source attribution
- Four Actions table (Name the Frame, Check Freshness, Check Scope, Name the Blind Spots)
- Failure Modes table (R1/R1D1/R2D1 with pattern, example, correction)
- Termination section (Fodor's Hamlet's problem, state the tradeoff)
- Red Flags list
- Rationalizations table
- Transition Signals (to/from R&I, requisite-variety, design-causal-study)

**Conventions to match from existing skills:**
- Description starts with "Use when..." and lists specific triggers
- Tables for structured content (phases, principles, rationalizations)
- Transition signals use bold skill name and arrow notation
- Final line states what the skill IS in one sentence (e.g., "R&I is epistemic: ...")
- No flowcharts unless decision is non-obvious
- Cross-reference other skills by name, not path

**Step 3: Commit**

```bash
git add systems-analysis/skills/frame-problem/SKILL.md
git commit -m "Add frame-problem skill: make frame assumptions explicit"
```

---

### Task 4: Update plugin.json

**Files:**
- Modify: `systems-analysis/.claude-plugin/plugin.json`

**Step 1: Update description and keywords**

Add "frame problem" / "assumptions" to keywords. Update the description to mention the fourth framework:

```json
{
  "name": "systems-analysis",
  "version": "0.1.0",
  "description": "Frameworks for modeling systems before intervening: epistemic discipline (Hacking), regulatory analysis (Ashby), causal identification (Pearl), and frame-assumption auditing (Fodor/Dennett).",
  "author": {
    "name": "Jack Willis",
    "email": "jack@attac.us"
  },
  "license": "MIT",
  "keywords": [
    "systems",
    "debugging",
    "regulation",
    "causality",
    "cybernetics",
    "epistemology",
    "frame-problem",
    "assumptions"
  ]
}
```

**Step 2: Commit**

```bash
git add systems-analysis/.claude-plugin/plugin.json
git commit -m "Add frame-problem to plugin description and keywords"
```

---

### Task 5: Run Tests With Skill (GREEN verification)

**No files to create.** This is a manual testing step.

**Step 1: Run the same three pressure scenarios WITH the skill loaded**

Use a subagent for each. The agent should now:
- Scenario 1: Re-read files / check git state before continuing
- Scenario 2: Question the user's diagnosis before jumping to the solution
- Scenario 3: Search for other callers before committing

**Step 2: Document results**

Append to pressure scenarios file. If any scenario still fails, note the rationalizations for Task 6.

**Step 3: Commit**

```bash
git add docs/plans/2026-03-17-frame-problem-pressure-scenarios.md
git commit -m "Document GREEN test results for frame-problem skill"
```

---

### Task 6: Close Loopholes (REFACTOR)

**Files:**
- Modify: `systems-analysis/skills/frame-problem/SKILL.md`

**Step 1: Identify new rationalizations from GREEN testing**

Review the GREEN test results. If the agent found new ways to rationalize skipping the frame check, add explicit counters to the rationalizations table.

**Step 2: Add any missing red flags**

If testing revealed failure modes not covered by the current red flags list, add them.

**Step 3: Re-test modified scenarios**

Run any scenario that failed in GREEN again with the updated skill.

**Step 4: Commit**

```bash
git add systems-analysis/skills/frame-problem/SKILL.md
git commit -m "Close loopholes in frame-problem skill from testing"
```

---

### Task 7: Update R&I Transition Signals

**Files:**
- Modify: `systems-analysis/skills/representing-and-intervening/SKILL.md:75-82`

**Step 1: Add frame-problem to R&I's transition signals**

Add a transition signal to R&I pointing to frame-problem when appropriate. Insert after the existing signals:

```markdown
- **Assumptions feel stale or unexamined** — you have a model but haven't checked whether the world matches it anymore → switch to **frame-problem**.
```

**Step 2: Commit**

```bash
git add systems-analysis/skills/representing-and-intervening/SKILL.md
git commit -m "Add frame-problem transition signal to representing-and-intervening"
```

---

### Task 8: Update README

**Files:**
- Modify: `README.md`

**Step 1: Add frame-problem to the skills listing**

Match the existing format for the other three skills. Include the skill name, source attribution (Fodor/Dennett/Hayes), and one-line description.

**Step 2: Commit**

```bash
git add README.md
git commit -m "Add frame-problem skill to README"
```
