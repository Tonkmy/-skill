---
name: build-research-benchmark
description: >-
  Lays out a lightweight research benchmark repo: code vs data vs artifacts,
  unique run_name, log/{run,model,eval,data}, config-driven ACP jobs, no
  overwrite, report vs logs. Use when creating a new benchmark, research
  project, experiment workspace, or when deciding where logs and checkpoints go.
---

# 轻量研究 Benchmark 建库

上半是可复用概念，不绑某个项目。下半是当前 SenseCore 机器的适配（具体路径与提交法）。不要把训练代码、checkpoint 或原始实验报告推进本 skill 仓库。

## 1. 要解决什么

新研究项目最容易在三件事上烂掉：产物找不到、同名覆盖、评测和训练不是同一套预处理。建库时先把这三件事钉死，再写模型。

目标：代码能直接跑；每一次实验都能找回 **配置、运行日志、模型、评测**；功能按需长，不先搭平台。

## 2. 关键概念

### 2.1 三层边界

| 层 | 放什么 | 是否进 git |
|---|---|---|
| 代码 | 训练/评测入口、config、薄提交脚本、报告 | 是 |
| 本项目产物 | 这次实验产生的 log、ckpt、评测、中间数据资产 | 否（目录占位可进） |
| 外部资产 | 大型 dataset、别人训好的 backbone、无关旧工程 | 否，只记绝对路径 |

不要把 Glint 一类大数据或现成 R50 权重复制进新仓库。冻结 backbone 时，只抄 **跑推理必需** 的定义和构建函数，不抄旧 loss、旧训练入口、无关依赖。

### 2.2 `run_name` 是实验身份

一次实验一个不重复的短名（字母数字 `._-`）。它同时是：

1. 集群作业名；
2. 运行日志目录名；
3. checkpoint 目录名。

名实必须由提交器构造保证，不要手改一处漏另一处。已存在则 **拒绝提交**，禁止覆盖。

评测若有多个输出（不同 feature、不同测试集、不同阈值），不要复用训练 `run_name` 当评测目录。派生一个评测名，例如 `RUN_NAME__FEATURE_target`，同样防覆盖。

提交器往往会先创建日志目录再启动 Python。拒覆盖检查 **不要** 把“只有空日志目录”当成已经跑过；应检查模型目录、tensorboard、评测结果。

### 2.3 产物四分

不要把所有东西塞进 `log/<run_name>/` 一个桶。按职责拆：

```text
log/
├── run/<run_name>/       # 作业 stdout、tensorboard
├── model/<run_name>/     # checkpoint、烘焙后的 config 快照
├── eval/<run_name>/      # 评测 json/npy/csv
└── data/<asset_name>/    # 本项目生成的可复用数据资产（不是外部 dataset）
```

只训一小块（router / predictor / LoRA）时，`model/` 只存那一块；backbone 原路径写进本次 config。

### 2.4 配置驱动，提交器要薄

- 超参放 `config/*.py`（或等价），一次实验一份 config。
- 差异用 config 或提交时 override，不复制近乎相同的训练脚本。
- 提交脚本只做：校验路径、烘焙 `run_name` 与资源、防覆盖、拉起容器、重定向日志。
- 训练入口必须也能在命令行直接跑，ACP 只是包装。
- 参数在 **提交瞬间烘焙** 进命令行，禁止提交后再改共享 config 指望正在跑的作业吃到新值。

### 2.5 训练和评测同一口径

backbone 构建、图像预处理、metric 取点必须共用工具。禁止训练一套融合、评测另一套。主裁指标写进报告入口；占用率、loss、单个 bin 只作诊断。

### 2.6 报告分层

`report/` 只留长期可读的判断。建议：

| 文档 | 职责 |
|---|---|
| 最高层实验结果记录 | 已确认判断与代表表 |
| 设计卡 | 方法语义，不是流水账 |
| 分数事实源 | 由脚本从落盘资产生成，不手改 |
| 实验索引 | run 名与资产路径 |

新分数先落盘，再生成事实表，最后摘要到最高层报告。日常命令留在 `log/`。

### 2.7 渐进扩展

