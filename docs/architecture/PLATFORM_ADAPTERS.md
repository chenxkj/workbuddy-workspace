# 多平台适配边界

本文定义“跨账号、跨平台内容运营系统”怎么拆分规则，避免把抖音经验、小红书经验、单账号数据混进通用 Skill。

## 分层原则

| 层级 | 放什么 | 唯一来源 | 是否跨账号复用 |
|:--|:--|:--|:--:|
| 通用内容流程 | 选题、写稿、评分、预测、复盘、bump 机制 | `SKILLS_BACKUP/laochen-core/*` 与已安装 skill | 是 |
| 账号人设偏好 | 主理人身份、口吻、禁用词、内容边界、账号标签 | 当前账号的 `account-profile.md` 或现阶段 `laochen-workstyle` | 否 |
| 平台适配规则 | 字段格式、标题/正文/话题、平台指标、发布检查 | `platforms/<platform>/platform.md` 或本文件后续拆分 | 是 |
| 账号平台数据 | 某账号在某平台的作品数据、后台截图、周期快照 | `accounts/<account>/platforms/<platform>/data/` | 否 |
| 项目状态索引 | 当前待拍、待复盘、路径索引、最近动作 | `.workbuddy/memory/MEMORY.md` 或后续 `accounts/<account>/state.md` | 否 |

## 平台适配接口

每个平台至少需要定义以下字段：

```yaml
platform: douyin | xiaohongshu | bilibili | video-account
content_types:
  - short_video
  - long_video
  - image_text
required_outputs:
  - title
  - body_or_script
  - cover_direction
  - tags
  - publish_checklist
metrics:
  primary:
    - views
    - completion_rate
  secondary:
    - likes
    - comments
    - saves
    - shares
    - follows
freshness_days: 7
```

通用 Skill 只能调用这个接口，不直接写某个平台的字段细节。平台字段细节必须放在平台适配文件。

## 抖音适配草案

| 项目 | 规则 |
|:--|:--|
| 内容形态 | 短视频为主，长视频按 C/D 类处理 |
| 核心交付 | 逐字稿、标题、简介、话题、封面建议、发布时间建议 |
| 核心指标 | 播放、5秒完播、整体完播、2秒跳出、点赞、评论、收藏、分享、涨粉 |
| 决策重点 | 前3秒钩子、完播、互动扩散、账号基准线 |
| 数据来源 | 当前账号导出的作品列表、关键数据时间点、单条后台数据 |

## 小红书适配草案

| 项目 | 规则 |
|:--|:--|
| 内容形态 | 图文笔记、视频笔记并行 |
| 核心交付 | 标题、正文、封面首图、图片结构、话题、评论区引导 |
| 核心指标 | 阅读/播放、点赞、收藏、评论、转发、涨粉、搜索曝光 |
| 决策重点 | 标题搜索意图、封面信息密度、收藏价值、评论讨论点 |
| 数据来源 | 小红书后台导出、笔记链接、周期截图、关键词表现 |

## 禁止事项

1. 不把抖音的完播阈值写进通用写稿 Skill。
2. 不把小红书的标题/封面规则写进账号人设文件。
3. 不把某个账号的粉丝数、播放量、爆款样本写进平台适配规则。
4. 不用同一个 `作品列表.xlsx` 混放多个平台数据。
5. 不在 `MEMORY.md` 保存数值真值，只保存路径索引和当前状态。

## 后续拆分建议

当开始正式做小红书或第三个平台时，把本文件拆成：

```text
platforms/
  douyin/platform.md
  xiaohongshu/platform.md
  bilibili/platform.md
```

拆分后 `docs/architecture/PLATFORM_ADAPTERS.md` 只保留接口总则和链接。
