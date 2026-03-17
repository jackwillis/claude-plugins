---
name: requisite-variety
description: Use when designing, evaluating, or diagnosing control and regulation systems — especially when asking "why can't we control this?", "why does this regulator fail?", "is our defense sufficient?", or when facing a system too large to regulate by brute force. Triggers on regulation failure, alert fatigue, oscillating controllers, defense ceilings, scaling limits.
---

# Requisite Variety

Three principles for regulation and control. Sources: Ashby (1956), Conant & Ashby (1970).

## Three Principles

| Principle | Statement | Diagnostic question |
|-----------|-----------|-------------------|
| **Requisite Variety** | Only variety can absorb variety. A regulator needs at least as much response variety as the disturbance variety it faces. | Does R have enough distinct responses to match D's distinct disturbances? |
| **Good Regulator** | Every good regulator must be a model of the system it regulates. Variety without structure is brute force. | Does the regulator contain a model of the system — or is it pattern-matching without representation? |
| **Constraints** | When the system is too large for brute-force regulation, discovering structure (constraints) in the disturbances is the regulator's only path. | Can you find constraints that reduce D's effective variety below R's capacity? |

Apply in order: first check variety (capacity), then check model (structure), then look for constraints (tractability).

## Error-Controlled Regulation

A feedback regulator is inherently imperfect: the more successfully it holds E constant, the more it blocks the channel carrying its own information. Error-controlled regulators (thermostats, auto-scalers, reactive defenses) can reduce variety but never eliminate it. For tighter regulation, shift to anticipatory: get information about D *before* it reaches E.

## Name the Parts

- **D** — disturbance source (what threatens the system)
- **R** — regulator (what you're building or evaluating)
- **T** — environment (the system D acts through)
- **E** — essential variables (what must stay within limits)
- **η** — acceptable range for E

A good regulator blocks the flow of variety from D to E. Test: can you tell from E what disturbances occurred? If yes, regulation is failing.

## Red Flags

- Adding responses one-by-one against an adaptive adversary (R can never catch D)
- Regulator has no model of "healthy" (no model → no regulation)
- Tuning an oscillating controller without measuring the oscillation
- "More alerts/rules/checks" without asking: variety bottleneck or structure bottleneck?

## Rationalizations

| Thought | Reality |
|---------|---------|
| "More rules" | Adaptive D outruns enumerated R. Find constraints. |
| "Covers everything" | Coverage ≠ model. What does R *model*? |
| "Tune until stable" | Error-controlled R is inherently imperfect. May need anticipatory. |
| "Too complex to model" | Then too complex to regulate. Find constraints first. |
| "More data helps" | Only if R can act on it. Variety bounds what R can do. |

## Related Skills

- **representing-and-intervening**: R&I's Represent phase is where the Good Regulator's model gets built.
- **design-causal-study**: Pearl's framework for what can be regulated from observational data.
