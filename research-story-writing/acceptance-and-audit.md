# Acceptance and audit

How the planner accepts a section and how facts get checked. Cold readers and auditors are fresh agents that get only the files named below. What they return is a judgment written into the tables here, not a pass/fail from a script.

## A. Planner judgment (in order)

1. Did it answer the reader's question and teach one new thing?
2. Story continuity: does it catch the previous hook and leave one for the next section?
3. Open, non-defensive tone; claims no stronger than their rows in `claims.md`.

## B. Cold-read tests

The cold reader gets only the section's `.tex` (or its compiled PDF pages); for the 5-minute test, only the front matter. It does not get `storyline.md`: the point is to see what a reader actually takes away.

**B1. Reverse outline (every section).** For each paragraph, one line on the job it does for the reader. Then the question the section answered and a one-sentence takeaway. Flag:

- paragraphs whose job is unclear or repeats another paragraph's job;
- sentences with no job: restatements, meta-commentary ("This section records…"), ornamental closers.

The planner compares the takeaway with the beat in `storyline.md`. If they differ, the section has not landed, however good the prose.

**B2. Topic-sentence skim (every section).** Read only the first sentence of each paragraph. Does the argument still hold, in order? List the paragraphs where the chain breaks.

**B3. 5-minute test (story probe in step 4; full set in step 7).** Read only the title, abstract, Figure 1 with its caption, and the intro. Then answer without looking back: what problem, what key idea, which contributions, what evidence for each. The planner compares the answers with `claims.md`. A contribution the reader missed or misstated is a front-matter defect.

### Example: reverse-outline output (illustrative; findings invented)

```
¶1 设问：为什么质量先升后降 —— 有作用
¶2 交代两次单变量实验的设置 —— 有作用
¶3 重复 ¶2 的设置，外加一句 caption 里已有的说明 —— 与 ¶2 重复，建议合并
¶4 给出三个答案 —— 有作用；末句 "This reveals a deeper truth about distillation." 无作用（警句式收尾）
本节回答：后期质量下降来自 GAN 项，与配对方式无关
一句话收获：关掉 GAN 项后，后期质量不再下降
```

## C. Fact audit

Depth comes from `rigor` in config:

- **report:** the planner spot-checks 5–10 numbers against their sources and scans the hard bottom lines.
- **paper:** a fresh auditor checks every number, citation and claim sentence, and re-runs after every round that changes the text (fixes, polish). Nothing is sampled.

The auditor writes three tables to `writing/reports/<id>-audit.md`.

**C1. Numbers.** Every number in the section, including tables and captions.

| # | 位置（label / 段落） | 原文 | 来源 file:line | 一致？ | 备注 |
|---|---|---|---|---|---|

Flag mismatches, missing sources, wrong rounding, and numbers derived from sources in a way the sources do not show.

**C2. Citations.** Every `\cite`.

| key | 位置 | 这句话借它支撑什么 | 在已验证列表？ | 这篇文献确实支持这句话？ |
|---|---|---|---|---|

The last column is the judgment a script cannot make: a real paper cited for something it does not say is still a fabricated citation. When unsure, the auditor opens the paper.

**C3. Claims.** Every sentence that asserts a result or contribution (outperforms, first, consistently, generalizes, causes, state of the art, …).

| 句子 | Claim ID | 措辞强度 ≤ 登记强度？ | 适用范围写清了吗？ |
|---|---|---|---|

A claim sentence with no row in `claims.md` is itself a finding: either the registry lacks a row (the planner adds it and the user confirms) or the sentence goes.

## D. Evidence gaps

A gap is whatever wording cannot fix: a missing baseline, ablation, seed or dataset, or a claim stronger than its evidence. Gaps found by audits or reviews go to the Gap 记录 table in `claims.md` and to the user, who decides: add evidence, downgrade the claim, or drop it. Until then the claim's status is `gap`, and writers leave its wording alone.
