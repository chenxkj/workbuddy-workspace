# .cheat-state.json 状态字段定义（Schema）

> 本文档是 `.cheat-state.json` 所有字段的权威定义。
> 任何 Skill 读写 state file 都必须以此文件为准。

---

## 版本与元数据

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `schema_version` | string | `"1.1"` | `cheat-init` / `laochen-orchestrator` | state file 格式版本 |
| `skill_version` | string | — | `cheat-init` | Skill 版本号 |
| `initialized_at` | ISO timestamp | — | `cheat-init` | 初始化时间 |
| `laochen_integration.laochen_skill_version` | string | — | `laochen-orchestrator` | laochen Skill 版本 |

---

## Rubric 与校准

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `rubric_version` | string | `"v1.0"` | `cheat-bump` / `laochen-bump` | 当前 rubric 版本 |
| `last_bump_at` | ISO timestamp / null | `null` | `cheat-bump` / `laochen-bump` | 上次 bump 时间 |
| `last_bump_self_audited` | boolean | `false` | `cheat-bump` / `laochen-bump` | 上次 bump 是否自审 |
| `calibration_samples` | integer | `0` | `laochen-data-review` | 已完成复盘的样本数 |
| `last_retro_at` | ISO timestamp / null | `null` | `laochen-data-review` | 上次复盘时间 |
| `last_retro_deviation` | float / null | `null` | `laochen-data-review` | 上次复盘偏差（实际/中枢比值） |
| `consecutive_directional_errors` | string[] | `[]` | `laochen-data-review` | 同向偏差队列（`"high"`/`"low"`） |
| `rubric_form_mismatch` | boolean | `false` | `cheat-init` / `laochen-orchestrator` | content_form 与内置 rubric 不匹配标记 |

---

## 内容形态与基准

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `content_form` | string | `"opinion-video"` | `cheat-init` / `laochen-orchestrator` | 内容形态（opinion-video / tutorial / 等） |
| `typical_duration_seconds` | integer | `90` | `cheat-init` | 典型时长（秒） |
| `baseline_plays` | integer / null | `null` | `laochen-view-prediction` | 播放量基准值（中位数） |
| `benchmark_status` | string | `"none"` | `cheat-learn-from` | 对标状态：`none` / `pending` / `imported` |
| `benchmark_name` | string / null | `null` | `cheat-learn-from` | 对标账号名称 |
| `benchmark_sample_count` | integer | `0` | `cheat-learn-from` | 对标样本数 |

---

## 发布节奏与 Buffer

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `target_publish_cadence_days` | integer / null | `null` | 用户设置 | 目标发布间隔天数（如 `2` = 隔日更） |
| `last_published_at` | ISO timestamp / null | `null` | `cheat-publish` / `laochen-orchestrator` | 上次发布时间 |
| `last_published_file` | string / null | `null` | `cheat-publish` / `laochen-orchestrator` | 上次发布的预测文件路径 |
| `shoots` | object[] | `[]` | `cheat-shoot` / `laochen-orchestrator` | 已拍摄未发布视频列表 |
| `in_progress_session` | object / null | `null` | `cheat-predict` / `laochen-view-prediction` | 进行中的预测会话 |
| `pending_retros` | string[] | `[]` | `laochen-data-review` | 待复盘视频路径列表 |

### `shoots[]` 元素结构

```json
{
  "file": "predictions/2026-05-09_xxx.md",
  "shot_at": "2026-05-10T14:00:00+08:00",
  "video_folder": "抖音账号运营模板包/03_选题评估/第X期/"
}
```

### `in_progress_session` 结构

```json
{
  "type": "prediction",
  "file": "predictions/2026-05-09_xxx.md",
  "video_folder": null,
  "started_at": "2026-05-09T14:12:00+08:00",
  "rubric_version": "v1.0"
}
```

### Buffer 颜色派生规则

```
buffer_count = len(shoots)
buffer_days = buffer_count × target_publish_cadence_days

buffer_days < 1   → 🔴 红（断更风险）
1 ≤ buffer_days ≤ 2 → 🟠 橙（偏低）
3 ≤ buffer_days ≤ 5 → 🟢 绿（健康）
buffer_days > 5   → 🔵 蓝（积压）
```

---

## 候选池与数据层

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `pool_status` | string | `"none"` | `cheat-seed` / `laochen-topic-research` | 候选池状态：`none` / `markdown` / `sqlite` |
| `pool_path` | string / null | `null` | `cheat-init` | 候选池路径 |
| `data_layer` | string | `"markdown"` | `cheat-init` | 数据存储层：`markdown` / `sqlite` |
| `data_collection` | string | `"manual"` | `cheat-init` | 数据收集方式 |

---

## 热点与来源

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `enabled_trend_sources` | string[] | `["manual-paste"]` | `cheat-trends` | 启用的热点来源列表 |
| `last_trends_run_at` | ISO timestamp / null | `null` | `cheat-trends` | 上次抓热点时间 |
| `last_trends_added_count` | integer | `0` | `cheat-trends` | 上次抓热点新增条数 |

---

## Hook 与审计

| 字段 | 类型 | 默认值 | 写入方 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `hooks_installed` | boolean | `false` | `cheat-init` | immutability hook 是否已安装 |
| `enabled_perf_adapters` | string[] | `[]` | 用户设置 | 启用的性能适配器 |

---

## laochen 集成字段

| 字段 | 类型 | 默认值 | 说明 |
|:-----|:-----|:-------|:-----|
| `laochen_integration.dual_scoring` | boolean | `true` | 是否启用双评分（A/B 独立） |
| `laochen_integration.cross_reference` | string | — | 交叉引用目标 |
| `laochen_integration.pool_reads_from` | string | — | 候选池读取路径 |
| `laochen_integration.calibration_data` | object | `{}` | 校准数据（视频ID → 数据映射） |

---

## 字段变更记录

| 日期 | 字段 | 变更类型 | 原因 |
|:-----|:-----|:---------|:-----|
| 2026-05-15 | `last_retro_deviation` | 新增 | `laochen-data-review` 校准触发机制需要 |
| 2026-05-15 | `laochen_integration` | 新增 | laochen Skill 集成需要 |
| 2026-05-15 | 本文档 | 新建 | Task 4 状态管理完善 |

---

## Skill 读写权限

| Skill | 可读字段 | 可写字段 |
|:-----|:--------|:--------|
| `laochen-data-review` | 全部 | `calibration_samples`, `consecutive_directional_errors`, `last_retro_at`, `last_retro_deviation`, `pending_retros` |
| `laochen-view-prediction` | `baseline_plays`, `calibration_samples`, `rubric_version` | `in_progress_session`, `last_published_at`, `last_published_file` |
| `laochen-orchestrator` | 全部 | `shoots`, `pending_retros`, `last_published_at`, `last_published_file`, `in_progress_session` |
| `laochen-topic-research` | `pool_status`, `pool_path` | `pool_status` |
| `laochen-script-scoring` | `rubric_version`, `calibration_samples` | `rubric_version`（bump 后） |
