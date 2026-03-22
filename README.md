# Systems Analysis for Claude Code

**Claude Code plugins that make the agent stop and think before changing your code.**

> **Experimental.** These plugins work but are under active development. Expect rough edges.

![Claude Code Plugins](assets/header.svg)

AI coding agents are biased toward action. They'll try a fix before understanding why something broke, add more rules when the problem is that rules can't keep up, or assume one thing causes another just because they happen together. These are the same mistakes humans make, just faster.

The systems-analysis plugin adds four skills that come back to one question: **do you understand the system you're about to change?** Skills activate automatically when Claude detects a matching situation, and can also be called directly with slash commands. A second plugin, text-utils, adds utilities for working with web content and PDFs.

### What it looks like (ideal)

You tell Claude a test passes locally but fails 30% of the time in CI. Without this plugin, it guesses "race condition" and starts adding sleep calls and retries.

With the plugin installed, Claude states two competing models — missing `ORDER BY` (CI uses a parallel test runner) vs. actual race condition — and picks the cheapest test that distinguishes them: check CI config for a parallel runner. Confirms it's parallel. Adds `ORDER BY`. Runs 50 iterations. All green.

The difference: instead of guessing and retrying, Claude writes down what it thinks is happening, names what would prove it wrong, and tests that first.

| Skill | Command | What it does | Auto-triggers on |
|-------|---------|-------------|-----------------|
| Debug with a model | `/representing-and-intervening` | Write down your model before debugging | "why is this happening", unexplained behavior |
| Check your controls | `/requisite-variety` | Check if your defenses can keep up with what they're defending against | regulation failure, alert fatigue |
| Verify causal claims | `/causal-analysis` | Verify the data supports a cause-and-effect claim | "does X cause Y", observational data |
| Surface stale assumptions | `/frame-problem` | Name assumptions that may no longer hold | stale state, inherited framing |
| Fetch markdown | `/fetch-markdown` | Get clean markdown from a URL | fetching web content |
| Markdown to PDF | `/markdown-to-pdf` | Render markdown to styled PDF | "make a PDF", "export as PDF" |
| PDF to text | `/pdf-to-text` | Extract text from PDFs (digital or scanned) | "read this PDF", scanned documents |
| Riff | `/riff` | Generate name/phrase variations via diverge/converge rounds | Invoke explicitly |

## Installation

Add the marketplace, then install either plugin:

```
/plugin marketplace add https://github.com/jackwillis/claude-plugins.git
```

Restart Claude Code after installing plugins to load new skills.

## Plugins

### Systems Analysis

```
/plugin install systems-analysis@jackwillis
```

#### Debug with a Model
*`/representing-and-intervening` — Hacking (1983), Schon (1983), Argyris & Schon (1978)*

Stop debugging by trial and error. This skill makes Claude write down what it thinks is happening and what it expects to see before touching anything — so when a test surprises you, you know whether the mental model is wrong or just needs tuning.

<img src="assets/representing-and-intervening.svg" width="120">

#### Check Your Controls
*`/requisite-variety` — Ashby (1956), Conant & Ashby (1970)*

Stop adding more rules when rules can't keep up. This skill checks whether your controls can actually handle the range of problems they'll face, whether they model how the system actually works, and whether there's structure in the problem you can exploit instead of brute-forcing it.

<img src="assets/requisite-variety.svg" width="120">

#### Verify Causal Claims
*`/causal-analysis` — Pearl & Mackenzie (2018)*

Stop assuming that correlation means causation. Whether you're designing a study or auditing someone else's causal reasoning, this skill makes Claude place claims on Pearl's causal ladder, draw the causal structure, and check whether the data can actually answer the question.

<img src="assets/causal-analysis.svg" width="120">

#### Surface Stale Assumptions
*`/frame-problem` — Fodor (1987), Dennett (1984), Hayes (1973)*

Stop acting on assumptions that may no longer hold. Every action assumes things that stay the same — this skill makes Claude name those assumptions and check whether they're still true. It catches three failure modes: ignoring side effects, trying to consider everything, and getting stuck deciding what's relevant.

<img src="assets/frame-problem.svg" width="120">

#### Transitions

