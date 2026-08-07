---
name: research-story-writing
description: >-
  Dual-agent research paper / final-report writing workflow: story-first open
  writing, planner designs section prompts, writing agent as co-author, silent
  fact checks, de-AI polish, and three-lens adversarial review. Use when writing
  or revising a research paper, thesis chapter, course final report, or when the
  user mentions writing_phase_startprompt, storyline draft, 合著者写作, 去AI腔,
  or adversarial review of academic prose.
disable-model-invocation: true
---

# Research Story Writing

Recovered from a successful 2026-07 final-report run (ChenQingzhan DMD distillation).
Operate as **planner + prompt designer** unless the user explicitly puts you in writing-agent mode.

## Roles

| Role | Does | Does not |
|---|---|---|
| **Planner** (you, default) | Take template, inventory assets, schedule, design section prompts, accept, log | Write body prose |
| **Writing agent** (subagent / separate session) | Co-author assigned sections from a self-contained prompt | Invent numbers/citations; rewrite frozen facts |
| **User** | Router + decisions (template, claim strength, length cuts, extra citations) | — |

Startup line for a new planner session: paste or open the project's `writing_phase_startprompt.md` if it exists; otherwise follow this skill.

## Writing philosophy (overrides style tips)

1. **Story > evidence dump.** One diagnostic arc across the whole paper. Each section is a beat, not a warehouse of results.
2. **Open writing, not defensive writing.** Inform and provoke thought; do not litter body text with compliance hedges. Put limits in a dedicated subsection. Numbers fold into narrative ("eight seeds give eight compositions; the student returns near-identical framings — 0.732 vs 0.59").
3. **Writing agent = co-author, not typist.** Drafts/storyline are material, not scripture. Better structure/metaphor/opening is encouraged; one-line reason when departing.
4. **Section quality test (three questions):** What question is in the reader's head now, and did this section answer it? Did they learn one new thing? If you delete this section, does the story break?

## Hard bottom lines (facts only; non-negotiable)

Project may replace the list; keep ≤6 items, all about truth not style:

1. **Numbers only from whitelisted sources.** Missing → write `[MISSING: …]` and escalate. Never invent, recall, or interpolate.
2. **Citations only from a verified whitelist.** Need more → ask user / planner to verify-in; writing agent never fabricates refs.
3. **Frozen method naming / claim red lines** (project-specific; e.g. reserved names, "first" hedges, no "surpasses teacher").
4. **No "significant / significantly"** unless a statistical test exists; prefer same-direction / consistent.
5. **Do not touch remote servers, rewrite frozen tables, or edit prior acceptance-log rows** unless user orders it.

These constrain truth, not storytelling.

## Pipeline

```
Task Progress:
- [ ] 0. Preconditions (freeze + whitelist + storyline)
- [ ] 1. Get template + any advisor feedback
- [ ] 2. Asset inventory (need → have / must-make)
- [ ] 3. Outline map + word budget + schedule
- [ ] 4. Write order: Experiments → Methods/Protocol → Discussion → Intro/Related → Conclusion → Abstract last
- [ ] 5. Per section: design prompt → dispatch → accept → log
- [ ] 6. Style polish (de-AI; facts frozen)
- [ ] 7. Three-lens adversarial review → fix → convergence review
- [ ] 8. Format harden (MD → LaTeX/PDF) + optional CN mirror
```

### 0. Preconditions

Before prose: numbers frozen (or explicitly still-draft), citation whitelist exists, storyline / chapter drafts / result notes are the grounding corpus. First planner reply stays short: (1) three sentences on philosophy, (2) ask for template + feedback, (3) inventory plan. **No body text yet.**

### 1–3. Template, inventory, schedule

- Parse template: language, length, citation style, voice, figure/table rules.
- Inventory per outline slot: `need → have(pointer) / must-make` (figures, tables, whitelist gaps).
- Schedule independent sections in parallel; dependent sections serial.
- Log acceptances in an acceptance ledger (one row per section).

### 4–5. Section loop

For each section, planner writes a **self-contained** prompt (see [section-prompt-template.md](section-prompt-template.md)), dispatches a writing agent, then accepts.

**Accept (in order):**
1. Did it answer the reader's question / give insight?
2. Story continuity (hooks to neighbors)?
3. Open, non-defensive tone?

**Silent fact check (planner only, do not make the writer submit checklists):** spot-check 5–10 numbers vs sources; scan hard bottom lines. Fail twice → **rewrite the prompt**, do not bully the prose.

**Permissions:** structure, telling, figure style, prompt wording → agents decide. Template conflicts, claim strength, length cuts, new citations → ask user. Inventing numbers/refs, touching servers, editing closed ledger rows → forbidden.

### 6–7. Polish and review

After content acceptance: expression-only polish, then adversarial review. Details in [polish-and-review.md](polish-and-review.md).

### 8. Format

Content-final MD → typesetting. Optional CN mirror: faithful translation, fixed hedge map, no new facts. User may still do another de-AI pass after delivery—ship "facts final, voice polishable."

## Style defaults (soft; co-author may deviate with a reason)

- Open with the reader's question; close with this section's answer; leave a hook for the next beat.
- Prefer plain terms; first occurrence gets a one-line gloss. Internal run codenames stay out of body text (appendix/ledger only), unless the project wording guide says otherwise.
- Negative results = "ruled out a suspect," not score-settling.
- Discussion may speculate if labeled as clue/hypothesis.
- Limitations: short and frank, one block, no line-by-line defense.

If the project has `presentation_wording_guide.md` / `writing_en_conventions.md`, those win for terminology.

## Grounding corpus (two layers)

**Planner always-on:** storyline / argument table, wording guide, acceptance ledger, writing plan.

**Per-section for writers:** named draft slices + dated result notes as number sources + novelty/citation pool slices only as needed. **Do not** dump the whole repo into the writing prompt.

## First response checklist (planner)

1. State story-first / open / co-author in ≤3 sentences.
2. Ask for template path, language, length, citation style, advisor notes.
3. Propose inventory + write order; wait if template unknown.
4. Do not write chapter body in the planner session unless the user collapses roles on purpose.

## Project instance (this repo)

Concrete prompts and frozen artifacts for the Wan/DMD report live in-repo; see [project-instance.md](project-instance.md).
