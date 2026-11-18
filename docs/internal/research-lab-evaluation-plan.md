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

### Additional withheld challenge categories (PE-AA-01 peer review, November 18)

An independent research session found a serious planning failure in a carefully controlled antialiasing study: a final convergence requirement was much tighter than the candidate-blind numerical preflight, and the expensive geographic references did not converge. This is a failure of **instrument feasibility**, not evidence against the renderer.

Before any new skill revision is tested, reserve at least two fresh, unexposed challenge scenarios **outside the skill prompt and public answer-key materials**:

- **Instrument-limited scored study:** pristine provenance and independent review, but an approximate reference cannot meet the original frozen decision precision and resource ceiling. The review must preserve failed/partial outcomes, avoid a candidate verdict from nonconvergence, reject post-hoc threshold relaxation and avoid selection of successful fixtures.
- **Disproportionate research ceremony:** the uncertainty is narrow and a cheap analytical or deterministic test suffices. The design should not add a large causal/statistical apparatus merely to look rigorous.

Construct new fictional details rather than recycling PE-AA-01's exact numbers; keep prompt wording and rubric inaccessible to responding agents, but preserve them for the independent reviewer. **The descriptions above are evaluation-design intent, not withheld test items.** A responder who has read this public file should not be used for the blind treatment/control runs.

Test both skills where relevant, record per-case decisions and unnecessary-ceremony penalties, and report results separately from the original eight cases. The evaluations have not yet been executed.

## Scoring and stopping

For each item, grade blindly where possible on three binary criteria: identifies the planted flaw, offers a valid bounded next action, and avoids a false certainty/overclaim. Record unnecessary ceremony as a fourth binary penalty. Run at least eight cases × two conditions × two model families if accessible; otherwise report the smaller study rather than extrapolating. Review individual failures, not just aggregate scores. No promotion threshold is preselected yet; choose it before inspecting treatment results.

## Publication gate

Only after independent evaluation and owner review: consider adding the plugin to the root marketplace and README, with appropriate version update. Until then this branch is a testable proposal, not an installed plugin.