Each skill can hand off to the others when the situation shifts. Debugging may reveal a control problem; a control problem may need causal evidence; a causal question may turn out to be "why is this behaving this way." The frame-problem skill cuts across the other three — it fires whenever assumptions about what hasn't changed might be wrong, no matter which skill is active.

> **Pairs well with [Superpowers](https://github.com/obra/superpowers)** (`/plugin install superpowers@claude-plugins-official`) — these skills focus on *when to stop and think*, not on managing plans or execution. Superpowers handles brainstorming, planning, and executing with review checkpoints; systems-analysis skills question the thinking at each stage.

<details>
<summary><strong>Sources</strong></summary>

- Argyris, C. & Schon, D. (1978). *Organizational Learning*. Addison-Wesley.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.
- Conant, R. C. & Ashby, W. R. (1970). Every good regulator of a system must be a model of that system. *International Journal of Systems Science*, 1(2), 89–97.
- Dennett, D. C. (1984). Cognitive wheels: The frame problem of AI. In C. Hookaway (Ed.), *Minds, Machines and Evolution*. Cambridge University Press.
- Fodor, J. A. (1987). Modules, frames, fridgeons, sleeping dogs, and the music of the spheres. In Z. W. Pylyshyn (Ed.), *The Robot's Dilemma: The Frame Problem in Artificial Intelligence*. Ablex.
- Hacking, I. (1983). *Representing and Intervening*. Cambridge University Press.
- Hayes, P. J. (1973). The frame problem and related problems in artificial intelligence. University of Edinburgh.
- McCarthy, J. & Hayes, P. J. (1969). Some philosophical problems from the standpoint of artificial intelligence. *Machine Intelligence*, 4, 463–502.
- Pearl, J. & Mackenzie, D. (2018). *The Book of Why*. Basic Books.
- Saravia, E. (2022). *Prompt Engineering Guide*. https://github.com/dair-ai/Prompt-Engineering-Guide
- Schon, D. A. (1983). *The Reflective Practitioner*. Basic Books.
- Shanahan, M. (1997). *Solving the Frame Problem*. MIT Press.

</details>

### Text Utils

```
/plugin install text-utils@jackwillis
```

Three skills for getting text in and out of formats without wasting context. Themes are customizable — edit the shipped CSS or drop in your own. Requires `pandoc`, `weasyprint`, `poppler` (for `pdftotext`). Optional: `tesseract` (OCR), `trafilatura` (article extraction).

#### macOS requirements

```bash
brew install pandoc weasyprint poppler qpdf # core
brew install tesseract                      # optional: OCR
pipx install trafilatura                    # optional: article extraction
```

#### Debian requirements

```bash
sudo apt update
sudo apt install pandoc weasyprint poppler-utils qpdf # core
sudo apt install tesseract-ocr                        # optional: OCR
pipx install trafilatura                              # optional: article extraction
```

#### Fetch Markdown

Get clean markdown from a URL. Tries two independent markdown proxies, then trafilatura for article extraction, local pandoc conversion, and lynx as a plain-text fallback. Uses much less context than WebFetch.

<img src="assets/fetch-markdown.svg" width="120">

**Use when:** fetching web content for analysis, summarization, or reference.

#### Markdown to PDF

Render markdown to styled PDF using pandoc + weasyprint + CSS. Ships with three themes (default, editing, correspondence) with cross-platform font stacks. Edit the CSS or drop in your own.

<img src="assets/markdown-to-pdf.svg" width="120">

**Use when:** "make a PDF", "printable version", "export as PDF".

#### PDF to Text

Extract text from PDFs. Tries `pdftotext` first (fast, digital PDFs), falls back to OCR via `tesseract` for scanned documents. Detects which is needed automatically.

<img src="assets/pdf-to-text.svg" width="120">

**Use when:** "read this PDF", "extract text", scanned documents, image-heavy PDFs.

#### Riff

Generate variations on a name, title, phrase, or sentence by running interleaved diverge/converge rounds. Prevents settling on the first decent option by forcing multiple generation passes with selection steps in between. Choose small (3-5 finalists), medium (6-10), or large (11-20).

**Use when:** naming things, exploring phrasings, generating title options. Invoke explicitly with `/riff`.

## License

[MIT](LICENSE)
