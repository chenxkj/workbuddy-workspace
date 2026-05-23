---
name: laochen-status
description: >-
  老陈抖音内容创作·状态看板。读取.cheat-state.json，
  显示当前模式/校准进度/Buffer状态/待办事项/发布节奏提醒。
  触发词：状态/看板/status/我现在该做什么/进度怎么样。
  无副作用，只读不写。
agent_created: true
---

# 老陈抖音·状态看板（laochen-status）

> **职责边界**：只读不写，只显示状态，不执行任何修改操作。
> **触发词**：状态/看板/status/我现在该做什么/进度怎么样

---

## Overview

```
[老陈：状态]
  ↓
[Phase 1: 读 .cheat-state.json + 扫文件系统]
  ↓
[Phase 2: 计算派生指标（Buffer颜色/Confidence等级/待办计数）]
  ↓
[Phase 3: 检测建议触发器（Buffer告警/待复盘/校准触发/积压提醒）]
  ↓
[Phase 4: 输出看板 + 下一步建议]
```

---

## Constants

- **SQLITE_UPGRADE_THRESHOLD = 30** — calibration_samples 达到 N 时建议升 SQLite
- **CLEANUP_LINE_THRESHOLD = 600** — rubric_notes.md 行数超 N 时建议清算
- **STALE_PREDICTION_DAYS = 30** — in_progress prediction 超 N 天未发布提示清理
- **BUFFER_WARNING_DAYS = 14** — 最早一拍至今天数 > N 天提示议题时效流失

---

## Inputs

| 来源 | 用途 |
|:-----|:-----|
| `.cheat-state.json` | 主要状态（所有字段） |
| `predictions/*.md` | 校准样本数 / pending retros |
| `抖音账号运营模板包/04_方案案例/` | 候选池规模（统计方案文件数） |
| `rubric_notes.md`（如有） | 行数 / 当前版本 |
| `predictions/` 中已发布文件 | 距上次 bump 多少次预测 |

---

## Workflow

### Phase 1: 读状态

```python
import json, glob, os
from datetime import datetime, timezone, timedelta

state_path = '.cheat-state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)

predictions = glob.glob('predictions/*.md')
# 候选池：统计 04_方案案例/ 下文件数
pool_path = state.get('pool_path', '')
pool_count = 0
if pool_path and os.path.isdir(pool_path):
    pool_count = len([f for f in os.listdir(pool_path) if f.endswith('.md')])

rubric_lines = 0
if os.path.exists('rubric_notes.md'):
    with open('rubric_notes.md', 'r', encoding='utf-8') as f:
        rubric_lines = len(f.readlines())
```

### Phase 2: 派生指标

| 指标 | 算法 |
|:-----|:-----|
| **Buffer 数** | `len(state.get('shoots', []))` |
| **Buffer 颜色** | 见下方"Buffer 颜色派生规则" |
| **Confidence 等级** | 从 `calibration_samples` 派生：0→🆕 未校准，1-2→🟡 低，3-5→🟠 中，6-10→🟢 较高，11+→🔵 高 |
| **最早一拍至今天数** | `now - state.shoots[0].shot_at`（如有），用于警告"拍了 N 天没发" |
| **校准样本数** | `state.get('calibration_samples', 0)` |
| **待复盘** | `len(state.get('pending_retros', []))` |
| **Buffer 天数** | `buffer_count × target_publish_cadence_days`（target=0 时禁用颜色） |

#### Buffer 颜色派生规则

```
buffer_count = len(state.shoots)
cadence = state.target_publish_cadence_days  # 如为 null，颜色禁用

if cadence is null:
    buffer_color = "⚪ 未设置节奏"
    buffer_advice = "请先设置 target_publish_cadence_days"
else:
    buffer_days = buffer_count × cadence
    if buffer_days < 1:   → 🔴 红（断更风险）
    if 1 ≤ buffer_days ≤ 2: → 🟠 橙（偏低，需关注）
    if 3 ≤ buffer_days ≤ 5: → 🟢 绿（健康）
    if buffer_days > 5:      → 🔵 蓝（积压，暂停拍摄）
```

#### Confidence 等级派生规则

| calibration_samples | 等级 | Emoji |
|:------------------:|:----:|:----:|
| 0 | 未校准 | 🆕 |
| 1-2 | 低 | 🟡 |
| 3-5 | 中 | 🟠 |
| 6-10 | 较高 | 🟢 |
| 11+ | 高 | 🔵 |

### Phase 3: 检测建议触发器

按优先级（高→低）逐项检查：

