# Example: Does the Mentorship Program Improve Promotion Rates?

A company observes that mentored employees get promoted at 2x the rate of unmentored employees. Leadership wants to expand the program, citing the data as evidence it works.

## Step 1: Pearl's Ladder

"Does mentorship improve promotion rates?" is Rung 2 (intervention). The evidence — observational comparison of mentored vs. unmentored employees — is Rung 1. The gap matters because mentorship assignment is not random.

## Step 2: Gather Context

Mentors select their own mentees. Selection criteria are informal: mentors pick people they see as promising — ambitious, visible, politically connected. These traits are not recorded in HR data. No prior experiment. No waitlist or lottery.

## Step 3: Estimand

The ATE of participating in the mentorship program on promotion within 2 years, compared to not participating, for all eligible employees.

## Step 4: DAG

```
Ambition/Visibility (U, unmeasured) → Selected for Mentorship (T)
Ambition/Visibility (U, unmeasured) → Promotion (Y)
Mentorship (T) → Promotion (Y)
```

U is the unmeasured set of traits that drive both mentor selection and promotion. Mentorship may also have a direct causal effect on promotion — that's what we want to estimate — but U confounds the naive comparison.

Emit the DAG as a spec for `dag_check.py`, marking the confounder as `unobserved`:

```json
{"edges":[["AmbitionVisibility","Mentorship"],["AmbitionVisibility","Promotion"],["Mentorship","Promotion"]],"treatment":"Mentorship","outcome":"Promotion","unobserved":["AmbitionVisibility"]}
```

## Step 5: Run the Identifiability Check

The structure has one backdoor path (Mentorship ← U → Promotion) and no colliders. The only variable that blocks the path is U, which is unmeasured — so no observable adjustment set satisfies the backdoor criterion. Controlling for observable proxies (job title, tenure, performance ratings) does not solve the problem unless they fully mediate U's effect on both T and Y, and "ambition" and "political savvy" are precisely the things HR data doesn't capture.

```bash
echo '{"edges":[["AmbitionVisibility","Mentorship"],["AmbitionVisibility","Promotion"],["Mentorship","Promotion"]],"treatment":"Mentorship","outcome":"Promotion","unobserved":["AmbitionVisibility"]}' | python3 systems-analysis/skills/causal-analysis/dag_check.py
```

```
Treatment: Mentorship    Outcome: Promotion
Observed: ['Mentorship', 'Promotion']
Unobserved: ['AmbitionVisibility']

Backdoor paths (open paths confound the estimate):
  [OPEN] Mentorship - AmbitionVisibility - Promotion

Adjustment set: NOT identifiable by backdoor adjustment from observed variables (an unmeasured confounder blocks it). Consider front-door or an instrument, or an experiment.

Node classification:
  AmbitionVisibility: confounder candidate
```

The path through Ambition/Visibility stays OPEN, and because that node is unobserved, no adjustment set can close it. The effect is **not identifiable** from this data. The tool's recommendation — front-door, an instrument, or an experiment — is exactly what Step 6b proposes.

**In plain terms:** We want to know whether being in the mentorship program actually causes promotions, not just whether mentored people get promoted more often. The 2x rate could look this way because mentors pick exactly the ambitious, visible, well-connected people who were going to be promoted anyway — the way a falling barometer predicts a storm without causing it. To call mentorship a cause, we'd have to compare like with like by accounting for ambition and political savvy, which we can't do with this data, because those traits were never recorded. That's why the only credible answer comes from a lottery.

## Step 6b: Experiment

The observational estimate is not credible. To identify the causal effect of mentorship:

- **Lottery-based assignment:** When more employees request mentorship than slots are available, assign slots by lottery. Compare lottery winners to lottery losers (intent-to-treat).
- **Randomization unit:** Individual employee
- **Stratify by:** Department, tenure band, job level
- **Primary outcome:** Promotion within 2 years of program start
- **Duration:** 2-year follow-up minimum

The lottery is both ethical (oversubscription means not everyone can participate anyway) and credible (it eliminates selection bias by construction).

**Key takeaway:** The 2x promotion rate among mentored employees is consistent with mentorship having zero causal effect and mentors simply picking people who were going to get promoted anyway. You cannot tell the difference without a randomized design.
