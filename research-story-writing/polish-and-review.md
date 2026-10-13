# Adversarial review + style polish

Two review scales:

- **Chapter review** (step 5, while drafting): one Lens A reviewer per accepted section, with its neighbors as context. Goal: a solid first draft, built chapter by chapter.
- **Full-set review** (step 7, after polish): all three lenses over the whole document, plus the 5-minute test and an audit.

High-intensity review of a finished paper (AC meta-review, domain expert, checklist auditor) is deferred; see [TODO.md](TODO.md).

## A. Review lenses (report only; no edits)

Each reviewer is a fresh agent and returns ≤10 issues, most severe first, in this form:

```
[MAJOR|MINOR] [WRITING|EVIDENCE_GAP] <\label or quoted sentence>
Problem: …
Fix: … (EVIDENCE_GAP: what evidence would settle it, or the weaker claim the current evidence supports)
```

An issue without a quoted sentence or a named figure/table is not actionable. Frozen numbers and hedges required by config are not defects.

| Lens | Persona | Looks for |
|---|---|---|
| **A Reviewer** | From config: thesis examiner, or a strict, fair reviewer at the target venue (top ML venue while the target is TBD) | Claim–evidence fit (too strong **or** too weak), missing baselines / ablations / seeds, argument flow, figures, related-work fairness, reproducibility narration, abstract/intro promises vs delivery |
| **B Style auditor** | Enforces the polish rubric in section B | AI tells, defensive repetition, readability of early chapters, broken story hooks |
| **C Cold reader** | ML-literate outsider | Late definitions, unclear referents, logic jumps, unanswered section openings, figure/text mismatch, sudden protocol switches, density-induced skimming |

Reviewers running on the same model diverge more when their inputs differ, so vary the inputs: Lens A gets the target's review form (if known) and `claims.md`; Lens B gets this rubric and the archetype exemplars; Lens C gets only the PDF.

**EVIDENCE_GAP issues are routed, never written around.** The planner moves them to the Gap 记录 table in `claims.md` for the user's decision ([acceptance-and-audit.md](acceptance-and-audit.md), section D). WRITING issues go to the writer or a fix agent.

## B. De-AI / anti-defensive polish

Dispatch one writing agent over the full set of section `.tex` files once all sections are accepted. Facts stay frozen; expression and clarity move. Invariants, checked afterwards by the auditor (C1–C3 in [acceptance-and-audit.md](acceptance-and-audit.md)):

- No add/delete/change of decimals, percents, × multiples, ±std, md5s, scientific notation.
- Protocol integers may be **deduplicated** (keep first occurrence of each protocol gloss) but not newly invented.
- Keep `\cite` keys and `\label` / `\ref` / `\cref`; table and figure environments byte-stable unless user allows.
- Preserve required hedges and scope conditions on first occurrence; preserve section hooks' **function** (wording may change).

Polish priority:

1. Drop repeated hedges / protocol glosses already in a nearby caption.
2. Kill AI tells: em-dash asides (>1 per paragraph), aphoristic closers, personification, theatrical colon lists, stacked triads, fancy diction.
3. Cap sharp `not X but Y` reversals (default ≤3 document-wide) for the heaviest claims only.
4. Prefer short SVO academic English; plain transitions (However / Therefore / Specifically).
5. Shorten by cutting: repeated hedges > ornament > chapter meta ("This section records…") > non-load-bearing detail. **Never cut** first number glosses, first hedges, scope conditions, first figure refs, findings, or limitation bullets.

### Examples (illustrative)

| Tell | Before | After |
|---|---|---|
| Aphoristic closer | "…and the gap closes. Distillation, it turns out, is about what the student learns to forget." | "…and the gap closes." |
| Stacked triad | "The relay student is faster, more stable, and more elegant." | "The relay student is faster and more stable." |
| Theatrical colon | "The culprit is simple: the GAN term." | "The drop comes from the GAN term." |
| Stacked hedges | "These results may potentially suggest that relay could possibly help." | "These results suggest that relay helps." |
| Scope (not a tell) | "Relay helps on the 1.3B model at 480p; larger models were not tested." | Unchanged: this is scope, not a hedge |

Reply format: per-file before→after word counts; top 5 deletion types with one example each; 2–3 "cut for length, maybe restore" notes. No body dump.

## C. Fix and convergence

The planner merges the lists (dedupe, resolve conflicts between lenses), applies WRITING fixes or dispatches a fix agent, then runs a **convergence review**: a new face verifies the listed fixes landed and reports ≤5 new MAJOR/MINOR issues. Under `paper` rigor the auditor re-runs after each fix round.

Stop when no MAJOR WRITING issue remains and every EVIDENCE_GAP has a user decision, or at the round cap in config, or when further edits would be change for change's sake.

## D. Optional CN mirror

Faithful sentence-level translation; numbers untouched; fixed translations from `wording.md`; keep `\cite` / `\cref` intact.