1. **🚨 Buffer = 🔴 红** → 第一行高优先级："Buffer 已 N 篇，下个发布日可能断更——今天必须拍 ≥1 条。说'推荐选题'我只推 top 1 稳分（不推实验性）"
2. **📦 Buffer = 🔵 蓝** → 高优先级："Buffer 已 N 篇积压。**暂停拍摄**，先发存货 + 复盘。说'已发布 ...'我帮你出队"
3. **shoots 中最早一项 shot_at > 14 天** → "你有视频拍了 N 天还没发——议题时效流失风险，建议尽快发或弃稿"
4. **in_progress 陈旧**（≥ `STALE_PREDICTION_DAYS`）→ 高优先级提示"清理或 publish"
5. **待复盘 ≥ 1** → 高优先级"今天该复盘 X 篇"
6. **pool_status=none + calibration_samples=0 + 距 initialized_at > 1天** → "🌱 你初始化完已经 N 天但还没拍——是因为没选题吗？跑 /laochen-topic-research 5 分钟拿候选"
7. **同向偏差信号**（不是死磕 ≥3 次）→ 提示"建议跑 /laochen-bump"
   - 默认参考：连续 ≥3 次同向偏差
   - 但 AI 可以更早：1 次极端偏差（≥10x）或 2 次同向 + 评论区强反向证据
   - 提示时显式标注："本次是 [default-aligned] / [judgment-driven]"
8. **calibration_samples 跨入新 confidence 等级** → 通知"🎉 confidence 升级"（仅通知，无必须操作）
9. **calibration_samples ≥ 5** → "可以跑 /laochen-bump 了"
10. **calibration_samples ≥ 10** → "可以跑 /laochen-bump --bucket-only 让 bucket 边界改用 percentile"
11. **calibration_samples ≥ SQLITE_UPGRADE_THRESHOLD** → "建议升级数据层到 SQLite"
12. **rubric_notes.md 行数 > CLEANUP_LINE_THRESHOLD** → "建议清算观察段"
13. **calibration_samples ≥ 5 + pool_status=none** → "可以开始建立选题池了"
14. **hooks_installed=false** → "你的 immutability 是君子协定，建议确认 checksum 机制"
15. **last_bump_self_audited=true** → "上次 bump 是自审。建议下次 bump 走交叉审核"
16. **rubric_form_mismatch=true** → "你的 content_form 不是 opinion-video，前几篇预测会更不准"
17. **benchmark_status=pending** → "🎯 你初始化时答应导入对标账号但还没做。跑 /laochen-topic-research 导入对标"
18. **benchmark_status=imported + AI 判断用户数据信号已超过 benchmark** → "📊 你的真实数据已经成为主信号，benchmark 影响淡出"

### Phase 4: 输出看板

```
🎛️ 老陈抖音·状态看板（更新于 YYYY-MM-DD HH:mm）

内容形态：opinion-video / 时长 90s / 节奏：隔日更
当前 rubric：v1.0（上次 bump：YYYY-MM-DD）
校准样本：15 篇
Confidence: 🟢 较高（中枢 ±15%，rubric 形态稳定）
Baseline: 4.2w 中位数

📦 Buffer：3 篇（🟢 绿色）
   按你的 cadence (隔日更)= 6 天 buffer，节奏稳定

📊 进度条
  [█████████████░░░░░] 15 / 30 → SQLite 升级建议门槛
  [██████████░░░░░░] 15 / 10 → percentile 桶可用（已超过门槛）

🎬 待办（按紧急度）
  🚨 复盘 1 篇（已过 T+3d）
     - predictions/2026-05-01_xxx.md（T+3d 到了）
  ⚠️  同向偏差 1 次（high）→ 继续观察
  💤 in-progress prediction 已陈旧 35 天

🔥 候选池
  - 04_方案案例/：X 个方案
  - 距上次抓选题：N 天

📈 健康度
  - rubric_notes.md: X 行（健康，<600 警戒线）
  - checksum 机制: ❌ → 建议确认 immutability 保护

下一步建议（按推荐优先级）：
1. /laochen-data-review 复盘 predictions/2026-05-01_xxx.md  ← 最紧急
2. 检查 Buffer 状态，如需拍摄：/laochen-topic-research 获取选题
3. 处理陈旧 in-progress（手动或说"清理"）
```

输出风格：**直白、具体、可操作**。每个建议附确切命令——用户应能直接说"复盘 XXX"执行。

---

## Key Rules

1. **无副作用**。读多写零。任何状态修改是其他 skill 的事
2. **不假装数据可用**。state file 字段缺失 → 显式标"未知/未设置"，不猜
3. **建议带优先级**。多个建议同时显示时按紧急度排序
4. **每个建议附操作指引**。不能只说"该 bump 了"——要给具体指令
5. **Buffer 颜色必须基于实际数据**。不得猜测或硬编码

---

## Refusals

- 「顺便帮我自动跑一下复盘」→ 拒绝。status 是只读，复盘是另一个动作
- 「我不想看 rubric_notes 行数」→ 输出仍包含但折叠到底部"健康度"区

---

## Integration

- 上游：所有其他 skill 完成时更新 `.cheat-state.json`，status 是这些更新的可视化
- 下游：每个建议都路由到具体子 skill
- 与 `laochen-orchestrator` 集成：orchestrator 执行流水线前可调 status 检查前置条件
