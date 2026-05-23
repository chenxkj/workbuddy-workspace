---
name: mempalace-auto-sync
description: |
  老陈记忆宫殿自动同步系统。在内容生产/数据复盘/评分修正/错误分析等关键节点后，
  自动将核心洞察写入 MemPalace。包含实时写入和定时批量兜底两种机制。
  触发词：记忆宫殿/更新记忆/写入宫殿/sync palace/自动同步。
  agent_created: true
---

# MemPalace 自动同步

## 触发时机（B+C方案）

### B层：Skill 内嵌（实时·每次内容生产后）

以下 skill 执行完毕后，**必须**调 `sync_mempalace.py` 写入关键结论：

| 触发 Skill | 写入内容 |
|-----------|---------|
| `laochen-data-review` | 复盘后的数据偏差、根因、对策 |
| `laochen-script-scoring` | 评分体系迭代（新版本号+关键改动） |
| `laochen-script-writing` | 新文案的核心策略选择+字数锚定值 |
| `laochen-topic-research` | 选题调研结论+否决原因 |
| `laochen-view-prediction` | 预测偏差>30%时记录预测vs实际 |

### C层：会话结束兜底（检查本次是否有新发现）

每次会话结束前（或用户说"更新记忆"时）：
1. 检查 `~/.openclaw/memory/self-improving/corrections.jsonl` 自上次同步以来是否有新条目
2. 有新条目→提取核心洞察→写入 MemPalace
3. 告知老陈写入数量

### 写入格式

所有写入 MemPalace 的内容以 `【类型·日期·标签】` 开头：
- `【事实·YYYY-MM-DD·标签】` - 客观数据发现
- `【踩坑·标签】` - 错误+根因+对策
- `【策略·标签】` - 策略调整决策

## 使用方法

### 方式一：手动触发
```
python scripts/sync_mempalace.py --mode incremental
```

### 方式二：Skill 内自动调用
```python
from mempalace.mcp_server import tool_add_drawer
result = tool_add_drawer("老陈工作区", "general", content)
```

### 方式三：批量兜底
```
python scripts/sync_mempalace.py --mode full
```

## 防重复机制

- 写入前检查 MemPalace 中是否已有高度相似内容（语义搜索匹配度>0.85→跳过）
- corrections.jsonl 中每条有 `logged_at` 时间戳，增量模式只同步新增条目
- 状态文件 `~/.mempalace/sync_state.json` 记录上次同步时间
