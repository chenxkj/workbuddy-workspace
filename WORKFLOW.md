# WORKFLOW — cheat-on-content 完整闭环

## 两套评分系统的协同（v1.1新增）

```
┌─────────────────────────────────────────────────────────┐
│  cheat-on-content（7维composite）  │  老陈SKILL（6维100分）  │
├─────────────────────────────────┼───────────────────────┤
│  7维质量校准                    │  传播结构评分            │
│  ER/HP/QL/NA/AB/SR/SAT         │  留存/收藏/分享/合规    │
│  内部质量标尺                    │  合规+踩坑红线          │
└─────────────────────────────────┴───────────────────────┘
```

### 评分流程（双评制）

1. **写稿** → `laochen-script-writing` 输出逐字稿
2. **双评分** →
   - `laochen-script-scoring`：百分制（合规优先）
   - `rubric_notes.md` 7维：composite分（质量校准）
3. **比对校验** →
   - composite高但老陈分低 → 检查合规/踩坑
   - 老陈分高但composite低 → 检查情感/叙事
4. **发布决策**：以老陈SKILL为主（合规优先），composite作为质量参考

---

## 日常流程

```
找选题 → 写稿 → 双评分 → 预测 → 拍摄 → 发布 → 复盘
```

### 每一步的 skill 触发词

| 步骤 | Skill | 触发词 |
|---|---|---|
| 找选题 | `/cheat-seed` 或 `/cheat-trends` | "找选题" / "抓热点" |
| 写稿 | `laochen-script-writing` | "写稿" / "写脚本" |
| 双评分 | `laochen-script-scoring` + `rubric_notes.md` | "评分" / "打分" |
| 预测 | `/cheat-predict` | "启动预测" |
| 拍摄登记 | `/cheat-shoot` | "拍了" |
| 发布登记 | `/cheat-publish` | "已发布 https://..." |
| 复盘 | `/cheat-retro`（读04_方案案例/） | "复盘 videos/..." |
| 看状态 | `/cheat-status` | "状态" |

### 核心原则

1. **预测锁**：预测文件写完后锁死，复盘只能追加
2. **盲预测铁律**：发布前写定，发布后不可修改
3. **每条必复盘**：跳过复盘 = 校准失败
4. **T+3 回收**：发布后 3 天内完成复盘

---

## 数据来源

- **方案复盘**：`抖音账号运营模板包/04_方案案例/*.md`（含播放量/完播率/收藏/分享）
- **脚本草稿**：`scripts/`
- **预测日志**：`predictions/`（hook保护，锁死）
- **工作目录**：`videos/`

---

## 文件命名规则

```
scripts/  → <date>_<id>_<short>.md
predictions/ → <date>_<id>_<short>.md
videos/   → <date>_<id>_<short>/
```

`<id>` = 12位 hash（对标题+平台ID做sha256）
`<short>` = 标题前3-8字

---

## 目录说明

- `scripts/` — 拍前草稿（cheat-seed写或手动）
- `predictions/` — immutable 预测日志（hook保护）
- `videos/` — 拍后工作目录（cheat-shoot建子目录）
- `samples/` — 对标账号样本（cheat-learn-from建立）
- `抖音账号运营模板包/04_方案案例/` — 方案复盘数据源