1. 先最小 baseline；
2. 用现有目录实现；
3. 补 config、工具、记录；
4. 确认复用后再抽象；
5. 只加能抓住真实错误的测试。

## 3. 推荐空仓库骨架

```text
project/
├── config/
├── backbones/           # 仅在需要自带模型定义时
├── tools/
├── report/
├── acp/                 # 或 jobs/：集群提交
├── log/.gitkeep
├── train.py             # 或 train_*.py
├── eval.py
├── workflow.md          # 本项目落地约束（可链到本 skill）
└── .gitignore           # 忽略 log/*，保留 log/.gitkeep
```

目录按需创建。`.gitignore` 至少包含：

```gitignore
log/*
!log/.gitkeep
```

---

# 适配：当前服务器（SenseCore / project-face）

以下路径只适用于开发机 `/home/mnt/chenhingchin`。换机器时改这一节，不要改上半概念。

## 4. 机器入口

| 项 | 值 |
|---|---|
| 工作区根 | `/home/mnt/chenhingchin` |
| 代码 | `/home/mnt/chenhingchin/code/<project>` |
| 外部数据 | `/home/mnt/chenhingchin/data/` |
| 部分项目的外部产物 | `/home/mnt/chenhingchin/logs/`（注意是 `logs`，不是项目内 `log/`） |
| ACP 作业包装（InsightFace） | `/home/mnt/chenhingchin/jobs/acp/` |
| Python | `source /home/mnt/chenhingchin/source.sh` → conda env `/home/mnt/chenhingchin/envs/insightface_py38` |
| 容器内启动 | `cd /home/mnt/chenhingchin && source source.sh && bash start.sh` |

`start.sh` 只在 ACP 容器里跑，用来补登录环境。不要把它的内容复制进 git。

集群提交用 `srun`（SenseCore ACP），不是本机 `sbatch`。

## 5. ACP 环境文件

每个项目一份，提交前 `source`。Jacobian 现用：

`/home/mnt/chenhingchin/code/jacobian_pathway/acp/scc_env.sh`

InsightFace DualBranch 现用：

`/home/mnt/chenhingchin/jobs/acp/scc_env.sh`

字段：

```bash
export SCC_WORKSPACE_NAME=project-face
export SCC_PARTITION_ID=project-face
export SCC_RESOURCE=N1lS.Ib.I20.8          # 训练常用 8 卡
# export SCC_RESOURCE=N1lS.Ib.I20.1        # 评测常用 1 卡；InsightFace 也可用 TRAIN_RESOURCE / EVAL_RESOURCE 覆盖
export SCC_IMAGE='registry.st-sh-01.sensecore.cn/scg_rdbp_ccr/wangyongcong:20260129-12h45m33s'
```

提交时把 SKU 末段改成实际卡数，例如 `N1lS.Ib.I20.$NPROC_PER_NODE`。不要靠改共享 `scc_env.sh` 在训练和评测之间抢默认值；用环境变量覆盖。

`srun` 最小形：

```bash
srun \
  --job-name "$RUN_NAME" \
  --workspace-name "$SCC_WORKSPACE_NAME" \
  --partition-id "$SCC_PARTITION_ID" \
  --nodes 1 \
  --framework pytorch \
  --resource "$SCC_RESOURCE" \
  --output "$LOG_PATH" --async \
  --container-image "$SCC_IMAGE" \
  bash -c "$CONTAINER_CMD"
```

Jacobian 的 `submit.sh` 额外加了 `--force`。新项目与现有提交器保持同构即可。

## 6. 两种已落地布局（同一套概念）

新项目优先用 **布局 A**。布局 B 是历史 DualBranch 仓库，产物在代码仓外面。

### 布局 A · 产物在项目内 `log/`（Jacobian Pathway）

根：`/home/mnt/chenhingchin/code/jacobian_pathway`

```text
code/jacobian_pathway/
├── config/*.py
├── acp/submit.sh          # 现行提交器
├── acp/scc_env.sh
└── log/
    ├── run/<run_name>/run.log
    ├── model/<run_name>/
    ├── eval/<run_name>/
    └── data/<asset_name>/
```

