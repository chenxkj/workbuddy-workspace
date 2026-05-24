# Multiplatform Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare the migrated content-operations workspace for multiple accounts and platforms without breaking existing Douyin workflows.

**Architecture:** Keep universal rules in skills, platform-specific behavior in platform adapters, account identity and data in account folders, and state files as indexes only. Execute the reorganization in phases so existing scripts and paths keep working until each migration is verified.

**Tech Stack:** Markdown architecture docs, Codex skills, PowerShell path checks, existing workspace files.

---

### Task 1: Freeze Boundaries

**Files:**
- Modify: `AGENTS.md`
- Create: `docs/architecture/PLATFORM_ADAPTERS.md`
- Create: `docs/architecture/PROJECT_STRUCTURE.md`

- [ ] **Step 1: Verify source boundaries are declared**

Run:

```powershell
rg -n "通用规则|账号数据|平台适配|唯一来源" AGENTS.md docs/architecture
```

Expected: output includes `AGENTS.md`, `PLATFORM_ADAPTERS.md`, and `PROJECT_STRUCTURE.md`.

- [ ] **Step 2: Verify no active rule file hardcodes the old model**

Run:

```powershell
rg -n "DeepSeek-V4-Flash|/model DeepSeek" SKILLS_BACKUP/laochen-core C:/Users/86151/.codex/skills
```

Expected: no output.

### Task 2: Add Platform Skeletons

**Files:**
- Create: `platforms/douyin/platform.md`
- Create: `platforms/xiaohongshu/platform.md`
- Create: `accounts/laochen/account-profile.md`
- Create: `accounts/laochen/platforms/douyin/README.md`

- [ ] **Step 1: Create platform directories**

Run:

```powershell
New-Item -ItemType Directory -Force -Path platforms/douyin,platforms/xiaohongshu,accounts/laochen/platforms/douyin | Out-Null
```

Expected: command succeeds.

- [ ] **Step 2: Add adapter files**

Add platform files using the schema from `docs/architecture/PLATFORM_ADAPTERS.md`.

- [ ] **Step 3: Verify skeleton**

Run:

```powershell
Test-Path platforms/douyin/platform.md; Test-Path platforms/xiaohongshu/platform.md; Test-Path accounts/laochen/account-profile.md
```

Expected: all three outputs are `True`.

### Task 3: Migrate One Asset Class

**Files:**
- Move later: `predictions/*`
- Target: `accounts/laochen/platforms/douyin/predictions/`

- [ ] **Step 1: Count current files**

Run:

```powershell
(Get-ChildItem predictions -File).Count
```

Expected: record the number before moving.

- [ ] **Step 2: Move predictions only**

Run after confirming paths:

```powershell
New-Item -ItemType Directory -Force -Path accounts/laochen/platforms/douyin/predictions | Out-Null
Move-Item -LiteralPath predictions\* -Destination accounts/laochen/platforms/douyin/predictions
```

Expected: no files remain in `predictions/`.

- [ ] **Step 3: Update references**

Run:

```powershell
rg -n "predictions/" .
```

Expected: update active references to the new path; leave historical migration docs unchanged only if marked as archive.

### Task 4: Migrate Douyin Content Assets

**Files:**
- Move later: `抖音账号运营模板包/`
- Target: `accounts/laochen/platforms/douyin/`

- [ ] **Step 1: Build a mapping table**

Create a migration table before moving:

```text
抖音账号运营模板包/00_数据存档 -> accounts/laochen/platforms/douyin/data
抖音账号运营模板包/04_方案案例 -> accounts/laochen/platforms/douyin/content/plans
```

- [ ] **Step 2: Move one subfolder at a time**

Use `Move-Item -LiteralPath` only after verifying the target path is inside the workspace.

- [ ] **Step 3: Verify no active old path remains**

Run:

```powershell
rg -n "抖音账号运营模板包" AGENTS.md SKILLS_BACKUP/laochen-core scripts .workbuddy
```

Expected: old path appears only in migration/archive notes until those are cleaned.

### Task 5: Retire Legacy Layout

**Files:**
- Modify: `CODEX_README.md`
- Move later: `MIGRATION.md`, `SKILLS_LIST.md`
- Target: `archive/migration/`

- [ ] **Step 1: Make README current-state only**

Keep `CODEX_README.md` as a short entry file pointing to `AGENTS.md`, `docs/architecture/`, `accounts/`, and `platforms/`.

- [ ] **Step 2: Archive migration docs**

Move migration-only docs into `archive/migration/` after all active references are updated.

- [ ] **Step 3: Final verification**

Run:

```powershell
rg -n "WorkBuddy/Claw|DeepSeek-V4-Flash|当前粉丝|732粉|1031粉" AGENTS.md CODEX_README.md SKILLS_BACKUP/laochen-core docs
```

Expected: no output except explicitly archived migration docs.

---

## Self-Review

- Spec coverage: covers multi-platform adapter boundaries, account/rule/data separation, and phased directory cleanup.
- Placeholder scan: no `TBD` or unresolved placeholders.
- Risk control: avoids immediate mass moves; every move has a search verification step.
