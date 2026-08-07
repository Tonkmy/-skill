# -skill

自用 Cursor Agent Skills 仓库。每个 skill 一个文件夹，入口都是该目录下的 `SKILL.md`。

## 目录

| 文件夹 / 文件 | 用途 | 何时用 |
|---|---|---|
| [`research-story-writing/`](research-story-writing/) | 科研论文 / final report 双 agent 写作工作流（故事优先、分节派发、去 AI 腔、三镜头对抗审查） | 写或改论文、章节、课程 final report；提到合著者写作、storyline、去 AI 腔 |
| [`report_style_guide.md`](report_style_guide.md) | 实验报告整理风格指南（表格叙事、设定→表→发现） | 重写/新写实验报告，要短、结构化、少 prose |

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

## 怎么调用

`research-story-writing` 默认 `disable-model-invocation: true`，需要显式点名，例如：

- 「用 research-story-writing skill，按它启动论文写作 planner」
- 「按 research-story-writing 做去 AI 腔打磨 + 三镜头对抗审查」

入口说明见 [`research-story-writing/SKILL.md`](research-story-writing/SKILL.md)。同目录还有：

- `section-prompt-template.md` — 分节写作 prompt 模板
- `polish-and-review.md` — 风格打磨与对抗审查
- `project-instance.md` — 一次成功实例的文件指针（可按新项目改写）

## 新增 skill 约定

1. 新建 `kebab-case/` 文件夹
2. 必有 `SKILL.md`（YAML frontmatter：`name` + `description`）
3. 细节放到同级 `*.md`，由 `SKILL.md` 一层链接
4. 更新本 README 的「目录」表
