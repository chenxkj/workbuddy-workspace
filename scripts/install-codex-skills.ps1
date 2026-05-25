$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$SourceRoot = Join-Path $ProjectRoot "SKILLS_BACKUP\laochen-core"
$CodexSkillsRoot = Join-Path $env:USERPROFILE ".codex\skills"

if (-not (Test-Path -LiteralPath $SourceRoot)) {
  throw "Cannot find source skills: $SourceRoot"
}

New-Item -ItemType Directory -Force -Path $CodexSkillsRoot | Out-Null

Get-ChildItem -LiteralPath $SourceRoot -Directory | ForEach-Object {
  $destination = Join-Path $CodexSkillsRoot $_.Name
  New-Item -ItemType Directory -Force -Path $destination | Out-Null
  Get-ChildItem -LiteralPath $_.FullName -Force | Copy-Item -Destination $destination -Recurse -Force
}

Write-Host "Installed laochen skills to $CodexSkillsRoot"

