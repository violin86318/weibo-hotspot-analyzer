#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Claude Agent SDK 分析微博热搜并生成产品创意

功能：
- 读取微博热搜数据
- 调用 Claude API 生成产品创意
- 保存结构化创意数据

用法：
python claude_analysis.py

环境变量：
- ANTHROPIC_API_KEY: Claude API 密钥（必需）

作者：
Claude Code Skill Generator

版本：
v2.0.0 (2026-01-18) - GitHub Actions 迁移版本
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List

try:
    from anthropic import Anthropic
except ImportError:
    print("错误: 未安装 anthropic 库")
    print("请运行: pip install anthropic")
    sys.exit(1)


class ClaudeHotspotAnalyzer:
    """基于 Claude 的微博热搜创意分析器"""

    def __init__(self, api_key: str):
        """
        初始化分析器

        Args:
            api_key: Anthropic API 密钥
        """
        if not api_key:
            raise ValueError("未提供 ANTHROPIC_API_KEY")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def find_latest_hotspot_data(self) -> str:
        """
        查找最新的热搜数据文件

        Returns:
            最新 JSON 文件的路径

        Raises:
            FileNotFoundError: 未找到热搜数据文件
        """
        import glob

        json_files = glob.glob('weibo_hotspots_*.json')

        if not json_files:
            raise FileNotFoundError("未找到热搜数据文件，请先运行 fetch_weibo_hot.py")

        # 返回最新修改的文件
        return max(json_files, key=os.path.getctime)

    def load_hotspots(self, filepath: str, limit: int = 10) -> List[Dict]:
        """
        加载热搜数据

        Args:
            filepath: JSON 文件路径
            limit: 分析的热搜数量限制

        Returns:
            热搜数据列表
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hotspots = data.get('data', [])[:limit]

        if not hotspots:
            raise ValueError("热搜数据为空")

        return hotspots

    def create_analysis_prompt(self, hotspot: Dict) -> str:
        """
        创建分析提示词

        Args:
            hotspot: 热搜数据字典

        Returns:
            完整的提示词字符串
        """
        hotword = hotspot['hotword']
        hotness = hotspot['hotword_num_int']

        prompt = f"""你是一位资深产品经理，擅长发现热点背后的产品机会。

请基于以下微博热搜话题，生成 3 个产品创意。

## 热搜信息
- **话题**: {hotword}
- **热度指数**: {hotness:,}

## 评分标准
1. **有趣度 (80%权重)**: 创意新颖性、话题热度、用户参与度、传播潜力
2. **有用度 (20%权重)**: 实用价值、需求强度、市场痛点解决程度

## 输出要求
为每个创意提供以下信息：
1. **产品名称**: 简洁易记，体现热点元素 (2-8个字)
2. **综合评分**: 0-100分 (有趣度×0.8 + 有用度×0.2)
3. **有趣度评分**: 0-100分
4. **有用度评分**: 0-100分
5. **核心功能**: 3-5个关键功能点
6. **目标用户**: 用户画像描述 (年龄、兴趣、需求场景)
7. **产品描述**: 100字以内的简洁描述

## 输出格式
请**只返回 JSON 格式**，不要包含其他解释文字：

```json
{{
  "ideas": [
    {{
      "name": "产品名称",
      "score": 85,
      "fun_score": 82,
      "use_score": 88,
      "features": ["功能1", "功能2", "功能3"],
      "target_users": "25-35岁职场人士，需要...",
      "description": "基于热搜话题的..."
    }},
    {{
      "name": "产品名称2",
      "score": 78,
      "fun_score": 80,
      "use_score": 72,
      "features": ["功能1", "功能2", "功能3"],
      "target_users": "18-25岁大学生，喜欢...",
      "description": "利用热点趋势的..."
    }},
    {{
      "name": "产品名称3",
      "score": 72,
      "fun_score": 75,
      "use_score": 65,
      "features": ["功能1", "功能2", "功能3"],
      "target_users": "目标用户群体",
      "description": "产品描述"
    }}
  ]
}}
```

