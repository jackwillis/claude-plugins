---
name: review-evidence
description: Use when reviewing experiment results, benchmarks, UX observations or research reports to decide what the findings establish, whether to adopt a proposed change, or which follow-up would be informative.
---

# Review Evidence — provisional, pending independent evaluation

Decide what the evidence supports, not what a persuasive summary implies.

## Fast exit

For a low-stakes deterministic invariant with an independently checked oracle and exact reproduction, a brief result and limitation statement is sufficient. Do not invent uncertainty calculations.

## Review procedure

1. **Recover the question:** Locate the original protocol and intended decision. Identify the predeclared outcome, comparator, thresholds, guardrails and stop rule.
2. **Validate observations:** Inspect raw rows including missing and failed trials, source/fixture hashes, exact revision, environment, commands and analysis. Re-run a deterministic check if available. If raw data or a preregistered protocol is absent, say so.
3. **Check study design:** Match experimental units to randomization or sampling; flag correlated repeats masquerading as independent replicates, confounders, order/carryover effects, measurement changes and selective exclusion of failures.
4. **Compare prediction with observation:** Report meaningful effect sizes, dispersion/uncertainty when justified, negative cases, and guardrail failures. Distinguish a controlled causal comparison from observational correlation and a synthetic contract check from real-world accuracy.
5. **Challenge the inference:** Try a plausible alternative explanation or counterexample. Identify whether the report generalizes beyond the tested inputs, platform, population or hardware.
6. **Make a bounded recommendation:** *adopt*, *reject*, *revise and repeat*, *defer* or *insufficient evidence*, stating the exact reason and cheapest next test if needed. Preserve negative findings.
7. **Respect ownership:** Research results never authorize a merge, source/license approval, owner-hardware access, release scope or new implementation on their own.

## Output

Separate **observed**, **inferred**, **uncertain**, and **decision requested**. Provide links or exact reproduction commands. Don't conceal a missing protocol or revise its success metric retroactively.

**Transition:** If evidence contradicts the causal model, return to *representing-and-intervening*; if test guards are weak, use *is-it-tested* or *what-to-test*.
