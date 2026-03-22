# Example: Do Push Notifications Improve Retention?

Product team sees that users who receive push notifications have 20% higher 30-day retention. They want to increase notification volume.

## Step 0: Gather Context

Notifications are sent to users who showed engagement signals (opened app in last 3 days). Users who disabled notifications are excluded. No prior experiment. **Uncertain about:** whether the engagement signal is a confounder or a mediator.

## Step 1: Estimand

The ATE of receiving any push notification in days 1-7 on 30-day retention, compared to receiving no notification, for all eligible users.

## Step 2: DAG

```
Engagement (C) → Notification (T)
Engagement (C) → Retention (Y)
Notification (T) → Retention (Y)
```

Engagement is a confounder — it causes both treatment assignment and outcome.

## Step 3: Backdoor Paths

T ← C → Y. One open backdoor path through Engagement.

## Step 4: Collider Check

No colliders in the proposed adjustment set.

## Step 5: Adjustment Set

{Engagement} blocks the backdoor path. But engagement is measured crudely (binary: opened app or not). **Confidence note:** if engagement has unmeasured dimensions (e.g., session depth, feature usage) that affect both notification targeting and retention, the adjustment is incomplete.

## Step 6b: Experiment

Adjustment set may be insufficient — unmeasured engagement dimensions. Recommend a randomized holdout: randomly withhold notifications from 10% of eligible users for 30 days.

## Step 7: Threats

- **Unmeasured confounders:** Engagement granularity beyond binary open/not-open
- **SUTVA:** Users may discuss notifications socially, contaminating control group
- **Attrition:** Users who churn can't receive notifications — survivorship bias in observational data
