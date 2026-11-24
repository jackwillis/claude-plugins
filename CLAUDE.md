# CLAUDE.md

## What this repo is

Four Claude Code plugins (systems-analysis, break-things, text-utils, output-styles) in a single repo with a shared marketplace. Each plugin is a top-level directory with its own `.claude-plugin/plugin.json` and a `skills/` tree (or an `output-styles/` directory for output-styles).

## Structure

```
systems-analysis/     # epistemic frameworks (R&I, requisite variety, causal analysis, staleness check)
break-things/         # test design (what-to-test, is-it-tested)
text-utils/           # text tools (fetch-markdown, markdown-to-pdf, pdf-to-text, riff, disfluent)
output-styles/        # output styles (plain-dev); no skills, so the skill conventions below do not apply
docs/                 # per-skill user-facing docs
docs/internal/        # contributor-facing: evaluation methodology, open questions, interagent memos
assets/               # static files
```

## Conventions

### Skills
- Each skill is a single `SKILL.md` file in `skills/<skill-name>/SKILL.md`
- Examples go in `skills/<skill-name>/examples/` as individual `.md` files
- Skills have YAML frontmatter with `name`, `description`, and nothing else
- The `description` field is the trigger — it determines when Claude loads the skill. Keep it specific and observable. Broad triggers bleed context.

### Cross-references
- Skills reference each other via "Arriving From Another Skill" and "Transition Signals" sections
- When renaming or removing a skill, grep all `skills/` directories across all three plugins for stale references

### Versioning
- Each plugin has its own version in `.claude-plugin/plugin.json`
- Bump on any skill content change, not just structural changes
- No lockstep versioning across plugins

### Voice
- Direct, concise, slightly self-aware about limitations
- State what the skill can't do, not just what it can
- Proportionality clauses: every skill should have a fast exit for simple cases
- Don't add ceremony that doesn't earn its keep

## Design principles

- **One signal per skill.** A skill that triggers on everything triggers on nothing. The staleness-check rewrite (from frame-problem) is the canonical example: "may no longer hold" → "turns passed or user acted since last read."
- **Mechanical over metacognitive.** Prefer steps the model can verifiably execute (draw a DAG, count variety, re-read a file) over steps that require introspection (name your blind spots).
- **Examples demonstrate the hard case.** The easy case is what the model already does. Examples should show where the skill changes the answer — collider detection, not simple confounding.
- **Bound generative steps.** Any step that says "enumerate" or "generate" needs a stopping condition. See is-it-tested's generator boundaries.

## Current state

See `docs/internal/evaluation.md` for the skill testing methodology.
See `docs/internal/open-questions.md` for deferred work items.
