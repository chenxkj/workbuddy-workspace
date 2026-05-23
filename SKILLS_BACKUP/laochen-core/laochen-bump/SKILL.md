---
name: laochen-bump
description: >
  老陈抖音内容创作·Rubric升级Skill（吸收CHEAT bump机制）。
  当评分偏差持续>5分或连续同向偏差≥3次时触发。
  5步强制流程（校准池重打 + 跨模型审核 + 落地 + cleanup）。
  **Phase 2强制走laochen-score-blind sub-agent**，不接受self-scored fallback。
  触发词：升级评分公式/调整权重/重校bucket/校准偏差大。
agent_created: true
---

# 老陈抖音·Rubric升级 Skill（v1.0·吸收CHEAT bump）

> **核心原则**：Rubric升级是最高风险动作，必须5步强制 + 跨模型审核。
> **与CHEAT的区别**：老陈体系用`laochen-score-blind`（Task tool spawn），CHEAT用`cheat-score-blind`。

---

## 两种模式

| 模式 | 触发 | 做什么 | 验证强度 |
|---|---|---|---|
| **完整rubric bump** | `—propose "<新公式>"` | 改公式/维度/权重 | 5步 + 跨模型审核（强制） |
| **bucket-only 重校** | `—bucket-only` | 只重新派生bucket边界 | 数据自动派生，无审核 |

---

## 完整 Rubric Bump 流程

```
[用户：升级rubric —propose "ER×2.0，砍NA，加MS"]
  ↓
[Phase 0: 前置门槛检查]
  ↓
[Phase 1: 写出新公式完整方程]
  ↓
[Phase 2: 校准池全量重打分（强制走laochen-score-blind）]
  ↓
[Phase 3: 计算排序一致性]
  ↓
[Phase 4: 跨模型独立审核（强制）]
  ↓
[Phase 5: 落地 + cleanup pass]
  ↓
[Phase 6: 更新所有校准样本的prediction文件]
```

### Constants

- **READINESS_HEURISTIC** —
  - 默认参考：校准池 ≥ 5样本 + 至少1个跨样本观察有 ≥3样本支持
  - 但Claude可以提议bump（即使样本少）如果观察信号特别强
  - Claude也可以拒绝bump（即使样本足）如果证据弱
- **THRESHOLD = 0.8** — 新排序与实绩排序一致性阈值（4/5）。写死
- **CROSS_MODEL_AUDIT = true** — 调外部LLM独立审核
- **REQUIRE_CONFIRM = true** — 落地前要求用户明确"yes, bump"

---

### Phase 0: 前置门槛检查

按以下检查清单执行：

| 检查 | 失败处理 |
|---|---|
| 校准池总样本数 vs 观察强度 | Claude判断——按READINESS_HEURISTIC |
| 上次bump距今的新校准数 vs 观察成熟度 | 默认建议 ≥3篇新样本 |
| `in_progress_session == null` | 拒绝："你有in-progress预测未完成。先走完那条流程或清掉state" |
| 触发条件成立（系统性偏差/跨样本新观察/新维度证据足） | 警告但不阻塞 |

通过 → 进入Phase 1。

---

### Phase 1: 写出新公式完整方程

**不能只接受用户的简短描述**。把它展开为完整方程：

```
当前：v5.20 composite = (ER×1.5 + SR×1.5 + HP×1.5 + QL + NA + AB + SAT) / 8.5 × 2.0
提议：v5.21 composite = (ER×2.0 + HP×1.5 + MS×1.5 + QL + SR + TS + SAT) / 9.0 × 2.0

变化总结：
- ER ×1.5 → ×2.0（升）
- SR ×1.5 → ×1.0（降）
- 新增 MS ×1.5（Memetic Shareability）
- 新增 TS ×1.0（Topic Shareability）
- 删除 NA（与HP重叠）
- 删除 AB（被TS替代）
- 归一化常数 8.5 → 9.0
- 公式总维度数：7 → 7（净变化0）
```

如果用户的提议含糊（如"ER权重提一点"）→ 询问具体数值，**禁止自己猜**。

---

### Phase 2: 校准池全量重打分（**强制走laochen-score-blind**）

Glob `predictions/*.md` 中所有有完整复盘段的文件 → 校准池。

#### 2.0 校准池纯度检查（盲验结果验证）

> **目的**：保证校准池只有盲验通过的数据，防止 contaminated 数据污染 rubric。

对校准池**每个文件**，检查盲验结果（文件第一行或复盘段第一行）：

