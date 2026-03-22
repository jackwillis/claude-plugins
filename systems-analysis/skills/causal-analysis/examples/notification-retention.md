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
