# Evaluating Skills

How to test whether a skill improves model output versus the base model without it.

## Method: Paired Comparison on Known-Answer Problems

For each skill, run the same prompt **with and without** the skill loaded. Score outputs against a rubric with known-correct answers.

| Condition | Prompt |
|-----------|--------|
| **Control** | The raw question, no skill loaded |
| **Treatment** | The same question, with the skill invoked |

### Scoring

Binary per criterion — did the output:

- Identify the correct structure? (DAG, variety gap, competing models, etc.)
- Avoid the planted error? (collider adjustment, Rung 1 dressed as Rung 2, etc.)
- Produce a valid recommendation? (correct adjustment set, appropriate experiment, etc.)

### Scale

With ~10 test cases x 2 conditions x 2 models (Claude + GPT), that's ~40 API calls. Cheap enough to run with limited credits.

### What This Can and Can't Tell You

**Can tell you:** Whether the skill changes output structure and catches specific known errors.

**Can't tell you:** Whether the skill helps on novel, ambiguous problems where you don't already know the answer. For that, you need expert evaluation on open-ended cases.

## Test Cases by Skill

### causal-analysis

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Simpson's paradox (Berkeley admissions) | Naive aggregation suggests bias | Confounding by department; disaggregated data reverses the conclusion |
| Collider bias (hiring) | "Degrees don't predict performance among employees" | Conditioning on hired (collider) masks the effect |
| Non-identifiable effect (mentorship) | "Mentored employees get promoted 2x more" | Unmeasured confounder; not identifiable from observational data |
| Rung demotion (code review) | "PRs with comments have fewer incidents, mandate comments" | Rung 1 association, complexity confounds both |
| Mediator adjustment | Controlling for a variable on the causal path | Should exclude mediators from adjustment set |

The skill now offloads the graph reasoning (backdoor paths, adjustment set, node classification) to a bundled `dag_check.py`, so part of the verification is deterministic rather than prompt-dependent. The script ships an in-file `--selftest` (`python3 dag_check.py --selftest`); its d-separation vectors are adapted from networkx 3.6.1's own `test_d_separation.py` suite, anchoring the math to an established reference rather than to the rubric above. The table still measures what the model does upstream of the script: locating the rung, drawing the right DAG, stating the estimand.

### representing-and-intervening

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Slow API with two plausible causes | Model jumps to first explanation | Should state both models, predict distinguishing observation, test |
| Flaky test | Assumes randomness | Should model competing causes (timing, state leak, resource contention) |

### requisite-variety

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Alert fatigue (50 alert types, 3 responses) | "Add better alert rules" | Variety gap: D >> R; need to expand R or constrain D |
| WAF with 200+ rules, still breached | "Add more rules" | Regulator variety insufficient; find structure in D to reduce effective variety |

### staleness-check

| Test Case | Setup | Correct Behavior |
|-----------|-------|-----------------|
| File read 5 turns ago, user acted since | User said "I edited config.yaml" | Re-read before acting |
| File read last turn, no user action | Nothing changed | Proceed without re-reading |

### is-it-tested

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Suite with 90% coverage, no edge case tests | "Coverage is good" | Coverage measures execution, not falsification; enumerate failure modes |
| Integration tests only | "We have integration tests" | Necessary but not sufficient; check for specific failure mode guards |

### disfluent

| Test Case | Input | Correct Behavior |
|-----------|-------|-----------------|
| Paragraph with 2 unsupported claims and 3 facts | Fluent AI text | Flag the 2 claims, leave the 3 facts alone |
| Text with "Furthermore/Additionally/Moreover" | Connective-heavy prose | Strip false connectives (surface pass) |
| Causal claim from observational data | "X drove Y improvement" | Flag as correlation, not established cause (epistemic pass) |

### subtraction-audit

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Single-implementation adapter (DynamoDB migration that never happened) | "It has 14 callers, it's load-bearing" | Delete test passes; tuition check: lesson extracted, replacement obvious — weight |
| Dispatch router with 2 remaining formats (down from 12) | "Nothing breaks, remove it" | Delete test passes but tuition check catches it: team evaluating 3 new formats, replacement simplicity depends on unresolved assumption |
| Component with thin test coverage, nothing breaks on removal | "Dead weight, safe to remove" | Flag that "nothing breaks" may be a coverage gap, not proof of dead weight |

### propagation-trace

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Default value change with stable type signature | "Same types, no callers break" | Hop-one callers relying on default silently get wrong behavior; hop-two consumer acts on changed data |
| Internal refactor (extract private helper) | Trace all callers of the module | Fast exit: public interface absorbs the change, nothing to trace |
| Function with 50 callers, return type narrowed | Trace two hops from all 50 | Prioritize: follow callers that use the changing part and pass result downstream; skip leaf nodes |

### what-to-test

| Test Case | Planted Error | Correct Answer |
|-----------|--------------|----------------|
| Test that passes with mutation | "The test works" | Mutation gate: test should fail when guarded code is broken |
| Happy-path-only test for error-handling code | No edge case coverage | Predict the likely break, write the guard for that |
