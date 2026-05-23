#!/usr/bin/env python3
"""MemPalace 自动同步脚本 - 从 corrections.jsonl 提取新洞察写入宫殿"""
import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

CORRECTIONS_FILE = Path.home() / ".openclaw" / "memory" / "self-improving" / "corrections.jsonl"
SYNC_STATE = Path.home() / ".mempalace" / "sync_state.json"


def get_last_sync():
    if SYNC_STATE.exists():
        return json.loads(SYNC_STATE.read_text(encoding="utf-8")).get("last_sync", "1970-01-01T00:00:00")
    return "1970-01-01T00:00:00"


def save_sync_state():
    SYNC_STATE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE.write_text(json.dumps({
        "last_sync": datetime.now(timezone.utc).isoformat(),
        "total_corrections": sum(1 for _ in open(CORRECTIONS_FILE, encoding="utf-8")) if CORRECTIONS_FILE.exists() else 0,
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_insights(corrections, since=None):
    """从纠正记录中提取可写入宫殿的洞察"""
    insights = []
    seen_topics = set()

    for entry in corrections:
        ts = entry.get("logged_at", entry.get("timestamp", ""))
        if since and ts < since:
            continue

        topic = entry.get("topic", "")
        correct = entry.get("correct", "")
        wrong = entry.get("wrong", "")

        # 去重
        if topic in seen_topics:
            continue
        seen_topics.add(topic)

        # 分类标签
        if "评分" in topic:
            tag = "【踩坑·评分】"
        elif "预测" in topic:
            tag = "【踩坑·预测】"
        elif "内容" in topic or "开头" in topic or "时长" in topic:
            tag = "【踩坑·内容】"
        elif "流程" in topic or "铁律" in topic:
            tag = "【踩坑·流程】"
        elif "技术" in topic:
            tag = "【踩坑·技术】"
        else:
            tag = "【踩坑】"

        # 构建记忆条目
        content = f"{tag}{topic} | 错误: {wrong[:100]} | 对策: {correct[:200]}"
        insights.append(content)

    return insights


def main():
    mode = sys.argv[2] if len(sys.argv) > 2 else "incremental"

    if not CORRECTIONS_FILE.exists():
        print("No corrections file found.")
        return 1

    corrections = []
    with open(CORRECTIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                corrections.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass

    print(f"Total corrections: {len(corrections)}")

    if mode == "incremental":
        last_sync = get_last_sync()
        print(f"Last sync: {last_sync}")
        new_count = sum(1 for c in corrections if c.get("logged_at", c.get("timestamp", "")) > last_sync)
        print(f"New since last sync: {new_count}")
        insights = extract_insights(corrections, since=last_sync)
    else:
        insights = extract_insights(corrections)

    print(f"Insights to sync: {len(insights)}")

    if not insights:
        print("Nothing new to sync.")
        save_sync_state()
        return 0

    # 写入 MemPalace
    try:
        from mempalace.mcp_server import tool_add_drawer, tool_status

        written = 0
        skipped = 0
        for content in insights:
            # 简单去重：截取前80字符比较
            preview = content[:80]

            try:
                result = tool_add_drawer("老陈工作区", "general", content)
                written += 1
            except Exception as e:
                print(f"  SKIP: {preview}... ({e})")
                skipped += 1

        status = tool_status()
        print(f"Synced: {written} added, {skipped} skipped")
        print(f"Total drawers: {status.get('total_drawers', '?')}")
    except ImportError:
        print("ERROR: mempalace not installed or not importable")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1

    save_sync_state()
    return 0


if __name__ == "__main__":
    sys.exit(main())