请开始分析。"""

        return prompt

    def analyze_hotspot(self, hotspot: Dict) -> List[Dict]:
        """
        分析单个热搜并生成创意

        Args:
            hotspot: 热搜数据字典

        Returns:
            产品创意列表
        """
        hotword = hotspot['hotword']
        hotness = hotspot['hotword_num_int']
        rank = hotspot.get('rank', '?')

        try:
            # 创建提示词
            prompt = self.create_analysis_prompt(hotspot)

            # 调用 Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # 提取响应内容
            content = response.content[0].text

            # 解析 JSON 响应
            ideas = self.parse_claude_response(content)

            # 为每个创意添加热搜关联信息
            for idea in ideas:
                idea['hotword'] = hotword
                idea['hotness'] = hotness
                idea['rank'] = rank

            return ideas

        except Exception as e:
            print(f"  ❌ 分析失败: {str(e)}")
            # 返回一个失败占位符
            return [{
                "hotword": hotword,
                "hotness": hotness,
                "rank": rank,
                "name": f"「{hotword}」分析失败",
                "score": 0,
                "fun_score": 0,
                "use_score": 0,
                "features": [f"错误: {str(e)}"],
                "target_users": "无法生成",
                "description": f"Claude API 调用失败: {str(e)}"
            }]

    def parse_claude_response(self, content: str) -> List[Dict]:
        """
        解析 Claude 响应，提取 JSON 数据

        Args:
            content: Claude 返回的文本内容

        Returns:
            创意列表

        Raises:
            ValueError: 无法解析 JSON
        """
        # 尝试直接解析
        try:
            data = json.loads(content)
            return data.get('ideas', [])
        except json.JSONDecodeError:
            pass

        # 尝试提取 JSON 代码块
        json_match = re.search(r'```json\s*(\{[\s\S]*?\})\s*```', content)
        if not json_match:
            json_match = re.search(r'```\s*(\{[\s\S]*?\})\s*```', content)
        if not json_match:
            json_match = re.search(r'\{[\s\S]*"ideas"[\s\S]*\}', content)

        if json_match:
            try:
                json_str = json_match.group(1) if json_match.lastindex else json_match.group(0)
                data = json.loads(json_str)
                return data.get('ideas', [])
            except json.JSONDecodeError as e:
                raise ValueError(f"无法解析 Claude 返回的 JSON: {str(e)}")

        raise ValueError("Claude 响应中未找到有效的 JSON 数据")

    def analyze_batch(self, hotspots: List[Dict]) -> List[Dict]:
        """
        批量分析热搜

        Args:
            hotspots: 热搜数据列表

        Returns:
            所有创意列表
        """
        all_ideas = []
        total = len(hotspots)

        print(f"\n🤖 开始分析 {total} 个热搜话题")
        print("=" * 60)

        for idx, hotspot in enumerate(hotspots, 1):
            hotword = hotspot['hotword']
            print(f"\n[{idx}/{total}] 分析: {hotword}")

            ideas = self.analyze_hotspot(hotspot)

            if ideas and ideas[0]['score'] > 0:
                print(f"  ✅ 成功生成 {len(ideas)} 个创意")
                for idea in ideas:
                    print(f"     - {idea['name']} ({idea['score']}分)")
            else:
                print(f"  ⚠️  分析失败")

            all_ideas.extend(ideas)

        return all_ideas

    def save_ideas(self, ideas: List[Dict], output_file: str = None):
        """
        保存创意数据到文件

        Args:
            ideas: 创意列表
            output_file: 输出文件路径（可选）
        """
        if output_file is None:
            output_file = f"weibo_ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # 统计信息
        total = len(ideas)
        successful = len([i for i in ideas if i['score'] > 0])
        excellent = len([i for i in ideas if i['score'] > 80])
        good = len([i for i in ideas if 60 <= i['score'] <= 80])

        output_data = {
            'generate_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': {
                'total': total,
                'successful': successful,
                'excellent': excellent,
                'good': good,
                'avg_score': sum(i['score'] for i in ideas if i['score'] > 0) / max(successful, 1)
            },
            'ideas': ideas
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 创意数据已保存: {output_file}")

        # 打印统计信息
        stats = output_data['statistics']
        print(f"\n📊 统计信息:")
        print(f"   总创意数: {stats['total']}")
        print(f"   成功生成: {stats['successful']}")
        print(f"   优秀(>80): {stats['excellent']}")
        print(f"   良好(60-80): {stats['good']}")
        print(f"   平均分: {stats['avg_score']:.1f}")


def main():
    """主函数"""
    print("=" * 60)
    print("微博热搜创意分析器 (Claude Edition)")
    print("=" * 60)

    # 检查 API 密钥
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ 错误: 未设置 ANTHROPIC_API_KEY 环境变量")
        print("\n请在运行前设置环境变量:")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        print("\n或在 GitHub Secrets 中配置:")
        print("  ANTHROPIC_API_KEY = sk-ant-xxx...")
        sys.exit(1)

    try:
        # 创建分析器
        analyzer = ClaudeHotspotAnalyzer(api_key)

        # 查找最新数据
        print("\n📂 查找热搜数据文件...")
        hotspot_file = analyzer.find_latest_hotspot_data()
        print(f"✅ 找到文件: {hotspot_file}")

        # 加载热搜数据
        print("\n📊 加载热搜数据...")
        hotspots = analyzer.load_hotspots(hotspot_file, limit=10)
        print(f"✅ 加载 {len(hotspots)} 个热搜话题")

        # 批量分析
        ideas = analyzer.analyze_batch(hotspots)

        # 保存结果
        print("\n" + "=" * 60)
        analyzer.save_ideas(ideas)

        # 返回最新的 JSON 文件名，供后续脚本使用
        latest_ideas = max([f for f in os.listdir('.') if f.startswith('weibo_ideas_')])
        with open('.latest_ideas', 'w') as f:
            f.write(latest_ideas)

        print("\n✅ 分析完成!")
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ 错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
