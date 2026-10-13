---
name: research-story-writing
description: >-
  Multi-agent writing workflow for research papers, theses and final reports:
  story-first co-author writing directly in LaTeX, a planner that designs
  self-contained section prompts, a per-project rules config, a claim–evidence
  registry, agent-run fact and citation audits, cold-read acceptance tests,
  de-AI polish and adversarial review. Use when writing or revising a paper,
  thesis chapter or course final report, or when the user mentions a writing
  startprompt, storyline, 合著者写作, 去AI腔, or adversarial review of academic prose.
disable-model-invocation: true
---

# Research Story Writing

A planner–writer–reviewer workflow for academic writing, first distilled from a thesis final-report run ([example](examples/dmd-final-report.md)). What carries over between projects is the roles, the file-based handoffs and the review loops. Target rules, budgets and writing patterns live in per-project files and change with the task.

Operate as **planner** unless the user explicitly puts you in another role.

## How this skill steers judgment

Every agent here is a strong model acting as a responsible judge. Hard rules are kept to the truth constraints below; everything else is steered through context and examples:

- Give agents the project's materials, an archetype card with exemplars, and already-accepted sections as voice anchors, rather than more rules.
- Every default is soft. An agent may deviate when it serves the reader, with a one-line reason.
- When an agent misjudges the same thing twice, add an example or the missing context to the relevant template or prompt, not a new rule.

## Roles

| Role | Does | Does not |
|---|---|---|
| **Planner** (you, default) | Bootstrap project files, inventory, schedule, write task prompts, accept, route decisions, keep the ledger, compile | Write body prose |
| **Writer** | Co-author assigned sections in LaTeX from a self-contained prompt; polish passes | Invent numbers or citations; edit other sections, `main.tex`, `refs.bib` |
| **Cold reader** | Acceptance tests (reverse outline, topic sentences, 5-minute test) without the planner's context | Propose new content |
| **Auditor** | Check every number, citation and claim against `sources.md` / `claims.md` | Edit prose |
| **Reviewer** | Adversarial review through one lens; tag each issue WRITING or EVIDENCE_GAP | Edit prose; close gaps |
| **User** | Target and config, claim strength, evidence gaps, length cuts, new citations | — |

Every role except the planner runs as a fresh agent that sees only its prompt file and the files the prompt lists.

## Dispatch: everything goes through files

Each task is a prompt file `writing/prompts/<id>.md`. The agent writes its artifact (e.g. `paper/sections/04_experiments.tex`) and a short report `writing/reports/<id>.md`. Neither depends on chat history, so both modes use the same files:

- **Mode A — agent dispatch.** The host supports subagents: the planner launches one per prompt file and reads the report when it returns. Independent tasks may run in parallel, never two on the same file.
- **Mode B — human routing.** The planner writes the prompt files and tells the user which can run now. The user opens a new session per task with `读 writing/prompts/<id>.md，按它执行`, then tells the planner `<id> 完成`.

Reports stay short: status, budget vs actual, open `\missing` / `\citeneeded` markers, 0–3 judgment calls for the planner. Never paste the body.

## Writing philosophy (overrides style tips)

1. **Story > evidence dump.** One arc across the whole document; each section is a beat, not a warehouse of results. The arc's shape comes from the archetype card ([paper-archetypes.md](paper-archetypes.md)).
2. **Open writing, not defensive writing.** Inform and provoke thought; limits go in one dedicated subsection. Drop hedges (vague doubt, "may potentially"); keep scope (precise conditions, "on a 1.3B T2V model at 480p"). Numbers fold into narrative ("eight seeds give eight compositions; the student returns near-identical framings, 0.732 vs 0.59 [metric, which direction is better]"); a number's first mention names its metric and direction, and tables carry the full evidence.
3. **Writer = co-author, not typist.** Drafts and storyline are material, not scripture. A better structure or opening is welcome; a metaphor only when it maps onto a precise technical point. One-line reason when departing.
4. **Section quality test:** What question is in the reader's head now, and did this section answer it? Did they learn one new thing? If you delete this section, does the story break?

## Hard bottom lines (facts only; non-negotiable)

`writing/config.md` may replace this list; keep ≤6 items, all about truth, not style:

1. **Numbers only from sources listed in `sources.md`.** Missing → `\missing{…}` and escalate. Never invent, recall or interpolate.
2. **Citations only from the verified list in `sources.md`.** Need another → `\citeneeded{…}`; the planner has it verified and added.
3. **Project red lines** from config (reserved method names, "first" claims, off-limits comparisons).
4. **No "significant / significantly"** without a statistical test; prefer "consistent" / "same direction".
5. **Evidence gaps are never closed by wording.** A claim its evidence does not support gets new evidence or a weaker claim, and the user decides which.
6. **Do not touch remote servers, rewrite frozen tables, or edit closed ledger rows** unless the user orders it.

## Pipeline

```
Task Progress:
- [ ] 0. Bootstrap: copy templates/; fill config, sources, claims v0, storyline, wording
- [ ] 1. Target template + advisor feedback → LaTeX skeleton that compiles
- [ ] 2. Asset inventory (need → have / must-make); pick or distill the archetype card
- [ ] 3. Outline map + budget (from config) + schedule
- [ ] 4. Story probe: contribution list + Figure 1 sketch + intro v0 → 5-minute test
- [ ] 5. Section loop: Experiments → Method → Analysis/Discussion → Related → Intro → Conclusion → Abstract
- [ ] 6. Full-set polish (expression only; facts frozen)
- [ ] 7. Full-set review + audit → fix → convergence
- [ ] 8. Finalize: compile, config compliance, markers cleared, optional CN mirror
```

