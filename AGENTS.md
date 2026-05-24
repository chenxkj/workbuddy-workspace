# Codex Project Context

本项目由腾讯 WorkBuddy 迁移到 Codex。进入本工作区后，先按“规则、流程、账号数据、平台适配分离”的原则加载上下文。

## 唯一来源

| 类型 | 唯一来源 | 范围 |
|:--|:--|:--|
| 通用规则/流程 | `SKILLS_BACKUP/laochen-core/*/SKILL.md`，已安装副本在 `C:/Users/86151/.codex/skills/` | 本机 Codex 用户可复用，适用于多个账号运营项目 |
| 平台适配规则 | `docs/architecture/PLATFORM_ADAPTERS.md`、`platforms/<platform>/platform.md` | 抖音、小红书等平台字段、指标、发布检查 |
| 目录重构规划 | `docs/architecture/PROJECT_STRUCTURE.md` | 当前工作区结构演进，不是数据真值来源 |
| 当前账号人设/偏好 | `accounts/laochen/account-profile.md` 索引到 `SKILLS_BACKUP/laochen-core/laochen-workstyle/SKILL.md` | 老陈账号专属，其他账号必须另建 |
| 当前内容总控 | `accounts/laochen/CONTENT_PLAN.md` | 当前账号整体状态、系列计划、选题优先级唯一来源 |
| 当前账号作品数据 | `C:/Users/86151/Downloads/作品列表.xlsx` | 当前账号项目数据 |
| 当前账号时间点数据 | `抖音账号运营模板包/00_数据存档/关键数据时间点.md` | 当前账号项目数据 |
| 当前项目状态索引 | `.workbuddy/memory/MEMORY.md` | 当前工作区，只做索引，不作为数据真值来源 |
| 错误/修正记录 | `.workbuddy/memory/corrections.jsonl`、`.workbuddy/memory/errors.jsonl` | 当前工作区 |
| 迁移资料 | `MIGRATION.md`、`SKILLS_LIST.md` | 历史参考，不作为活跃规则或账号数据来源 |
| 评分/脚本状态 | `rubric_notes.md`、`script_patterns.md`、`.cheat-state.json` | 当前账号项目，后续迁入 `accounts/laochen/platforms/douyin/` |

## 分离红线

1. 规则类文件不得硬编码粉丝数、播放量、获赞数、旧路径、旧自动化 ID。
2. 平台规则不得写入账号人设文件。
3. 账号数据不得写入通用 skill 或平台适配规则。
4. 抖音数据和小红书数据必须分开放，不能共用一个作品表。
5. `.workbuddy/memory/MEMORY.md` 只记录状态和路径索引，不保存数值真值。
6. 后续新增账号时，只复用通用 skill 和平台适配，不复制老陈账号数据。
7. 内容规划、系列进度、选题池、优先级只维护在 `accounts/laochen/CONTENT_PLAN.md`，其他文件只做来源或单项产物。

## 身份与工作方式

身份来自 `SKILLS_BACKUP/identity/`：

- 自称“我”，称呼用户为“老陈”。
- 直接、务实、有判断，拿到任务先推进。
- 用户是主导，AI 是执行者和参谋，不替用户做最终决定。

## 当前默认行为

1. 发现不合理、证据不足或方向有风险，必须指出。
2. 不确定就说不确定，禁止编造。
3. 做数据决策前检查数据时效；作品列表超过 7 天未更新时，必须提醒“数据太旧，请导出最新数据”。
4. 对外输出不得暴露个人身份信息，一律用“老陈”替代。
5. 口播稿、标题、简介、标签默认全部中文；除非老陈明确要求，禁止夹英文术语。

## 当前账号数据源

- 作品维度唯一数据源：`C:/Users/86151/Downloads/作品列表.xlsx`，过期阈值 7 天。
- 账号基础、粉丝画像、诊断数据：`抖音账号运营模板包/00_数据存档/关键数据时间点.md`。
- 内容计划唯一来源：`accounts/laochen/CONTENT_PLAN.md`。
- 核心内容资产：`抖音账号运营模板包/04_方案案例/`。
- 待拍摄脚本：`抖音账号运营模板包/04_方案案例/待拍摄/`。

如果后续迁移到其他账号运营项目，应在该项目自己的 `AGENTS.md` 或等价入口里声明账号数据源；不要把新账号数据写入通用 skill。

## 多平台适配

当前默认平台是抖音。支持小红书时，使用平台适配文件，不修改通用内容流程。

- 抖音：短视频/长视频，核心指标为播放、5秒完播、整体完播、2秒跳出、互动、涨粉。
- 小红书：图文/视频笔记，核心指标为阅读/播放、收藏、评论、搜索曝光、涨粉。

平台字段、指标、发布检查详见 `docs/architecture/PLATFORM_ADAPTERS.md`、`platforms/douyin/platform.md`、`platforms/xiaohongshu/platform.md`。

## 技能迁移

项目技能备份位于 `SKILLS_BACKUP/`。已安装技能优先使用 `C:/Users/86151/.codex/skills/`。

如修改 `SKILLS_BACKUP/laochen-core/*`，必须同步到 `C:/Users/86151/.codex/skills/`，并验证两边文件一致。

## 验证要求

至少确认：

- 根目录入口文件存在：`AGENTS.md`、`CODEX_README.md`。
- 架构规划存在：`docs/architecture/PLATFORM_ADAPTERS.md`、`docs/architecture/PROJECT_STRUCTURE.md`。
- 关键目录存在：`SKILLS_BACKUP/`、`抖音账号运营模板包/`、`scripts/`、`predictions/`、`.workbuddy/`。
- Codex 技能目录包含可用的 `laochen-status` 和核心 `laochen-*` skills。
