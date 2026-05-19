#!/bin/bash
# Data Update Script for AIDevHub
# 使用方法: ./update.sh

set -e

echo "=== AIDevHub Data Update ==="
echo "更新日期: $(date '+%Y-%m-%d %H:%M:%S')"

# Pull latest from git
echo "Pulling latest changes..."
git pull origin master

# Step 1: Update JSON data files
echo ""
echo "请运行以下提示词来更新数据:"
echo "---"
cat << 'PROMPT'
请更新 /data 目录下的JSON数据文件。

需要更新的数据源:
1. AI编程工具: https://cursor.com, https://claude.ai/code 等官方页面
2. 大模型编程能力: https://www.datalearner.com/en/leaderboards/category/code
3. 编程语言: https://www.tiobe.com/tiobe-index/, https://survey.stackoverflow.co
4. 数据库: https://db-engines.com/en/ranking
5. GitHub AI项目: https://api.github.com/search/repositories

请:
1. 访问上述数据源获取最新数据
2. 更新对应的JSON文件
3. 确保数据格式与现有格式一致
4. 保持中英文双语描述
5. 保持每个item有icon字段（格式: https://logo.clearbit.com/domain.com）

JSON文件结构:
- data/tools.json: AI编程工具数组
- data/models.json: 大模型数据 (按swe-bench/livecode/swe-pro/multilingual分类)
- data/languages.json: 编程语言数组
- data/databases.json: 数据库数据 (按rdbms/kv/document等分类)
- data/github.json: GitHub AI项目数组
PROMPT
echo "---"

# Step 2: Download icons
echo ""
echo "下载图标中..."
python download_icons.py

echo ""
echo "更新完成！"
echo "提示: 运行 'python download_icons.py' 可以单独下载缺失的图标"