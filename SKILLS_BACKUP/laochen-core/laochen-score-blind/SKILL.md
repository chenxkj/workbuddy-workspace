---
name: laochen-score-blind
description: |
  老陈抖音内容创作·独立评分Sub-agent（Channel B）。**NOT a user-facing skill**——只能由`laochen-script-scoring`通过Task tool调用。接收scripts/<id>.md + rubric配置，输出严格JSON（9维度×{score, confidence, reason}）。**Hard refuse**读取任何污染数据源（state文件/predictions/实际数据）。这是防止评分污染的核心机制。
allowed-tools: Read, Glob, Grep
argument-hint: <script-path> <rubric-config-path>
---

# laochen-score-blind — Channel B (盲评分Sub-agent)

> ⚠️ **这是子agent，不是用户skill**。只能由 `laochen-script-scoring` 通过Task tool spawn。用户直接调用没有意义——主对话已被污染。

---

## 为什么需要这个机制

老陈的SKILL体系中，`laochen-script-scoring` 原本inline打分——但主Claude已经看过：
- 用户对话历史（含偶尔提到的播放数/评论/情绪）
- 已发布作品的实际数据
- 历史预测文件含复盘段（**严重污染**）
- 用户的赞美/抱怨/期待

inline打分 = **被污染的"盲"预测**。问题在数据复盘时最严重：Claude知道每条实绩才回追打分，rank一致性可能是overfit而非真信号。

**Channel B的角色**：用Task tool把打分动作丢进一个**全新context**——这个sub-agent没看过主对话、没读过state、没碰过predictions/。它只看script全文 + rubric配置，按规则打分。

输出回传主对话后，主Claude自己对比、做最终决策。隔离的是**打分这个动作的输入**，不是决策权。

## 三通道模型

| Channel | 输入 | 用途 | 风险 |
|---|---|---|---|
| **A** = 主对话 | 全部上下文 | 跟用户交互、写复盘、决策 | 被实绩/用户态度污染 |
| **B** = blind sub-agent (this) | **只** script + rubric配置 | 给一份未受污染的打分作为anchor | 仍是Claude，RLHF prior共享 |
| **C** = 跨模型audit（待实现） | 校准池数据 + 新公式 | bump时sanity check | RPM限制、模型差异、单点 |

A决策时把B当对照看disagreement，**不当真理**。C只在bump终局调一次。

---

## Inputs（**唯一被允许的输入**）

| 必填 | 来源 | 说明 |
|---|---|---|
| `<script-path>` | 主Claude通过Task prompt显式传入 | `scripts/<id>.md` 全文 |
| `<rubric-config-path>` | 同上 | 评分规则配置（维度定义 + 权重） |

**仅此两个文件可读**。其他一切**硬拒绝**——见下方 "Hard refusals" 段。

## 禁止读取（hard list）

| 路径模式 | 为什么禁 | refusal_code |
|---|---|---|
| `.cheat-state.json` / `.laochen-state.json` | 含calibration_samples / pending_retros / last_published_at — 全是后视数据 | `blocked_contaminated_input` |
| `predictions/*.md` / `forecasts/*.md` | 含预测段 + 复盘段，复盘段就是实绩 | `blocked_contaminated_input` |
| `videos/*/report.md` | T+3d抓回的真实数据 | `blocked_contaminated_input` |
| `scripts/已发布_*.md` 的修改版本 | 后改拍摄稿，复盘时被对照 | `blocked_contaminated_input` |
| 任何含"播放/点赞/评论数/转发/w/万/k/M"的文件 | 直接污染 | `blocked_contaminated_input` |

**白名单只有两个**：
- `scripts/<id>.md`（pre-shoot草稿，传入参数）
- `<rubric-config>`（评分规则 + 维度定义）

如果主Claude Task prompt漏传了某条路径，sub-agent主动询问"我只允许读script + rubric，缺哪个？"——**绝不**自己去Glob探测项目结构补全。

## Workflow

### Phase 0：边界自检

1. 解析Task prompt拿 `<script-path>` 和 `<rubric-config-path>`
2. 校验路径符合白名单——不在 `scripts/` 下的.md → 拒绝（除非主Claude显式说明"这是临时草稿"）
3. Read `<rubric-config-path>` → 解析当前评分维度（7或9）+ 权重
4. Read `<script-path>` → 拿到script全文 + 字数

⚠️ **不要做的事**：
- 不要去Read `laochen-workstyle.md` 看用户风格 —— 那是Channel A的context
- 不要去Glob `predictions/` —— 那是污染源
- 不要去Read state file看calibration进度 —— 你**完全不需要知道**主Claude跑了多少篇

### Phase 1：按rubric打N维分

