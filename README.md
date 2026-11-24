# Claude Code Plugins for Systems Thinking

**Three plugins that add structured reasoning prompts to Claude Code.**

> **Experimental.** Under active development. These skills are prompt-based — the model doesn't always follow them. See `docs/internal/evaluation.md` for the testing methodology.

AI coding agents tend toward action over diagnosis. They can guess before modeling the problem, and sometimes treat correlation as causation. These plugins prompt for structured reasoning at the points where that tendency costs the most.

### What it looks like

You tell Claude a test passes locally but fails 30% of the time in CI. Without a structured prompt, it might guess "race condition" and start adding sleeps.

With the representing-and-intervening skill, the goal is for Claude to state two competing models (missing `ORDER BY` vs. race condition), pick the cheapest distinguishing test, and confirm before fixing. In practice, how reliably this happens varies — the skills add structure, not guarantees.

## Skills

### Systems Analysis

Analysis frameworks for modeling, causation, and control. Install:

```
/plugin install systems-analysis@jackwillis
```

| Skill | Command | Auto-triggers on |
|-------|---------|-----------------|
| [Debug with a model](docs/representing-and-intervening.md) | `/representing-and-intervening` | "why is this happening", unexplained behavior |
| [Check your controls](docs/requisite-variety.md) | `/requisite-variety` | regulation failure, alert fatigue |
| [Verify causal claims](docs/causal-analysis.md) | `/causal-analysis` | "does X cause Y", observational data |
| [Trace change propagation](docs/propagation-trace.md) | `/propagation-trace` | changing a shared interface, editing function signatures, altering defaults |
| [Staleness check](docs/staleness-check.md) | `/staleness-check` | acting on information read earlier, user signals changes |

### Break Things

Failure-mode-first test design. Install:

```
/plugin install break-things@jackwillis
```

| Skill | Command | Auto-triggers on |
|-------|---------|-----------------|
| [What to test](docs/what-to-test.md) | `/what-to-test` | "what tests do I need?", writing code that needs guards |
| [Is it tested](docs/is-it-tested.md) | `/is-it-tested` | "is this well-tested?", tests pass but production breaks |
| [Subtraction audit](docs/subtraction-audit.md) | `/subtraction-audit` | "is this over-engineered?", "what can we remove?", inherited code |

### Text Utils

Text extraction, conversion, and generation. Install:

```
/plugin install text-utils@jackwillis
```

| Skill | Command | Auto-triggers on |
|-------|---------|-----------------|
| [Disfluent](docs/disfluent.md) | `/disfluent` | "add friction", "make this rougher", reviewing AI text |
| [Riff](docs/riff.md) | `/riff` | Invoke explicitly |
| Fetch markdown | `/fetch-markdown` | Fetching web content |
| Markdown to PDF | `/markdown-to-pdf` | "make a PDF", "export as PDF" |
| Markdown to EPUB | `/markdown-to-epub` | "make an epub", "ebook version" |
| PDF to text | `/pdf-to-text` | "read this PDF", scanned documents |

### Output Styles

Claude Code output styles. Install:

```
/plugin install output-styles@jackwillis
```

| Style | What it changes |
|-------|-----------------|
| Plain dev | Literal wording, references that stand alone, and a fixed final report (What changed, Why, Verified, Not verified, Noticed not changed) |

After installing, select a style with `/config` (Output style).

### Marketplace

All four plugins are in the same marketplace:

```
/plugin marketplace add https://github.com/jackwillis/claude-plugins.git
```

Restart Claude Code after installing to load new skills.

### Requirements (text-utils)

```bash
# macOS
brew install pandoc weasyprint poppler qpdf   # core
brew install tesseract                         # optional: OCR
pipx install trafilatura                       # optional: article extraction

# Debian/Ubuntu
sudo apt install pandoc weasyprint poppler-utils qpdf
sudo apt install tesseract-ocr                 # optional: OCR
pipx install trafilatura                       # optional: article extraction
```

> **Pairs well with [Superpowers](https://github.com/obra/superpowers)** — these plugins focus on *when to stop and think*. Superpowers handles planning and execution with review checkpoints. They complement each other.

## License

[MIT](LICENSE)
