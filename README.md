# -skill

自用 Cursor Agent Skills 仓库。每个 skill 一个文件夹，入口都是该目录下的 `SKILL.md`。

## 目录

| 文件夹 / 文件 | 用途 | 何时用 |
|---|---|---|
| [`research-story-writing/`](research-story-writing/) | 科研论文 / 学位论文 / final report 多 agent 写作工作流（故事优先、LaTeX 直写、规则配置、claim 登记、分节派发与冷读验收、事实审计、去 AI 腔、对抗审查） | 写或改论文、章节、课程 final report；提到合著者写作、storyline、去 AI 腔 |
| [`report_style_guide.md`](report_style_guide.md) | 实验报告整理风格指南（表格叙事、设定→表→发现） | 重写/新写实验报告，要短、结构化、少 prose |
| [`paper-figure/`](paper-figure/) | AI 论文作图，以 PPT 为主：用 python-pptx 原生形状画可编辑的架构图、机制图，数据图用 matplotlib 出图后插入；遵守 6 条作图规则（结构不写句子、灰底高亮创新点、Inter 三档字号、形状线条统一、只用 2–4 种颜色、留白）；渲染自查并自动审计 | 画、改、审论文图；提到论文作图、架构图、teaser、配色、图的风格 |

## 安装到 Cursor

把需要的 skill 文件夹拷到本机 skills 目录（不要放进 `~/.cursor/skills-cursor/`，那是 Cursor 内置区）：

```bash
git clone https://github.com/Tonkmy/-skill.git
cp -R -skill/research-story-writing ~/.cursor/skills/
```

或在某个项目里做项目级 skill：

```bash
mkdir -p /path/to/your-repo/.cursor/skills
cp -R -skill/research-story-writing /path/to/your-repo/.cursor/skills/
```

`report_style_guide.md` 目前是单文件指南，可直接 `@` 引用，或自行包成带 `SKILL.md` 的文件夹后再拷贝。

## 安装到 Claude Code

用软链接，仓库里的改动会立即生效：

```bash
ln -s "$PWD/-skill/paper-figure" ~/.claude/skills/paper-figure
```

`paper-figure` 还依赖以下工具：

- Python 包：python-pptx、matplotlib、pymupdf、Pillow
- LibreOffice（`soffice`），用于渲染自查
- 安装在 `~/Library/Fonts` 的 Inter 静态字体

详见 [`paper-figure/SKILL.md`](paper-figure/SKILL.md) 的「环境」一节。

## 怎么调用

`research-story-writing` 默认 `disable-model-invocation: true`，需要显式点名，例如：

- 「用 research-story-writing skill，按它启动论文写作 planner」
- 「按 research-story-writing 做去 AI 腔打磨 + 三镜头对抗审查」
- 已有项目续写：「读 writing/startprompt.md，按它启动」

入口说明见 [`research-story-writing/SKILL.md`](research-story-writing/SKILL.md)。同目录还有：

- `section-prompt-template.md` — 分节写作 prompt 模板
- `acceptance-and-audit.md` — 冷读验收（反向大纲、首句、5 分钟测试）与数字 / 引用 / claim 审计
- `polish-and-review.md` — 章节与全文对抗审查、去 AI 腔打磨、收敛
- `paper-archetypes.md` — 论文原型卡与从范文蒸馏的流程
- `templates/` — 启动时拷进项目的文件（规则配置、claims、storyline、术语、来源、台账、启动 prompt、LaTeX 标记宏）
- `examples/dmd-final-report.md` — 最初那次 final report 的文件指针
- `TODO.md` — 暂缓的模块（成稿后高强度审稿、rebuttal 等）

`paper-figure` 可以自动触发，也可以点名，例如：

- 「用 paper-figure 按规则重画 Fig. 1，另存新版本」
- 「用 paper-figure 审一下这份 pptx 的图」

论文相关的信息写在 `paper-figure/projects/<论文>.md`，这个文件只留在本地，已加入 .gitignore，因为它含有未发表的内容。

## 新增 skill 约定

1. 新建 `kebab-case/` 文件夹
2. 必有 `SKILL.md`（YAML frontmatter：`name` + `description`）
3. 细节放到同级 `*.md`，由 `SKILL.md` 一层链接；模板和示例可放 `templates/`、`examples/` 子目录
4. 更新本 README 的「目录」表
