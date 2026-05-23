---
name: laochen-project
description: |
  Use when a task needs account-operations project context for short-video accounts, including where to find the current account's data, assets, scripts, status, and publishing materials.
agent_created: true
---

# 账号运营项目上下文

## Quick Reference Index
| Domain | Detail Location |
|--------|----------------|
| 来源边界 | `references/project-config.md` → Source Boundaries |
| 当前账号数据 | 当前工作区 `AGENTS.md` → 当前账号数据源 |
| 项目状态索引 | 当前工作区 `.workbuddy/memory/MEMORY.md` |
| 内容资产 | 当前工作区的账号模板包/方案案例目录 |
| 运行状态 | 当前工作区 `.cheat-state.json`、`rubric_notes.md`、`script_patterns.md` |

## Progressive Disclosure Rules
1. This SKILL.md (~20 lines) loads on trigger — minimal token cost
2. Read `references/project-config.md` when deciding whether something belongs in reusable rules or account data
3. Read current workspace `AGENTS.md` before using account-specific paths
4. Never treat this skill as an account-data source; it is only a routing guide
