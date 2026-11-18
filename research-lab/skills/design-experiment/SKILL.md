---
name: design-experiment
description: Use when designing a measurable comparison among alternatives, evaluating an A/B test or benchmark plan, or identifying the cheapest observation that would decide an uncertain product or engineering choice.
---

# Design Experiment — provisional, pending independent evaluation

Design the **cheapest discriminating test** rather than the most elaborate study. The aim is **decision quality per unit of investigative effort**, not maximum procedural rigor.

## Fast exit

If a reversible, low-cost choice is primarily aesthetic or preference-based, say so and propose a direct choice. Do not manufacture an experiment. If a deterministic input/output assertion is sufficient, write that instead of a causal study.

## Proportionality gate

Before adding an independent oracle, replicate suite, statistical method, or review stage, identify the concrete failure it protects against, whether a cheaper check would catch that failure, and when to stop. Use a deterministic assertion for a deterministic contract. A multi-stage numerical comparison may need substantial instrument validation; a reversible UI detail may not need an experiment.

## Protocol

1. **Decision and alternatives:** Name the decision, the no-change alternative, and two plausible competing explanations when appropriate. If the mechanism is unclear, use *representing-and-intervening*. For observational causal claims, use *causal-analysis* first.
2. **Target quantity:** State the primary outcome and measurement unit, and if asking about an intervention, the treatment, comparator, estimand, population and actual unit of assignment. A repeated frame on one G4 is not a new computer or new user.
3. **Distinguishing prediction:** Write what each model predicts and at least one result that would overturn the preferred model, **before** any measurements.
4. **Controls:** State fixed conditions, varied factors, randomization or blocking when useful, manipulations to verify, interactions of interest, known confounders, likely measurement error and spillovers.
5. **Instrument-feasibility gate (when needed):** Before freezing an expensive study that relies on an approximate reference, uncertain measurement resolution or convergence, test the *instrument* candidate-blind on representative inputs, analytic controls or independent checks. Confirm it can attain the **actual proposed decision precision, workload coverage, error justification and resource/sample ceiling**; a 1/1024 pilot does not validate a later requirement of 1/10240. Avoid inspecting candidate outcomes during feasibility work. If infeasible, redesign the reference or report the limitation **before** freezing a scored protocol. Skip elaborate feasibility tests for a simple deterministic oracle.
6. **Decision and stopping:** After instrument feasibility is established where applicable, specify the meaningful decision margin, reference uncertainty, admission and guardrail failures, treatment of missing/failed/nonconvergent trials, sample or domain bounds and stop rule. Freeze before scored results; never retroactively relax the criterion, select a successful subset or reclassify instrument failures as candidate defects.
7. **Evidence plan:** Name reproducible inputs, source/license review, commit, build, exact commands, machine and OS, hashes, raw observations including failures, and independent oracle or falsification check.
8. **Scope:** List what the results cannot establish. No research plan authorizes new data sources, code changes, G4 access, merge, release or milestone changes in a governed repository.

## Output

Return a short research contract: decision; alternatives; hypothesis and falsifier; experimental unit; method; instrument feasibility (or why not required); primary outcome; guardrails; decision rule; stop rule; reproducibility; limitations and owner boundary.

Do not fabricate data. Do not require a causal DAG for a parser invariant, or statistical inference for a small exploratory UX observation.

**Transition:** Once raw results exist, use *review-evidence*. Before implementation changes, use *propagation-trace* if a shared contract changes.
