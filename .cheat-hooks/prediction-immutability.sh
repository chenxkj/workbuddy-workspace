#!/bin/bash
# prediction-immutability hook
# Blocks edits to the prediction段 of predictions/*.md files
# Called by Claude Code PreToolUse hook

ARGS="$*"
FILE=$(echo "$ARGS" | grep -oE 'predictions/[^"]+\.md' | head -1)

if [[ -z "$FILE" ]]; then
    exit 0
fi

# Check if this is an Edit or Write operation targeting prediction段
if echo "$ARGS" | grep -qE "(Edit|Write|Write_to_file)"; then
    if [[ "$ARGS" == *"## 预测"* ]] || [[ "$ARGS" == *"预测\n"* ]]; then
        echo "❌ 预测段受保护 — 预测文件写完后不可修改" >&2
        echo "   如需补充复盘，在 '## 复盘' 段追加" >&2
        exit 1
    fi
fi

exit 0
