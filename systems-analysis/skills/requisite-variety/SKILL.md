---
name: requisite-variety
description: Use when designing, evaluating, or diagnosing control and regulation systems — especially when asking "why can't we control this?", "why does this regulator fail?", "is our defense sufficient?", or when facing a system too large to regulate by brute force. Triggers on regulation failure, alert fatigue, oscillating controllers, defense ceilings, scaling limits, "we keep adding rules/alerts but it's not working", whack-a-mole against adaptive adversaries, reactive controls hitting a ceiling.
---

# Requisite Variety

Three principles for regulation and control. Sources: Ashby (1956), Conant & Ashby (1970).

## Three Principles

| Principle | Statement | Diagnostic question |
|-----------|-----------|-------------------|
| **Requisite Variety** | Only variety can absorb variety. A regulator needs at least as much response variety as the disturbance variety it faces. | Does R have enough distinct responses to match D's distinct disturbances? |
| **Good Regulator** | Every good regulator must be a model of the system it regulates. Variety without structure is brute force. | Does the regulator contain a model of the system — or is it pattern-matching without representation? |
| **Constraints** | When the system is too large for brute-force regulation, discovering structure (constraints) in the disturbances is the regulator's only path. | Can you find constraints that reduce D's effective variety below R's capacity? |

Apply in order: first check variety (capacity), then check model (structure), then look for constraints (tractability). At each step, note what you're least confident about — that's where the analysis is weakest and where you should warn the human.

## Error-Controlled Regulation

A feedback regulator is inherently imperfect: the more successfully it holds E constant, the more it blocks the channel carrying its own information. Error-controlled regulators (thermostats, auto-scalers, reactive defenses) can reduce variety but never eliminate it. For tighter regulation, shift to anticipatory: get information about D *before* it reaches E.

## Name the Parts

- **D** — disturbance source (what threatens the system)
- **R** — regulator (what you're building or evaluating)
- **T** — environment (the system D acts through)
- **E** — essential variables (what must stay within limits)
- **η** — acceptable range for E

A good regulator blocks the flow of variety from D to E. Test: can you tell from E what disturbances occurred? If yes, regulation is failing.

**Prefer executable verification.** If you can count D's states, enumerate R's responses, or measure E's variance, do that rather than reasoning about it. A computed variety gap is more convincing than an argued one.

## Worked Example: WAF That Can't Keep Up

A team has 200+ custom WAF rules but keeps getting breached. The SOC wants more rules.

**Name the parts:** D = adversary's attack variety (open, adaptive). R = WAF rule set (fixed between updates). T = web application. E = application integrity. η = no unauthorized access.

**Requisite Variety:** D is adversarially adaptive — it expands in response to R. R grows only through manual rule authorship after breaches. R can never catch D. This is a structural losing position, not a resourcing problem.

**Good Regulator:** The WAF's model of the adversary is "attacks look like past attacks." A capable adversary's next move is specifically designed to not look like past attacks. The model is wrong.

**Constraints:** The WAF constrains at the syntactic level (payload patterns). Attacks operate at the semantic level (what the application does). Syntactic constraints on a semantic adversary are leaky by construction. R needs to operate at the same level as D — behavioral analysis, runtime application self-protection.

## Red Flags

- Adding responses one-by-one against an adaptive adversary (R can never catch D)
- Regulator has no model of "healthy" (no model → no regulation)
- Tuning an oscillating controller without measuring the oscillation
- "More alerts/rules/checks" without asking: variety bottleneck or structure bottleneck?
- Accepting "we need more rules" at face value — check whether rules *can* keep up before adding more

## Rationalizations

| Thought | Reality |
|---------|---------|
| "More rules" | Adaptive D outruns enumerated R. Find constraints. |
| "Covers everything" | Coverage ≠ model. What does R *model*? |
| "Tune until stable" | Error-controlled R is inherently imperfect. May need anticipatory. |
| "Too complex to model" | Then too complex to regulate. Find constraints first. |
| "More data helps" | Only if R can act on it. Variety bounds what R can do. |
| "We need more rules" | Do rules *can* keep up? If D is adaptive, enumeration loses. |

## Examples

- [Alert fatigue](examples/alert-fatigue.md) — 400 rules with 15 effective responses, executable variety counting, constraint discovery

## Transition Signals

- **Can't name D/R/T/E/η** — you don't have a model yet → start with **representing-and-intervening**.
- **Need to establish a causal link from observational data** before designing the regulator → use **design-causal-study**.
- **Variety is sufficient but system is still failing** — the problem may be epistemic (wrong model), not regulatory → return to **representing-and-intervening**.
- **Analysis complete, regulator needs redesign** — the three principles told you what's wrong. If **brainstorming** is available, use it to explore redesign options. If **writing-plans** is available, use it to structure the work. For independent workstreams, **subagent-driven-development** can parallelize.

## Related Skills

- **representing-and-intervening**: R&I's Represent phase is where the Good Regulator's model gets built.
- **design-causal-study**: Pearl's framework for what can be regulated from observational data.
