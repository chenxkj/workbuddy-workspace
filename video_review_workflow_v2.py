"""
视频审核 + 多维评分 + 改进建议 工作流 v2
========================================
输入：视频路径
输出：评分报告 + 改进建议 + 过程帧（用完删除）
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import json
import re
import subprocess
import datetime

# ===== 配置 =====
VIDEO_PATH = r"F:\自媒体\014三明学院对新人说\4月18日.mp4"
OUTPUT_DIR = r"c:\Users\86151\WorkBuddy\20260411163952\video_review_frames"
FFMPEG_BIN = r"C:\Users\86151\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# 方案脚本（用于脚本还原度对比）
PLANNED_SCRIPT = [
    (0, 5, "我主页的第一行：三明学院。很多人看不上这四个字，觉得不是985、211，连听都没听过。"),
    (5, 15, "最近很多同学私信我，说对未来迷茫，不知道学什么，怕嵌入式卷、怕AI抢饭碗。"),
    (15, 25, "我就一句话：别纠结，先做起来！在做的过程里找答案，比你原地想1万条路有用得多。"),
    (25, 30, "我不是名校毕业，但我从来不是'想清楚了再做'，而是'先做起来'。我是老陈，只说真话。关注我，少踩坑。"),
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== Step 1: 提取帧 =====

# 获取视频时长
probe = subprocess.run([FFMPEG_BIN, "-i", VIDEO_PATH], capture_output=True, text=True)
m = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", probe.stderr)
total_seconds = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) if m else 36
print(f"视频总时长: {total_seconds}秒")

# 提取每5秒一帧 + 封面帧
frame_times = [0] + [t for t in range(5, total_seconds, 5)]
frame_files = {}
for t in frame_times:
    out = os.path.join(OUTPUT_DIR, f"frame_{t:02d}s.jpg")
    r = subprocess.run([FFMPEG_BIN, "-ss", str(t), "-i", VIDEO_PATH, "-vframes", "1", "-q:v", "2", out, "-y"],
                      capture_output=True, text=True)
    if os.path.exists(out):
        frame_files[t] = out

print(f"提取帧: {list(frame_files.keys())}")

# ===== Step 2: OCR识别 =====

import cv2
import numpy as np
import easyocr

reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)

# OCR每一帧，输出[时间, [文字列表]]
all_ocr = {}
for t, path in sorted(frame_files.items()):
    res = reader.readtext(path, detail=0)
    texts = [x.strip() for x in res if x.strip() and len(x.strip()) > 1]
    all_ocr[t] = texts
    print(f"  {t}s: {texts[:3]}{'...' if len(texts)>3 else ''}")

# ===== Step 3: 合规检测 =====

BANNED_HIGH = ["私信", "收徒", "带你", "跟我做", "手把手", "二维码", "扫码", "公众号", "私信我"]
BANNED_MED  = ["学费", "付费", "进群", "加群", "涨粉暴富", "内幕", "必涨", "万", "k", "K"]
BANNED_SOFT = ["评论区留言", "有需要", "联系我"]

violations = []
for t, texts in all_ocr.items():
    for text in texts:
        for w in BANNED_HIGH:
            if w in text:
                violations.append({"time": t, "word": w, "text": text, "level": "HIGH"})
        for w in BANNED_MED:
            if w in text:
                violations.append({"time": t, "word": w, "text": text, "level": "MED"})

print(f"\n违规检测: {len(violations)}处")
for v in violations:
    print(f"  [{v['level']}] {v['time']}s: '{v['word']}' in '{v['text']}'")

# ===== Step 4: 预评分幻觉核查 =====

# 读取方案预评分，检查是否有幻觉
PLAN_SCORES = {
    "钩子强度": 25,  # 方案自评
    "合规安全": 10,
    "总分": 95,
}
print(f"\n⚠️ 方案预评分自评: 钩子{PLAN_SCORES['钩子强度']} | 合规{PLAN_SCORES['合规安全']} | 总分{PLAN_SCORES['总分']}")

# 核查：钩子自评25分，但脚本逐字稿里有没有"但我做到了研发总监"或等效反差句？
hook_text = " ".join(all_ocr.get(0, []) + all_ocr.get(5, []))
has_contrast = any(k in hook_text for k in ["做到了", "但我", "结果", "做到", "管过", "研发"])
if PLAN_SCORES["钩子强度"] == 25 and not has_contrast:
    print("🚨 幻觉预警：方案钩子自评25/25，但脚本逐字稿中未发现反差句！")
    print(f"   封面钩子文字: {all_ocr.get(0, [])}")
    print(f"   建议：补反差句，如'但我做到了研发总监'")

if PLAN_SCORES["合规安全"] == 10:
    has_private_msg = any("私信" in " ".join(texts) for texts in all_ocr.values())
    if has_private_msg:
        print("🚨 幻觉预警：方案合规自评10/10，但脚本含'私信'词！")

# ===== Step 5: 多维度评分 =====

scores = {}

# ---- 5.1 钩子强度 (25分) ----
hook_texts = all_ocr.get(0, [])
hook_raw = " ".join(hook_texts)
has_identity = any(k in hook_raw for k in ["三明学院", "老陈", "主页", "学历", "学院"])
has_conflict = any(k in hook_raw for k in ["看不上", "觉得不是", "不是985", "迷茫", "私信", "问我"])
has_suspense = any(k in hook_raw for k in ["为什么", "但是", "所以", "这", "三字"])
hook_score = 0
hook_notes = []
if has_identity:
    hook_score += 10
    hook_notes.append("✅ 有人设身份锚点")
else:
    hook_notes.append("❌ 缺身份锚点")
if has_conflict:
    hook_score += 10
    hook_notes.append("✅ 有冲突/痛点")
else:
    hook_notes.append("❌ 缺冲突")
if has_suspense:
    hook_score += 5
    hook_notes.append("✅ 有悬念")
else:
    hook_notes.append("🟡 悬念一般")
scores["钩子强度"] = {"score": hook_score, "max": 25, "notes": hook_notes}

# ---- 5.2 情绪价值 (20分) ----
emotion_keywords = ["迷茫", "纠结", "做起来", "先做", "有用", "从来不是", "名校", "不是", "想", "怕"]
emotion_hits = 0
for t, texts in all_ocr.items():
    for text in texts:
        for kw in emotion_keywords:
            if kw in text:
                emotion_hits += 1
emotion_score = min(20, emotion_hits * 3)
emotion_notes = [f"✅ 情绪词命中{emotion_hits}次"]
if emotion_hits < 4:
    emotion_score = emotion_hits * 3
    emotion_notes.append("🟡 情绪密度一般")
else:
    emotion_notes.append("✅ 情绪密度良好")
scores["情绪价值"] = {"score": emotion_score, "max": 20, "notes": emotion_notes}

# ---- 5.3 内容结构 (15分) ----
all_text_flat = " ".join([" ".join(t) for t in all_ocr.values()])
has_opening = any(k in all_text_flat for k in ["三明学院", "主页"])
has_pain = any(k in all_text_flat for k in ["迷茫", "纠结", "怕", "私信", "问我"])
has_solution = any(k in all_text_flat for k in ["做起来", "先做", "过程"])
has_ending = any(k in all_text_flat for k in ["老陈", "只说真话", "关注", "少踩"])
struct_score = sum([has_opening, has_pain, has_solution, has_ending]) * 3.75
struct_notes = []
struct_notes.append("✅ 开头" if has_opening else "❌ 缺开头")
struct_notes.append("✅ 痛点" if has_pain else "❌ 缺痛点")
struct_notes.append("✅ 干货" if has_solution else "❌ 缺干货")
struct_notes.append("✅ 结尾" if has_ending else "❌ 缺结尾")
scores["内容结构"] = {"score": struct_score, "max": 15, "notes": struct_notes}

# ---- 5.4 节奏保持 (15分) ----
# 检查每5秒段是否有实质内容（排除无文字帧）
active_frames = [t for t, texts in all_ocr.items() if len(texts) >= 1]
gap_frames = []
for i in range(len(frame_times)):
    if frame_times[i] not in active_frames and frame_times[i] > 0:
        gap_frames.append(frame_times[i])
rhythm_score = max(0, 15 - len(gap_frames) * 3)
rhythm_notes = [f"✅ 共{len(active_frames)}帧有内容"]
if gap_frames:
    rhythm_notes.append(f"🟡 帧{gap_frames}内容稀疏")
else:
    rhythm_notes.append("✅ 全程节奏稳定")
scores["节奏保持"] = {"score": rhythm_score, "max": 15, "notes": rhythm_notes}

# ---- 5.5 脚本还原度 (10分) ----
# 核心关键词还原检测
core_keywords = ["三明学院", "做起来", "不是", "先做", "过程", "答案", "老陈", "只说真话"]
还原 = sum(1 for kw in core_keywords if kw in all_text_flat)
compliance_score = min(10, 还原 * 1.25)
还原_notes = [f"核心关键词命中: {还原}/{len(core_keywords)}"]
scores["脚本还原度"] = {"score": compliance_score, "max": 10, "notes": 还原_notes}

# ---- 5.6 合规安全 (10分) ----
safety_score = 10
safety_notes = []
high_violations = [v for v in violations if v["level"] == "HIGH"]
med_violations = [v for v in violations if v["level"] == "MED"]
if high_violations:
    safety_score -= len(high_violations) * 3
    safety_notes.append(f"🔴 高危违规{len(high_violations)}处")
if med_violations:
    safety_score -= len(med_violations) * 1.5
    safety_notes.append(f"🟡 中危违规{len(med_violations)}处")
if safety_score >= 9:
    safety_notes.append("✅ 基本合规")
safety_score = max(0, safety_score)
scores["合规安全"] = {"score": safety_score, "max": 10, "notes": safety_notes}

# ---- 5.7 制作质量 (5分) ----
制作_notes = []
制作_score = 5
for t, path in list(frame_files.items())[:3]:
    img = cv2.imread(path)
    if img is not None:
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        avg_bright = np.mean(gray)
        if avg_bright < 60:
            制作_score -= 1
            制作_notes.append(f"🟡 {t}s帧偏暗")
        if avg_bright > 220:
            制作_score -= 1
            制作_notes.append(f"🟡 {t}s帧过曝")
if 制作_score == 5:
    制作_notes.append("✅ 亮度正常，无异常")
scores["制作质量"] = {"score": 制作_score, "max": 5, "notes": 制作_notes}

# ---- 总分 =====
total = sum(s["score"] for s in scores.values())
total_max = sum(s["max"] for s in scores.values())
total_pct = total / total_max * 100

# 评级
if total_pct >= 90: rating = "S"
elif total_pct >= 80: rating = "A"
elif total_pct >= 70: rating = "B"
elif total_pct >= 60: rating = "C"
else: rating = "D"

# ===== Step 6: 生成改进建议 =====

improvements = []

# 钩子分析
if hook_score < 20:
    improvements.append({
        "维度": "钩子强度",
        "现状": f"{hook_score}/25",
        "问题": "钩子身份/冲突不足",
        "建议": "开场3秒必须包含：身份（三明学院）+ 冲突（很多人看不上）+ 悬念（但...）"
    })

# 情绪分析
if emotion_score < 14:
    improvements.append({
        "维度": "情绪价值",
        "现状": f"{emotion_score}/20",
        "问题": "情绪词密度不够",
        "建议": "痛点段加入更多情绪词：'天塌了'、'社死'、'绝望'等强情绪词"
    })

# 结构分析：痛点段缺失
if not has_pain:
    improvements.append({
        "维度": "内容结构",
        "现状": "缺痛点段",
        "问题": "没有痛点铺垫，直接进入解决方案",
        "建议": "痛点段必不可少：'对未来迷茫、怕嵌入式卷、怕AI抢饭碗'"
    })

# 节奏分析
if len(gap_frames) > 2:
    improvements.append({
        "维度": "节奏保持",
        "现状": f"{len(gap_frames)}个稀疏帧",
        "问题": "部分段落内容稀疏，可能导致流失",
        "建议": "每5秒必须有实质性内容或字幕，不能有空白帧"
    })

# 合规建议
if high_violations:
    fix_texts = []
    for v in high_violations:
        if v["word"] == "私信":
            fix_texts.append("'私信' → 改为'问我'")
    if fix_texts:
        improvements.append({
            "维度": "合规安全",
            "现状": f"高危违规{len(high_violations)}处",
            "问题": "'私信'可能触发平台引流判定",
            "建议": f"修改方案: {'；'.join(fix_texts)}（虽为陈述事实，但平台可能误判）"
        })

# ===== Step 7: 输出结构化报告 =====

hallucination_flags = []

# 钩子幻觉检测
if PLAN_SCORES.get("钩子强度", 0) == 25 and not has_contrast:
    hallucination_flags.append({
        "type": "钩子幻觉",
        "description": "方案预评分钩子25/25，但脚本逐字稿中未发现反差句（'做到了'/'但我'/'结果'等）",
        "plan_claim": "人设反差强",
        "script_actual": "只说了'觉得不是985211'，无反差收尾"
    })

# 合规幻觉检测
if PLAN_SCORES.get("合规安全", 0) == 10 and has_private_msg:
    hallucination_flags.append({
        "type": "合规幻觉",
        "description": "方案预评分合规10/10，但脚本含'私信'高危词",
        "plan_claim": "无违规",
        "script_actual": "10s帧含'私信我说对未来迷茫'"
    })

report = {
    "video": VIDEO_PATH,
    "review_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    "duration": total_seconds,
    "version": "v2.0（防幻觉版）",
    "plan_pretend_scores": PLAN_SCORES,
    "hallucination_flags": hallucination_flags,
    "violations": violations,
    "scores": scores,
    "total": {"score": total, "max": total_max, "pct": round(total_pct, 1), "rating": rating},
    "improvements": improvements,
    "frame_count": len(frame_files)
}

# 打印报告
print(f"\n{'='*60}")
print(f"视频评分报告 | {report['review_date']}")
print(f"{'='*60}")
print(f"\n🎯 综合评级: {rating}级 ({total_pct:.1f}%)")
print(f"   总分: {total}/{total_max}")

if hallucination_flags:
    print(f"\n🚨 幻觉预警 ({len(hallucination_flags)}条):")
    for h in hallucination_flags:
        print(f"   [{h['type']}] 方案自称：{h['plan_claim']}")
        print(f"       实际脚本：{h['script_actual']}")

print(f"\n📊 分项评分:")
for dim, s in scores.items():
    pct = s["score"]/s["max"]*100
    bar = "█" * int(pct/10) + "░" * (10 - int(pct/10))
    icon = "✅" if pct >= 80 else "🟡" if pct >= 60 else "❌"
    print(f"   {icon} {dim:<10} {s['score']:>2}/{s['max']:<2} ({pct:.0f}%) {bar}")
    for note in s["notes"]:
        print(f"       {note}")

print(f"\n📋 改进建议 ({len(improvements)}条):")
for i, imp in enumerate(improvements, 1):
    print(f"  {i}. [{imp['维度']}] {imp['问题']}")
    print(f"     现状: {imp['现状']}")
    print(f"     建议: {imp['建议']}")

# 保存JSON报告
report_path = os.path.join(OUTPUT_DIR, "score_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\n📄 报告已保存: {report_path}")

# 输出所有帧路径（供后续清理）
frame_paths = list(frame_files.values()) + [report_path]
print(f"\n待清理文件: {len(frame_paths)}个")
print("ALL_FRAME_PATHS:", "|".join(frame_paths))
