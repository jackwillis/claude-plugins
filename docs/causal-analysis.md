# Verify Causal Claims

`/causal-analysis` — based on Pearl & Mackenzie (2018) · [Full skill](../systems-analysis/skills/causal-analysis/SKILL.md)

## When to use

Someone (you, a coworker, a report) is claiming that X causes Y. Or you're designing a study to test whether it does. The data looks convincing, but you haven't checked whether it can actually answer a causal question.

Auto-triggers on: "does X cause Y", "should we change X to improve Y", "the data shows...", observational data presented as evidence for intervention.

## What it does

Walks through Pearl's causal framework:

1. **Rung placement** — is this an association (what correlates?), an intervention (what happens if we do X?), or a counterfactual (what would have happened?)? Most claims from observational data are associations dressed up as interventions.
2. **Estimand** — states precisely what you're trying to measure before touching data.
3. **DAG** — draws the causal structure. Identifies confounders, mediators, and colliders.
4. **Identification** — checks whether the causal effect can be estimated from the available data, or whether an experiment is needed.
5. **Threats** — checks for reverse causation, collider bias, SUTVA violations, and other common mistakes.

## What to expect

You'll see Claude push back on causal language that isn't supported by the study design. If the data is observational, it identifies confounders and says whether adjustment can fix them. If not, it recommends an experiment and sketches the design.

For simple causal structures, it states the estimand and the main threat in a sentence each.

## How the graph math is done

Rather than reasoning about d-separation, backdoor paths, and adjustment sets by hand, the skill emits the DAG as a JSON spec and runs a bundled solver, `dag_check.py`, to compute them. The script reports the backdoor paths (each marked open or blocked), a valid adjustment set or a verdict that the effect is not identifiable, and a classification of each node as confounder, mediator, descendant, or collider.

The script is pure standard-library Python — no install or dependencies needed. After reading off the result, the skill appends a plain-language explanation so the conclusion is legible to readers who don't know the graph terminology.

## Examples

**Collider bias in hiring.** A company finds no correlation between degree prestige and job performance among employees. The expected output identifies "Hired" as a collider — by only looking at hired employees, you've induced a spurious negative association. The null finding is exactly what collider bias predicts, even if degrees genuinely matter.

**Correlation mistaken for causation.** A manager sees that PRs with more review comments have fewer production incidents and proposes requiring 3+ comments on all PRs. The expected output identifies PR complexity as a confounder — complex PRs attract both more review and more careful authoring. The policy intervenes on the signal, not the cause.

**Non-identifiable effect.** Mentored employees get promoted at 2x the rate. The expected output identifies that mentors select mentees based on unmeasured traits (ambition, visibility) that also drive promotion. The effect isn't identifiable from observational data — recommends a lottery-based assignment when the program is oversubscribed.
