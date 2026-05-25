# Errors

Command failures and integration errors.

---

## [ERR-20260525-001] skill-sync quoting

**Logged**: 2026-05-25T15:30:00+08:00
**Area**: shell

### Summary
Nested PowerShell `-Command` quoting caused variable stripping during skill sync.

### Resolution
Run the PowerShell script directly in the current shell with escalation instead of nesting `powershell.exe -Command` inside another PowerShell command.

## [ERR-20260525-002] export sandbox write

**Logged**: 2026-05-25T16:40:00+08:00
**Area**: migration

### Summary
Project export script failed inside sandbox when creating `C:\tmp\laochen-codex-project-migration`.

### Resolution
Rerun the same export script with escalated permissions. The script completed and produced `C:\tmp\laochen-codex-project-migration.zip`.
