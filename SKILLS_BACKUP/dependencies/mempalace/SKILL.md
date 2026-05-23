---
name: mempalace
description: "MemPalace — 本地AI记忆系统，语义搜索+时序知识图谱+宫殿架构（wings/rooms/drawers）。免费，本地运行，无需API Key。触发词：查一下记忆、记忆里有没有、搜一下我之前、记忆宫殿。"
version: 3.3.0
homepage: https://github.com/MemPalace/mempalace
metadata:
  clawdbot:
    emoji: "🏛️"
    requires:
      bins: ["python"]
    os: ["darwin", "linux", "win32"]
---

# MemPalace SKILL

本地 AI 记忆系统，为 AI 提供持久化记忆能力。

## 架构

```
Wings（侧翼） = 人物或项目
     ↓
Halls（大厅） = 分类（事实/事件/偏好/建议）
     ↓
Rooms（房间） = 具体话题
     ↓
Drawers（抽屉）= 逐字存储的记忆块
```

## 安装状态

- Python 包：`mempalace 3.3.2` ✅ 已安装
- Palace 路径：`C:\Users\86151\.mempalace\palace` ✅ 已初始化
- Wing：`老陈工作区`
- Drawers：9个（安全红线/账号配置/评分标准/合集编号/踩坑流程/Skill索引/铁律自评/操作规律/嵌入式合集）

## 使用时机

**每次会话开始**（涉及老陈工作区话题前）：
```
python -m mempalace wake-up --wing "老陈工作区"
```

**老陈主动查询**：说"记忆宫殿"/"查一下记忆"/"搜一下我之前" → 执行 search

**会话结束**：调用 diary_write 记录本次重要结论

**注意**：语义搜索中文匹配有局限，重要信息以 wake-up 全文输出为准。

## 工具使用规则

1. **唤醒时**：调用 `mempalace_status` 加载宫殿概览
2. **响应前**：关于人物、项目或过去事件，先 `mempalace_search` 查询，不凭记忆猜测
3. **不确定时**：说"让我查一下"然后查询。错误比缓慢更糟糕
4. **会话结束时**：调用 `mempalace_diary_write` 记录重要内容

## MCP 工具清单

### 🔍 搜索与浏览

| 工具 | 功能 |
|------|------|
| `mempalace_search` | 语义搜索所有记忆 |
| `mempalace_status` | 获取宫殿概览 |
| `mempalace_list_wings` | 列出所有侧翼 |
| `mempalace_list_rooms` | 列出某侧翼的房间 |
| `mempalace_check_duplicate` | 存储前检查是否已存在 |

### 🕸️ 知识图谱（时序事实）

| 工具 | 功能 |
|------|------|
| `mempalace_kg_query` | 查询实体关系（支持时间过滤） |
| `mempalace_kg_add` | 添加事实：主体→谓词→客体 |
| `mempalace_kg_invalidate` | 标记旧事实失效 |
| `mempalace_kg_timeline` | 获取实体的时序故事 |

### ✏️ 写入

| 工具 | 功能 |
|------|------|
| `mempalace_add_drawer` | 存入内容到指定侧翼/房间 |
| `mempalace_delete_drawer` | 按 ID 删除抽屉 |
| `mempalace_diary_write` | 写会话日记 |
| `mempalace_diary_read` | 读取最近日记 |

## 调用示例

```bash
# 语义搜索
python -m mempalace search "老陈的抖音策略"

# 写入记忆
python -m mempalace add-drawer --wing workbuddy --room imax-upload "上传脚本已升级v2，支持断点续传"

# 查看状态
python -m mempalace status
```

## 提示

- 搜索是**语义搜索**（基于含义），不是关键词搜索
- 知识图谱存储带时间窗口的**类型化关系**
- 日记条目跨会话累积，在每次对话结束时写一条
