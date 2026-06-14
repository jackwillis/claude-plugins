# Example: Do Push Notifications Improve Retention?

Product team sees that users who receive push notifications have 20% higher 30-day retention. They want to increase notification volume.

## Step 1: Pearl's Ladder

"Do push notifications improve retention?" is a Rung 2 question (intervention). The available data — observational correlation between notification receipt and retention — lives on Rung 1. The gap between the question and the evidence is the core problem.

## Step 2: Gather Context

Notifications are sent to users who showed engagement signals (opened app in last 3 days). Users who disabled notifications are excluded. No prior experiment. **Uncertain about:** whether the engagement signal is a confounder or a mediator.

## Step 3: Estimand

The ATE of receiving any push notification in days 1-7 on 30-day retention, compared to receiving no notification, for all eligible users.

## Step 4: DAG

```
Engagement (C) → Notification (T)
Engagement (C) → Retention (Y)
Notification (T) → Retention (Y)
```

Engagement is a confounder — it causes both treatment assignment and outcome.

Running this DAG through `dag_check.py` confirms the structure mechanically. The spec:

```json
{"edges":[["Engagement","Notification"],["Engagement","Retention"],["Notification","Retention"]],"treatment":"Notification","outcome":"Retention","adjustment_set":["Engagement"]}
```

```bash
echo '{"edges":[["Engagement","Notification"],["Engagement","Retention"],["Notification","Retention"]],"treatment":"Notification","outcome":"Retention","adjustment_set":["Engagement"]}' | python3 systems-analysis/skills/causal-analysis/dag_check.py
```

```
Treatment: Notification    Outcome: Retention
Observed: ['Engagement', 'Notification', 'Retention']
Unobserved: none

Backdoor paths (open paths confound the estimate):
  [BLOCKED] Notification - Engagement - Retention

Adjustment set: ['Engagement'] (condition on these to identify the effect)

Proposed adjustment set ['Engagement']: VALID - blocks all backdoor paths without opening a collider

Node classification:
  Engagement: confounder candidate
```

The tool agrees: one backdoor path, blocked by conditioning on Engagement, which it classifies as a confounder candidate. This is only as good as the assumption that Engagement is measured well enough to block the path — see Step 7.

**In plain terms:** We want to know whether sending push notifications actually keeps users around, not just whether the two show up together. Right now the numbers could look this way because users who were already engaged — already opening the app — both get targeted with notifications and stick around anyway, the way a falling barometer predicts a storm without causing it. To call notifications a cause, we'd have to compare like with like by accounting for baseline engagement, which we can only partly do here, because our engagement measure is a crude binary that may miss the dimensions that matter.

## Step 5: Backdoor Paths

T ← C → Y. One open backdoor path through Engagement.

## Step 6: Collider Check

No colliders in the proposed adjustment set.

## Step 7: Adjustment Set

{Engagement} blocks the backdoor path. But engagement is measured crudely (binary: opened app or not). **Confidence note:** if engagement has unmeasured dimensions (e.g., session depth, feature usage) that affect both notification targeting and retention, the adjustment is incomplete.

## Step 8b: Experiment

Adjustment set may be insufficient — unmeasured engagement dimensions. Recommend a randomized holdout: randomly withhold notifications from 10% of eligible users for 30 days.

## Step 9: Threats

- **Unmeasured confounders:** Engagement granularity beyond binary open/not-open
- **SUTVA:** Users may discuss notifications socially, contaminating control group
- **Attrition:** Users who churn can't receive notifications — survivorship bias in observational data
