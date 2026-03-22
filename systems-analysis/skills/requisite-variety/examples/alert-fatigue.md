# Example: Alert Fatigue in a Monitoring System

An SRE team has 400+ alert rules. On-call engineers ignore most alerts because 95% are false positives. The team's response: add more precise alert rules.

## Name the Parts

- **D** — system disturbances (deployments, traffic spikes, infrastructure failures, dependency outages, config changes)
- **R** — alert rule set (400 static threshold rules)
- **T** — production environment
- **E** — service health (latency, error rate, availability)
- **η** — SLA targets (p99 < 200ms, error rate < 0.1%, availability > 99.9%)

## Requisite Variety

**Executable verification:** Count D's variety — enumerate distinct disturbance categories from the last 90 days of incident reports. Result: 47 distinct root cause categories, with new categories appearing at ~3/month. R has 400 rules, but they're threshold rules on ~15 metrics. R's *effective* variety is ~15 (one response per metric), not 400. D (47+ and growing) > R (15 effective). Variety gap.

## Good Regulator

The alert rules model "healthy" as "metrics within static thresholds." They have no model of what the system looks like during deployments, traffic ramps, or dependency degradation. The regulator can't distinguish a normal deploy spike from a real incident — so it alerts on both.

## Constraints

Can we find structure in D that reduces its effective variety? Yes: 80% of false positives come from three patterns — deploy windows, autoscaler ramps, and a noisy dependency health check. These are predictable and periodic. Constraining these (deployment-aware alert suppression, autoscaler-aware baselines, dependency health check deduplication) drops D's effective variety from 47 to ~12, which R can handle.

## Recommendation

Don't add more rules (R is already at 400 with 15 effective responses). Instead: (1) add deployment and scaling context to the regulator's model (Good Regulator), (2) suppress alerts during known-predictable disturbances (Constraints), (3) consolidate the 400 rules into ~20 SLO-based alerts that directly measure E against η.
