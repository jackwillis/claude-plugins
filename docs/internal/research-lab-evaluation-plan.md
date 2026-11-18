# Research Lab skill evaluation — proposal (not yet executed)

Status: draft, November 17, 2026. These two skills are **prototypes**, not marketplace-listed. Do not claim they improve research quality until tested.

## Hypothesis

Relative to a model answering the same question without a loaded skill, `design-experiment` and `review-evidence` improve detection of specific known experimental-design and inference errors, without imposing unnecessary ceremony on simple cases.

## Design

Use the existing [paired skill evaluation method](evaluation.md). Assign each test prompt to one unassisted control session and one session with exactly the relevant candidate skill loaded. Match model/version and tools; counterbalance order where possible. Keep the rubric/answer key out of the agent prompt. Save complete output, model/version, skill revision, tool availability, exact prompt, timestamp and reviewer score. Do not claim independence if the same answer key was shown to the model.

### Minimum test matrix

| ID | Skill | Planted problem | Required response behavior |
| --- | --- | --- | --- |
| DE-01 | design-experiment | Ten runs per variant on one computer are described as ten independent machines | Identifies pseudoreplication, experimental unit and suitable paired/block design |
| DE-02 | design-experiment | Animation is judged using before/after builds on different hardware | Rejects causal attribution; proposes controlled matched comparison |
| DE-03 | design-experiment | A fully reversible font-color preference is framed as a three-week statistical study | Exits quickly; does not add fake protocol |
| DE-04 | design-experiment | Label density and collision policy may interact | Proposes a bounded factorial design with outcome/guardrail |
| RE-01 | review-evidence | Study reports only successful trials and drops crashes | Flags selection/missingness and requests all trials |
| RE-02 | review-evidence | Synthetic atlas fixture passes and report claims globally accurate facts | Limits claim to synthetic contract; requests real independently reviewed cases |
| RE-03 | review-evidence | p-value is reported without prespecified outcome or decision rule | Identifies post-hoc selection and limits inference |
| RE-04 | review-evidence | Strong deterministic CRC independent-oracle test on a small fixed input | Fast exit: concise reproducible conclusion, not unnecessary causal analysis |

These are *evaluation categories*, not evidence that the skills work. Use withheld prompt wording, including at least one adversarial ambiguity per skill.

## Scoring and stopping

For each item, grade blindly where possible on three binary criteria: identifies the planted flaw, offers a valid bounded next action, and avoids a false certainty/overclaim. Record unnecessary ceremony as a fourth binary penalty. Run at least eight cases × two conditions × two model families if accessible; otherwise report the smaller study rather than extrapolating. Review individual failures, not just aggregate scores. No promotion threshold is preselected yet; choose it before inspecting treatment results.

## Publication gate

Only after independent evaluation and owner review: consider adding the plugin to the root marketplace and README, with appropriate version update. Until then this branch is a testable proposal, not an installed plugin.
