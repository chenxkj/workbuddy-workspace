---
name: cheat-shoot
description: 登记一条视频已拍摄。**建 video folder + 询问实际拍摄稿是否与 scripts/<id>.md 一致 + buffer +1**。与 cheat-publish 配对：拍了进队列，发了出队列。触发词："拍了"/"拍了 X"/"shot"/"shot it"/"已拍 X"/"录完了"。
argument-hint: <scripts-path-or-id>
allowed-tools: Bash(*), Read, Write, Edit, Glob
---

# /cheat-shoot — 登记拍摄完成 + 建 video folder

把视频从"已写预测、未拍摄"状态推进到"已拍摄、未发布"状态。这一步：
1. **建 `videos/<同 id>/`** 目录（之前没有的话）
2. **询问用户**："实际拍摄时用的稿子和 `scripts/<id>.md` 一致吗？"——根据答案决定 `videos/<id>/script.md` 的内容
3. 把 video folder 加进 state.shoots 队列，buffer +1

不写 prediction（预测早在 cheat-predict 时锁了），不发布（发布是 cheat-publish）。

为什么单独一个 skill：
- buffer 警戒系统需要明确区分"拍了" vs "发了"。视频可以批量拍（一天拍 5 条），分散发（每天发 1 条）
- "实际拍摄稿"可能与"pre-shoot 草稿"不同（用户改了 / 即兴 / 大改）——cheat-shoot 是把这个差异显式化的入口

## Overview

```
[用户：拍了 scripts/2026-05-04_abc123_停止期待.md]
  ↓
[Phase 0: 解析路径 + 验证 prediction 已存在]
  ↓
[Phase 1: 检查是否已登记（避免重复）]
  ↓
[Phase 2: 建 videos/<id>/ + 询问"实际拍摄稿一致吗？"]
  ↓
[Phase 3: 写 videos/<id>/script.md]
  ↓
[Phase 4: append state.shoots]
  ↓
[Phase 5: 输出 buffer 状态]
```

## Constants

- **REQUIRE_PREDICTION = true** — 拍前必须先有 prediction 文件（否则违反盲预测——拍完才写预测会被诱导事后修改）

## Inputs

| 必填 | 来源 |
|---|---|
| `<scripts-path-or-id>` | 用户参数；缺失则询问 |
| `.cheat-state.json` | 状态文件 |
| `scripts/*.md` | pre-shoot 草稿 |
| `predictions/*.md` | 验证对应预测存在 |

## Workflow

### Phase 0：解析 + 验证

1. 解析用户给的路径——支持几种形态：
   - 完整路径 `scripts/2026-05-04_abc123_停止期待.md`
   - 简写 `2026-05-04_abc123_停止期待`
   - id 简写 `abc123` → glob `scripts/*_abc123_*.md` 找匹配
2. 验证 `scripts/<id>.md` 存在：不存在 → 报错"找不到 pre-shoot 草稿"
3. 验证有对应 prediction `predictions/<同名>.md`：
   - 不存在 → **拒绝登记**，提示"先跑 /cheat-predict 写预测，否则违反盲预测原则——你不能拍完才写预测，那等于事后看了画面写"
   - 存在 → 通过

### Phase 1：检查重复

读 `.cheat-state.json`，检查 `shoots[]` 是否已含此 id：
- 已存在 → 警告"已登记过（X 天前）。是要重新登记，还是要用 /cheat-publish 发布？"
- 不存在 → 进入 Phase 2

### Phase 2：建 video folder + 询问稿子一致性

1. 建目录 `videos/<id>_<short>/`（同 scripts/ + predictions/ 的命名）
2. **询问用户**：

```
拍 「<title>」 的时候，你实际用的稿子和 scripts/<id>.md 一致吗？

a) 一致——直接用 scripts/<id>.md 内容存为 videos/<id>/script.md
b) 不太一致——我改了一些
   ↓ 接着问："你能提供拍摄时实际用的稿子吗？"
     - 是 → 用户提供（粘贴或路径），存为 videos/<id>/script.md
     - 否（即兴 / 没保留）→ 标 script_lost：videos/<id>/script.md 留空，
                          只在头部加注释说明
c) 大改了——拍出来其实是另一条
   ↓ 提示用户：建议走 _redo 流程——
     scripts/<id>_redo.md → 重新 cheat-predict → 再 cheat-shoot
     原 prediction 仍保留，但和实际拍摄脱钩
```

### Phase 3：写 videos/<id>/script.md

