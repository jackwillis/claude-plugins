# Example: Do Code Review Comments Prevent Production Incidents?

An engineering team observes that PRs with more review comments take longer to merge but have fewer production incidents. A manager proposes requiring all PRs to receive at least 3 review comments before merge: "code review prevents bugs."

## Step 1: Pearl's Ladder

The manager's proposal is Rung 2: "If we mandate ≥3 comments, will incidents decrease?" The evidence is Rung 1: an association between comment count and incident rate. This is a classic case of Rung 1 data dressed up as a Rung 2 claim.

## Step 2: Gather Context

Review comments are not randomly distributed across PRs. Complex, risky, or large changes attract scrutiny — reviewers spend more time and leave more comments on code they find concerning. The same complexity that attracts comments also causes the author to implement more carefully (more tests, smaller increments, extra validation).

## Step 3: Estimand

The ATE of requiring ≥3 review comments on all PRs on production incident rate, compared to the current process (no comment minimum).

## Step 4: DAG

```
PR Complexity (C) → Review Comments (T)
PR Complexity (C) → Careful Implementation → Fewer Incidents (Y)
Review Comments (T) → Fewer Incidents (Y)  [maybe — but weaker than confounded path]
```

PR Complexity is a confounder. It drives both comment volume and implementation care. The observed correlation between comments and fewer incidents is largely (possibly entirely) explained by complexity: risky PRs get both more review AND more careful authoring.

**Rung demotion:** The strongest claim the data supports is "complex PRs that receive review comments have fewer incidents." But this does not entail "mandating comments on simple PRs will reduce incidents." The comments are a *signal* of complexity-driven care, not a *cause* of quality. Mandating 3 comments on a trivial config change tests a completely different causal question than the one the data answers.

The confounding structure is identifiable on paper — running the DAG through `dag_check.py` shows the backdoor through PR Complexity and the adjustment set that would close it:

```json
{"edges":[["PRComplexity","ReviewComments"],["PRComplexity","CarefulImplementation"],["CarefulImplementation","FewerIncidents"],["ReviewComments","FewerIncidents"]],"treatment":"ReviewComments","outcome":"FewerIncidents"}
```

```bash
echo '{"edges":[["PRComplexity","ReviewComments"],["PRComplexity","CarefulImplementation"],["CarefulImplementation","FewerIncidents"],["ReviewComments","FewerIncidents"]],"treatment":"ReviewComments","outcome":"FewerIncidents"}' | python3 systems-analysis/skills/causal-analysis/dag_check.py
```

```
Treatment: ReviewComments    Outcome: FewerIncidents
Observed: ['CarefulImplementation', 'FewerIncidents', 'PRComplexity', 'ReviewComments']
Unobserved: none

Backdoor paths (open paths confound the estimate):
  [BLOCKED] ReviewComments - PRComplexity - CarefulImplementation - FewerIncidents

Adjustment set: ['PRComplexity'] (condition on these to identify the effect)

Node classification:
  CarefulImplementation: other
  PRComplexity: confounder candidate
```

But this is the trap, not the rescue. The tool answers a Rung-1 question — *adjusting for complexity, what residual association remains between comments and incidents?* — which is not the manager's Rung-2 question about what a mandate would do. Even if you measured PR Complexity perfectly and the adjusted association vanished, that tells you the comments were never the cause; it does not license forcing comments onto simple PRs where no complexity-driven care exists to signal.

**In plain terms:** We want to know whether requiring review comments actually prevents incidents, not just whether comment-heavy PRs happen to have fewer of them. The numbers look this way because complex, risky changes draw both more comments and more careful authoring — the way a falling barometer predicts a storm without causing it. Mandating comments on a trivial config change forces the barometer needle down by hand and expects the weather to follow. The data can tell us comments track care; it can't tell us that manufacturing comments manufactures care.

**Key takeaway:** The policy intervenes on the signal, not the cause. Expect the mandate to produce pro-forma "LGTM" comments on simple PRs with no effect on incident rates — while adding merge latency across the board.
