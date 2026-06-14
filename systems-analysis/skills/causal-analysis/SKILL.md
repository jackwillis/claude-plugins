---
name: causal-analysis
description: Use when evaluating whether evidence supports a causal claim or designing a study to test one. Triggers on "does X cause Y", "should we change X to improve Y", "we noticed X and Y move together", "the data shows...", "our A/B test found...", auditing causal reasoning in a document or analysis, drawing conclusions from observational data, confounders, selection bias.
---

# Causal Analysis

## Overview

Correlation does not establish cause. Whether you're designing a study or auditing someone else's causal reasoning, you need: (1) where the claim sits on Pearl's ladder, (2) what the causal structure is, and (3) whether the quantity is identifiable from available data.

Follow the steps in order. Do not skip to study design before completing the DAG and identifiability check.

## Proportionality

Not every causal question needs the full pipeline. If the causal structure is simple (one obvious cause, no plausible confounders) and the stakes are low, state the estimand and the threat you're dismissing in one sentence each. The discipline is *locating the question on the ladder* (Pearl), not running nine steps for a two-variable system. Scale the rigor to the cost of a wrong causal conclusion.

## Evaluating Existing Claims

If you're auditing causal reasoning rather than designing a study, start here:

1. **What rung?** Place each claim on Pearl's Ladder (Step 1). Most claims from observational data are Rung 1 dressed up as Rung 2.
2. **What's the implicit estimand?** The author may never state it. Write it for them.
3. **What confounds aren't acknowledged?** Draw the DAG (Step 4). Look for backdoor paths the author didn't close.
4. **What's the strongest claim the evidence actually supports?** Often weaker than what's stated.

Then use the full pipeline below for any claim that needs deeper analysis.

## Step 1: Pearl's Causal Ladder

Locate the question on the ladder first — this determines what kind of evidence can even address it:

| Rung | Question type | Example |
|------|--------------|---------|
| **1 — Association** | What does X tell us about Y? | "Users with notifications have lower retention" |
| **2 — Intervention** | What happens if we *do* X? | "If we disable notifications, what happens to retention?" |
| **3 — Counterfactual** | What *would have* happened? | "Would this user have churned if they hadn't gotten a notification?" |

Observational data lives on Rung 1. Causal claims require Rung 2 or 3. Identify which rung the question is asking about — this determines what study design can answer it.

---

## Step 2: Gather Context

Before defining anything, build a model of the system. What's been tried? What constraints exist? What data is available? State what you're confident about and what you're uncertain about — uncertainty tells you where the DAG edges are weakest.

If entering from **representing-and-intervening**, the Represent phase already covers this — use that model directly.

---

## Step 3: Define the Estimand

State precisely what you want to measure before touching data.

- **Treatment (T):** What is the intervention? (binary, continuous, multi-valued?)
- **Outcome (Y):** What metric? Over what time window?
- **Population:** ATE (average over everyone), ATT (average over those who would receive treatment), LATE (local effect for compliers)?
- **Counterfactual:** "Compared to what?" — What is the baseline/control condition?

> Example: *"The ATT of receiving any push notification in days 1–7 on 30-day retention, compared to receiving no notification in days 1–7, for users who would be targeted by the current notification system."*

If you cannot write this sentence, stop. The question is not yet well-formed.

---

## Step 4: Draw the DAG

Draw a directed acyclic graph (DAG) of the causal structure. This is not optional.

