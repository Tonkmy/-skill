---
type: log
status: active
updated: 2026-10-29
---

# 意见日志

按时间记录用户的意见。每条写清：日期 · 针对什么 · 原话 · 落成了什么（改了哪个文件或哪条规则）。同一意见第二次出现时，升级进 [design-principles.md](design-principles.md)，并在这里注明「已升级」。

## 2026-10-29 · 京城生存挑战拆解后 · 方向和理念

- **原话**：
  - 「我希望可以做点女性向游戏」
  - 「对，可以赚钱，有爽点。其实他的系统很简单，物价也未必有设计过，我们可以参考一些优质的独立经营游戏去设计。主线设计很不错，推进游戏进度，还能成长。」
  - 「我对游戏设计有几个大概的理念：1. 有成长有推进 2 简单，系统不能太复杂 3 有主线，以免不知道干什么，承担指引工作 4 丰富玩法和细节，贴图音乐等」
  - 「设计要复合 agent engineering 的理念，作为 context 以外的记忆和数据库」
- **落成**：
  - 四条理念写进 design-principles.md 第 1–4 条，已升级。
  - 「物价参考优质经营游戏」：写进 playbook/economy.md 的方法和参考游戏清单；原作的数值体检写进 games/jingcheng-shengcun/03-economy.md。
  - 「主线设计很不错」：拆成 playbook/narrative.md 的主线骨架（隐式三线交替，加显式目标栏）。
  - agent engineering：SKILL.md 里的分层存放、按需加载、记忆协议、frontmatter、事实和判断分开、数据放 JSON 并由脚本生成。