提交：

```bash
cd /home/mnt/chenhingchin/code/jacobian_pathway
NPROC_PER_NODE=8 RUN_NAME=my_exp \
  bash acp/submit.sh train_xxx.py config/train_xxx.py
# 可选：OVERRIDE_CONFIG='key=value key=value'
```

默认 `RUN_NAME` = config 文件名去 `.py`。日志固定 `log/run/$RUN_NAME/run.log`。训练脚本应拒绝已有 `log/model/$RUN_NAME`、`log/eval/$RUN_NAME`、`log/run/$RUN_NAME/tensorboard`。

外部资产只引用，不复制：

| 内容 | 路径 |
|---|---|
| R50 checkpoint | `/home/mnt/chenhingchin/logs/insightface/model/glint360k_r50/model.pt` |
| Glint360K RecordIO | `/home/mnt/chenhingchin/data/insightface/glint360k_rec` |

`acp/submit_train.sh` 与 `acp/submit_eval.sh` 仍写旧路径 `log/<run_name>/`，**新实验不要用**。

### 布局 B · 产物在仓外 `logs/` + `jobs/acp/runs/`（InsightFace DualBranch）

代码根：`/home/mnt/chenhingchin/code/insightface/recognition/arcface_torch`

```text
jobs/acp/runs/<RUN_NAME>/srun.log              # 训练作业日志
jobs/acp/runs/<EVAL_NAME>/srun.log             # 评测作业日志
logs/insightface/model/<RUN_NAME>/model.pt
logs/insightface/eval/bin_eval/<EVAL_NAME>/
logs/insightface/eval/IJB_eval/<EVAL_NAME>/
data/insightface/glint360k_rec/                # 外部数据
```

`RUN_NAME` 一名三用：作业名 = `jobs/acp/runs/$RUN_NAME` = `logs/insightface/model/$RUN_NAME`。目录已存在则拒绝。

评测名：

```text
EVAL_NAME=${RUN_NAME}__${FEATURE}_${tgt}
# FEATURE ∈ fused|vt|src|none
# tgt     ∈ bin|ijbb|ijbc
```

提交：

```bash
cd /home/mnt/chenhingchin/jobs/acp

TRAIN_RESOURCE=N1lS.Ib.I20.8 \
RUN_NAME=glint360k_r50_my_exp FLAG=top30 MAX_STEPS=201720 NUM_EPOCH=99 \
EXTRA_OVERRIDES='key=value' \
  bash insightFace.sh

EVAL_RESOURCE=N1lS.Ib.I20.1 \
RUN_NAME=glint360k_r50_my_exp FEATURE=fused TARGET=all \
  bash insightFace_eval.sh
```

`EXTRA_OVERRIDES` 空格分隔 `key=value`，值里不能有空格。评测旋钮（阈值、λ）若要扫，必须换独立 `EVAL_NAME`，禁止覆盖 canonical 结果。

分数事实源由 `tools/build_eval_master.py` 从落盘 npy/json 生成，写入 `code/insightface/report/eval_master_table.md`，不要手改分数。

## 7. 在这台机器上新建一个 benchmark

1. 在 `/home/mnt/chenhingchin/code/<project>` 建骨架（§3），`.gitignore` 忽略 `log/*`。
2. 复制一份 `acp/scc_env.sh`（§5），不要改别人项目的共享文件当默认资源。
3. 写薄 `acp/submit.sh`：校验 `run_name`、创建 `log/run/$RUN_NAME`、`srun` 调 `torchrun`/`python`。
4. 训练脚本里实现拒覆盖：已有 `log/model/$RUN_NAME` 则退出。
5. 外部数据只写绝对路径进 config。
6. `report/` 先放一份最高层记录 + 一份设计卡，分数表能生成再生成。
7. 先跑通最小 baseline 再加模块。

本地对照项目：

- 布局 A：`/home/mnt/chenhingchin/code/jacobian_pathway`
- 布局 B：`/home/mnt/chenhingchin/code/insightface` 与 `/home/mnt/chenhingchin/jobs/acp`

本 skill 只约束建库与落盘，不代替各项目的方法设计文档。
