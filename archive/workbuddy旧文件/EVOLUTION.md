# 进化协议

## 核心理念
- 固定文件只增不覆盖，jsonl每行一条，对话闭环后追加
- 每次启动只读 INDEX.md（<5KB），不读全量历史
- 用户纠正自动捕获 → corrections.jsonl → 更新 INDEX.md摘要

## 三步闭环

### Step 1 — 对话开始（读）
读取 INDEX.md + corrections.jsonl + best_practices.jsonl + errors.jsonl 全部内容

### Step 2 — 对话中（捕获）
- 捕获用户纠正 → 追加到 corrections.jsonl（一行JSON）
- 捕获验证有效的方法 → 追加到 best_practices.jsonl
- 捕获执行错误 → 追加到 errors.jsonl

### Step 3 — 对话结束（写）
- 更新 INDEX.md corrections/best_practices/errors 摘要区（保留最新5/3/3条）

## jsonl 格式规范

### corrections.jsonl
```
{"ts":"YYYY-MM-DD","type":"correction","topic":"主题","wrong":"错误做法","correct":"正确做法","source":"来源"}
```

### best_practices.jsonl
```
{"ts":"YYYY-MM-DD","type":"best_practice","topic":"主题","content":"具体做法","source":"来源"}
```

### errors.jsonl
```
{"ts":"YYYY-MM-DD","type":"error","topic":"主题","error":"错误描述","fix":"修复方法"}
```

## 隐私隔离
- 全局 C:\Users\86151\.workbuddy\ = 通用配置，无私人信息
- 本任务 C:\Users\86151\WorkBuddy\20260411163952\.workbuddy\ = 完整数据
