#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from datetime import datetime

# 读取产品创意数据
with open('weibo_ideas_20260104_205541.json', 'r', encoding='utf-8') as f:
    hotspots_data = json.load(f)

# 准备数据
report_data = {
    "date": datetime.now().strftime('%Y-%m-%d'),
    "time": datetime.now().strftime('%H:%M:%S'),
    "total_count": len(hotspots_data),
    "hotspots": hotspots_data
}

# 统计所有创意
all_ideas = []
for h in hotspots_data:
    for idea in h['ideas']:
        idea['source_hotword'] = h['hotword']
        idea['source_rank'] = h['rank']
        all_ideas.append(idea)

# 按评分排序
all_ideas_sorted = sorted(all_ideas, key=lambda x: x['total_score'], reverse=True)

# 生成HTML内容
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>微博热搜产品创意分析报告 - {report_data['date']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .meta {{
            font-size: 1.1em;
            opacity: 0.95;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
        }}

        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #FF6B35;
            margin-bottom: 5px;
        }}

        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
        }}

        .section {{
            padding: 40px;
        }}

        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #FF6B35;
        }}

        .hotspot-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border-left: 5px solid #FF6B35;
        }}

        .hotspot-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .hotspot-rank {{
            background: #FF6B35;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .hotword {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
            flex: 1;
            margin-left: 15px;
        }}

        .hot-info {{
            display: flex;
            gap: 15px;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}

        .tag {{
            background: #e9ecef;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.85em;
        }}

        .tag.new {{
            background: #28a745;
            color: white;
        }}

        .tag.hot {{
            background: #FF6B35;
            color: white;
        }}

        .background {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            color: #555;
            line-height: 1.8;
        }}

        .idea-list {{
            display: grid;
            gap: 15px;
        }}

        .idea-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e9ecef;
            transition: all 0.3s;
        }}

        .idea-card:hover {{
            border-color: #FF6B35;
            box-shadow: 0 4px 12px rgba(255,107,53,0.2);
        }}

        .idea-card.excellent {{
            border-color: #FFD700;
            background: linear-gradient(135deg, #fffdf0 0%, #ffffff 100%);
        }}

        .idea-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .idea-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #FF6B35;
        }}

        .idea-score {{
            font-size: 1.5em;
            font-weight: bold;
            color: #FF6B35;
        }}

        .idea-score.excellent {{
            color: #FFD700;
        }}

        .idea-score.good {{
            color: #28a745;
        }}

        .idea-features {{
            margin: 12px 0;
        }}

        .idea-features h4 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 8px;
        }}

        .idea-features ul {{
            list-style: none;
            padding-left: 0;
        }}

        .idea-features li {{
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
            color: #555;
        }}

        .idea-features li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #FF6B35;
            font-weight: bold;
        }}

        .idea-target {{
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 6px;
            margin-top: 12px;
            font-size: 0.9em;
            color: #666;
        }}

        .idea-target strong {{
            color: #333;
        }}

        .ranking {{
            padding: 40px;
            background: #f8f9fa;
        }}

        .ranking-item {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .ranking-number {{
            font-size: 2em;
            font-weight: bold;
            color: #FF6B35;
            min-width: 50px;
        }}

        .ranking-info {{
            flex: 1;
        }}

        .ranking-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .ranking-source {{
            color: #666;
            font-size: 0.9em;
        }}

        .ranking-score {{
            font-size: 2em;
            font-weight: bold;
            color: #FF6B35;
        }}

        .footer {{
            background: #333;
            color: white;
            padding: 30px;
            text-align: center;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .section {{
                padding: 20px;
            }}

            .hotspot-header {{
                flex-direction: column;
                align-items: flex-start;
            }}

            .hotword {{
                margin-left: 0;
                margin-top: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 微博热搜产品创意分析报告</h1>
            <div class="meta">
                📅 {report_data['date']} | 🕐 {report_data['time']} | 🔥 分析TOP{report_data['total_count']}热搜
            </div>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="number">{report_data['total_count']}</div>
                <div class="label">分析热搜数</div>
            </div>
            <div class="stat-card">
                <div class="number">{len(all_ideas)}</div>
                <div class="label">生成创意数</div>
            </div>
            <div class="stat-card">
                <div class="number">{len([i for i in all_ideas if i['total_score'] > 80])}</div>
                <div class="label">优秀创意(>80分)</div>
            </div>
            <div class="stat-card">
                <div class="number">{sum(i['total_score'] for i in all_ideas) / len(all_ideas):.1f}</div>
                <div class="label">平均评分</div>
            </div>
        </div>

        <div class="section">
            <h2 class="section-title">🔥 TOP10热搜详细分析</h2>
"""

# 添加每个热搜的详细分析
for hotspot in hotspots_data:
    score_class = "excellent" if hotspot['ideas'][0]['total_score'] > 80 else ""
    tag_class = ""
    if hotspot.get('hot_tag') == '新':
        tag_class = "new"
    elif hotspot.get('hot_tag') == '沸':
        tag_class = "hot"

    tag_html = f'<span class="tag {tag_class}">{hotspot["hot_tag"]}</span>' if hotspot.get('hot_tag') else ''
    category_html = f'<span class="tag">{hotspot["category"]}</span>'

    html_content += f"""
            <div class="hotspot-item">
                <div class="hotspot-header">
                    <div class="hotspot-rank">{hotspot['rank']}</div>
                    <div class="hotword">{hotspot['hotword']}</div>
                </div>
                <div class="hot-info">
                    <span>🔥 热度: {hotspot['hotword_num']}</span>
                    {tag_html}
                    {category_html}
                </div>
                <div class="background">
                    <strong>📝 事件背景：</strong>{hotspot['background']}
                </div>
                <div class="idea-list">
    """

    for idea in hotspot['ideas']:
        idea_score_class = "excellent" if idea['total_score'] > 80 else ("good" if idea['total_score'] >= 60 else "")
        features_html = "".join(f'<li>{feature}</li>' for feature in idea['features'])

        html_content += f"""
                    <div class="idea-card {idea_score_class}">
                        <div class="idea-header">
                            <div class="idea-name">💡 {idea['name']}</div>
                            <div class="idea-score {idea_score_class}">{idea['total_score']}分</div>
                        </div>
                        <div class="idea-features">
                            <h4>核心功能：</h4>
                            <ul>
                                {features_html}
                            </ul>
                        </div>
                        <div class="idea-target">
                            <strong>👥 目标用户：</strong>{idea['target_users']}
                        </div>
                        <div class="idea-target">
                            <strong>📊 评分分解：</strong>有趣度 {idea['fun_score']}分 × 80% + 有用度 {idea['useful_score']}分 × 20%
                        </div>
                    </div>
        """

    html_content += """
                </div>
            </div>
    """

# 添加TOP10创意排行
html_content += """
        </div>

        <div class="ranking">
            <h2 class="section-title">🏆 TOP10产品创意排行</h2>
"""

for i, idea in enumerate(all_ideas_sorted[:10], 1):
    score_class = "excellent" if idea['total_score'] > 80 else ("good" if idea['total_score'] >= 60 else "")
    html_content += f"""
            <div class="ranking-item">
                <div class="ranking-number">#{i}</div>
                <div class="ranking-info">
                    <div class="ranking-name">{idea['name']}</div>
                    <div class="ranking-source">来源: #{idea['source_rank']} {idea['source_hotword']}</div>
                </div>
                <div class="ranking-score {score_class}">{idea['total_score']}分</div>
            </div>
    """

# 添加页脚
html_content += f"""
        </div>

        <div class="footer">
            <p>📊 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>💡 本报告由AI自动生成，基于微博热搜实时数据与智能分析</p>
            <p style="margin-top: 10px; opacity: 0.7;">Powered by 微博热搜智能分析系统</p>
        </div>
    </div>
</body>
</html>
"""

# 保存HTML文件
output_filename = f"weibo_hotspot_report_{datetime.now().strftime('%Y-%m-%d')}.html"
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ HTML报告生成成功！")
print(f"📄 文件名: {output_filename}")
print(f"📏 文件大小: {len(html_content)} 字符")
print(f"\n📊 报告包含:")
print(f"   • {len(hotspots_data)} 个热搜详细分析")
print(f"   • {len(all_ideas)} 个产品创意")
print(f"   • TOP10创意排行榜")
print(f"\n💡 提示: 可以直接在浏览器中打开查看")
