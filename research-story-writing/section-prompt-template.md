# Section writing prompt template

Planner fills every bracket, then dispatches one writing agent per independent section (or a small dependent bundle). Keep the prompt self-contained; list only the files the writer may read.

```text
你是本论文的合著者,负责「[SECTION]」([~N words / soft budget]).

**这一节要回答读者的问题**:
"[READER QUESTION]"

**故事落点**:
[2–5 sentence beat: what this section proves, what it rules out, closing hook into the next section]

**素材**:
- Draft/material: [paths; structure may be reorganized; rewrite allowed with one-line reason]
- Number sources (whitelist only): [dated result notes / tables]
- Style/terminology: [wording guide + EN conventions if any]
- Citations: only keys from [verified_citations / whitelist]; do not invent

**硬底线(仅事实)**:
- Numbers only from the sources above; else [MISSING: …]
- [project red lines: naming, first-claim hedges, no surpasses-teacher, no "significant", …]
- Voice/format from template: [no I/we; tense; cross-refs as Section {n} / Figure {F…} / Table {T-…}; [@key] cites]

**写法自由**:
开头、比喻、图文配合由你定。写成读者愿意读完的一段推理,不是结果清单。
偏离底稿结构时给一句理由。

**交付**:
- Write [output path]; first line HTML comment with draft tag + date
- Final reply only: status, word count vs budget, [MISSING] list, 0–3 judgment calls for planner
- Do not paste the full body
- Do not ssh / edit acceptance-log / touch other sections' files
```

## Prompt design rules

- One reader question per section (or per subsection if the chapter is long).
- Name the **closing hook** explicitly so adjacent sections can catch it.
- Budget is soft (±10% OK if forced content); abstract band is hard if the template says so.
- Parallelize independent sections; never parallelize two writers on the same file.
- After acceptance, ledger one row: date, artifact paths, spot-check note, rulings on judgment calls.

## Example beat (pattern only)

> Reader Q: "Quality peaks early then falls, and the relay student moves a lot — who did that?"
> Beat: two single-variable surgeries (GAN off / pairing change) → three answers + hook that diversity did not move → next section's attribution close.
