#!/bin/bash

# MediaCrawler GUI 启动脚本
# 适用于 Linux 和 macOS 系统

echo "========================================"
echo "    MediaCrawler GUI 启动器"
echo "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "[错误] 未检测到Python，请先安装Python 3.11+"
    exit 1
fi

# 确定Python命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "[信息] 使用Python命令: $PYTHON_CMD"

# 检查Python版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 11 ]); then
    echo "[警告] Python版本 $PYTHON_VERSION 可能不兼容，建议使用Python 3.11+"
fi

# 检查虚拟环境
if [ -f ".venv/bin/activate" ]; then
    echo "[信息] 检测到虚拟环境，正在激活..."
    source .venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    echo "[信息] 检测到虚拟环境，正在激活..."
    source venv/bin/activate
else
    echo "[警告] 未检测到虚拟环境，使用系统Python"
fi

# 检查tkinter依赖
echo "[信息] 检查GUI依赖..."
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[错误] tkinter未安装，请安装完整的Python或tkinter包"
    echo "Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "CentOS/RHEL: sudo yum install tkinter"
    echo "macOS: tkinter通常已包含在Python中"
    exit 1
fi

# 检查其他依赖
$PYTHON_CMD -c "import subprocess, threading, webbrowser" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[错误] 缺少必要的Python标准库模块"
    exit 1
fi

# 启动GUI
echo "[信息] 启动MediaCrawler GUI..."
echo

$PYTHON_CMD gui_app.py

# 检查退出状态
if [ $? -ne 0 ]; then
    echo
    echo "[错误] GUI启动失败，请检查错误信息"
    exit 1
fi

echo
echo "[信息] MediaCrawler GUI 已退出"