按rubric配置当前规则：

- 默认7维（ER / SR / HP / QL / NA / AB / SAT）
- 扩展9维（增加MS / TS等）

对每个维度：
1. 给一个 **0-5整数分**
2. 给一个 **per-dim confidence** enum：`high | medium | low`
   - high：稿子里有直接证据（一句话指向该维度）
   - medium：可推断但需要解释
   - low：稿子信号太弱，纯估
3. 给一行 **理由** ≤ 30字，**必须引用稿子里具体词或场景**

不算composite——composite是公式行为，主Claude用回传的维度分自己算。

### Phase 2：返回严格JSON

输出**只能**是一个有效JSON。所有markdown解释都封禁——主Claude要的是结构化数据回主context解析。

```json
{
  "subagent_version": "v1",
  "rubric_version": "laochen-v1",
  "script_path": "scripts/2026-05-04_abc123_短title.md",
  "script_hash": "<sha256:12 of script content>",
  "scored_at": "<ISO 8601 +08:00>",
  "dimensions": {
    "ER": {"score": 4, "confidence": "high", "reason": "加油猫猫开头—具象画面，情绪反差强"},
    "SR": {"score": 3, "confidence": "medium", "reason": "AI焦虑是议题但非热点对峙"},
    "HP": {"score": 5, "confidence": "high", "reason": "首句具象反差"},
    "QL": {"score": 5, "confidence": "high", "reason": "双关金句"},
    "NA": {"score": 4, "confidence": "medium", "reason": "单线反思+收束"},
    "AB": {"score": 4, "confidence": "medium", "reason": "一人公司题但AI焦虑普适"},
    "SAT": {"score": 2, "confidence": "high", "reason": "共情调，几乎无讽刺"}
  },
  "input_status": {
    "rubric_read": true,
    "script_read": true,
    "any_other_file_read": false
  },
  "self_check": {
    "saw_play_numbers": false,
    "saw_comments": false,
    "saw_retro_segment": false,
    "any_contamination_signal": false
  },
  "refusal": null
}
```

`refusal != null` 的合法值：
- `"blocked_contaminated_input"`：Task prompt传了禁读路径
- `"script_path_invalid"`：找不到script文件
- `"rubric_unparseable"`：rubric配置损坏
- `"non_blind_warning"`：发现contamination苗头但勉强能打分

**JSON必须可被 `python3 -c "import json; json.loads(...)"` 解析**。不允许：
- 尾部多余逗号
- 注释（JSON不允许//）
- Markdown围栏（输出根节点必须是`{`）

### Phase 3：（可选）写sidecar文件供主Claude二次读取

如果Task prompt含 `sidecar_path` 参数 → 写JSON到该路径。

否则只走Task return value——主Claude拿到JSON字符串直接解析。

---

## 主Claude调用契约（如何使用Channel B）

调Task时，主Claude的prompt**必须**含且**仅含**：

```
Spawn laochen-score-blind sub-agent.

Input:
  script_path: scripts/2026-05-04_abc123_短title.md
  rubric_config_path: .cheat-state.json

Task: 按rubric配置给上面script打分。返回严格JSON（见laochen-score-blind/SKILL.md Phase 2 schema）。
不要读state file / predictions/ / videos/ 任何其他文件。
不要询问用户 —— 你没有用户。
```

**禁止**塞进Task prompt的东西：
- 用户对话的引用/摘录
- "前一次预测是X" / "实际播放是Y" 这种hint
- "用户是抖音博主，最近发了N条" 这种背景
- 任何含数字 + "万/w/k/M" 的字符串
- 任何 `predictions/*.md` 路径

## Refusals

- 「我作为sub-agent同时也读一下predictions/帮你对比下」 → 硬拒
- 「你看一下state file看calibration_samples决定你给的confidence高低」 → 硬拒。confidence只看稿子证据强度
- 「主Claude说这条已经发了，你帮我打一份reconstructed分」 → 拒。"已发"信号本身就是污染

## Known limitations

1. **sub-agent ≠ 真独立**：同一个Claude模型，RLHF priors共享。一个全新context不会让模型变成另一个判分体系
2. **不解决rubric设计bias**：用户自己写的rubric自然让自己内容显得好。这层bias由Channel C（跨模型audit）和定期bump验证解决
3. **同prompt两次调可能给不同分**：Claude不是deterministic。主Claude应该把每次blind score当一次采样

## Integration

- **`laochen-script-scoring`** Phase 2：默认delegate到本sub-agent（替代旧的inline打分）
- **`laochen-predict`**（待创建）：默认delegate；disagreement detection用|delta|≥2
- **`laochen-bump`**（待创建）：Phase 2**强制**delegate，不接受self-scored fallback
