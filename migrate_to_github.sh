#!/bin/bash
# 微博热搜分析器 - GitHub Actions 迁移脚本
#
# 功能：
# 1. 复制 skill 到独立目录
# 2. 初始化 Git 仓库
# 3. 创建必要的配置文件
#
# 用法：
#   bash migrate_to_github.sh
#
# 版本：v1.0.0 (2026-01-18)

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
SOURCE_DIR="/Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping/.claude/skills/weibo_hotspot_analyzer"
TARGET_DIR="/tmp/weibo-hotspot-analyzer"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}微博热搜分析器 - GitHub 迁移工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查源目录
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}❌ 错误: 源目录不存在${NC}"
    echo "路径: $SOURCE_DIR"
    exit 1
fi

echo -e "${GREEN}✓ 源目录确认${NC}"
echo "  $SOURCE_DIR"
echo ""

# 询问是否继续
echo -e "${YELLOW}⚠️  即将创建独立仓库${NC}"
echo "  源目录: $SOURCE_DIR"
echo "  目标目录: $TARGET_DIR"
echo ""
read -p "是否继续？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}取消操作${NC}"
    exit 0
fi

# 步骤1: 复制文件
echo -e "${BLUE}[步骤 1/5] 复制项目文件...${NC}"
echo "  清理目标目录..."
rm -rf "$TARGET_DIR"
echo "  复制文件..."
cp -r "$SOURCE_DIR" "$TARGET_DIR"
echo -e "${GREEN}✓ 文件复制完成${NC}"
echo ""

# 步骤2: 重命名脚本文件
echo -e "${BLUE}[步骤 2/5] 更新脚本文件...${NC}"
cd "$TARGET_DIR/scripts"

# 备份原文件
if [ -f "fetch_weibo_hot.py" ]; then
    mv fetch_weibo_hot.py fetch_weibo_hot_legacy.py
fi

if [ -f "generate_html_report.py" ]; then
    mv generate_html_report.py generate_html_report_legacy.py
fi

# 使用 v2 版本
if [ -f "fetch_weibo_hot_v2.py" ]; then
    mv fetch_weibo_hot_v2.py fetch_weibo_hot.py
    echo "  ✓ fetch_weibo_hot.py 已更新"
fi

if [ -f "generate_html_report_v2.py" ]; then
    mv generate_html_report_v2.py generate_html_report.py
    echo "  ✓ generate_html_report.py 已更新"
fi

echo -e "${GREEN}✓ 脚本文件更新完成${NC}"
echo ""

# 步骤3: 创建 GitHub 配置
echo -e "${BLUE}[步骤 3/5] 创建 GitHub Actions 配置...${NC}"
cd "$TARGET_DIR"

# 创建 .github/workflows 目录
mkdir -p .github/workflows

# 如果 workflow 文件不存在，从备份复制
if [ ! -f ".github/workflows/weibo-daily.yml" ]; then
    echo "  ⚠️  警告: weibo-daily.yml 不存在，请手动创建"
    echo "  位置: .github/workflows/weibo-daily.yml"
else
    echo "  ✓ GitHub Actions workflow 已存在"
fi

echo -e "${GREEN}✓ GitHub 配置准备完成${NC}"
echo ""

# 步骤4: 初始化 Git
echo -e "${BLUE}[步骤 4/5] 初始化 Git 仓库...${NC}"

# 检查是否已经是 Git 仓库
if [ -d ".git" ]; then
    echo "  ⚠️  目录已经是 Git 仓库，跳过初始化"
else
    git init
    echo "  ✓ Git 仓库初始化完成"
fi

# 检查 .gitignore
if [ ! -f ".gitignore" ]; then
    echo "  ⚠️  .gitignore 不存在，请手动创建"
else
    echo "  ✓ .gitignore 已存在"
fi

echo -e "${GREEN}✓ Git 初始化完成${NC}"
echo ""

# 步骤5: 创建迁移文档
echo -e "${BLUE}[步骤 5/5] 创建迁移指南...${NC}"

cat > MIGRATION_GUIDE.md << 'EOF'
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
EOF

echo "  ✓ 迁移指南已创建: MIGRATION_GUIDE.md"
echo -e "${GREEN}✓ 迁移指南创建完成${NC}"
echo ""

# 完成
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✅ 迁移准备完成！${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "📁 目标目录: $TARGET_DIR"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo "  1. 检查文件: cd $TARGET_DIR"
echo "  2. 查看指南: cat MIGRATION_GUIDE.md"
echo "  3. 创建 GitHub 仓库"
echo "  4. 配置 GitHub Secrets"
echo "  5. 推送代码"
echo ""
echo -e "${BLUE}详细说明请查看: ${NC}MIGRATION_GUIDE.md"
echo ""
