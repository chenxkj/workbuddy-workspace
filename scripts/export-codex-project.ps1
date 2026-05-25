$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$OutputZip = "C:\tmp\laochen-codex-project-migration.zip"
$StagingRoot = "C:\tmp\laochen-codex-project-migration"
$StagingProject = Join-Path $StagingRoot "laochen-codex-project"

if (Test-Path -LiteralPath $StagingRoot) {
  Remove-Item -LiteralPath $StagingRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $StagingProject | Out-Null

$excludeDirs = @(
  ".git",
  "node_modules",
  "outputs"
)

$excludeFiles = @(
  "wechat_article.html",
  "wechat_article_2020a.html",
  "wechat_article_2020a_short.html",
  "wechat_article_2020b.html",
  "wechat_article_2020b_short.html",
  "cover-preview.html",
  "douyin-page.png"
)

Get-ChildItem -LiteralPath $ProjectRoot -Force | ForEach-Object {
  if ($excludeDirs -contains $_.Name) { return }
  if ($excludeFiles -contains $_.Name) { return }

  $destination = Join-Path $StagingProject $_.Name
  Copy-Item -LiteralPath $_.FullName -Destination $destination -Recurse -Force
}

if (Test-Path -LiteralPath $OutputZip) {
  Remove-Item -LiteralPath $OutputZip -Force
}

Compress-Archive -LiteralPath $StagingProject -DestinationPath $OutputZip -Force

Write-Host "Exported migration package: $OutputZip"
