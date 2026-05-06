#!/bin/bash
# session-start hook
# Shows buffer / pending retro status on session start

WORKSPACE_DIR="c:/Users/86151/WorkBuddy/20260411163952"
STATE_FILE="$WORKSPACE_DIR/.cheat-state.json"

cd "$WORKSPACE_DIR" || exit 1

if [[ ! -f "$STATE_FILE" ]]; then
    echo "cheat-on-content 未初始化"
    exit 0
fi

# Extract key fields using grep (no jq dependency)
CAL=$(grep -oP '"calibration_samples":\s*\K\d+' "$STATE_FILE" 2>/dev/null || echo "?")
PENDING=$(grep -oP '"pending_retros":\s*\[[^\]]*\]' "$STATE_FILE" 2>/dev/null | grep -o "{" | wc -l)
SHOOTS=$(grep -oP '"shoots":\s*\[[^\]]*\]' "$STATE_FILE" 2>/dev/null | grep -o "{" | wc -l)
LAST_PUB=$(grep -oP '"last_published_at":\s*"\K[^"]*' "$STATE_FILE" 2>/dev/null || echo "无")
LAST_RETRO=$(grep -oP '"last_retro_at":\s*"\K[^"]*' "$STATE_FILE" 2>/dev/null || echo "无")

echo "=== cheat-on-content 状态 ==="
echo "校准样本: $CAL"
echo "待复盘:   $PENDING 条"
echo "拍摄队列: $SHOOTS 条"
echo "最近发布: $LAST_PUB"
echo "最近复盘: $LAST_RETRO"