按 Phase 2 答案：
- 答 a → cp scripts/<id>.md → videos/<id>/script.md
- 答 b 提供新稿 → 写入用户提供的内容
- 答 b 没保留 → 写一个占位文件：
  ```markdown
  # <title> — 实际拍摄稿（已遗失）
  
  > 用户在 cheat-shoot 时未保留实际拍摄稿（标记 script_lost）。
  > 复盘时无法 diff `scripts/<id>.md` vs 实际拍摄版本——
  > script_patterns 学习能力受限。
  > 
  > 下次建议保留拍摄草稿（哪怕只是 voice memo 转录）。
  ```
- 答 c → 不写 videos/<id>/script.md（走 _redo 流程后再来）

### Phase 4：state 更新

```json
{
  "shoots": [
    ...,
    {
      "video_folder": "videos/2026-05-04_abc123_停止期待/",
      "prediction_file": "predictions/2026-05-04_abc123_停止期待.md",
      "scripts_path": "scripts/2026-05-04_abc123_停止期待.md",
      "shot_at": "<ISO timestamp>",
      "script_consistency": "consistent" | "modified" | "lost",
      "script_hash_at_shoot": "<sha256:12 of videos/<id>/script.md>"
    }
  ]
}
```

如 `script_consistency = modified` → diff `scripts/<id>.md` 和 `videos/<id>/script.md` 的 hash → 若不同，将 diff 信息标到 prediction 文件**复盘段**（不是预测段）作为日后 retro 的种子。

### Phase 5：输出 buffer 状态

读完 state 后立即算 buffer + 颜色（按 [cadence-protocol.md](../../shared-references/cadence-protocol.md) 的派生规则）：

```
✅ 已登记拍摄：videos/2026-05-04_abc123_停止期待/
   预测文件：predictions/2026-05-04_abc123_停止期待.md

📦 当前 buffer：3 篇（🟢 绿色，正常）
   按你的 cadence（隔日更）= 6 天 buffer，节奏稳定。

下一步：拍其他候选 / 等下个发布日 / 不动
```

如果 buffer 颜色变了（如从绿到蓝）→ 高亮提醒：
```
📦 当前 buffer：6 篇（🔵 蓝色，**积压**）
⚠️  建议暂停拍摄，全力发布存货 + 复盘。
   按你的 cadence（日更）= 6 天预备，已超过健康上限。
```

## Key Rules

1. **不写 prediction**——拍了 ≠ 发了。预测在 /cheat-predict 锁，拍只是事件
2. **不动 video folder 内容**——script.md / draft-v0.md 都不改
3. **必须先有 prediction**——否则违反盲预测（拍完看了画面再写预测 = 数据泄漏到判断）
4. **buffer 计算实时**——每次 shoot / publish 后立刻重算，state.shoots 是真值
5. **支持批量**：用户可以一天连说 "拍了 X / 拍了 Y / 拍了 Z" 三次连续登记

## Refusals

- 「拍了 X，顺便给我写个预测」 → 拒绝。预测必须**拍前**写（盲预测）。请先 /cheat-predict 再来 /cheat-shoot
- 「我没有 video folder，我直接拍的」 → 询问用户 → 帮他建一个 video folder + 提示下次走完整流程；登记时标 `ad_hoc: true` 提醒下次走标准流程
- 「拍了 X 但还没改完 script」 → 拒绝。如果 script 还在改，预测段已经过期——请改完后重新跑 /cheat-predict 再 /cheat-shoot

## Integration

- 上游：`/cheat-predict` 写完 prediction → 用户拍摄 → `/cheat-shoot` 登记
- 下游：`/cheat-publish` 发布时把对应项从 state.shoots 移除
- `/cheat-status` 看板的 buffer 数字直接来自 `state.shoots.length`
- `/cheat-recommend` 看 buffer 颜色调推荐策略
- SessionStart hook 看 buffer 颜色决定报告第一行

## state.shoots 数据结构

```json
{
  "shoots": [
    {
      "video_folder": "videos/2026-05-04_abc123_停止期待/",
      "prediction_file": "predictions/2026-05-04_abc123_停止期待.md",
      "shot_at": "2026-05-04T18:30:00+08:00",
      "ad_hoc": false  // true if user shot without going through full flow
    }
  ]
}
```

按 `shot_at` 升序——最早拍的在前面。`/cheat-status` 显示最早一项的 days-since-shoot 警告（避免有视频拍了 30 天没发）。