**Node types:**
- **T** — Treatment (your intervention)
- **Y** — Outcome
- **C** — Confounders (common causes of T and Y)
- **M** — Mediators (on the causal path T → M → Y — do not adjust for these)
- **Col** — Colliders (common effects of two variables — do not adjust for these)
- **U** — Unmeasured variables (note them even if you can't use them)

**Draw edges for every plausible direct causal relationship.** Ask for each pair: "Could X directly cause Y, independent of all other variables?" For each edge, note your confidence — low-confidence edges are where sensitivity analysis should focus.

**Common confounders to check:**
- Selection mechanism: what determines treatment assignment? Is that mechanism causally related to the outcome?
- Time: did early outcome values cause treatment receipt?
- User/subject characteristics that affect both treatment eligibility and outcome

**Reverse causation check:** Could Y (or early Y) cause T? If yes, add that edge. This is selection bias.

**Emit the DAG as data.** After drawing it, write the graph as a JSON spec so the
identifiability check can run on it:

```json
{"edges": [["Engagement","Notif"], ["Engagement","Retention"], ["Notif","Retention"]],
 "treatment": "Notif", "outcome": "Retention",
 "unobserved": ["Engagement"], "adjustment_set": ["Engagement"]}
```

`edges` is the list of directed edges; `treatment`/`outcome` name T and Y; `unobserved`
lists nodes that exist causally but aren't measured (they're excluded from candidate
adjustment sets); `adjustment_set` (optional) is a set you want validated. Edge-confidence
notes stay in your prose, not the JSON.

---

## Step 5: Run the Identifiability Check

Do not enumerate backdoor paths or pick an adjustment set by hand — that graph reasoning
is mechanical and error-prone to do in your head. Run the check on the DAG you emitted:

```bash
echo '<the JSON spec from Step 4>' | python3 dag_check.py
```

(The script is in this skill's directory: `skills/causal-analysis/dag_check.py`. It is
pure standard-library Python — no install needed. If `python3` is genuinely unavailable,
fall back to the manual rules in the appendix at the end of this skill.)

The report tells you:

- **Backdoor paths**, each marked OPEN or BLOCKED. Open paths confound the estimate.
- **Adjustment set** — a minimal set of observed variables to condition on, OR
  `{}` (identifiable, no adjustment needed), OR `not identifiable` (an unmeasured
  confounder blocks backdoor adjustment — go to Step 6b).
- **Proposed set validation** — if you supplied `adjustment_set`, whether it is valid
  (and why not, if it adjusts a collider or a descendant of the treatment).
- **Node classification** — mediators and descendants of the treatment (never adjust for
  these), collider-ish nodes (adjusting them opens spurious paths), and confounder
  candidates.

Read the verdict off the report rather than re-deriving it. If the report says
`not identifiable`, the effect cannot be obtained from observational data by adjustment;
proceed to Step 6b (experiment design).

---

## Step 6a: Observational Study Design (if identifiable)

If the effect is identified from observational data via the adjustment set:

- Use regression adjustment, matching, IPW (inverse probability weighting), or doubly-robust estimation on the adjustment set
- Report the adjustment set explicitly in any write-up
- Sensitivity analysis: how much unmeasured confounding would overturn the estimate? (Rosenbaum bounds or E-value)
- Check overlap: are there regions of the adjustment variables where T=1 and T=0 are both represented? If not, extrapolation is occurring.

---

## Step 6b: Experiment Design (if not identifiable from observational data)

If unmeasured confounders block identification, random assignment is required.