| 盲验结果 | 处理方式 |
|:---------|:---------|
| ✅ 通过 | 保留在校准池 |
| ❌ 失败（reconstructed） | **移除**，不计入重打分 |
| ❌ 失败（contaminated） | **移除**，不计入重打分 |
| ❌ 失败（modified-post-hoc） | **移除**，不计入重打分 |
| 无盲验结果 | **移除**，标注"缺少盲验，不计入" |

**输出**：校准池纯度报告（在重打表之前输出）：

```
校准池纯度检查：
- 初始样本数：N
- 盲验通过：N1（计入校准池）
- 盲验失败：N2（已移除）
- 缺少盲验：N3（已移除）
- 最终校准池：N1 样本
```

**最终校准池 < 3** → **中止 bump**，输出："校准池不足3个盲验通过样本，无法可靠升级rubric。需要更多盲验通过的复盘数据。"

**bump是最高风险动作——所有重打必须走laochen-score-blind sub-agent**。inline重打 = 主Claude已经看过实绩，rank一致性变成overfit而非真信号。

#### 强制约束

- **不接受self-scored fallback**——`laochen-script-scoring`有双盲评审，但`laochen-bump`**没有**self-scored选项。如果Task tool不可用 → **abort bump**，向用户报告"先解决Task tool再bump"
- **不接受"我只重算composite不重打dim"** —— 即使新公式只调权重不加维度，每条prediction的所有dim都要由sub-agent重新审script

#### 对每篇prediction：

1. 解析prediction文件拿到对应`scripts/<id>.md`路径（从header字段）
2. 校验script文件存在 + hash跟header `Script Hash`一致；不一致 → 警告但仍spawn sub-agent
3. **通过Task tool spawn laochen-score-blind sub-agent**：
   ```
   Spawn laochen-score-blind sub-agent.
   
   Input:
     script_path: <prediction header的Script Path>
     rubric_config_path: .cheat-state.json
   
   Task: 按当前rubric配置给script打分。
   返回严格JSON。
   
   不要读state file / predictions/ / videos/ 任何其他文件。
   不要询问用户 —— 你没有用户。
   不要读这份prediction文件本身 —— 你只看script + rubric。
   ```
4. 等sub-agent完成 → 主流程用新公式算composite
5. 写"重打表"到`.cheat-cache/bump-rescores.json`（汇总）

**重打表结构**（增加"盲验"字段）：
```json
{
  "samples": [
    {
      "file": "predictions/2026-05-04_abc123.md",
      "script": "scripts/2026-05-04_abc123_短title.md",
      "blind_check": "✅ 通过 / ❌ 失败（reconstructed）",
      "composite_old": 8.24,
      "composite_new": 9.11,
      "rank_old": 2,
      "rank_new": 2,
      "delta": 0
    }
  ],
  "purity_report": {
    "total_initial": 7,
    "passed_blind_check": 5,
    "failed_blind_check": 2,
    "final_calibration_pool": 5
  }
}
```

---

### Phase 3: 计算排序一致性

```
每个样本：
  new_composite_rank: 用新公式排序的rank
  actual_plays_rank: 用实际播放排序的rank
  delta: |new_rank - actual_rank|

输出对照表：
| 样本 | composite (旧) | composite (新) | rank (new) | actual | rank (actual) | delta |
|---|---|---|---|---|---|---|
| 视频A | 9.41 | 9.55 | 1 | 124.8w | 1 | 0 |
| 视频B | 8.24 | 9.11 | 2 | 71.1w | 2 | 0 |

排序一致性：4/5 在 |delta| ≤ 1
Pairwise no-regression：旧公式做对的所有pair在新公式下未颠倒 ✓
```

判定：
- 排序一致性 < THRESHOLD（默认0.8） → **本地拒绝**，转Phase 4之前明确报告失败
- pairwise出现回归 → **本地拒绝**

---

### Phase 4: 跨模型独立审核（**强制**，除非escape hatch）

`CROSS_MODEL_AUDIT=true`（默认）：

调用外部LLM（如qwen-max或通过`neodata-financial-search`的LLM接口）：

```
prompt:
你是一个独立审稿人。下面是一个内容创作者准备升级的rubric公式。
请独立判定两件事：
1. 排序一致性：新公式给样本的排序与实际表现排序，是否真的在 ≥80% 样本上一致？
2. 解释力：新公式相比旧公式，是否更好地解释了校准池的实绩分布？

数据：
旧公式：(ER×1.5 + SR×1.5 + HP×1.5 + QL + NA + AB + SAT) / 8.5 × 2.0
新公式：(ER×2.0 + HP×1.5 + MS×1.5 + QL + SR + TS + SAT) / 9.0 × 2.0

校准池：
[Phase 2重打表的完整JSON]

排序对照：
[Phase 3表格的完整JSON]

输出格式：
- 判定：PASS 或 REJECT
- 理由：≥100字
- 关键风险：[如有，列出新公式的潜在问题]
```

