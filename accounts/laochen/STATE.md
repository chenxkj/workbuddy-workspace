# 老陈账号状态索引

> 用途：Codex 项目内的当前状态索引。这里只放路径和状态，不保存数据真值。

## 当前入口

| 类型 | 路径 |
|:--|:--|
| 项目入口 | `AGENTS.md` |
| 账号总控 | `accounts/laochen/CONTENT_PLAN.md` |
| 账号配置索引 | `accounts/laochen/account-profile.md` |
| 抖音平台适配 | `platforms/douyin/platform.md` |
| 小红书平台适配 | `platforms/xiaohongshu/platform.md` |
| B站平台适配 | `platforms/bilibili/platform.md` |
| 公众号平台适配 | `platforms/wechat-official/platform.md` |

## 当前状态

| 项目 | 状态 |
|:--|:--|
| 主平台 | 抖音 |
| 扩展平台 | 小红书、B站、公众号已建适配文件 |
| 当前阶段 | 早期涨粉期，爆款后回落，需要制造新的强场景内容 |
| 本周主线 | 谈薪话术、面试避坑、面试加分、真实职场故事 |
| 商业试验线 | 技术外包避坑 + 产品落地拆解，小比例测试 |

## 数据源

| 类型 | 路径 |
|:--|:--|
| 作品数据 | `AGENTS.md` 中声明的作品表路径；迁移新电脑后需重新导出或更新路径 |
| 账号时间点 | `抖音账号运营模板包/00_数据存档/关键数据时间点.md` |
| 单条方案 | `抖音账号运营模板包/04_方案案例/` |
| 账号复盘 | `抖音账号运营模板包/05_账号复盘/账号复盘/` |
| 预测记录 | `predictions/` |
| 校准状态 | `.cheat-state.json` |

## 迁移说明

旧 `.workbuddy/` 目录不再作为当前状态来源。换电脑时只迁移本项目文件和 Codex skills，不迁移 WorkBuddy 运行时数据。

