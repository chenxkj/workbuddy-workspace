"""
老陈说AI · 账号数据自动化记录工具
用途：录入每期视频数据，自动计算关键指标，生成复盘建议
"""

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime
import os

# 路径配置
DATA_DIR = r"c:\Users\86151\WorkBuddy\20260411163952\抖音账号运营模板包\05_数据记录"
DATA_FILE = os.path.join(DATA_DIR, "账号数据汇总.xlsx")

# 样式定义
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill("solid", fgColor="2F5496")
GOOD_FILL = PatternFill("solid", fgColor="C6EFCE")  # 绿色-达标
BAD_FILL = PatternFill("solid", fgColor="FFC7CE")   # 红色-不达标
WARN_FILL = PatternFill("solid", fgColor="FFEB9C")  # 黄色-警告
THIN_BORDER = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)


def create_new_workbook():
    """创建新的数据记录工作簿"""
    wb = Workbook()

    # Sheet1: 数据总览
    ws1 = wb.active
    ws1.title = "数据总览"

    # 表头
    headers = ["期次", "主题", "发布日期", "播放量", "完播率", "2s跳出率",
               "点赞率", "评论率", "涨粉", "评级", "状态"]
    ws1.append(headers)

    # 格式化表头
    for col, header in enumerate(headers, 1):
        cell = ws1.cell(row=1, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = THIN_BORDER

    # 预设数据样例
    sample_data = [
        ["第1期", "42岁研发总监的转型焦虑", "2026-04-14", 26000, "4.45%", "36.13%", "1.43%", "0.2%", 194, "B+", ""],
        ["第7期", "AI骂完养虾做运营总监", "2026-04-14", 519, "3.71%", "23.79%", "2.12%", "1.35%", 0, "C", ""],
        ["第11期", "天塌了！被同事刷到抖音", "2026-04-17", 1123, "13.98%", "26.71%", "1.69%", "0.53%", 7, "B", ""],
        ["第18期", "真实自我vs AI数据焦虑", "2026-04-20", 264, "5.79%", "39.1%", "2.27%", "0.76%", 0, "C", ""],
    ]

    for row_data in sample_data:
        ws1.append(row_data)

    # 设置列宽
    column_widths = [8, 30, 12, 10, 10, 10, 10, 10, 8, 8, 15]
    for i, width in enumerate(column_widths, 1):
        ws1.column_dimensions[get_column_letter(i)].width = width

    # Sheet2: 规律总结
    ws2 = wb.create_sheet("规律总结")

    ws2.append(["指标", "达标线", "优秀线", "说明"])
    rules = [
        ["完播率", "≥10%", "≥35%", "30秒视频基准"],
        ["2s跳出率", "≤30%", "≤25%", "越低越好，但老陈人设可偏高"],
        ["点赞率", "≥1.5%", "≥3%", ""],
        ["评论率", "≥0.5%", "≥1%", ""],
        ["涨粉率", "≥0.5%", "≥1%", ""],
    ]

    for row_data in rules:
        ws2.append(row_data)

    # 格式化
    for col in range(1, 5):
        cell = ws2.cell(row=1, column=col)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.border = THIN_BORDER

    # Sheet3: 待拍摄计划
    ws3 = wb.create_sheet("待拍摄计划")

    ws3.append(["期次", "主题", "优先级", "状态", "备注"])
    plans = [
        ["第13期", "我把AI逼到说实话", "P1", "待拍摄", ""],
        ["第14期", "想让AI不说废话", "P1", "待拍摄", ""],
        ["第19期", "一条笑话悟出老子哲学", "P2", "待拍摄", ""],
        ["第20期", "图文系列：抖音踩坑实录", "P2", "待拍摄", ""],
        ["第21期", "向288位股东汇报", "P1", "待拍摄", ""],
    ]

    for row_data in plans:
        ws3.append(row_data)

    # 设置列宽
    ws3.column_dimensions['A'].width = 10
    ws3.column_dimensions['B'].width = 25
    ws3.column_dimensions['C'].width = 10
    ws3.column_dimensions['D'].width = 12
    ws3.column_dimensions['E'].width = 30

    wb.save(DATA_FILE)
    print(f"[OK] 数据文件已创建: {DATA_FILE}")
    return DATA_FILE


def add_new_episode(episode_num, theme, publish_date=None, views=0,
                    completion_rate=0, bounce_2s=0, like_rate=0,
                    comment_rate=0, followers=0, rating="", status=""):
    """添加新一期数据"""
    if not os.path.exists(DATA_FILE):
        create_new_workbook()

    wb = load_workbook(DATA_FILE)
    ws = wb["数据总览"]

    # 找到下一个空行
    next_row = ws.max_row + 1

    # 转换百分比
    def fmt_pct(val):
        if isinstance(val, str) and '%' in val:
            return val
        return f"{val}%"

    ws.cell(row=next_row, column=1, value=f"第{episode_num}期")
    ws.cell(row=next_row, column=2, value=theme)
    ws.cell(row=next_row, column=3, value=publish_date or datetime.now().strftime("%Y-%m-%d"))
    ws.cell(row=next_row, column=4, value=views)
    ws.cell(row=next_row, column=5, value=fmt_pct(completion_rate))
    ws.cell(row=next_row, column=6, value=fmt_pct(bounce_2s))
    ws.cell(row=next_row, column=7, value=fmt_pct(like_rate))
    ws.cell(row=next_row, column=8, value=fmt_pct(comment_rate))
    ws.cell(row=next_row, column=9, value=followers)
    ws.cell(row=next_row, column=10, value=rating)
    ws.cell(row=next_row, column=11, value=status)

    wb.save(DATA_FILE)
    print(f"[OK] 第{episode_num}期数据已添加")


def update_episode_status(episode_num, status):
    """更新期次状态"""
    if not os.path.exists(DATA_FILE):
        print("[X] 数据文件不存在")
        return

    wb = load_workbook(DATA_FILE)
    ws = wb["数据总览"]

    for row in range(2, ws.max_row + 1):
        cell_val = ws.cell(row=row, column=1).value
        if cell_val and f"第{episode_num}期" in str(cell_val):
            ws.cell(row=row, column=11, value=status)
            wb.save(DATA_FILE)
            print(f"[OK] 第{episode_num}期状态已更新为: {status}")
            return

    print(f"[X] 未找到第{episode_num}期")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("老陈说AI · 数据记录工具")
        print("=" * 40)
        print("用法:")
        print("  python 账号数据自动化.py create    # 创建新文件")
        print("  python 账号数据自动化.py add [参数] # 添加数据")
        print("  python 账号数据自动化.py update [参数] # 更新状态")
        print("\n添加数据示例:")
        print('  python 账号数据自动化.py add 19 "一条笑话悟出老子哲学" 2026-04-21 1500 8.5 25 2.1 0.8 15 B+ ""')
        print("\n更新状态示例:")
        print('  python 账号数据自动化.py update 19 "已发布"')
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "create":
        create_new_workbook()

    elif cmd == "add":
        # python 账号数据自动化.py add 期次 主题 日期 播放 完播 2s跳出 点赞 评论 涨粉 评级 状态
        if len(sys.argv) < 12:
            print("[X] 参数不足")
            sys.exit(1)
        add_new_episode(
            sys.argv[2], sys.argv[3], sys.argv[4],
            int(sys.argv[5]), sys.argv[6], sys.argv[7],
            sys.argv[8], sys.argv[9], int(sys.argv[10]),
            sys.argv[11], sys.argv[12] if len(sys.argv) > 12 else ""
        )

    elif cmd == "update":
        # python 账号数据自动化.py update 期次 状态
        if len(sys.argv) < 4:
            print("[X] 参数不足")
            sys.exit(1)
        update_episode_status(sys.argv[2], sys.argv[3])

    else:
        print(f"❌ 未知命令: {cmd}")
