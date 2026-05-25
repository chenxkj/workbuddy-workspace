# Codex 换电脑迁移说明

目标：把本项目迁移到另一台电脑上的 Codex，尽量做到打开即用。

## 迁移原则

| 类型 | 是否迁移 | 说明 |
|:--|:--:|:--|
| 项目文件 | 是 | 本仓库全部内容 |
| Codex skills | 是 | 从 `SKILLS_BACKUP/laochen-core/` 同步到新电脑 `~/.codex/skills/` |
| 当前账号数据 | 是 | `accounts/`、`抖音账号运营模板包/`、`predictions/`、`.cheat-state.json` |
| 旧 WorkBuddy 运行时 | 否 | `.workbuddy/` 不作为新电脑运行依赖 |
| node_modules | 否 | Codex 自带运行时，不随项目迁移 |
| 临时输出 | 否 | `outputs/`、临时 HTML、预览文件可重建 |
| 下载目录作品表 | 需要手动 | `C:/Users/86151/Downloads/作品列表.xlsx` 不在项目内，新电脑需重新导出或复制到同等路径 |

## 一键导出

在旧电脑项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export-codex-project.ps1
```

导出文件默认生成在：

```text
C:\tmp\laochen-codex-project-migration.zip
```

## 新电脑导入

1. 安装 Codex 并启动一次，确保生成 `C:\Users\<你>\.codex\`。
2. 把 zip 复制到新电脑。
3. 解压到你想放项目的位置，例如：

```text
C:\Users\<你>\Work\laochen-codex
```

4. 在新电脑项目根目录运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-codex-skills.ps1
```

5. 打开 Codex，选择这个项目目录。
6. 进入后先让 Codex 检查：

```text
确认 AGENTS.md、CODEX_README.md、docs/architecture、SKILLS_BACKUP、accounts、抖音账号运营模板包、predictions、.cheat-state.json 都存在；并检查 ~/.codex/skills 下 laochen-* skills 是否已安装。
```

## 新电脑必须补齐的数据

作品数据源仍来自抖音后台导出。新电脑首次复盘前，必须做其中一种：

1. 从旧电脑复制最新 `作品列表.xlsx` 到新电脑下载目录。
2. 在新电脑重新从抖音后台导出作品列表。
3. 如果路径变了，更新 `AGENTS.md` 中“当前账号数据源”的作品表路径。

## 推荐迁移后检查

```powershell
Test-Path .\AGENTS.md
Test-Path .\CODEX_README.md
Test-Path .\docs\architecture\PLATFORM_ADAPTERS.md
Test-Path .\docs\architecture\PROJECT_STRUCTURE.md
Test-Path .\SKILLS_BACKUP
Test-Path '.\抖音账号运营模板包'
Test-Path .\accounts\laochen\CONTENT_PLAN.md
Test-Path .\.cheat-state.json
Test-Path "$env:USERPROFILE\.codex\skills\laochen-workstyle\SKILL.md"
```

## 不迁移的历史残留

以下属于旧环境残留或可重建产物，不影响新电脑使用：

- `node_modules/`
- `outputs/`
- `wechat_article*.html`
- 预览 HTML
- WorkBuddy 自动化运行日志

