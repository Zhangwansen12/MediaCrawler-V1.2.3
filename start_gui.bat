@echo off
chcp 65001 >nul
title MediaCrawler GUI 启动器

echo.
echo ========================================
echo    MediaCrawler GUI 启动器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.11+
    echo.
    pause
    exit /b 1
)

REM 检查虚拟环境
if exist ".venv\Scripts\activate.bat" (
    echo [信息] 检测到虚拟环境，正在激活...
    call .venv\Scripts\activate.bat
) else (
    echo [警告] 未检测到虚拟环境，使用系统Python
)

REM 检查依赖
echo [信息] 检查依赖包...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo [错误] tkinter未安装，请安装完整的Python
    pause
    exit /b 1
)

REM 启动GUI
echo [信息] 启动MediaCrawler GUI...
echo.
python gui_app.py

REM 如果程序异常退出，显示错误信息
if errorlevel 1 (
    echo.
    echo [错误] GUI启动失败，请检查错误信息
    echo.
    pause
)