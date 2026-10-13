# Claims 登记表 (claim–evidence registry)

文中每一句"我们发现 / 我们提出 / 优于 …"都应能对上这里的一行。Intro 的贡献列表、Abstract 和审查 Lens A 都以这张表为准。

Strength: `strong`（多设置、多 seed、有对照）/ `moderate`（单一设置但有对照）/ `suggestive`（单次或间接证据）
Status: `supported` / `gap`（证据不够，等用户决定）/ `downgraded`（已降级措辞）/ `dropped`

| ID | Claim（读者能复述的一句话） | Scope（在什么条件下成立） | Evidence（表/图/节 + 来源文件） | Strength | 最相关工作 → 区别 | Status | 允许 / 禁止措辞 |
|---|---|---|---|---|---|---|---|

## 示例（虚构，只示意粒度）

| ID | Claim | Scope | Evidence | Strength | 最相关工作 → 区别 | Status | 允许 / 禁止措辞 |
|---|---|---|---|---|---|---|---|
| C1 | 4 步采样时，接力蒸馏的画质高于直接蒸馏 | 单个 1.3B T2V 模型，480p，3 seeds | Tab 2（`results/2026-07-20.md`） | moderate | [@keyA] 只做图像 → 我们做视频，且控制总训练步数 | supported | 允许 "consistently higher in our setting"；禁止 "outperforms existing methods" |
| C2 | 后期质量下降由 GAN 项造成 | 同上 | Fig 4，单次消融 | suggestive | — | gap | 禁止 "is caused by"；等用户决定补 seed 还是降级为 "suggests" |

## Gap 记录
| 日期 | Claim | 来源（审计 / 审查原文） | 用户决定（补证据 / 降级 / 删除） | 结果 |
|---|---|---|---|---|
