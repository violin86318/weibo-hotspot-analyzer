#!/usr/bin/env python3
"""生成历史报告列表页面"""

import os
from pathlib import Path
from datetime import datetime

def generate_reports_list():
    """生成报告列表 HTML 页面"""
    
    pages_dir = Path("pages")
    
    # HTML 头部
    html_header = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析报告 - 历史报告</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #FF6B35, #FF8C42);
            color: #2D3142;
            line-height: 1.6;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 40px;
            border-radius: 16px;
            margin-bottom: 32px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
        }
        .header h1 {
            font-size: 32px;
            margin-bottom: 16px;
            color: #FF6B35;
        }
        .header p {
            font-size: 16px;
            color: #666;
        }
        .reports-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }
        .report-card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .report-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }
        .report-card h3 {
            color: #FF6B35;
            margin-bottom: 12px;
            font-size: 18px;
        }
        .report-card a {
            display: inline-block;
            margin-top: 12px;
            padding: 8px 16px;
            background: #FF6B35;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 14px;
        }
        .report-card a:hover {
            background: #FF8C42;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            color: white;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 微博热搜产品创意分析报告</h1>
            <p>历史报告列表 - 每日自动更新</p>
        </div>
        <div class="reports-grid">
"""

    # 查找所有报告文件
    report_files = []
    for html_file in pages_dir.rglob("*.html"):
        if html_file.name not in ["index.html", "reports.html"]:
            relative_path = html_file.relative_to(pages_dir)
            # 从文件名提取日期
            filename = html_file.stem
            date_str = filename.replace("_weibo_hotspot_report", "")
            report_files.append((date_str, str(relative_path)))
    
    # 按日期倒序排序
    report_files.sort(reverse=True, key=lambda x: x[0])
    
    # 只保留最近30个报告
    report_files = report_files[:30]
    
    # 生成报告卡片
    cards_html = ""
    for date_str, relative_path in report_files:
        cards_html += f"""            <div class="report-card">
                <h3>📅 {date_str}</h3>
                <p>微博热搜产品创意分析报告</p>
                <a href="{relative_path}">查看报告 →</a>
            </div>
"""
    
    # HTML 尾部
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_footer = f"""        </div>
        <div class="footer">
            <p>自动生成时间: {current_time}</p>
            <p>Powered by Claude AI & GitHub Actions</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 写入文件
    output_file = pages_dir / "reports.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_header)
        f.write(cards_html)
        f.write(html_footer)
    
    print(f"✅ 已生成报告列表页面: {output_file}")
    print(f"   共找到 {len(report_files)} 个历史报告")

if __name__ == "__main__":
    generate_reports_list()
