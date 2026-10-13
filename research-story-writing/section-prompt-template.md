# Section writing prompt template

Planner fills every bracket, saves the result as `writing/prompts/<id>.md`, then dispatches one writing agent per independent section (or a small dependent bundle). Keep the prompt self-contained; list only the files the writer may read.

```text
你是本文的合著者，负责「[SECTION]」（`paper/sections/[NN_name].tex`，[~N 页 / 字，软预算]）。

**这一节要回答读者的问题**：
"[READER QUESTION]"

**故事落点**：
[2–5 sentence beat: what this section proves, what it rules out, closing hook into the next section]
- 上一节的收尾 hook（原文）："[…]"
- 下一节开头要接的问题："[…]"

**本节承载的 claims**（来自 writing/claims.md；措辞不能强于登记的 Strength）：
- [C1: claim | scope | 允许 / 禁止措辞]

**素材**：
- Draft/material: [paths; structure may be reorganized; rewrite allowed with one-line reason]
- Number sources (whitelist only): [files listed in writing/sources.md]
- Terminology/notation: writing/wording.md
- Citations: only keys verified in writing/sources.md; need another → \citeneeded{the claim it should support}
- Structure/pattern reference: [archetype card excerpt + 1–2 exemplar sentences]
- Voice anchor: [path of an accepted section; omit for the first one]

**硬底线（仅事实）**：
- Numbers only from the sources above; else \missing{what is missing}
- 证据撑不住的 claim 不要用措辞圆过去，在回报里提出来
- [project red lines: naming, first-claim hedges, no surpasses-teacher, no "significant", …]
- Voice/format from config: [we / impersonal; tense; \cref{sec:…} / \cref{fig:…}; \citep{key}]

**写法自由**：
开头、比喻、图文配合由你定。写成读者愿意读完的一段推理，不是结果清单。
偏离底稿结构时给一句理由。

**这一节会怎么被验收**（让你知道标准，不需要提交自查表）：
一位没有上下文的读者只读本节，写出每段的作用和本节回答的问题，再只读每段首句看推理是否连贯；之后审计会逐个核对数字、引用和 claim 措辞。

**交付**：
- Write only `paper/sections/[NN_name].tex`; first line `% draft: [tag] [YYYY-MM-DD]`
- Report to `writing/reports/[id].md`: status, budget vs actual, open \missing / \citeneeded list, 0–3 judgment calls for planner
- Do not paste the full body
- Do not ssh / edit main.tex, refs.bib, the ledger, or other sections' files
```

## Prompt design rules

- One reader question per section (or per subsection if the chapter is long).
- Quote the previous section's closing hook verbatim so the writer can catch it.
- Budget is soft (±10% OK if forced content); a hard page or abstract limit in config stays hard.
- Prefer context and examples to extra rules: when a writer misses the same thing twice, add an example or the missing material to the prompt.
- Parallelize independent sections; never parallelize two writers on the same file.
- After acceptance, ledger one row: date, artifact paths, checks, rulings on judgment calls.

## Example beat (pattern only)

> Reader Q: "Quality peaks early then falls, and the relay student moves a lot — who did that?"
> Beat: two single-variable surgeries (GAN off / pairing change) → three answers + hook that diversity did not move → next section's attribution close.
