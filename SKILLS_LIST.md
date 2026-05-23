# 老陈抖音项目 · SKILL依赖清单

> 生成日期：2026-05-23 | 用于项目迁移到CODEX

---

## 一、核心SKILL（15个·老陈自建·必须迁移）

| # | SKILL名称 | 版本 | 类型 | 触发词/职责 |
|---|----------|:----:|------|-----------|
| 1 | `laochen-script-scoring` | v5.20 | 评分 | 内容评分+合规否决（6维100分+9维盲评） |
| 2 | `laochen-script-writing` | v5.15 | 文案 | 口播逐字稿+情绪节奏图（故事驱动+结论克制） |
| 3 | `laochen-topic-research` | v5.6 | 选题 | 7关否决制选题评审（受众宽度FG建议化） |
| 4 | `laochen-plan-generator` | v5.4 | 方案 | 11项交付物组装（标题+简介+标签+封面） |
| 5 | `laochen-view-prediction` | v5.4 | 预测 | 播放量盲预测（规范唯一来源） |
| 6 | `laochen-data-review` | — | 复盘 | 单条视频数据复盘+偏差根因分析 |
| 7 | `laochen-account-review` | — | 账号 | 账号层面数据变化+合集规划+选题方向 |
| 8 | `laochen-orchestrator` | — | 协调 | 多Agent协同流水线（选题→文案→评分→方案→复盘） |
| 9 | `laochen-bump` | — | 校准 | Rubric升级（吸收CHEAT bump机制） |
| 10 | `laochen-score-blind` | — | 子Agent | 独立盲评Sub-agent（Channel B隔离） |
| 11 | `laochen-project` | — | 配置 | 项目级配置（账号/素材库/发布模板） |
| 12 | `laochen-research` | — | 调研 | 深度调研+专家调度（整合hv-analysis） |
| 13 | `laochen-status` | — | 看板 | 状态看板（校准进度/Buffer/待办） |
| 14 | `laochen-workstyle` | — | 风格 | 工作风格定义（人设/语速/禁用词/评论策略） |
| 15 | `laochen-longvideo-scoring` | v4.0 | 别名 | 长视频评分别名/路由（已整合到script-scoring） |

---

## 二、CHEAT校准系统（14个·内容质量闭环·必须迁移）

| # | SKILL名称 | 类型 | 职责 |
|---|----------|------|------|
| 1 | `cheat-on-content` | 核心 | 7/8维composite内容质量校准（方法论通用） |
| 2 | `cheat-init` | 初始化 | 首次onboarding+脚手架创建 |
| 3 | `cheat-score` | 评分 | 单篇稿子轻量打分（控制台输出） |
| 4 | `cheat-predict` | 预测 | 盲预测日志（immutable·发布前写定） |
| 5 | `cheat-retro` | 复盘 | T+N天数据回收+复盘+写入rubric_notes |
| 6 | `cheat-bump` | 升级 | Rubric/bucket升级（5步+跨模型审核） |
| 7 | `cheat-seed` | 选题 | 对话式选题讨论（一次一个·深度挖掘） |
| 8 | `cheat-trends` | 热点 | 热点抓取+粗打分+写入candidates.md |
| 9 | `cheat-recommend` | 推荐 | 按rubric排序推荐top N选题 |
| 10 | `cheat-publish` | 发布 | 登记已发布+更新元数据 |
| 11 | `cheat-shoot` | 拍摄 | 登记已拍摄+Buffer管理 |
| 12 | `cheat-status` | 看板 | CHEAT状态看板 |
| 13 | `cheat-learn-from` | 对标 | 对标账号数据导入+pattern拆解 |
| 14 | `cheat-migrate` | 迁移 | .cheat-state.json版本升级 |

---

## 三、关键依赖SKILL（6个·功能支撑·建议迁移）

| # | SKILL名称 | 类型 | 职责 |
|---|----------|------|------|
| 1 | `douyin-forbidden` | 合规 | 抖音敏感词库+平台红线检测（含敏感词检查） |
| 2 | `self-improving-agent` | 质量 | 错误处理5步流程+corrections.jsonl写入 |
| 3 | `mempalace` | 记忆 | 本地AI记忆系统（语义搜索+知识图谱） |
| 4 | `mempalace-auto-sync` | 记忆 | 自动同步核心洞察到MemPalace |
| 5 | `fuzhou-exam` | 教育 | 福州中考AI教师团队（老陈孩子用） |
| 6 | `humanizer-zh` | 文案 | 去除AI生成痕迹（可选） |

---

## 四、未备份SKILL（需在CODEX中另行获取）

以下SKILL在WorkBuddy可用但未打包到SKILLS_BACKUP（源目录名称不匹配或为外部安装）：

| SKILL名称 | 类型 | 未备份原因 |
|-----------|------|-----------|
| `douyin-sensitive-check` | 合规 | 功能已整合到`douyin-forbidden`中 |
| `karpathy-guidelines` | 规范 | 源目录名`andrej-karpathy-skills`，为独立安装 |
| `copywriting` | 文案 | 源目录名`copywriter-pro`，需单独获取 |
| `khazix-writer` | 长文 | 需在CODEX中重新安装 |
| `local-whisper` | 语音 | 需在CODEX中重新安装 |
| `markitdown` | 转换 | 需在CODEX中重新安装 |
| `yt-dlp-downloader` | 下载 | 需在CODEX中重新安装 |

---

## 五、SKILL安装优先级

### 必须先装（核心流水线缺一不可）
```
laochen-script-scoring  laochen-script-writing   laochen-topic-research
laochen-plan-generator  laochen-view-prediction  laochen-data-review
laochen-workstyle       laochen-score-blind
```

### 第二梯队（校准闭环）
```
cheat-on-content   cheat-score   cheat-predict   cheat-retro   cheat-bump
```

### 第三梯队（合规+辅助）
```
douyin-forbidden   self-improving-agent   mempalace   mempalace-auto-sync
```

### 按需安装
```
laochen-orchestrator  laochen-account-review  laochen-research
laochen-status        laochen-project         laochen-bump
cheat-*（其余）       fuzhou-exam             humanizer-zh
```

---

## 六、SKILL存储位置

| 来源 | 路径 | 说明 |
|------|------|------|
| 备份副本 | `./SKILLS_BACKUP/laochen-core/` | 15个老陈核心SKILL |
| 备份副本 | `./SKILLS_BACKUP/cheat-system/` | 14个CHEAT SKILL |
| 备份副本 | `./SKILLS_BACKUP/dependencies/` | 6个关键依赖 |
| 备份副本 | `./SKILLS_BACKUP/identity/` | 3个身份文件（SOUL/IDENTITY/USER） |
| 原始位置 | `~/.workbuddy/skills/` | WorkBuddy全局SKILL目录 |
