# Jack's Claude Pluginz

## Install

Add the marketplace in Claude Code:

```
/plugin marketplace add https://github.com/jackwillis/claude-plugins.git
```

Then install individual plugins:

```
/plugin install systems-analysis@jackwillis
```

---

## systems-analysis

Claude Code plugin for systems analysis.

AI coding agents are biased toward action and toward agreement. They'll try a fix before understanding why something broke, add more rules when the problem is that rules can't keep up, or draw causal conclusions from correlations. Worse, LLMs agree with user framing 88% of the time (Cheng et.&nbsp;al) -- so if you frame the problem wrong, the agent will run with it rather than questioning it. These are the same mistakes humans make, just faster and more agreeable.

This plugin adds three skills that enforce one shared discipline: **model the system before intervening.**

### Skills

Each skill activates automatically when Claude Code detects a matching situation -- you don't invoke them directly. They add structure to the agent's reasoning at the moments where unstructured reasoning tends to go wrong.

#### Representing and Intervening

```
/representing-and-intervening
```

State what you think is happening, predict what you should see, then test one thing at a time. Forces you to enumerate available tests (REPL, spec, logs, query inspection) before grabbing the first one. When a prediction fails, asks whether the model is structurally wrong or just miscalibrated — the difference between rethinking your approach and tuning a parameter (Hacking, Schon, Argyris).

Use when: "why is this happening", "help me debug", unexplained gaps between expected and observed behavior.

#### Requisite Variety

```
/requisite-variety
```

When a control system keeps failing despite more rules, more alerts, more checks — this skill asks whether the controller has enough response variety to match its disturbances, whether it contains a model of what it's controlling, and whether you can find structure in the problem that makes it tractable. Three principles applied in order: capacity, then structure, then constraints (Ashby, Conant & Ashby).

Use when: "why can't we control this", regulation failure, alert fatigue, whack-a-mole against adaptive adversaries.

#### Design a Causal Study

```
/design-causal-study
```

Before claiming X causes Y, define exactly what you're measuring, draw the causal structure, and check whether the data can actually answer the question. Seven steps that prevent the most common errors: adjusting for variables on the causal path, conditioning on colliders, and skipping the estimand entirely (Pearl).

Use when: "does X cause Y", "should we change X to improve Y", drawing conclusions from observational data.

#### Transitions

Each skill includes transition signals. Debugging may reveal a regulation problem; regulation may need causal evidence; a causal question may turn out to be "why is this behaving this way" — and the skills hand off to each other at those points.

### Works well with Superpowers

These skills focus on *when to stop and think* — they don't manage plans, tasks, or execution. For that, pair them with [Superpowers](https://github.com/obra/superpowers):

- **Brainstorming** — explore the problem space before committing to an approach. Systems-analysis skills then pressure-test whatever direction you choose.
- **Writing Plans** — turn your model into a structured plan. Representing and Intervening builds the model; Writing Plans turns it into steps.
- **Subagent-Driven Development / Executing Plans** — execute the plan with review checkpoints. The analysis skills catch when execution reveals a wrong model.

```
/plugin install superpowers@claude-plugins-official
```

### Sources

- Hacking, I. (1983). *Representing and Intervening.*
- Ashby, W.R. (1956). *An Introduction to Cybernetics.*
- Conant, R.C. & Ashby, W.R. (1970). "Every good regulator of a system must be a model of that system."
- Schon, D. (1983). *The Reflective Practitioner.*
- Argyris, C. & Schon, D. (1978). *Organizational Learning.*
- Pearl, J. & Mackenzie, D. (2018). *The Book of Why.*
- Cheng, M. et al. (2025). "ELEPHANT: Measuring Social Sycophancy in LLMs." [arXiv:2505.13995](https://arxiv.org/abs/2505.13995).

## License

[MIT](LICENSE)
