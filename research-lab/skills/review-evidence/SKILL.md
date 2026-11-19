---
name: review-evidence
description: Use when reviewing experiment results, benchmarks, UX observations or research reports to decide what the findings establish, whether to adopt a proposed change, or which follow-up would be informative.
---

# Review Evidence — provisional, pending independent evaluation

Decide what the evidence supports, not what a persuasive summary implies.

## Fast exit

For a low-stakes deterministic invariant with an independently checked oracle and exact reproduction, a brief result and limitation statement is sufficient. Do not invent uncertainty calculations.

## Minimum sufficient conclusion

Check whether six obligations are met in proportion to the claim: target, instrument validity, consequential controls, propagated uncertainty, frozen PASS/FAIL/INCONCLUSIVE semantics, and evidence provenance. Classify safeguards as **core obligations**, **conditional controls** addressing demonstrated risk, or **discovery tools** that need not be repeated. Do not elevate a successful exploratory check into an unapproved acceptance criterion.

**Stop when sufficient:** If a valid measurement and its decision-level uncertainty already resolve the frozen decision, recommend concluding the investigation, not automatically increasing precision or commissioning another review. Additional work must name a consequential open failure mode and explain why resolving it could change the decision. A well-supported narrow conclusion is preferable to endless certification.

## Review procedure

1. **Recover the question:** Locate the original protocol and intended decision. Identify the predeclared outcome, comparator, thresholds, guardrails and stop rule.
2. **Validate observations:** Inspect raw rows including missing, failed, partially completed and nonconvergent trials, source/fixture hashes, exact revision, environment, commands and analysis. Re-run a deterministic check if available. If raw data or a preregistered protocol is absent, say so.
3. **Check reference validity before scoring:** For expensive or approximate references, inspect candidate-blind feasibility, known-answer or independent correctness controls, the **actual metric domain** and resource ceilings. Distinguish **VALID** (mathematically sound enclosure), **PRECISE** (operational target reached), and **DECISION-RESOLVED** (bounds support a threshold verdict). A sound enclosure need not meet the precision target to resolve a well-separated decision; successive estimates agreeing is *not* a proved error bound.
4. **Check study design:** Match experimental units to randomization or sampling; flag correlated repeats masquerading as independent replicates, confounders, order/carryover effects, measurement changes and selective exclusion of failures.
5. **Classify validity before conclusions:** Report (a) valid evidence supporting or refuting the hypothesis, (b) valid but insufficient evidence, (c) instrument-limited findings such as reference nonconvergence or invalid reference assumptions, or (d) protocol-invalid findings such as failed admission or unapproved post-hoc threshold changes. Cases (c) and (d) **do not refute the candidate**. Do not score a convenient successful subset as the full population; preserve missingness and partial histories. Difficulty certifying a case is not permission to silently exclude it.
6. **Compare prediction with valid observation:** Where the protocol and instrument permit it, report meaningful effect sizes, dispersion/uncertainty when justified, negative cases and guardrail failures. For an uncertain common reference, propagate *coupled* reference uncertainty, quantization and metric eligibility through paired differences and decision thresholds; independently subtracting error bounds may lose cancellation. Evaluate bounds on the original metric's mask or population; a whole-frame average cannot substitute. Statistical bootstrap sensitivity does not repair numerical-reference uncertainty. Distinguish controlled causal comparisons from observational correlation and synthetic contract checks from real-world accuracy.
7. **Challenge the inference:** Try a plausible alternative explanation or counterexample. Identify whether the report generalizes beyond the tested inputs, platform, population or hardware. Ask whether a cheaper analytical/deterministic check could answer the outstanding question.
8. **Make a bounded recommendation:** *adopt*, *reject*, *revise and repeat*, *defer* or *insufficient evidence*, stating the exact reason and cheapest next test if needed. Keep the evidence-validity classification distinct from the product decision. If the measurement instrument fails, recommend instrument diagnosis or a separately authorized new protocol, not after-the-fact relaxation of the existing freeze.
9. **Respect ownership:** Research results never authorize a merge, source/license approval, owner-hardware access, release scope or new implementation on their own.

## Output

Separate **observed**, **instrument validity/precision/decision resolution (where applicable)**, **evidence-validity classification**, **inferred**, **uncertain**, and **decision requested**. Provide links or exact reproduction commands. Don't conceal a missing protocol, an instrument feasibility failure, or revise its success metric retroactively.

**Transition:** If evidence contradicts the causal model, return to *representing-and-intervening*; if test guards are weak, use *is-it-tested* or *what-to-test*.
