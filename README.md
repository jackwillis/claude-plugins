# Jack's Claude Code Plugins

## Installation

Add the marketplace, then install any plugin:

```
/plugin marketplace add https://github.com/jackwillis/claude-plugins.git
```

Reboot Claude after installing plugins to load new skills.

## Plugins

### Systems Analysis

**Make your agent think before it acts.**

```
/plugin install systems-analysis@jackwillis
```

AI coding agents are biased toward action. They'll try a fix before understanding why something broke, add more rules when the problem is that rules can't keep up, or draw causal conclusions from correlations. These are the same mistakes humans make, just faster.

This plugin adds three skills that enforce one shared discipline: **model the system before intervening.** Skills activate automatically when Claude detects a matching situation, and can also be invoked directly.

#### Representing and Intervening

```
/representing-and-intervening
```

State what you think is happening, predict what you should see, then test one thing at a time. Forces you to enumerate available tests (script runner, spec, logs, query inspection) before grabbing the first one. When a prediction fails, asks whether the model is structurally wrong or just miscalibrated — the difference between rethinking your approach and tuning a parameter.

**Use when:** "why is this happening", "help me debug", unexplained gaps between expected and observed behavior.

**Sources:** Hacking (1983), Schon (1983), Argyris & Schon (1978)

#### Requisite Variety

```
/requisite-variety
```

When a control system keeps failing despite more rules, more alerts, more checks — this skill asks whether the controller has enough response variety to match its disturbances, whether it contains a model of what it's controlling, and whether you can find structure in the problem that makes it tractable. Three principles applied in order: capacity, then structure, then constraints.

**Use when:** "why can't we control this", regulation failure, alert fatigue, whack-a-mole against adaptive adversaries.

**Sources:** Ashby (1956), Conant & Ashby (1970)

#### Design a Causal Study

```
/design-causal-study
```

Before claiming X causes Y, define exactly what you're measuring, draw the causal structure, and check whether the data can actually answer the question. Seven steps that prevent the most common errors: adjusting for variables on the causal path, conditioning on colliders, and skipping the estimand entirely.

**Use when:** "does X cause Y", "should we change X to improve Y", drawing conclusions from observational data.

**Sources:** Pearl & Mackenzie (2018)

#### Transitions

Each skill includes transition signals. Debugging may reveal a regulation problem; regulation may need causal evidence; a causal question may turn out to be "why is this behaving this way" — and the skills hand off to each other at those points.

#### Works well with Superpowers

These skills focus on *when to stop and think* — they don't manage plans, tasks, or execution. For that, pair them with [Superpowers](https://github.com/obra/superpowers):

- **Brainstorming** — explore the problem space before committing to an approach. Systems-analysis skills then pressure-test whatever direction you choose.
- **Writing Plans** — turn your model into a structured plan. Representing and Intervening builds the model; Writing Plans turns it into steps.
- **Executing Plans** — execute with review checkpoints. The analysis skills catch when execution reveals a wrong model.

```
/plugin install superpowers@claude-plugins-official
```

#### References

- Hacking, I. (1983). *Representing and Intervening.*
- Ashby, W.R. (1956). *An Introduction to Cybernetics.*
- Conant, R.C. & Ashby, W.R. (1970). "Every good regulator of a system must be a model of that system."
- Schon, D. (1983). *The Reflective Practitioner.*
- Argyris, C. & Schon, D. (1978). *Organizational Learning.*
- Pearl, J. & Mackenzie, D. (2018). *The Book of Why.*

## License

[MIT](LICENSE)
