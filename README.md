# systems-analysis

Claude Code plugin: systems analysis skills from Hacking, Ashby, and Pearl.

## The shared principle

Model the system before intervening. All three skills enforce this in different domains:

| Skill | Domain | Enforces |
|-------|--------|----------|
| **representing-and-intervening** | Debugging and diagnosis | Represent → Predict → Intervene. No fix without a written prediction. |
| **requisite-variety** | Regulation and control | Name D/R/T/E/η. Check variety, then model, then constraints. |
| **design-causal-study** | Causal claims | Define estimand → Draw DAG → Check identifiability. No study without structure. |

## Skills

### representing-and-intervening

Epistemic discipline for debugging. Based on Ian Hacking's *Representing and Intervening*: you must model a system before predicting its behavior, and predict before intervening. Check whether you're solving the right problem before solving it (Schon). Update decisions distinguish single-loop from double-loop learning (Argyris).

Triggers on: "why is this happening", "help me debug", unexplained gaps between expected and observed behavior.

### requisite-variety

Regulatory analysis for control systems. Based on Ashby's *Introduction to Cybernetics* (1956) and Conant & Ashby's Good Regulator theorem (1970). Three principles applied in order: requisite variety (capacity), good regulator (structure), constraints (tractability). Includes error-controlled regulation limits and the D/R/T/E/η framework.

Triggers on: "why can't we control this", regulation failure, alert fatigue, oscillating controllers, scaling limits.

### design-causal-study

Causal identification before study design. Based on Pearl's causal inference framework. Seven steps from estimand definition through DAG construction, backdoor paths, collider checks, to threat assessment. Prevents the most common causal reasoning errors (mediator adjustment, collider conditioning, skipping the estimand).

Triggers on: "does X cause Y", "should we change X to improve Y", correlation-vs-causation questions.

## Transitions between skills

Each skill includes transition signals — conditions under which the current skill's output becomes the entry point for another:

- **R&I → requisite-variety**: Model reveals a regulation problem (regulator can't match disturbance variety)
- **R&I → design-causal-study**: Represent phase needs causal structure from observational data
- **requisite-variety → R&I**: Can't name D/R/T/E/η (need a model first)
- **requisite-variety → design-causal-study**: Need to establish a causal link before designing the regulator
- **design-causal-study → R&I**: Question is "why is this behaving this way" rather than "does X cause Y"
- **design-causal-study → requisite-variety**: Causal structure reveals a regulation problem

## Sources

- Hacking, I. (1983). *Representing and Intervening.*
- Ashby, W.R. (1956). *An Introduction to Cybernetics.*
- Conant, R.C. & Ashby, W.R. (1970). "Every good regulator of a system must be a model of that system."
- Schon, D. (1983). *The Reflective Practitioner.*
- Argyris, C. & Schon, D. (1978). *Organizational Learning.*
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference.*

## License

[MIT](LICENSE)
