---
name: st-article-writing
description: This skill should be used when writing or rewriting ST Channel long-form science articles, including balanced 5-article sets across AI/ML, fluid dynamics, chemistry/materials, bio/medical, and engineering domains.
---

# ST-article-writing

## Purpose
Create high-retention scientific explainer articles for ST Channel using primary sources by domain, with conclusion-first structure, curiosity hooks, and evidence-backed technical depth. For generic "記事を書いて" requests, produce a balanced 5-article set with fixed domain allocation.

## When to Use
Trigger this skill when the request includes any of the following:
- Explain a recent paper for general technical readers
- Rewrite an article to make it more engaging without losing rigor
- Produce a Nazology-like flow (hook, surprise, why-it-matters)
- Add stronger technical depth and practical applications in the summary
- User asks to "write articles" or "記事を書いて" without specifying sources (in this case, apply the fixed 5-domain allocation and source priorities below)

## Hard Rules (Fixed 5-Article Mix + Primary Sources)
- For generic "記事を書いて" requests without explicit count/domain constraints, produce exactly 5 articles.
- Use this fixed allocation (1 article per domain):
  1. AI/ML
  2. 流体系（流体力学・CFD）
  3. 化学系（化学・材料）
  4. バイオ/医療
  5. 工学系（ロボティクス・制御・システム）
- For each article, choose one focal primary source from the domain-specific priority list below.
- Treat news/media links as context only; the focal claim source must be a paper/preprint/journal/conference primary source.
- Include absolute publication date and primary source URL in every article.

## Domain Source Priority (Primary Sources First)
- AI/ML: arXiv (`cs.AI`, `cs.LG`, `cs.CL`, `cs.CV`) + official research blogs
- 流体系: arXiv (`physics.flu-dyn`) + JFM / Physics of Fluids
- 化学系: ChemRxiv + major journals (JACS, Angewandte, Nature Chemistry family)
- バイオ/医療: bioRxiv / medRxiv + major journals
- 工学系: arXiv (`cs.RO`, `eess.SY`, `eess.SP`) + major conferences/journals

## Output Contract
Default output for generic requests: 5 Markdown articles (one per fixed domain above).  
If the user explicitly requests a single article or gives a specific single paper, follow the user request.

Each article must satisfy all conditions:
- Open with a conclusion-first lead in the first 1-2 lines
- Keep a curiosity hook in the first 3-5 lines without delaying the core conclusion
- Use a reader-facing title, never a date/slug/filename as the headline
- Add one-line catch copy under the title to spark curiosity
- State the paper title, primary link (domain-appropriate source URL), and absolute publication date
- Explain methodology and evaluation setup with specific terms before interpretation
- Report findings as claims tied to the paper, not speculation
- Use conversational Japanese while preserving technical names exactly
- Add plain-language explanations for technical terms at first mention
- Include a short actionable checklist section
- End with a summary section that lists practical application examples

## AI文体除去リライトモード（明示依頼時のみ・最優先）
Use this mode only when the user explicitly asks to rewrite existing draft text to remove AI-like tone.

Activation examples:
- `AIっぽさを消して書き直して`
- `この下書きを人が書いたように自然にして`
- `この文章を全面的にリライトして`

Hard constraints in this mode:
- Preserve meaning and facts; do not add unsupported numbers, entities, or examples.
- Keep ambiguous points ambiguous; improve readability without fabricating detail.
- Do not ask follow-up questions; complete with provided input only.
- Start directly from body text; avoid prefatory declarations.
- Remove filler hedges unless strictly necessary.
- Prefer concrete verb-led phrasing over abstract buzzwords.
- Avoid repetitive synonym chains and repeated abstract summaries.
- Vary sentence rhythm; avoid template-like cadence.
- Keep first-person voice consistent if used.

Notation constraints in this mode:
- Return only rewritten text.
- Do not use Markdown formatting.
- Minimize overuse of quotes and parentheses.
- Avoid label-style colon lists, slash-stacking concepts, and arrow notation.
- Avoid stock closing phrases.

Scope guard:
- This mode is for rewrite requests only.
- Standard long-form article generation in this skill continues to use Markdown structure and existing output contract.

## Title and Catch Copy Rules
- Prefer patterns that create tension, surprise, or risk awareness.
- Keep the title concrete and specific; avoid generic wording like "論文解説".
- Keep catch copy to one sentence and tie it to the reader's cost of being wrong.
- Do not use raw strings like `2026-02-07_xxx_note` as titles.

Examples:
- Title: `高精度なのに危ない？ SCALAR論文が暴く材料AIの盲点`
- Catch copy: `精度が高くても壊れるAIを、指標のトレードオフで見抜く。`

## Workflow

### 1) Lock coverage and focal sources
- For generic requests, pre-allocate 5 slots using the fixed domain mix (AI/ML, 流体系, 化学系, バイオ/医療, 工学系).
- For each slot, pick one focal primary source using the domain source priority rules.
- Record title, authors (if needed), abstract-level claim, publication date, and primary URL.
- Prefer one focal source per article; add secondary references only when they clarify context.

### 2) Build the narrative skeleton
- Follow the structure defined in `references/narrative-structure.md`.
- Select one central tension:
  - "High score but low trust"
  - "Common fix with hidden side effects"
  - "Lab success that fails under deployment conditions"

### 3) Draft the technical core
- Explain dataset/task/metric design before jumping to conclusions.
- Name critical terms exactly as in the paper (e.g., hallucination, consistency, retrieval regret).
- Separate observed results from interpretation.

### 4) Apply writing-technique gates
- Front-load the most important message in 1-2 lines.
- Prefer concrete nouns and visual descriptions over abstract wording.
- Assume "reader does not share your context" and add missing bridge sentences.
- Keep the main flow in inverted-pyramid order:
  1. Conclusion / what changed
  2. Evidence and method
  3. Background and bonus context
- For each technical term, explain it in one short phrase at first mention.
  - Example: `retrieval regret（目標に届かない候補を選んでしまう損失）`
  - Example: `hallucination（実在しない構造をもっともらしく出す誤り）`

### 5) Translate for practical use
- Add a "practical checklist" section with 4-6 items.
- Add a final "applications" section with 3-5 concrete use cases.
- Tie each application to a risk reduction or decision improvement.

### 6) Run quality gates
- Apply `references/fact-integrity-checklist.md` before finalizing.
- Remove any unsupported numeric claim.
- Remove sensational language that is not evidence-backed.

### 7) Save in project convention
- Save output under `02_Articles/<year>/YYYY-MM-DD_<slug>.md`.
- Keep headings concise and skimmable.

## Quick Start (Template Generator)
Use the bundled script to scaffold an article file:

```bash
python3 scripts/new_st_article.py \
  --date 2026-02-07 \
  --slug scalar_materials_foundation_models \
  --title "高精度なのに危ない？ SCALAR論文が暴く材料AIの盲点" \
  --catch-copy "精度が高くても壊れるAIを、指標のトレードオフで見抜く。" \
  --paper-title "SCALAR: Quantifying Structural Hallucination, Consistency, and Reasoning Gaps in Materials Foundation Models" \
  --paper-url "https://arxiv.org/abs/2601.22312" \
  --out /Users/akitomo/src/vault/10_Projects/ST_channnel/02_Articles/2026
```

## Resources
- `references/narrative-structure.md`: Narrative patterns for high-retention science explainers.
- `references/fact-integrity-checklist.md`: Evidence and rigor checks before publishing.
- `assets/st_article_template.md`: Reusable article template with required sections.
- `scripts/new_st_article.py`: Deterministic scaffold generator.
