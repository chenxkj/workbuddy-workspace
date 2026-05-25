# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260525-001] correction

**Logged**: 2026-05-25T15:30:00+08:00
**Priority**: high
**Status**: pending
**Area**: content-ops

### Summary
老陈账号语速标准必须按后期1.2倍加速后的成片口径统一更新。

### Details
之前只在单次计划里临时调整字数区间，没有替换 `laochen-workstyle` 中的唯一语速基准。正确做法是把原始 3.35字/秒换算为成片等效 4.02字/秒，并同步更新 A类字数上限、计划表和已安装 skill。

### Suggested Action
后续所有脚本字数和时长预测都以 4.02字/秒为唯一成片估算基准；不要继续用3.35字/秒单独估算发布成片。

### Metadata
- Source: user_feedback
- Related Files: SKILLS_BACKUP/laochen-core/laochen-workstyle/SKILL.md; accounts/laochen/CONTENT_PLAN.md
- Tags: laochen, speech-rate, short-video

