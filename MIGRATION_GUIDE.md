# GitHub Actions 迁移指南

本文档指导如何将微博热搜分析器迁移到 GitHub Actions。

## 前置准备

### 1. 创建 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库: weibo-hotspot-analyzer
# 访问: https://github.com/new
```

### 2. 配置 GitHub Secrets

在仓库页面设置以下 Secrets：

**路径**: Settings → Secrets and variables → Actions

| Secret 名称 | 值 | 获取方式 |
|------------|---|---------|
| `TIANAPI_KEY` | `your-tianapi-key` | [tianapi.com](https://www.tianapi.com/) |
| `ANTHROPIC_API_KEY` | `sk-ant-xxx` | [console.anthropic.com](https://console.anthropic.com/) |

### 3. 推送代码到 GitHub

```bash
cd /tmp/weibo-hotspot-analyzer

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer.git

# 提交代码
git add .
git commit -m "Initial commit: 微博热搜分析器"

# 推送
git branch -M main
git push -u origin main
```

### 4. 测试 Workflow

1. 访问 Actions 页面: `https://github.com/YOUR_USERNAME/weibo-hotspot-analyzer/actions`
2. 点击 "weibo-daily" workflow
3. 点击 "Run workflow" 按钮手动触发
4. 查看执行日志

### 5. 查看生成的报告

报告会保存在仓库的 `reports/YYYY/MM/` 目录下。

## 目录结构

```
weibo-hotspot-analyzer/
├── .github/
│   └── workflows/
│       └── weibo-daily.yml      # GitHub Actions 配置
├── scripts/
│   ├── fetch_weibo_hot.py       # 热搜抓取 (v2)
│   ├── claude_analysis.py       # Claude 分析 (新增)
│   └── generate_html_report.py  # 报告生成 (v2)
├── reports/                     # 生成的报告
│   └── 2026/01/
│       └── 2026-01-18_weibo_hotspot_report.html
├── .gitignore
├── requirements.txt
└── README_GITHUB.md
```

## 本地测试

在推送前，可以先本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export TIANAPI_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'

# 运行测试
python scripts/fetch_weibo_hot.py
python scripts/claude_analysis.py
python scripts/generate_html_report.py
```

## 常见问题

### Q1: Workflow 执行失败？

**A**: 检查以下几点：
1. Secrets 是否正确配置
2. 脚本是否有执行权限
3. Python 版本是否兼容
4. 查看日志中的具体错误信息

### Q2: 如何修改执行时间？

**A**: 编辑 `.github/workflows/weibo-daily.yml`:

```yaml
schedule:
  # 每天 UTC 14:00 (北京时间 22:00)
  - cron: '0 14 * * *'
```

### Q3: 如何停止自动执行？

**A**: 有两种方法：
1. 删除或禁用 workflow 文件
2. 在 workflow 文件中注释掉 `schedule` 部分

## 成本估算

| 服务 | 免费额度 | 预计成本 |
|-----|---------|---------|
| GitHub Actions | 2000分钟/月 | 免费 |
| 天聚数行 API | 100次/天 | 免费 |
| Claude API | - | $2-5/月 |

**总计**: 约 $2-5/月

## 下一步

1. ✅ 推送代码到 GitHub
2. ✅ 配置 Secrets
3. ✅ 测试 Workflow
4. ✅ 查看生成的报告
5. ✅ 根据需要调整配置

---

**生成时间**: 2026-01-18
**版本**: v1.0.0
