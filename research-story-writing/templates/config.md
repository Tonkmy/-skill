# 文章规则配置 (writing config)

所有字段随时可改。未定的写 `TBD`，planner 先用默认值，需要时再问。每次改动在末尾「变更记录」追加一行。
目标确定后，由 agent 读取当年的 CFP / 作者指南 / LLM 政策 / checklist（或学校的论文规定）来填写，附上链接和核对日期，不凭记忆填。

## 目标
- 文档类型: [学位论文 / 课程 final report / 会议论文 / 期刊 / workshop]
- 目标: [会议名 + 年份 / 学校与院系 / TBD]
- 规则来源: [链接]（核对日期: YYYY-MM-DD）
- 语言: [EN / CN]；中文镜像: [需要 / 不需要]
- 原型卡: [archetypes/<field>-<type>.md，或 paper-archetypes.md 里的 seed 名]

## 篇幅与格式
- 正文上限: [N 页 / N 字 / 无]；不计入: [参考文献、附录、checklist …]
- 各节预算: 见 storyline.md 大纲表（第 3 步填）
- LaTeX 模板: [路径或来源]；编译命令: [latexmk -pdf main.tex]
- 引用格式: [natbib author-year / numeric …]；交叉引用: [\cref / \ref]
- 人称与时态: [we / 无人称；方法现在时、实验过去时 …]
- 匿名: [双盲 / 单盲 / 不需要]；需要清除: [作者、机构、致谢、自引措辞、代码与项目链接 …]

## 必需部分
- Abstract: [字数上限]
- [ ] Limitations
- [ ] Broader impact / ethics statement
- [ ] Reproducibility statement
- [ ] Checklist: [名称 + 链接]
- [ ] 附录 / 补充材料（截止: …）
- [ ] LLM 使用披露: [政策链接；写在哪里、怎么写]
- 其他: [封面、声明页、中英文摘要 …]

## 审查强度
- rigor: [report / paper]
  - report: planner 抽查 5–10 个数字；每节章节审查 1 轮；全文审查 ≤2 轮
  - paper: 每轮改动后由新 auditor 全量审计数字、引用、claim；全文审查反复到收敛，上限 [N] 轮
- 章节审查: [每节 / 每章 / 关闭]
- Lens A 人设: [答辩委员 / <目标会议> 的严格公正审稿人 / 目标未定时: 顶级 ML 会议的严格公正审稿人]
- 审稿表: [目标会议审稿表的链接或字段；未知就留空]

## 项目红线（硬底线第 3 条的实例；≤6 条，只管事实）
1. [保留的方法名: … ；禁用叫法: …]
2. [不允许的比较或表述: 例如"学生超过老师"]
3. ["first …" 只在什么条件下可以说、带什么限定]

## 数字
- 格式: [小数位、是否带 %、±std 写法、seed 数怎么交代]
- 数字宏: [off / on]。on 时所有正文数字写成 `paper/numbers.tex` 里的宏，由 planner 按 sources.md 维护；实验还在变时建议 on，结果一改全文同步。

## 变更记录
| 日期 | 改了什么 | 受影响章节 | 处理 |
|---|---|---|---|