**Experiment design checklist:**
- **Eligibility:** Define the population precisely (matches the estimand's target population)
- **Randomization unit:** User, session, cluster? Cluster if treatment can spill over between units
- **Randomization stratified by:** Key confounders (engagement tier, cohort, platform) to reduce variance
- **Control condition:** Matches the counterfactual in the estimand
- **Primary outcome and time window:** Pre-specified, not chosen post-hoc
- **Sample size / power:** Calculated from minimum detectable effect and baseline variance
- **Duration:** Long enough to capture the full outcome window after treatment exposure
- **Secondary outcomes:** List pre-specified secondary outcomes; apply multiple comparison correction

---

## Step 7: Threat Assessment

Before finalizing, run through the threat list:

| Threat | Check |
|--------|-------|
| **Unmeasured confounders** | Are there common causes of T and Y not in the adjustment set? |
| **Reverse causation** | Could early Y cause T? Is there a time ordering check? |
| **Collider bias** | Are you conditioning on any variable caused by T or Y? |
| **Mediator adjustment** | Are you controlling for any variable on the causal path T→Y? |
| **SUTVA violation** | Can one unit's treatment affect another's outcome? (spillover) |
| **Measurement error in T** | Is treatment receipt measured accurately? |
| **Attrition / selection into outcome** | Does missingness in Y depend on T or confounders? |
| **External validity** | Does the study population match the target population for the intervention? |
| **Time-varying confounding** | In systems that evolve (e.g., software across releases), before/after comparisons are confounded by everything else that changed between versions. |

---

## Output Format

Summarize findings as:

```
Estimand: [precise statement]
DAG: [sketch or list of key edges]
Open backdoor paths: [list]
Adjustment set: [variables] or [not identifiable — unmeasured U]
Recommended design: [observational with adjustment / experiment with holdout]
Key threats: [top 2-3]
What this study can and cannot answer: [1-2 sentences]
```

Then append a plain-language layer for readers who don't know causal inference — keep the
technical summary above it intact:

```
In plain terms: We want to know whether [doing T] actually changes [Y], not just whether
they show up together. Right now the numbers could look this way because [confounder, in
plain words] drives both — the way a falling barometer predicts a storm without causing
it. To call it cause, we'd have to compare like with like by accounting for [confounders],
which [we can / can't] do with this data.
```

If the check flagged a collider, add one sentence: conditioning on [collider] is like
judging dating partners you've only met because they were attractive or kind — it
manufactures a correlation that isn't really there.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adjusting for mediators | Check: does the variable sit on the T→Y path? If yes, exclude from adjustment set |
| Conditioning on colliders | Check: does the variable have arrows from both T-side and Y-side? If yes, exclude |
| Skipping the estimand | You cannot design a study without knowing what quantity you're estimating |
| Treating selection as confounding | Reverse causation requires time-ordering check, not just adjustment |
| Running an experiment on the wrong population | Eligibility criteria must match the estimand's target population |
| Choosing outcomes post-hoc | Pre-specify primary outcome before data collection or analysis |

## Examples

- [Push notifications and retention](examples/notification-retention.md) — engagement as confounder, incomplete adjustment set, experiment recommendation
- [Collider bias in hiring](examples/collider-hiring.md) — conditioning on a collider (hired) masks the effect of degree prestige on performance
- [Non-identifiable mentorship effect](examples/non-identifiable-mentorship.md) — unmeasured confounder blocks identification, lottery experiment required
- [Rung demotion: code review comments](examples/rung-demotion-code-review.md) — Rung 1 association mistaken for Rung 2 intervention, policy targets signal not cause

## Arriving From Another Skill

- **From representing-and-intervening:** You have a model with identified relationships. These relationships are your candidate DAG edges. Start at Step 4 (Draw the DAG) rather than Step 2 (Gather Context) — R&I already did that work. Flag which edges R&I was least confident about; those are your priority for confounding checks.
- **From staleness-check:** A re-read revealed that a causal assumption no longer holds ("we assumed X causes Y but the system changed"). That assumption is your target estimand. Start at Step 1 to locate it on Pearl's Ladder.

## Transition Signals

- **Question is "why is this behaving this way"** rather than "does X cause Y" → suggest **representing-and-intervening** to the user.
- **Causal structure reveals a regulation problem** (not enough control variety to act on identified causes) → suggest **requisite-variety** to the user.
- **Can't state the estimand** — the question may not be causal yet. Suggest **representing-and-intervening** to the user to model the system first.
- **Study designed, ready to execute** — if **writing-plans** is available, suggest it to the user to structure the study execution. For independent workstreams (e.g., data extraction, power analysis, sensitivity analysis), suggest **subagent-driven-development**.

## Appendix: Manual Backdoor Tracing (fallback only)

Use this only if `python3` is unavailable. A backdoor path is any path from T to Y
starting with an arrow into T (T ← …). List every such path. A path is blocked if it
contains a non-collider you condition on, or a collider (→ C ←) that you do not condition
on (and none of whose descendants you condition on). A valid adjustment set blocks every
backdoor path, contains no descendant of T, and adjusts no collider. If no such set
exists among measured variables, the effect is not identifiable from observational data.
