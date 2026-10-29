---
name: wenyou-dangan
description: >-
  文游档案：手机 HTML 文字游戏（文游）的设计知识库，外加每个游戏一个档案工作区，作为跨会话的外部记忆和数据库。
  拆解参考游戏、设计或开发新文游（尤其女性向、经营养成、古风）、定数值和物价、写主线和角色剧情、规划贴图和音乐、
  续做某个游戏的档案时使用。Use when the user mentions 文游档案, 文游, 文字游戏, 女性向游戏, 经营游戏, 养成游戏,
  拆解或参考某个小游戏, 游戏数值, 物价, 主线, 男主, 台词, 立绘, BGM, or asks to continue a game dossier.
---

# 文游档案

做文游时的外部记忆：对话结束上下文就没了，文件会留下。知识分三层存放：

- **原则**：用户的设计理念，优先级最高。[design-principles.md](design-principles.md)
- **方法库**：可以跨游戏复用的做法，放在 [playbook/](playbook/)
- **档案**：一个游戏一个工作区，放在 `games/<slug>/`，登记在 [games/INDEX.md](games/INDEX.md)

## 开工前读（按需加载，不要一次全读）

1. [design-principles.md](design-principles.md)：必读。
2. [games/INDEX.md](games/INDEX.md)：找到这次要处理的游戏。
3. `games/<slug>/README.md`：档案首页，写着现状、下一步和文件地图。上次做到哪，从这里接上。
4. 按任务从 playbook 里挑一篇读：

   | 任务 | 读 |
   |---|---|
   | 写代码、搭骨架 | [playbook/skeleton.md](playbook/skeleton.md) |
   | 设计系统和玩法 | [playbook/systems.md](playbook/systems.md) |
   | 写主线、角色、台词 | [playbook/narrative.md](playbook/narrative.md) |
   | 定数值、物价、收益 | [playbook/economy.md](playbook/economy.md) |
   | 贴图、立绘、音乐 | [playbook/assets.md](playbook/assets.md) |

5. [taste-log.md](taste-log.md)：用户历次意见的原话。要拍板之前先查一遍。

## 目录

```
wenyou-dangan/
├── SKILL.md                入口（本文件）
├── design-principles.md    用户的设计理念 + 立项自检表
├── taste-log.md            用户意见原话，按日期追加
├── playbook/               跨游戏的方法库
│   ├── skeleton.md         单 HTML 技术骨架
│   ├── systems.md          系统模式卡
│   ├── narrative.md        主线、角色卡、台词矩阵、文风
│   ├── economy.md          数值与物价方法、参考游戏清单
│   └── assets.md           贴图音乐清单与规格
└── games/
    ├── INDEX.md            所有档案的登记表
    ├── _template/          新档案的模板
    └── <slug>/             一个游戏一个工作区
        ├── README.md       档案首页：现状、下一步、文件地图
        ├── 01…05-*.md      分篇内容
        ├── data/*.json     结构化数据：数值表、事件表、角色表
        ├── tools/          从源码抽数据、算数值的脚本
        └── log.md          维护日志
```

## 任务流程

### A. 拆解一款参考游戏

1. 在 INDEX.md 登记一行，把 `games/_template/` 复制成 `games/<slug>/`（slug 用拼音 kebab-case）。
2. 通读源文件。数值用脚本从源码抽到 `data/`，不要手抄；脚本放进 `tools/`，保证能重跑。事件和角色登记进 `data/events.json`、`data/characters.json`。
3. 按模板写分篇：技术、玩法、数值、剧情、短板。事实附上出处（`源文件:行号`），自己的判断标【判断】。
4. 把能复用的做法提炼进 playbook 对应那一篇，注明来源档案。别只留在档案里。
5. 写回（见下文「记忆协议」）。

### B. 设计或开发新作

1. 新建档案，类型填「原创」。先写 README 里的一句话定位，以及「对照设计理念」表。
2. 设计顺序：主线节拍（narrative.md）→ 成长阶梯（systems.md）→ 数值，用脚本算回本周期和目标间隔（economy.md）→ 角色卡和台词矩阵 → 素材清单（assets.md）。
3. 代码按 skeleton.md 搭。数值表的唯一来源放 `data/`，代码从这里读或从这里生成。
4. 每次改完都写回。

### C. 续做已有档案

读 README，看「下一步」，做完再写回。

## 记忆协议（每次会话结束前必做）

- **README.md**：把「现状」和「下一步」改成最新。下一个会话只读这一个文件就要能接上。
- **log.md**：追加一条，写日期、做了什么、做了什么决定及理由、还有哪些没定。
- **playbook**：新的通用做法写进对应那篇，注明来源档案。
- **taste-log.md**：用户的新意见按原话记下；同一意见第二次出现，就升级进 design-principles.md。
- **INDEX.md**：更新状态和日期。
- 日期一律写绝对日期，如 2026-10-29。

## 写法约定

- 每篇 md 开头写 frontmatter：`type`（principle / playbook / dossier / data / log / template / index）、`game`、`status`、`updated`、`sources`。以后靠 grep 就能按类型、游戏、日期检索。
- 事实和判断分开写。事实给出处；判断前加【判断】；没核实的加【待验证】；脚本估出来的数加【估算】。
- 数值放进 `data/*.json`，md 里只写结论和小表。同一条知识只存一处：档案写「这个游戏怎么做的」，playbook 写「以后怎么做」，两边互相链接，不复制内容。
- 单篇控制在约 300 行以内，超了就拆。

## 底线

- **本仓库公开。** 参考作品的完整原文、源代码、美术和音乐链接都不进仓库。仓库里只放摘要、短引用（单段不超过两句）和数值表。源文件留在本地，档案里只记本地路径。
- **不编数据。** 数值只能来自源码或脚本输出。外部游戏的数值没查证过，一律标【待验证】。
- **用户的原创作品未发布前要不要公开，先问用户。** 需要保密就像 `paper-figure/projects/` 那样，在 `.gitignore` 里忽略对应档案目录。
