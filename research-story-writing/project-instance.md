# Project instance: Wan2.1-T2V DMD distillation report

Canonical artifacts from the 2026-07-28…31 final-report run. Prefer these over chat memory when working in that repo.

## Startup prompts (paste into a new agent)

| Role | File |
|---|---|
| Research planner (literature / experiments phase) | `research/planner_startprompt.md` |
| Writing-phase planner | `research/writing_phase_startprompt.md` ← **primary for this skill** |
| Earlier storyline-draft writer (pre-final) | session prompt pattern in Claude history 2026-07-26; outputs `research/thesis_ch*_draft.md` + `research/report_storyline_0728.md` |

User kickoff that worked: `读 research/writing_phase_startprompt.md,按它启动`

## Grounding files

- Story / argument map: `research/report_storyline_0728.md`
- Wording (no internal codenames in body): `research/presentation_wording_guide.md`
- EN bans + fixed translations: `research/writing_en_conventions.md`
- Plan + outline map: `research/final_report_plan.md`
- Citation whitelist: `research/verified_citations.md`
- Chapter materials: `research/thesis_ch1_draft.md`, `thesis_ch2_draft.md`, `thesis_ch3_draft.md`
- Acceptance ledger: `experiments/results/acceptance-log.md` (writing rows from #14)
- Number sources: `experiments/results/2026-07-{14,20,23,24,25,26}-*.md`, `research/E5_probe_results.md`
- Novelty red lines: `research/T3_novelty_adjudication.md`

## Deliverable layout from that run

- English section MD: `report/00_abstract.md` … `09_appendix.md`
- CN mirror: `report/report_cn.md`
- Figures: `figures/`
- LaTeX: `latex/main.tex`, `latex/refs.bib`

## Project hard lines (instance of skill §Hard bottom lines)

1. Numbers only from whitelist sources; freeze commit referenced in writing_phase prompt.
2. Citations only from `verified_citations.md`.
3. Method name: **step-count relay** only (never progressive/phased DMD).
4. No "student surpasses teacher"; no bare "first …" (controlled relay-vs-direct claim needs knowledge hedge).
5. No "significant".

## Observed successful order

1. Inventory + outline (`final_report_plan.md`) + whitelist + EN conventions + LaTeX skeleton  
2. Figures F1–F6 ∥ write §6 → §5 → §4  
3. §1 / §2 / §3 / §7 / §8  
4. Abstract last  
5. Full-set de-AI polish  
6. Three-lens review → fix → convergence review  
7. LaTeX assemble + CN sync  

Method kit behind the broader research phase (T0–T4): `research/workflow.md`.
