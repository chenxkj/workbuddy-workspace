# 项目目录重构规划

当前工作区是从 WorkBuddy 迁移来的历史结构，能用，但不适合长期维护多账号、多平台运营。重构目标是：规则、账号、平台、数据、脚本、归档各自独立。

## 目标目录

```text
workspace/
  AGENTS.md
  CODEX_README.md
  docs/
    architecture/
      PROJECT_STRUCTURE.md
      PLATFORM_ADAPTERS.md
    superpowers/plans/
  skills/
    backup/
    installed-sync-notes.md
  platforms/
    douyin/platform.md
    xiaohongshu/platform.md
  accounts/
    laochen/
      account-profile.md
      CONTENT_PLAN.md
      state.md
      platforms/
        douyin/
          data/
          content/
            scripts/
            plans/
            published/
          predictions/
          reviews/
          assets/
        xiaohongshu/
          data/
          content/
          predictions/
          reviews/
  shared/
    scripts/
      active/
      archive/
    assets/
    templates/
  archive/
    migration/
    legacy-workbuddy/
  .workbuddy/
    memory/
```

## 当前到目标的映射

| 当前路径 | 目标归属 | 处理方式 |
|:--|:--|:--|
| `SKILLS_BACKUP/` | `skills/backup/` | 暂不搬；先作为规则备份唯一来源 |
| `抖音账号运营模板包/` | `accounts/laochen/platforms/douyin/` | 第二阶段迁移，先保持原路径 |
| `抖音账号运营模板包/00_数据存档/` | `accounts/laochen/platforms/douyin/data/` | 数据唯一来源；只存导出、关键时间点、数据规范 |
| `抖音账号运营模板包/05_账号复盘/` | `accounts/laochen/platforms/douyin/reviews/` | 历史复盘归档；不再放当前总计划和最新数据导出 |
| 各处系列规划/选题库/素材库 | `accounts/laochen/CONTENT_PLAN.md` | 总控唯一来源；原文件降级为来源材料 |
| `predictions/` | `accounts/laochen/platforms/douyin/predictions/` | 第二阶段迁移 |
| `rubric_notes.md` / `script_patterns.md` / `.cheat-state.json` | `accounts/laochen/platforms/douyin/` 或账号根状态 | 第二阶段迁移 |
| `scripts/` | `shared/scripts/active/` | 先清单化，再迁移 |
| `archive/` | `archive/legacy-workbuddy/` | 第三阶段整理 |
| `.workbuddy/memory/MEMORY.md` | `accounts/laochen/state.md` 的过渡索引 | 暂保留，后续只做索引 |

## 迁移阶段

### Phase 0：现在执行

- 明确规则、账号、平台、数据的边界。
- 新增规划文件，不搬现有资产。
- 所有新规则先写到 `docs/architecture/` 或对应 skill reference。
- `AGENTS.md` 只声明当前项目入口和唯一来源。

### Phase 1：建立新骨架

- 创建 `platforms/douyin/` 和 `platforms/xiaohongshu/`。
- 创建 `accounts/laochen/account-profile.md`。
- 创建 `accounts/laochen/CONTENT_PLAN.md`，作为系列计划、选题池、优先级唯一来源。
- 创建 `accounts/laochen/platforms/douyin/` 空目录。
- 不移动历史文件，只在新目录放 README/索引。

### Phase 2：迁移当前抖音账号资产

- 迁移 `抖音账号运营模板包/04_方案案例/` 到 `accounts/laochen/platforms/douyin/content/`。
- 迁移 `predictions/` 到 `accounts/laochen/platforms/douyin/predictions/`。
- 迁移账号数据存档到 `accounts/laochen/platforms/douyin/data/`。
- 更新所有 skill 和脚本读取路径。
- 跑路径验证，确认没有旧路径残留。

### Phase 3：清理历史目录

- 将旧 WorkBuddy 迁移资料归入 `archive/migration/`。
- 将不用的脚本归入 `shared/scripts/archive/`。
- `CODEX_README.md` 只保留当前入口，不再承载迁移历史。

## 命名规则

| 类型 | 规则 |
|:--|:--|
| 账号目录 | `accounts/<account-id>/`，例如 `accounts/laochen/` |
| 平台目录 | `platforms/<platform-id>/`，例如 `platforms/douyin/` |
| 账号平台目录 | `accounts/<account-id>/platforms/<platform-id>/` |
| 数据文件 | 带采集日期，例如 `works_2026-05-23.xlsx` |
| 复盘文件 | 跟内容 ID 走，例如 `reviews/<content-id>.md` |
| 预测文件 | 跟内容 ID 走，例如 `predictions/<content-id>.md` |

## 重构红线

1. 不一次性大搬家。
2. 每次迁移一类资产，迁移后跑路径搜索。
3. 迁移前先写映射表，迁移后保留 1 个版本周期的旧路径索引。
4. 账号数据不能进入 `skills/` 或 `platforms/`。
5. 平台规则不能进入账号人设文件。
6. `docs/architecture/` 是规划，不是数据真值来源。
