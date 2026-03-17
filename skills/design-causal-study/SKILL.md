---
name: design-causal-study
description: Use when evaluating whether a dataset or finding supports a causal claim, designing an observational study or experiment, or asked to analyze why something happens (not just whether it correlates). Triggers on phrases like "does X cause Y", "should we change X to improve Y", "we noticed X and Y move together".
---

# Design a Causal Study

## Overview

Correlation does not establish cause. Before recommending an intervention or designing a study, you must establish: (1) what causal quantity you're estimating, (2) what the causal structure is, and (3) whether the quantity is identifiable from available data.

Follow the steps in order. Do not skip to study design before completing the DAG and identifiability check.

## Pearl's Causal Ladder

Before anything else, locate the question on the ladder:

| Rung | Question type | Example |
|------|--------------|---------|
| **1 — Association** | What does X tell us about Y? | "Users with notifications have lower retention" |
| **2 — Intervention** | What happens if we *do* X? | "If we disable notifications, what happens to retention?" |
| **3 — Counterfactual** | What *would have* happened? | "Would this user have churned if they hadn't gotten a notification?" |

Observational data lives on Rung 1. Causal claims require Rung 2 or 3. Identify which rung the question is asking about — this determines what study design can answer it.

---

## Step 1: Define the Estimand

State precisely what you want to measure before touching data.

- **Treatment (T):** What is the intervention? (binary, continuous, multi-valued?)
- **Outcome (Y):** What metric? Over what time window?
- **Population:** ATE (average over everyone), ATT (average over those who would receive treatment), LATE (local effect for compliers)?
- **Counterfactual:** "Compared to what?" — What is the baseline/control condition?

> Example: *"The ATT of receiving any push notification in days 1–7 on 30-day retention, compared to receiving no notification in days 1–7, for users who would be targeted by the current notification system."*

If you cannot write this sentence, stop. The question is not yet well-formed.

---

## Step 2: Draw the DAG

Draw a directed acyclic graph (DAG) of the causal structure. This is not optional.

**Node types:**
- **T** — Treatment (your intervention)
- **Y** — Outcome
- **C** — Confounders (common causes of T and Y)
- **M** — Mediators (on the causal path T → M → Y — do not adjust for these)
- **Col** — Colliders (common effects of two variables — do not adjust for these)
- **U** — Unmeasured variables (note them even if you can't use them)

**Draw edges for every plausible direct causal relationship.** Ask for each pair: "Could X directly cause Y, independent of all other variables?"

**Common confounders to check:**
- Selection mechanism: what determines treatment assignment? Is that mechanism causally related to the outcome?
- Time: did early outcome values cause treatment receipt?
- User/subject characteristics that affect both treatment eligibility and outcome

**Reverse causation check:** Could Y (or early Y) cause T? If yes, add that edge. This is selection bias.

---

## Step 3: Identify Open Backdoor Paths

A backdoor path is any non-causal path from T to Y (one that goes "backward" through T's causes).

List every backdoor path: T ← C → Y

For each path, check:
- Is it open? (no colliders blocking it, no conditioning on a collider opening it)
- Is it blocked by conditioning on a variable in the path?

**Backdoor criterion:** The effect of T on Y is identifiable from observational data if you can find an adjustment set Z such that:
1. Z blocks all backdoor paths from T to Y
2. Z contains no descendants of T (no mediators or colliders on T→Y paths)

If the backdoor criterion cannot be satisfied (because confounders are unmeasured), check the frontdoor criterion or instrumental variable conditions.

---

## Step 4: Collider Check

Before specifying your adjustment set, check whether any candidate control variable is a collider — a variable caused by both T and Y (or their causes).

Conditioning on a collider **opens** a spurious path. This is a common error.

> Example: If "notification opened" is caused by both receiving a notification (T) and by the user already being engaged (a cause of Y), then conditioning on "opened" opens a spurious path between T and Y.

If a proposed control variable has arrows pointing *into* it from multiple other variables, it may be a collider. Do not include it in the adjustment set without checking the graph.

---

## Step 5: Specify the Adjustment Set

From the DAG analysis, list the variables that must be conditioned on to block all backdoor paths without opening collider paths.

If the adjustment set is feasible (all variables are measured): the effect may be identifiable from observational data. Proceed to Step 6a.

If the adjustment set requires unmeasured variables: the effect is not identified from observational data. Proceed to Step 6b.

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
