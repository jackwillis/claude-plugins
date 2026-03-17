# Jack's Claude Code Plugins

## Installation

Add the marketplace, then install any plugin:

```
/plugin marketplace add https://github.com/jackwillis/claude-plugins.git
```

Reboot Claude after installing plugins to load new skills.

![Claude Code Plugins](assets/header.svg)

## Plugins

### Systems Analysis

![systems-analysis](assets/systems-analysis.svg)

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

### Text Utils

![text-utils](assets/text-utils.svg)

```
/plugin install text-utils@jackwillis
```

Three skills for getting text in and out of formats without wasting context. Themes are customizable — edit the shipped CSS or drop in your own.

**Dependencies:** `pandoc`, `weasyprint`, `poppler` (for `pdftotext`). Optional: `tesseract` (OCR), `trafilatura` (article extraction).

```bash
brew install pandoc weasyprint poppler qpdf # core
brew install tesseract                      # optional: OCR
pipx install trafilatura                    # optional: article extraction
```

#### Fetch Markdown

```
/fetch-markdown
```

Get clean markdown from a URL. Tries a markdown proxy, then trafilatura for article extraction, then local pandoc conversion, then lynx as a plaintext fallback. Uses significantly less context than WebFetch.

**Use when:** fetching web content for analysis, summarization, or reference.

#### Markdown to PDF

```
/markdown-to-pdf
```

Render markdown to styled PDF using pandoc + weasyprint + CSS. Ships with three themes (default, editing, correspondence) with cross-platform font stacks. Edit the CSS or drop in your own.

**Use when:** "make a PDF", "printable version", "export as PDF".

**Requires:** `pandoc`, `weasyprint`

#### Read PDF

```
/read-pdf
```

Extract text from PDFs. Tries `pdftotext` first (fast, digital PDFs), falls back to OCR via `tesseract` for scanned documents. Detects which is needed automatically.

**Use when:** "read this PDF", "extract text", scanned documents, image-heavy PDFs.

**Requires:** `poppler` (`pdftotext`), optionally `tesseract` for OCR

## License

[MIT](LICENSE)
