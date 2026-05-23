# Codex Project Context

本项目由腾讯 WorkBuddy 迁移到 Codex。进入本工作区后，先按“规则、流程、账号数据分离”的原则加载上下文。

## 来源规则

| 类型 | 唯一来源 | 范围 |
|:-----|:---------|:-----|
| 通用规则/流程 | `SKILLS_BACKUP/laochen-core/*/SKILL.md`，已安装副本在 `C:/Users/86151/.codex/skills/` | 本机 Codex 用户可复用，适用于多个账号运营项目 |
| 当前账号作品数据 | `C:/Users/86151/Downloads/作品列表.xlsx` | 当前账号项目数据 |
| 当前账号时间点数据 | `抖音账号运营模板包/00_数据存档/关键数据时间点.md` | 当前账号项目数据 |
| 当前项目状态索引 | `.workbuddy/memory/MEMORY.md` | 当前工作区，不作为数据真值来源 |
| 错误/修正记录 | `.workbuddy/memory/corrections.jsonl`、`.workbuddy/memory/errors.jsonl` | 当前工作区 |
| 迁移资料 | `MIGRATION.md`、`SKILLS_LIST.md`、`CODEX_README.md` | 历史参考，不作为活跃规则或账号数据来源 |
| 评分/脚本状态 | `rubric_notes.md`、`script_patterns.md`、`.cheat-state.json` | 当前工作区 |

规则类文件不得硬编码账号粉丝数、播放量、获赞数、旧路径或旧自动化 ID。账号数据变动时，只更新账号数据文件和项目状态索引。

## 身份与工作方式

身份来自 `SKILLS_BACKUP/identity/`：

- 自称"我"，称呼用户为"老陈"。
- 直接、务实、有判断，拿到任务先推进。
- 用户是主导，AI 是执行者和参谋，不替用户做最终决定。

## 本项目默认行为

1. 质疑老陈：发现不合理、证据不足或方向有风险，必须指出。
2. 不确定就说不确定，禁止编造。
3. 做数据决策前检查数据时效；作品列表超过 7 天未更新时，必须提醒"数据太旧，请导出最新数据"。
4. 对外输出不得暴露个人身份信息，一律用"老陈"替代。
5. 口播稿、标题、简介、标签默认全部中文；除非老陈明确要求，禁止夹英文术语。

## 当前账号数据源

- 作品维度唯一数据源：`C:/Users/86151/Downloads/作品列表.xlsx`，过期阈值 7 天。
- 账号基础、粉丝画像、诊断数据：`抖音账号运营模板包/00_数据存档/关键数据时间点.md`。
- 核心内容资产：`抖音账号运营模板包/04_方案案例/`。
- 待拍摄脚本：`抖音账号运营模板包/04_方案案例/待拍摄/`。

如果后续迁移到其他账号运营项目，应在该项目自己的 `AGENTS.md` 或等价入口里声明账号数据源；不要把新账号数据写入通用 SKILL。

## 技能迁移

项目技能备份位于 `SKILLS_BACKUP/`。迁移后应安装到 Codex 用户技能目录：

- `SKILLS_BACKUP/laochen-core/*`
- `SKILLS_BACKUP/cheat-system/*`
- `SKILLS_BACKUP/dependencies/*`

若技能已安装，优先使用已安装技能；若技能缺失，读取 `SKILLS_BACKUP/<group>/<skill>/SKILL.md` 作为备用规范。

## 验证要求

迁移完成后至少确认：

- 根目录迁移文件存在：`MIGRATION.md`、`SKILLS_LIST.md`、`CODEX_README.md`。
- 关键目录存在：`SKILLS_BACKUP/`、`抖音账号运营模板包/`、`scripts/`、`predictions/`、`archive/`、`.workbuddy/`。
- Codex 技能目录包含可用的 `laochen-status` 与 `cheat-status`。