收到外部LLM回复 → 解析判定。

判定逻辑：
- 本地PASS + 外部PASS → 通过，进入Phase 5
- 本地PASS + 外部REJECT → **视为REJECT**
- 本地REJECT → 已在Phase 3终止

---

### Phase 5: 落地 + cleanup pass

通过审核后，**REQUIRE_CONFIRM=true** → 询问用户："新公式PASS本地与外部审核。最后确认：执行bump落地？这会修改rubric配置 + 删除若干已被吸收的观察。回答 'yes, bump' 才执行。"

用户确认后：

#### 5a. 更新rubric配置

- 更新`laochen-script-scoring`的维度定义
- 更新权重
- 增加/删除维度

#### 5b. Cleanup pass

- 已被吸收为新维度的观察 → 删
- 被新数据推翻的观察 → 删
- 仍未解决的观察 → 迁移到"待验证假设"段

---

### Phase 6: 校准样本批量更新

对每个校准样本prediction文件，**底部追加**（不动预测段、不动复盘段）：

```
---

**Re-scored under v5.21 on YYYY-MM-DD**: composite=8.24 → 9.11 (blind: true)
（rubric bump时全量重算，由laochen-score-blind sub-agent独立打分）
```

用Edit工具，匹配每个文件的最末尾。

---

## Bucket-Only 重校（轻量分支）

`/laochen-bump —bucket-only [—scheme ratio|absolute|percentile]`

**与完整bump的本质区别**：bucket边界不是规则的一部分，是数据派生量。重新派生它**不需要跨模型审核**。

### B1: 选择算法

| 算法 | 适用 | 边界派生方式 |
|---|---|---|
| `ratio`（默认 N=1-4） | 小样本 | 上一篇 / 最近3篇中位数 × {0.3, 1, 3, 10, 30} |
| `absolute`（默认 N=5-9）| 中等样本 | 校准池中位数 × {0.3, 1, 3, 10, 30}，固定边界 |
| `percentile`（默认 N≥10）| 大样本 | 校准池实绩 percentile {30, 60, 85, 95, 100} |

### B2: 派生新边界

读`predictions/*.md`中所有有`actual_plays`的样本。

**ratio模式**：
```
baseline = median(最近3篇actual_plays)
buckets = {
  "退步": (-inf, baseline * 0.3),
  "持平": (baseline * 0.3, baseline * 1),
  "命中": (baseline * 1, baseline * 3),
  "小爆": (baseline * 3, baseline * 10),
  "大爆": (baseline * 10, +inf),
}
```

### B3: 报告变化 + 用户确认

```
当前bucket scheme: ratio
Proposed scheme: absolute
Baseline: 4.2w 中位数（基于5篇校准样本）

新边界：
- 底部:   < 1.3w
- 基础盘: 1.3w - 4.2w
- 命中:   4.2w - 12.6w
- 爆款:   12.6w - 42w
- 现象级: > 42w

确认应用？(yes / no)
```

### B4: 落地

用户确认后：
1. 编辑rubric配置中的"Bucket方案"段，替换为新表
2. 更新`.cheat-state.json`的`baseline_plays`字段

---

## Key Rules

1. **5步不可跳**（仅完整rubric bump）。任何"先简化跑一下"的请求都拒绝
2. **THRESHOLD写死**（仅完整rubric bump）。不允许动态调整
3. **跨模型审核是默认**（仅完整rubric bump）
4. **Phase 2强制走laochen-score-blind**，不接受self-scored fallback
5. **REQUIRE_CONFIRM**（两种模式都要）
6. **⛔ 校准池纯度强制**：Phase 2.0 必须检查盲验结果，失败数据不计入校准池，最终校准池<3 → 中止bump

---

## Integration

- 上游：`laochen-data-review`检测到≥3同向偏差 → 提议跑`/laochen-bump`
- 依赖：Task tool（spawn laochen-score-blind）
- 修改：
  - `laochen-script-scoring`（结构性更新）
  - `predictions/*.md`（追加Re-scored行）
  - `.cheat-state.json`
- 下游：下一篇`/laochen-predict`自动按新rubric_version打分
