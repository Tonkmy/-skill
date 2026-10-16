---
name: paper-figure
description: >-
  Draw top-venue figures for AI papers (architecture / method diagrams, teasers, mechanism and
  analysis figures, data plots) as editable PowerPoint: native shapes built with python-pptx,
  matplotlib plots inserted as images, every figure rendered and self-checked before hand-off.
  Follows the user's figure rules: structure over sentences, grey base with the novelty
  highlighted, one typeface (Inter) in three sizes, one shape and line language, 2-4 colours,
  generous whitespace, one style across all figures. Use when the user asks to draw, redraw,
  polish or audit a paper figure, or says 论文作图, 画图, 架构图, 方法图, 结构图, teaser, 机制图,
  数据图, 配色, 图的风格.
---

# 论文作图（PPT 优先）

把论文里的一个论点画成一眼能看懂的图。在 PowerPoint 里用原生形状画，用户可以直接改；数据图用 matplotlib 出图后插进去。每张图交付前都要渲染成 PNG 自己看，再跑审计脚本，对照规则改到通过。

## 开工前读

1. [style-rules.md](style-rules.md)：用户定的规则和对应的参数。必读，优先级最高。
2. `projects/<论文>.md`：当前论文的档案，记录版式尺寸、语义配色、记号、图清单、数据来源和路径。这是本地文件，含未发表内容，不进仓库。没有就按 [projects/_template.md](projects/_template.md) 新建。
3. [taste-log.md](taste-log.md)：用户历次的修改意见。同一意见出现第二次，就升级进 style-rules.md。

## 工作流

0. **定位**：这张图在哪一节、支撑哪句话（写成"读者 5 秒内要看懂：……"）、放单栏还是通栏。画布宽度用 `tokens.frame_width(slot)`；IEEE 单栏 5.67 in，通栏 11.67 in，打印比例统一 0.6。
1. **结构稿**：先不画。列出模块、信息流、语义分组、唯一的高亮对象和要出现的记号，画一个 ASCII 线框给用户确认。改已有图的小修可以跳过这步。
2. **画**：在论文的作图工作区写一个 build 脚本（不放进 skill），用 `scripts/figkit.py` 生成 pptx。数据图用 `scripts/plot_style.py` 出 PNG，再用 `fig.picture()` 按 1:1 插入。
3. **自查**：
   - 运行 `python render.py deck.pptx -o out --frame`，用 Read 逐页看 PNG。
   - 运行 `python audit_pptx.py deck.pptx`，逐条过一遍 [checklist.md](checklist.md)。
   - 审计里的 ❌ 和 ⚠️ 要么改掉，要么在交付说明里写明保留的理由。
4. **交付**：
   - 另存新版本（如 `<名字>_v1017.pptx`），绝不覆盖用户原件。
   - 附上渲染 PNG 和 3–5 行说明：改了什么，哪些需要用户拍板。
   - 最终效果以 PowerPoint 为准。用户在 PowerPoint 里"另存为 PDF"后，运行 `python render.py that.pdf --pptx deck.pptx -o out --frame`，把每张图裁成单独的 PDF。
   - LaTeX 里按 `width=\columnwidth` 或 `\textwidth` 插入，不再额外缩放。
5. **沉淀**：把用户的修改意见原话记进 taste-log.md，写明日期、哪张图、意见原话、落成了什么改动。

## figkit 速查

```python
import os, sys; sys.path.insert(0, os.path.expanduser("~/.claude/skills/paper-figure/scripts"))
from figkit import Deck
deck = Deck()                                   # 新建；Deck(path=...) 在已有 pptx 后面追加页
fig = deck.figure("full", height=4.4, name="Fig.1 architecture")
a = fig.box(x, y, w, h, "Stem")                 # 灰 = 现成 / 冻结
b = fig.box(x, y, w, h, "Adapter", role="orange", emphasis=True)  # 创新：亮色 + 粗描边 + glow
fig.arrow(a, b)                                 # 直线箭头，两端吸附在框上，用户拖框会跟着走
fig.path([p1, p2, p3], dashed=True)             # 折线（训练专用关系用虚线）；不吸附
fig.group(x, y, w, h, "Frozen backbone")        # 语义分组底框，自动置底
fig.op(x, y, "+", role="violet")                # 运算节点 ⊕
fig.vector(x, y, n=4, role="orange")            # 向量 / 嵌入图标
fig.icon("snowflake", x, y)                     # 冻结；"flame" = 可训练
fig.text(x, y, w, h, "$z_p = α e_0$")           # 标签；$…$ 里字母斜体，_ 下标，^ 上标
fig.title(x, y, "(a)", "Shared architecture")   # 面板标题
fig.legend(x, y, [("arrow", "Forward"), ("dashed", "Training only"), ("icon:snowflake", "Frozen")])
fig.picture("plot.png", 0, 0, w=fig.width)      # matplotlib 图，1:1
fig.fit("Encoder")                              # 一行放下这段文字需要的框宽
deck.save("out.pptx")
```

坐标单位是英寸，从图的导出框（FRAME）左上角算起，自动吸附 0.05 in 网格。颜色可以写 token（`"muted"`、`"orange.text"`）或十六进制。完整示例见 [scripts/demo_specimen.py](scripts/demo_specimen.py)，效果见 `examples/specimen_slide*.png`。

## 环境

- **Python**：`~/miniconda3/bin/python3`，需要 python-pptx、matplotlib、pymupdf、Pillow。脚本靠同目录 import `tokens`，运行时不要加 `-I`。
- **渲染**：用 LibreOffice（`soffice`）。它在 headless 模式下只认 fontconfig 列出的字体，所以 `render.py` 会把 `FONTCONFIG_FILE` 指向 Homebrew 的 fonts.conf。不这样做，Inter、Arial 会被悄悄换成别的字体。
- **字体**：Inter 静态 TTF 装在 `~/Library/Fonts`（Regular / Medium / SemiBold / Bold 及斜体）。PowerPoint 里非常规字重的族名写成 "Inter Medium"、"Inter SemiBold"。
- **最终效果**：以 PowerPoint 为准。glow 和字距可能与 LibreOffice 略有差别。

## 底线

- 数字只来自用户的结果文件或账本。没有数据就用醒目标注的占位，不编。
- 不覆盖、不移动用户的原始 pptx 和图，新版本另存。
- 本仓库是公开的。未发表论文的内容（方法细节、数字、图）只放在 `projects/` 和论文自己的目录里，`projects/` 已加入 .gitignore。