### 0. Bootstrap

Copy [templates/](templates/) into the project: the `.md` files into `writing/`, `writing-macros.tex` into `paper/`; create `writing/prompts/` and `writing/reports/`. Fill what is known and leave `TBD` elsewhere.

Preconditions before prose: number sources listed (frozen, or marked still-moving), a verified citation list, and a storyline and claims v0 grounded in the drafts and result notes. The first planner reply stays short: (1) the philosophy in three sentences, (2) ask for target, template and advisor feedback, (3) an inventory plan. **No body text yet.**

The config can change at any time (target, page limit, language). Log each change in its change log and check which accepted sections it affects. Once the target is chosen, dispatch an agent to read that year's call for papers, author guide, LLM-use policy and checklist (or the school's thesis rules) and fill the config with source URLs and the date checked. Never fill these from memory.

### 1–3. Template, inventory, outline

- Set up `paper/` from the target's LaTeX template: `\input{writing-macros}` after the template's own packages, one `\input` per section file, then compile. From here on everything is written in LaTeX, and humans read the PDF.
- Inventory per outline slot: `need → have (pointer) / must-make` (figures, tables, citation gaps).
- Use the archetype card named in config. If none fits the field, run the distillation in [paper-archetypes.md](paper-archetypes.md) first.
- Outline map in `storyline.md`: per section, the reader question, beat, claim IDs, evidence, closing hook and budget.
- Schedule independent sections in parallel, dependent ones serially.

### 4. Story probe

Before the section loop, a writer drafts three disposable pieces from `claims.md` and `storyline.md`: the contribution list, a Figure 1 sketch (what it must show, described or roughly plotted), and intro v0. A cold reader runs the 5-minute test on them ([acceptance-and-audit.md](acceptance-and-audit.md)). If the reader cannot restate the contributions, fix the story now while it is cheap. The intro is rewritten late in step 5 and the abstract comes last, since both get overturned as results settle.

### 5. Section loop

Write order: Experiments → Method/Protocol → Analysis/Discussion → Related work → Intro (rewrite of v0) → Conclusion → Abstract.

For each section:

1. **Prompt.** Fill [section-prompt-template.md](section-prompt-template.md). After the first acceptance, attach one accepted section as a voice anchor.
2. **Write.** The writer edits only its `.tex` file and reports.
3. **Accept** ([acceptance-and-audit.md](acceptance-and-audit.md)): planner judgment, cold-read tests, and the fact audit at the depth set in config. Two failures → **rewrite the prompt** (add an example or the missing material); do not bully the prose.
4. **Chapter review** (per section or per chapter, as config sets). A Lens A reviewer reads the text with its neighbors as context ([polish-and-review.md](polish-and-review.md)). WRITING issues go back to the writer; EVIDENCE_GAP issues go to the user through `claims.md`.
5. **Ledger and compile.** One ledger row (artifact, checks, rulings); compile and check the budget.

**Permissions:** structure, telling, figure style, prompt wording → agents decide. Config conflicts, claim strength, evidence gaps, length cuts, new citations → ask the user. Inventing numbers or references, touching servers, editing closed ledger rows → forbidden.

### 6–7. Polish and full-set review

Once every section is accepted: one expression-only polish over the full set, then a full-set review (all lenses plus the 5-minute test) and audit, fixes, and a convergence review. Details in [polish-and-review.md](polish-and-review.md).

### 8. Finalize

Compile and check against config: pages, required sections and statements, anonymity, LLM-use disclosure. No `\missing`, `\citeneeded` or `\plannernote` may remain in the text. Optional CN mirror per config. Ship "facts final, voice polishable": the user may still do a pass after delivery.

## Style defaults (soft; co-author may deviate with a reason)

- Open with the reader's question; close with this section's answer; leave a hook for the next beat.
- Prefer plain terms; the first occurrence gets a one-line gloss. Internal run codenames stay out of body text (appendix/ledger only) unless `wording.md` says otherwise.
- Negative results = "ruled out a suspect," not score-settling.
- Discussion may speculate if labeled as a clue or hypothesis.
- Limitations: short and frank, one block, no line-by-line defense.

`wording.md` wins on terminology and notation; the archetype card wins on structure.

## Grounding corpus (two layers)

**Planner always-on:** `config.md`, `storyline.md`, `claims.md`, `wording.md`, the ledger, the archetype card.

**Per task:** named draft slices, the number sources the section uses, the claim rows it carries, the relevant archetype excerpt and exemplars, the neighbors' hooks. **Do not** dump the whole repo into a prompt.

## Planner continuity

Long runs span several sessions. Keep `writing/startprompt.md` current (phase, tasks in flight, open decisions) so a new planner session resumes with `读 writing/startprompt.md，按它启动`. The ledger and `claims.md` are the memory; chat history is not.

## Files

| File | Purpose |
|---|---|
| [section-prompt-template.md](section-prompt-template.md) | Section writing prompt and prompt design rules |
| [acceptance-and-audit.md](acceptance-and-audit.md) | Cold-read acceptance tests; number, citation and claim audits; evidence gaps |
| [polish-and-review.md](polish-and-review.md) | Chapter and full-set review, de-AI polish, convergence, CN mirror |
| [paper-archetypes.md](paper-archetypes.md) | Archetype cards and how to distill them from exemplar papers |
| [templates/](templates/) | Project files copied at bootstrap |
| [examples/dmd-final-report.md](examples/dmd-final-report.md) | The original final-report run, file by file |
| [TODO.md](TODO.md) | Deferred: full-paper AC/expert review, rebuttal, literature tooling |
