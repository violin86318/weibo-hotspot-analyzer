# 微博热搜产品创意分析器

[![GitHub Actions](https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer/actions/workflows/weibo-daily.yml/badge.svg)](https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer/actions/workflows/weibo-daily.yml)

## 功能概述

这是一个自动化的微博热搜分析工具，能够：

- 🔥 **实时抓取**：通过天聚数行 API 获取微博热搜 TOP50
- 🤖 **AI 分析**：利用 Claude API 生成产品创意
- 📊 **可视化报告**：生成精美的 HTML 分析报告
- ⏰ **自动化执行**：每天定时运行并提交到 GitHub

## 技术栈

- **Python 3.11+**
- **Anthropic Claude API** (AI 分析)
- **天聚数行 API** (微博热搜数据)
- **GitHub Actions** (自动化 CI/CD)

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer.git
cd weibo-hotspot-analyzer
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install anthropic
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# 天聚数行 API 密钥
TIANAPI_KEY=your_api_key_here

# Claude API 密钥
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

### 4. 运行分析

```bash
# 抓取热搜数据
python scripts/fetch_weibo_hot.py

# Claude AI 分析
python scripts/claude_analysis.py

# 生成 HTML 报告
python scripts/generate_html_report.py
```

## GitHub Actions 自动化

### 配置 Secrets

在 GitHub 仓库设置中添加以下 Secrets：

1. 访问 **Settings** → **Secrets and variables** → **Actions**
2. 添加以下 secrets：

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `TIANAPI_KEY` | 天聚数行 API 密钥 | [tianapi.com](https://www.tianapi.com/) |
| `ANTHROPIC_API_KEY` | Claude API 密钥 | [console.anthropic.com](https://console.anthropic.com/) |

### 执行时间

- **默认时间**：每天 22:00 (北京时间)
- **手动触发**：在 Actions 页面点击 "Run workflow"

### 查看报告

生成的报告会保存在 `reports/YYYY/MM/` 目录下。

例如：`reports/2026/01/2026-01-18_weibo_hotspot_report.html`

## 项目结构

```
weibo-hotspot-analyzer/
├── .github/
│   └── workflows/
│       └── weibo-daily.yml      # GitHub Actions 配置
├── scripts/
│   ├── fetch_weibo_hot.py       # 热搜数据抓取
│   ├── claude_analysis.py       # Claude AI 分析
│   └── generate_html_report.py  # HTML 报告生成
├── templates/
│   └── report_template.html     # 报告模板
├── reports/                     # 生成的报告
│   └── 2026/01/
│       └── 2026-01-18_weibo_hotspot_report.html
├── logs/                        # 日志文件
├── .gitignore
├── README.md
└── requirements.txt
```

## 评分体系

产品创意采用**有趣度 80% + 有用度 20%** 的评分标准：

### 有趣度 (80%)
- 创意新颖性 (25分)
- 话题热度 (25分)
- 用户参与度 (20分)
- 传播潜力 (30分)

### 有用度 (20%)
- 实用价值 (8分)
- 需求强度 (7分)
- 市场痛点 (5分)

### 等级划分
- **优秀** (>80分)：金黄色，高有趣度+高实用价值
- **良好** (60-80分)：绿色，有潜力可考虑
- **普通** (<60分)：灰色，需要优化

## 本地开发

### 安装 Python 虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 运行测试

```bash
# 测试热搜抓取
python scripts/fetch_weibo_hot.py

# 测试 Claude 分析（需要 API Key）
export ANTHROPIC_API_KEY='your-key'
python scripts/claude_analysis.py
```

## API 限制

| 服务 | 免费额度 | 付费方案 |
|-----|---------|---------|
| 天聚数行 | 100次/天 | ¥20-65/月 |
| Claude API | 按 token 计费 | 约 $2-5/月 |
| GitHub Actions | 2000分钟/月 | 付费套餐 |

## 常见问题

### Q1: Claude API 调用失败？

**A**: 检查以下几点：
1. API 密钥是否正确
2. 账户是否有足够额度
3. 网络连接是否正常
4. 模型名称是否正确

### Q2: 报告没有生成？

**A**:
1. 检查 GitHub Actions 日志
2. 确认所有步骤都成功执行
3. 查看是否有错误信息

### Q3: 如何调整执行时间？

**A**: 修改 `.github/workflows/weibo-daily.yml` 中的 cron 表达式：

```yaml
schedule:
  # 每天 UTC 时间 14:00 (北京时间 22:00)
  - cron: '0 14 * * *'
```

Cron 格式：`分 时 日 月 周`

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- GitHub Issues: [提交问题](https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer/issues)
- Email: your@email.com

---

**生成时间**: 2026-01-18
**版本**: v2.0.0
