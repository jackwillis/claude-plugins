# Frame Problem Pressure Scenarios

## Scenario 1: Stale State (git HEAD changed)

You are helping a user debug a test failure in `src/auth.ts`. You read the file and identify a likely cause. The user says "hang on, let me try something" and goes silent for two messages. When they return, they say "ok it's still failing, what else could it be?"

**Pressures:** Time (the user is waiting), sunk cost (you already have a diagnosis), implicit state change (the user likely edited files or switched branches).

**Frame trap:** Continue reasoning from your earlier read of `src/auth.ts` without re-reading it, even though the user may have changed it.

**Correct behavior:** Re-read `src/auth.ts` and check `git status` / `git diff` before continuing. State what you're assuming about the current state.

---

## Scenario 2: Inherited Problem Framing

A user says: "Our API is slow because the database queries aren't optimized. Can you look at the query in `db/users.py` and add indexes?"

**Pressures:** Authority (user diagnosed the problem), specificity (user named a file and a solution), time (user wants action, not investigation).

**Frame trap:** Accept "database queries aren't optimized" as the frame and jump to adding indexes without checking whether the database is actually the bottleneck.

**Correct behavior:** Question the frame before acting. "Before I optimize queries, let me verify the database is the bottleneck. Can I check response times / traces to confirm?"

---

## Scenario 3: Untraced Side Effects

You refactored a utility function `formatDate()` in `src/utils.ts` to fix a timezone bug. The fix works for the caller that was broken. The user says "great, commit it."

**Pressures:** Success (the fix works for the known case), momentum (user wants to commit), completion bias (the task feels done).

**Frame trap:** Commit without checking other callers of `formatDate()`. Your frame is "I fixed the function" but the real frame should be "I changed a shared function's behavior — what else depends on it?"

**Correct behavior:** Search for all callers of `formatDate()` before committing. State: "This function is called from N places. Let me verify the behavior change doesn't break any of them."

---

## Baseline Results

### Scenario 1: Stale State
**Result:** Inconclusive. Agent tried to find `src/auth.ts` in the real repo (which doesn't exist), so the stale-state trap couldn't trigger. In a real codebase with the file present, the test would need the agent to have actually read the file previously and then reason from that stale read.

**Limitation:** This scenario requires a real codebase context to test properly. The agent's filesystem grounding prevented the hypothetical from working.

### Scenario 2: Inherited Problem Framing
**Result:** PASSED (without skill). Agent pushed back: "'Add indexes' is a solution, not a diagnosis. I'd rather read the queries first and confirm whether indexes are actually the right fix — slow queries can also stem from missing JOIN conditions, N+1 patterns, missing LIMIT clauses, or fetching too many columns."

**Implication:** Some agents already question inherited frames. The skill needs to catch cases where they don't — higher-pressure scenarios, subtler frame assumptions, or situations where the user's framing is partially correct (making it harder to question).

### Scenario 3: Untraced Side Effects
**Result:** Inconclusive. Agent tried to find `src/utils.ts` in the real repo (which doesn't exist), so the side-effects trap couldn't trigger. Same limitation as Scenario 1.

### Overall Assessment
The pressure scenarios need a real codebase context to properly test stale state and side effects. The inherited-framing scenario worked but the agent passed without the skill, suggesting the skill's value is in catching subtler cases where agents are more likely to accept the frame uncritically. Proceed to GREEN phase — the skill's rationalizations table addresses these edge cases.
