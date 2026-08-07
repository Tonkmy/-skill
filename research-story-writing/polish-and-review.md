# Style polish + adversarial review

Run **after** section content is accepted. Facts stay frozen; expression and clarity move.

## A. De-AI / anti-defensive polish

Dispatch one writing agent over the full MD set. Invariants (machine-checkable):

- No add/delete/change of decimals, percents, × multiples, md5s, scientific notation.
- Protocol integers may be **deduplicated** (keep first occurrence of each protocol gloss) but not newly invented.
- Keep cite keys and cross-ref placeholders; tables/captions byte-stable unless user allows.
- Preserve required hedges on first occurrence; preserve section hooks' **function** (wording may change).

Polish priority:

1. Drop repeated hedges / protocol glosses already in a nearby caption.
2. Kill AI tells: em-dash asides (>1 per paragraph), aphoristic closers, personification, theatrical colon lists, stacked triads, fancy diction.
3. Cap sharp `not X but Y` reversals (default ≤3 paper-wide) for the heaviest claims only.
4. Prefer short SVO academic English; plain transitions (However / Therefore / Specifically).
5. Shorten by cutting: repeated hedges > ornament > chapter meta ("This section records…") > non-load-bearing detail. **Never cut** first number glosses, first hedges, first figure refs, findings, or limitation bullets.

Reply format: per-file before→after word counts; top 5 deletion types with one example each; 2–3 "cut for length, maybe restore" notes. No body dump.

## B. Three-lens adversarial review (report only; no edits)

Run three reviewers in parallel (fresh agents). Each returns ≤10 issues, severity-tagged, with a one-line fix. Boundaries: no new experiments, no whitelist expansion, frozen hedges/numbers are not defects.

| Lens | Persona | Looks for |
|---|---|---|
| **A Conference reviewer** | Strict fair B-tier AI venue | Claim–evidence fit (too strong **or** too weak), argument flow, figures, related-work fairness, reproducibility narration, abstract/intro promises vs delivery, sentence clarity |
| **B Style auditor** | Enforces the polish rubric above | AI tells, defensive repetition, readability of early chapters, broken story hooks |
| **C Cold reader** | ML-literate outsider | Late definitions, unclear referents, logic jumps, unanswered section openings, figure/text mismatch, sudden protocol switches, density-induced skimming |

Planner merges, applies fixes (or dispatches a fix agent), then runs a **convergence review**: new face verifies listed fixes landed and reports ≤5 new MAJOR/MINOR issues. Stop when it says converged—or when further edits would be change-for-change's sake.

## C. Optional CN mirror

Faithful sentence-level translation; numbers untouched; fixed hedge map; keep `[@key]` / `{…}` placeholders; body terminology follows the project's wording guide.
