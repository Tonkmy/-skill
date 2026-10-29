---
type: log
game: jingcheng-shengcun
updated: 2026-10-29
---

# 维护日志

只追加，不改旧条目。

## 2026-10-29

- **做了**：
  - 通读 `page.html`（3942 行）；
  - 用 `tools/extract.js` 把数据常量抽成 `data/tables.json`，NPC 只留元数据；
  - 用 `tools/econ.js` 算出每旬收入、回本周期、买卖差价；
  - 手写 `data/events.json`（24 个事件）和 `data/characters.json`（8 个角色）；
  - 写完 01–05 分篇，并把可复用的做法提炼进 playbook 五篇。
- **决定**：
  - 仓库公开，所以只放梗概、短引用和数值，原文、代码、素材链接都不进仓库；
  - slug 用拼音（jingcheng-shengcun）；
  - 「主线」理解为四条隐式线交替触发，新作要补上显式目标栏和结局。
- **未决**：
  - 售卖渠道、定价、玩家评价，需要用户补充；
  - 参考经营游戏的研究还没开始（playbook/economy.md §8）。
