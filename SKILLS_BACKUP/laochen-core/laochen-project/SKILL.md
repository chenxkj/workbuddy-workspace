---
name: laochen-project
description: |
  Use when a task needs account-operations project context for short-video or content-platform accounts, including where to find current account data, platform adapters, assets, scripts, status, and publishing materials.
agent_created: true
---

# 账号运营项目上下文

## Quick Reference Index

| Domain | Detail Location |
|:--|:--|
| 来源边界 | `references/project-config.md` |
| 多平台适配 | 当前工作区 `docs/architecture/PLATFORM_ADAPTERS.md` |
| 目录重构规划 | 当前工作区 `docs/architecture/PROJECT_STRUCTURE.md` |
| 当前账号数据 | 当前工作区 `AGENTS.md` 的“当前账号数据源” |
| 当前账号人设/偏好 | 当前工作区 `AGENTS.md` 指定的账号人设文件 |
| 项目状态索引 | 当前工作区 `.workbuddy/memory/MEMORY.md` |
| 运行状态 | 当前工作区 `.cheat-state.json`、`rubric_notes.md`、`script_patterns.md` |

## Progressive Disclosure Rules

1. 先读 `references/project-config.md` 判断内容属于规则、平台、账号还是数据。
2. 涉及抖音/小红书等平台字段时，读平台适配文件，不从账号数据里推平台规则。
3. 涉及账号数据时，读当前工作区 `AGENTS.md`，不要把本 skill 当数据源。
4. 涉及目录搬迁时，读 `docs/architecture/PROJECT_STRUCTURE.md`，按阶段迁移，不一次性大搬家。
5. 复制到其他账号项目时，只复用通用流程和平台接口，不复制老陈账号数据。
