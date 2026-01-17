#!/bin/bash
# 微博热搜每日自动分析脚本
# 执行时间：每天22:00

# 设置脚本目录
SCRIPT_DIR="/Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping/.claude/skills/weibo_hotspot_analyzer"
VAULT_DIR="/Users/wanglingwei/Movies/violinvault/SynologyDrive/Clipping"

# 日志文件
LOG_FILE="${SCRIPT_DIR}/logs/daily_analysis_$(date +%Y%m%d).log"
REPORT_DIR="${VAULT_DIR}/19-ClaudeCode/微博热搜"

# 创建日志目录
mkdir -p "${SCRIPT_DIR}/logs"

# 记录开始时间
echo "========================================" >> "${LOG_FILE}"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "${LOG_FILE}"
echo "任务: 微博热搜每日分析" >> "${LOG_FILE}"
echo "========================================" >> "${LOG_FILE}"

# 切换到脚本目录
cd "${SCRIPT_DIR}" || exit 1

# 步骤1: 抓取微博热搜
echo "[步骤1] 抓取微博热搜数据..." >> "${LOG_FILE}"
source venv/bin/activate && python scripts/fetch_weibo_hot.py >> "${LOG_FILE}" 2>&1

if [ $? -ne 0 ]; then
    echo "[错误] 热搜抓取失败！" >> "${LOG_FILE}"
    exit 1
fi

echo "[成功] 热搜数据抓取完成" >> "${LOG_FILE}"

# 步骤2: 找到最新生成的JSON文件
LATEST_JSON=$(ls -t weibo_hotspots_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_JSON" ]; then
    echo "[错误] 未找到热搜数据文件！" >> "${LOG_FILE}"
    exit 1
fi

echo "[信息] 使用数据文件: ${LATEST_JSON}" >> "${LOG_FILE}"

# 步骤3: 生成HTML报告
echo "[步骤2] 生成HTML分析报告..." >> "${LOG_FILE}"

# 修改generate_html_report.py中的JSON文件名为最新文件
sed "s/weibo_hotspots_20260114_220449.json/${LATEST_JSON}/g" scripts/generate_html_report.py > scripts/generate_html_report_temp.py

# 执行生成报告
source venv/bin/activate && python scripts/generate_html_report_temp.py >> "${LOG_FILE}" 2>&1

if [ $? -ne 0 ]; then
    echo "[错误] 报告生成失败！" >> "${LOG_FILE}"
    rm -f scripts/generate_html_report_temp.py
    exit 1
fi

# 清理临时文件
rm -f scripts/generate_html_report_temp.py

echo "[成功] HTML报告生成完成" >> "${LOG_FILE}"

# 步骤4: 检查生成的报告
LATEST_REPORT=$(ls -t "${REPORT_DIR}"/2026/*/weibo_hotspot_report_*.html "${REPORT_DIR}"/2026/*/*_weibo_hotspot_report.html 2>/dev/null | head -1)

if [ -n "$LATEST_REPORT" ]; then
    echo "[信息] 报告路径: ${LATEST_REPORT}" >> "${LOG_FILE}"
    echo "[信息] 报告大小: $(du -h "${LATEST_REPORT}" | cut -f1)" >> "${LOG_FILE}"
else
    echo "[警告] 未找到生成的报告文件" >> "${LOG_FILE}"
fi

# 步骤5: 清理7天前的JSON数据文件（可选）
echo "[步骤3] 清理旧数据文件..." >> "${LOG_FILE}"
find "${SCRIPT_DIR}" -name "weibo_hotspots_*.json" -mtime +7 -delete 2>/dev/null
find "${SCRIPT_DIR}" -name "weibo_ideas_*.json" -mtime +7 -delete 2>/dev/null
echo "[完成] 旧数据清理完成" >> "${LOG_FILE}"

# 记录结束时间
echo "========================================" >> "${LOG_FILE}"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "${LOG_FILE}"
echo "任务状态: 成功完成 ✅" >> "${LOG_FILE}"
echo "========================================" >> "${LOG_FILE}"
echo "" >> "${LOG_FILE}"

# 可选：发送通知（macOS）
# osascript -e 'display notification "微博热搜分析完成" with title "定时任务"'
