# Codex 工作区入口

本工作区已从 WorkBuddy 迁移到 Codex。当前重点是把内容运营能力改成可复用的“多账号、多平台”结构。

## 先读这几个文件

1. `AGENTS.md`：当前项目入口，声明规则、账号数据、平台适配的唯一来源。
2. `docs/architecture/PLATFORM_ADAPTERS.md`：抖音、小红书等平台适配边界。
3. `docs/architecture/PROJECT_STRUCTURE.md`：目标目录结构和分阶段迁移路线。
4. `SKILLS_BACKUP/laochen-core/`：通用运营流程 skill 备份。
5. `C:/Users/86151/.codex/skills/`：Codex 实际运行使用的已安装 skill。
6. `docs/migration/CODEX_MACHINE_MIGRATION.md`：换电脑迁移说明。

## 当前原则

- 通用规则/流程放在 skill。
- 账号人设、账号数据、平台数据不写进通用 skill。
- 抖音、小红书等平台规则走平台适配层。
- `accounts/laochen/STATE.md` 只做状态索引，不做数据真值来源。
- 旧 `.workbuddy/` 运行时目录不再作为 Codex 新电脑迁移依赖。
- 历史迁移文档只做参考，不再作为当前规则入口。

## 下一步

按 `docs/superpowers/plans/2026-05-23-multiplatform-structure.md` 执行：

1. 建立 `platforms/` 和 `accounts/` 新骨架。
2. 先迁移索引和预测类文件。
3. 再迁移抖音内容资产。
4. 最后归档旧迁移资料和历史目录。
