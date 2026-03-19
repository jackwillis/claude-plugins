# Jack's Claude Code Plugins

![Claude Code Plugins](assets/header.svg)

Plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that make Claude stop and think before acting. Each plugin adds skills that trigger automatically when Claude detects a matching situation, or can be invoked directly with slash commands. Two plugins: one for disciplined thinking, one for getting text in and out of formats.

| Skill | What it does | Trigger |
|-------|-------------|---------|
| `/representing-and-intervening` | Write down your model before debugging | "why is this happening", unexplained behavior |
| `/requisite-variety` | Check if your controller can match its disturbances | regulation failure, alert fatigue |
| `/design-causal-study` | Verify the data supports the causal claim | "does X cause Y", observational data |
| `/frame-problem` | Surface assumptions that may have gone stale | stale state, inherited framing |
| `/fetch-markdown` | Get clean markdown from a URL | fetching web content for analysis |
| `/markdown-to-pdf` | Render markdown to styled PDF | "make a PDF", "export as PDF" |
| `/pdf-to-text` | Extract text from PDFs (digital or scanned) | "read this PDF", scanned documents |

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

No external dependencies — works with any Claude Code installation.

<img src="assets/systems-analysis.svg" width="120">

AI coding agents are biased toward action. They'll try a fix before understanding why something broke, add more rules when the problem is that rules can't keep up, or draw causal conclusions from correlations. These are the same mistakes humans make, just faster.

This plugin adds four skills that enforce one shared discipline: **model the system before intervening.** Skills activate automatically when Claude detects a matching situation, and can also be invoked directly.

#### Representing and Intervening

<img src="assets/representing-and-intervening.svg" width="120">

Stop debugging by trial and error. This skill makes you write down what you think is happening and what you expect to see before you touch anything — so when a test surprises you, you know whether your mental model is wrong or just needs tuning.

**Use when:** "why is this happening", "help me debug", unexplained gaps between expected and observed behavior. Based on Hacking (1983), Schon (1983), Argyris & Schon (1978).

#### Requisite Variety

<img src="assets/requisite-variety.svg" width="120">

Stop adding more rules when rules can't keep up. This skill checks whether your controller actually has enough response variety to match its disturbances, whether it contains a model of what it's regulating, and whether there's structure in the problem you can exploit instead of brute-forcing.

**Use when:** "why can't we control this", regulation failure, alert fatigue, whack-a-mole against adaptive adversaries. Based on Ashby (1956), Conant & Ashby (1970).

#### Design a Causal Study

<img src="assets/design-causal-study.svg" width="120">

Stop drawing causal conclusions from correlations. Seven steps that make you define what you're measuring, draw the causal structure, and check whether the data can actually answer the question — before you adjust for the wrong variables or condition on a collider.

**Use when:** "does X cause Y", "should we change X to improve Y", drawing conclusions from observational data. Based on Pearl & Mackenzie (2018).

#### The Frame Problem

<img src="assets/frame-problem.svg" width="120">

Stop acting on assumptions that may no longer hold. Every action assumes things that stay the same — this skill makes you name those assumptions and check whether they're still true. Catches three failure modes from Dennett's robot thought experiment: ignoring side effects, considering everything, and getting stuck deciding what's relevant.

**Use when:** stale state, inherited problem framing, confidence without re-verification, any gap between when information was gathered and when it's being used. Based on Fodor (1987), Dennett (1984), Hayes (1973).

#### Transitions

Each skill includes transition signals that hand off to the others when the situation shifts. Debugging may reveal a regulation problem; regulation may need causal evidence; a causal question may turn out to be "why is this behaving this way"; and at any point, assumptions may have gone stale without being re-examined. The frame-problem skill cuts across the other three — it fires whenever an agent's implicit assumptions about what hasn't changed might be wrong, regardless of which skill is currently active.

> **Pairs well with [Superpowers](https://github.com/obra/superpowers)** (`/plugin install superpowers@claude-plugins-official`) — these skills focus on *when to stop and think*, not on managing plans or execution. Superpowers handles brainstorming, planning, and executing with review checkpoints; systems-analysis skills pressure-test the thinking at each stage.


### Text Utils

```
/plugin install text-utils@jackwillis
```

<img src="assets/text-utils.svg" width="120">

Three skills for getting text in and out of formats without wasting context. Themes are customizable — edit the shipped CSS or drop in your own. Requires `pandoc`, `weasyprint`, `poppler` (for `pdftotext`). Optional: `tesseract` (OCR), `trafilatura` (article extraction).

```bash
brew install pandoc weasyprint poppler qpdf # core
brew install tesseract                      # optional: OCR
pipx install trafilatura                    # optional: article extraction
```

#### Fetch Markdown

<img src="assets/fetch-markdown.svg" width="120">

Get clean markdown from a URL. Tries a markdown proxy, then trafilatura for article extraction, then local pandoc conversion, then lynx as a plaintext fallback. Uses significantly less context than WebFetch.

**Use when:** fetching web content for analysis, summarization, or reference.

#### Markdown to PDF

<img src="assets/markdown-to-pdf.svg" width="120">

Render markdown to styled PDF using pandoc + weasyprint + CSS. Ships with three themes (default, editing, correspondence) with cross-platform font stacks. Edit the CSS or drop in your own.

**Use when:** "make a PDF", "printable version", "export as PDF".

#### PDF to Text

<img src="assets/pdf-to-text.svg" width="120">

Extract text from PDFs. Tries `pdftotext` first (fast, digital PDFs), falls back to OCR via `tesseract` for scanned documents. Detects which is needed automatically.

**Use when:** "read this PDF", "extract text", scanned documents, image-heavy PDFs.

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
- Schon, D. A. (1983). *The Reflective Practitioner*. Basic Books.
- Shanahan, M. (1997). *Solving the Frame Problem*. MIT Press.

</details>

## License

[MIT](LICENSE)
