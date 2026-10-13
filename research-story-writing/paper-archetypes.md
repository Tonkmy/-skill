# Paper archetypes

Papers of different types tell their story differently: the sequence of reader questions, how space is split, what Figure 1 does, what reviewers check first. An archetype card captures this for one field and one type. Cards should be distilled from real papers (section B); the seeds in section C are placeholders until then.

`config.md` names the card in use. The planner uses it for the outline and budget; section prompts quote the relevant part plus 1–2 exemplars, as few-shot material rather than rules.

## A. Card template

```markdown
# Archetype: <field> / <type>
来源: <N 篇论文（标题、venue、年份）>；蒸馏日期: YYYY-MM-DD

## 一句话骨架
<这类论文的论证链>

## 节序列
| § | 读者此时的问题 | 典型 beat | 篇幅占比（中位数，范围） | 常见图表 |
|---|---|---|---|---|

## Figure 1
<第一张图通常承担什么：方法总览 / 关键现象 / 结果对比 …>

## 贡献列表
<通常几条；每条的句式（We propose… / We show…）；是否带证据指针>

## 写法模式
- Intro 开头: <模式 + 1 条范例（≤2 句，注明出处）>
- 结果段落: <先结论还是先设置；数字怎么嵌入；和谁比>
- Limitations: <位置、长度、语气>

## 审稿人最先查什么
<从公开审稿意见总结；没有来源就写"未知">

## 反模式
<蒸馏时看到的、读起来差的写法>

## 篇际差异
<各篇做法不同的地方：这些是自由度，不是规则>
```

Exemplars are style anchors, never text to reuse: writers do not copy their sentences.

## B. Distilling a card from papers

Input: 5–15 papers of the same field and type, preferably accepted at the target venue (a few orals or award papers help), as PDFs, arXiv IDs or OpenReview links. Public reviews of those papers, where available, feed the 审稿人最先查什么 section.

1. **Per-paper parse** (one fresh agent per paper, in parallel). Read the whole paper and fill a skeleton: type; one-sentence thesis; per section the reader question, beat, closing hook and page share; Figure 1's role; contribution-list form; how results paragraphs are built; how limitations are written; two exemplar sentences (intro opening, a results paragraph) with their location. Mark readings you are unsure of.
2. **Aggregate** (one agent). Merge the skeletons into a card: the shared skeleton, ranges rather than single numbers, patterns with exemplars, the variance section and anti-patterns.
3. **Held-out check.** A cold reader compares the card with two papers not used in step 1: does the card describe them? Revise what it misses.
4. **Save** as `archetypes/<field>-<type>.md` in this skill so later projects can reuse it, and point config at it.

Distilling writing patterns (how strong papers in a field phrase things) follows the same procedure. Add the results to the card's 写法模式 section rather than to a separate rulebook.

## C. Seed cards (placeholders until distilled)

**Method paper.** Problem and why it matters → what existing methods miss, naming the closest 2–3 works → key insight → method → main comparison against strong baselines → ablations isolating each component → analysis and limitations. Figure 1: method overview or the key phenomenon. Contribution list at the end of the intro.

**Analysis / empirical-science paper.** A puzzling observation → hypotheses (suspects) → controlled experiments that rule them in or out → what remains → implications. Figure 1: the phenomenon itself. This is the diagnostic arc of the original final-report run.

**Benchmark / dataset paper.** Gap in current evaluation → design principles → construction and quality control → baselines evaluated → findings the benchmark exposes → intended use and limits. Figure 1: examples or a taxonomy.

**Theory paper.** Setting and question → main result stated informally early → intuition → formal statements → proof sketch (full proofs in the appendix) → experiments that illustrate rather than prove → limits of the assumptions.

**Thesis / final report.** Wider than a paper: fuller background, room for negative results and the path taken, and each chapter may carry its own mini-arc around one of the types above. Required chapters come from the school's rules in config.
