---
name: self-improving-trigger
enabled: true
event: prompt
pattern: "错了|不对|不是这样|怎么会|说过了|之前说过|我没让你|不要|禁止|别|停止"
action: warn
---

<user-correction-detected>

老陈发出了纠正信号。按铁律，必须立即执行自学习流程：

1. **识别**：老陈原话 vs AI错误输出的具体差异
2. **分析**：根因是什么（为什么错）
3. **固化**：调用 self-improving-agent skill 记录到 corrections.jsonl
4. **确认**：告知老陈改进内容和固化位置

**立即加载 self-improving-agent skill 执行。**

</user-correction-detected>
