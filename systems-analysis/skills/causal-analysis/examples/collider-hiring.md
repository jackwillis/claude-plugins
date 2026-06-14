# Example: Do Prestigious Degrees Predict Job Performance?

A company analyzes current employees and finds no correlation between degree prestige and job performance. They conclude prestigious degrees don't matter for hiring.

## Step 1: Pearl's Ladder

"Do prestigious degrees predict job performance?" is Rung 2 (intervention: should we weight degrees in hiring?). The data — performance reviews of current employees — is Rung 1. But the real problem isn't the rung gap. It's that the data was pre-filtered by a collider.

## Step 4: DAG

```
Degree Prestige → Hired (Col)
Interview Performance → Hired (Col)
Degree Prestige → Job Performance (Y)
Interview Performance → Job Performance (Y)
```

"Hired" is a collider: it is caused by both Degree Prestige and Interview Performance. The company only observes employees who were hired — they are implicitly conditioning on Hired = 1.

Emit the DAG as a spec for `dag_check.py`, with the (wrong) proposed adjustment set `["Hired"]` that the employee-only data implicitly forces:

```json
{"edges":[["DegreePrestige","Hired"],["InterviewPerformance","Hired"],["DegreePrestige","JobPerformance"],["InterviewPerformance","JobPerformance"]],"treatment":"DegreePrestige","outcome":"JobPerformance","adjustment_set":["Hired"]}
```

## Step 5: Run the Identifiability Check

First, the structure: the direct path Degree → Job Performance is the effect of interest. There are no confounders and no open backdoor path — the problem is collider stratification. Conditioning on Hired (which the dataset does by construction) opens a spurious path:

Degree → Hired ← Interview Performance → Job Performance

Among hired employees, Degree and Interview Performance become negatively correlated — a candidate with a less prestigious degree was hired because they interviewed exceptionally well, and vice versa. This induced negative association biases the estimate of Degree → Job Performance toward zero (or negative), because Interview Performance is a competing predictor of Y.

```bash
echo '{"edges":[["DegreePrestige","Hired"],["InterviewPerformance","Hired"],["DegreePrestige","JobPerformance"],["InterviewPerformance","JobPerformance"]],"treatment":"DegreePrestige","outcome":"JobPerformance","adjustment_set":["Hired"]}' | python3 systems-analysis/skills/causal-analysis/dag_check.py
```

```
Treatment: DegreePrestige    Outcome: JobPerformance
Observed: ['DegreePrestige', 'Hired', 'InterviewPerformance', 'JobPerformance']
Unobserved: none

Backdoor paths (open paths confound the estimate):
  none

Adjustment set: {} (identifiable; no adjustment needed)

Proposed adjustment set ['Hired']: INVALID - contains descendants of treatment: ['Hired']

Node classification:
  Hired: descendant-of-treatment (do not adjust), collider-ish (>=2 parents)
  InterviewPerformance: other
```

The tool flags `Hired` as both a descendant of the treatment and a collider (two parents), and rejects conditioning on it. Note what the report does *not* model: it analyzes the graph as drawn, where no backdoor path exists and the effect is identifiable with the empty set. The bias here doesn't come from an open backdoor path the tool can see — it comes from the dataset *itself* being pre-filtered to `Hired = 1`, which the JSON spec can't express. The tool tells you not to adjust for the collider; it cannot tell you that you have already selected on it.

So the effect is **not identifiable** from employee-only data. Controlling for Interview Performance doesn't fix it — it's part of the same collider structure. To estimate the effect of Degree on Job Performance, you need one of:
1. **Data on rejected applicants** — break the conditioning on Hired
2. **A hiring period where degrees were ignored** — natural experiment removing one arrow into the collider
3. **An entirely different study design** that doesn't select on hiring outcome

**In plain terms:** We want to know whether a prestigious degree actually makes someone perform better on the job, not just whether the two show up together among people we hired. The "no correlation" finding is an artifact: we only ever see people who cleared the hiring bar, and conditioning on being hired is like judging dating partners you've only met because they were attractive or kind — it manufactures a correlation (here, a negative one between degree and interview performance) that isn't really there. To call degree a cause, we'd have to compare like with like across everyone who applied, which we can't do with employee-only data.

**Key takeaway:** "No correlation among employees" does not mean "no effect." The null finding is exactly what collider bias predicts, even if prestigious degrees genuinely improve performance.
