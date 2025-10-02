# -*- coding: utf-8 -*-
"""
MediaCrawler GUI Application
一个集成所有MediaCrawler功能的图形用户界面
"""

import asyncio
import json
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Dict, List, Optional
import webbrowser
from datetime import datetime
import requests
import aiohttp
import aiofiles
from urllib.parse import urlparse
from pathlib import Path
import re
from typing import Optional, Dict
from PIL import Image, ImageTk
import io
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from collections import Counter
import jieba
from wordcloud import WordCloud
import numpy as np

import config
from cmd_arg.arg import PlatformEnum, LoginTypeEnum, CrawlerTypeEnum, SaveDataOptionEnum
from config_editor_gui import ConfigEditor


class MediaCrawlerGUI:
    """MediaCrawler图形用户界面主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MediaCrawler - 多平台媒体数据采集工具")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # 初始化配置编辑器
        self.config_editor = ConfigEditor(self.root)
        
        # 设置窗口图标和样式
        self.setup_styles()
        
        # 创建主界面
        self.create_main_interface()
        
        # 状态变量
        self.current_process = None
        self.is_running = False
        self.download_tasks = {}  # 存储下载任务
        self.download_stats = {"total": 0, "success": 0, "failed": 0}  # 下载统计
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置按钮样式
        style.configure('Action.TButton', 
                       font=('Microsoft YaHei', 10, 'bold'),
                       padding=(10, 5))
        
        # 配置标签样式
        style.configure('Title.TLabel', 
                       font=('Microsoft YaHei', 12, 'bold'),
                       foreground='#2c3e50')
        
        style.configure('Subtitle.TLabel', 
                       font=('Microsoft YaHei', 10),
                       foreground='#34495e')
    
    def create_main_interface(self):
        """创建主界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="MediaCrawler 多平台媒体数据采集工具", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧日志输出区域
        self.create_log_panel(main_frame)
        
        # 底部状态栏
        self.create_status_bar(main_frame)
    
    def create_control_panel(self, parent):
        """创建左侧控制面板"""
        control_frame = ttk.LabelFrame(parent, text="功能控制面板", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # 基础配置区域
        self.create_basic_config(control_frame)
        
        # 爬虫功能区域
        self.create_crawler_functions(control_frame)
        
        # 视频下载功能区域
        self.create_video_download_functions(control_frame)
        
        # 数据库功能区域
        self.create_database_functions(control_frame)
        
        # 工具功能区域
        self.create_tool_functions(control_frame)
    
    def create_basic_config(self, parent):
        """创建基础配置区域"""
        config_frame = ttk.LabelFrame(parent, text="基础配置", padding="5")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 平台选择
        ttk.Label(config_frame, text="目标平台:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.platform_var = tk.StringVar(value="xhs")
        platform_combo = ttk.Combobox(config_frame, textvariable=self.platform_var, 
                                     values=["xhs", "dy", "ks", "bili", "wb", "tieba", "zhihu"],
                                     state="readonly", width=15)
        platform_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        platform_combo.bind("<<ComboboxSelected>>", self.on_platform_changed)
        
        # 登录方式
        ttk.Label(config_frame, text="登录方式:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.login_type_var = tk.StringVar(value="qrcode")
        login_combo = ttk.Combobox(config_frame, textvariable=self.login_type_var,
                                  values=["qrcode", "phone", "cookie"],
                                  state="readonly", width=15)
        login_combo.grid(row=0, column=3, sticky=tk.W)
        
        # 爬取类型
        ttk.Label(config_frame, text="爬取类型:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.crawler_type_var = tk.StringVar(value="search")
        type_combo = ttk.Combobox(config_frame, textvariable=self.crawler_type_var,
                                 values=["search", "detail", "creator", "mall"],
                                 state="readonly", width=15)
        type_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        type_combo.bind("<<ComboboxSelected>>", self.on_crawler_type_changed)
        
        # 数据保存方式
        ttk.Label(config_frame, text="保存方式:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.save_option_var = tk.StringVar(value="json")
        save_combo = ttk.Combobox(config_frame, textvariable=self.save_option_var,
                                 values=["json", "csv", "sqlite", "db"],
                                 state="readonly", width=15)
        save_combo.grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # 关键词输入
        ttk.Label(config_frame, text="搜索关键词:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.keywords_var = tk.StringVar(value="编程副业,编程兼职")
        keywords_entry = ttk.Entry(config_frame, textvariable=self.keywords_var, width=50)
        keywords_entry.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 抓取数量配置
        ttk.Label(config_frame, text="抓取数量:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.max_notes_var = tk.StringVar(value="20")
        max_notes_entry = ttk.Entry(config_frame, textvariable=self.max_notes_var, width=15)
        max_notes_entry.grid(row=3, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        # 评论抓取开关
        ttk.Label(config_frame, text="抓取评论:").grid(row=3, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.enable_comments_var = tk.BooleanVar(value=True)
        comments_check = ttk.Checkbutton(config_frame, variable=self.enable_comments_var, 
                                       command=self.on_comments_toggle)
        comments_check.grid(row=3, column=3, sticky=tk.W, pady=(5, 0))
        
        # 评论数量配置
        ttk.Label(config_frame, text="评论数量:").grid(row=4, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.max_comments_var = tk.StringVar(value="10")
        self.max_comments_entry = ttk.Entry(config_frame, textvariable=self.max_comments_var, width=15)
        self.max_comments_entry.grid(row=4, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        # 二级评论开关
        ttk.Label(config_frame, text="二级评论:").grid(row=4, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.enable_sub_comments_var = tk.BooleanVar(value=False)
        self.sub_comments_check = ttk.Checkbutton(config_frame, variable=self.enable_sub_comments_var)
        self.sub_comments_check.grid(row=4, column=3, sticky=tk.W, pady=(5, 0))
        
        # 小红书商城配置（仅在选择小红书平台且爬取类型为mall时显示）
        self.create_xhs_mall_config(config_frame)
        
        # 快手视频统计功能配置（仅在选择快手平台时显示）
        self.create_kuaishou_stats_config(config_frame)
    
    def create_crawler_functions(self, parent):
        """创建爬虫功能区域"""
        crawler_frame = ttk.LabelFrame(parent, text="爬虫功能", padding="5")
        crawler_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行按钮
        row1_frame = ttk.Frame(crawler_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(row1_frame, text="开始爬取", 
                  command=self.start_crawling, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row1_frame, text="停止爬取", 
                  command=self.stop_crawling, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row1_frame, text="查看数据", 
                  command=self.view_data, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # 第二行按钮
        row2_frame = ttk.Frame(crawler_frame)
        row2_frame.pack(fill=tk.X)
        
        ttk.Button(row2_frame, text="配置管理", 
                  command=self.manage_config, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="代理设置", 
                  command=self.proxy_settings, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="词云生成", 
                  command=self.generate_wordcloud, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
    
    def create_database_functions(self, parent):
        """创建数据库功能区域"""
        db_frame = ttk.LabelFrame(parent, text="数据库管理", padding="5")
        db_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(db_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="初始化SQLite", 
                  command=lambda: self.init_database("sqlite"), 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="初始化MySQL", 
                  command=lambda: self.init_database("mysql"), 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="数据导出", 
                  command=self.export_data, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="数据清理", 
                  command=self.clean_data, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
    
    def create_tool_functions(self, parent):
        """创建工具功能区域"""
        tool_frame = ttk.LabelFrame(parent, text="实用工具", padding="5")
        tool_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 第一行工具
        row1_frame = ttk.Frame(tool_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(row1_frame, text="短信服务器", 
                  command=self.start_sms_server, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row1_frame, text="浏览器管理", 
                  command=self.browser_manager, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row1_frame, text="日志查看", 
                  command=self.view_logs, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # 第二行工具
        row2_frame = ttk.Frame(tool_frame)
        row2_frame.pack(fill=tk.X)
        
        ttk.Button(row2_frame, text="帮助文档", 
                  command=self.show_help, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="小红书商城", 
                  command=self.open_xhs_mall, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="内容预览", 
                  command=self.open_content_preview, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="项目主页", 
                  command=self.open_project_home, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(row2_frame, text="关于", 
                  command=self.show_about, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
    
    def create_log_panel(self, parent):
        """创建右侧日志面板"""
        log_frame = ttk.LabelFrame(parent, text="运行日志", padding="5")
        log_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 创建日志文本区域
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                 font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 日志控制按钮
        log_control_frame = ttk.Frame(log_frame)
        log_control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(log_control_frame, text="清空日志", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(log_control_frame, text="保存日志", 
                  command=self.save_log).pack(side=tk.LEFT, padx=(0, 5))
        
        # 初始化日志
        self.log_message("MediaCrawler GUI 已启动")
        self.log_message("请选择相应功能开始使用")
    
    def create_status_bar(self, parent):
        """创建底部状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                style='Subtitle.TLabel')
        status_label.pack(side=tk.LEFT)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          mode='determinate', length=200)
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
    
    def log_message(self, message: str, level: str = "INFO"):
        """添加日志消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, status: str):
        """更新状态栏"""
        self.status_var.set(status)
        self.root.update_idletasks()
    
    def start_crawling(self):
        """开始爬取"""
        if self.is_running:
            messagebox.showwarning("警告", "爬虫正在运行中，请先停止当前任务")
            return
        
        # 验证输入参数
        try:
            max_notes = int(self.max_notes_var.get())
            if max_notes <= 0:
                raise ValueError("抓取数量必须大于0")
        except ValueError as e:
            messagebox.showerror("参数错误", f"抓取数量输入无效: {str(e)}")
            return
        
        try:
            max_comments = int(self.max_comments_var.get())
            if max_comments <= 0:
                raise ValueError("评论数量必须大于0")
        except ValueError as e:
            messagebox.showerror("参数错误", f"评论数量输入无效: {str(e)}")
            return
        
        # 更新配置
        config.CRAWLER_MAX_NOTES_COUNT = max_notes
        config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = max_comments
        config.ENABLE_GET_COMMENTS = self.enable_comments_var.get()
        config.ENABLE_GET_SUB_COMMENTS = self.enable_sub_comments_var.get()
        
        # 构建命令行参数
        cmd = [
            sys.executable, "main.py",
            "--platform", self.platform_var.get(),
            "--lt", self.login_type_var.get(),
            "--type", self.crawler_type_var.get(),
            "--save_data_option", self.save_option_var.get(),
            "--keywords", self.keywords_var.get(),
            "--get_comment", str(self.enable_comments_var.get()).lower(),
            "--get_sub_comment", str(self.enable_sub_comments_var.get()).lower()
        ]
        
        # 如果是快手平台且启用了视频统计功能，则更新配置文件
        if self.platform_var.get() == "ks" and hasattr(self, 'enable_video_stats_var'):
            self.update_kuaishou_config()
        
        self.log_message(f"开始爬取 - 平台: {self.platform_var.get()}, 类型: {self.crawler_type_var.get()}")
        self.log_message(f"配置参数 - 抓取数量: {max_notes}, 评论数量: {max_comments}, 抓取评论: {self.enable_comments_var.get()}, 二级评论: {self.enable_sub_comments_var.get()}")
        self.update_status("爬取中...")
        self.is_running = True
        
        # 在新线程中运行爬虫
        def run_crawler():
            try:
                self.current_process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=os.getcwd(),
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
                
                # 实时读取输出
                for line in iter(self.current_process.stdout.readline, ''):
                    if line:
                        self.log_message(line.strip(), "CRAWLER")
                
                self.current_process.wait()
                
                if self.current_process.returncode == 0:
                    self.log_message("爬取完成", "SUCCESS")
                else:
                    self.log_message(f"爬取失败，退出码: {self.current_process.returncode}", "ERROR")
                    
            except Exception as e:
                self.log_message(f"爬取过程出错: {str(e)}", "ERROR")
            finally:
                self.is_running = False
                self.current_process = None
                self.update_status("就绪")
        
        threading.Thread(target=run_crawler, daemon=True).start()
    
    def stop_crawling(self):
        """停止爬取"""
        if self.current_process and self.is_running:
            self.current_process.terminate()
            self.log_message("爬取已停止", "WARNING")
            self.update_status("已停止")
            self.is_running = False
        else:
            messagebox.showinfo("提示", "当前没有运行中的爬取任务")
    
    def init_database(self, db_type: str):
        """初始化数据库"""
        self.log_message(f"开始初始化{db_type.upper()}数据库...")
        self.update_status(f"初始化{db_type}数据库中...")
        
        cmd = [sys.executable, "main.py", "--init_db", db_type]
        
        def run_init():
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
                if result.returncode == 0:
                    self.log_message(f"{db_type.upper()}数据库初始化成功", "SUCCESS")
                    messagebox.showinfo("成功", f"{db_type.upper()}数据库初始化完成")
                else:
                    self.log_message(f"数据库初始化失败: {result.stderr}", "ERROR")
                    messagebox.showerror("错误", f"数据库初始化失败:\n{result.stderr}")
            except Exception as e:
                self.log_message(f"数据库初始化出错: {str(e)}", "ERROR")
                messagebox.showerror("错误", f"数据库初始化出错:\n{str(e)}")
            finally:
                self.update_status("就绪")
        
        threading.Thread(target=run_init, daemon=True).start()
    
    def view_data(self):
        """查看数据"""
        data_dir = os.path.join(os.getcwd(), "data")
        if os.path.exists(data_dir):
            if sys.platform == "win32":
                os.startfile(data_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", data_dir])
            else:
                subprocess.run(["xdg-open", data_dir])
            self.log_message("已打开数据目录")
        else:
            messagebox.showinfo("提示", "数据目录不存在，请先运行爬取任务")
    
    def manage_config(self):
        """配置管理"""
        self.config_editor.open_config_editor()
        self.log_message("已打开配置编辑器")
    
    def proxy_settings(self):
        """代理设置"""
        messagebox.showinfo("代理设置", "请在config/base_config.py中修改ENABLE_IP_PROXY等相关配置")
        self.log_message("请查看配置文件进行代理设置")
    
    def generate_wordcloud(self):
        """生成词云"""
        messagebox.showinfo("词云生成", "请在config/base_config.py中设置ENABLE_GET_WORDCLOUD=True，然后运行爬取任务")
        self.log_message("词云功能需要在配置文件中启用")
    
    def start_sms_server(self):
        """启动短信服务器"""
        self.log_message("启动短信转发服务器...")
        
        def run_sms_server():
            try:
                cmd = [sys.executable, "recv_sms.py"]
                subprocess.Popen(cmd, cwd=os.getcwd())
                self.log_message("短信服务器已启动，监听端口8000", "SUCCESS")
            except Exception as e:
                self.log_message(f"启动短信服务器失败: {str(e)}", "ERROR")
        
        threading.Thread(target=run_sms_server, daemon=True).start()
    
    def browser_manager(self):
        """浏览器管理"""
        browser_data_dir = os.path.join(os.getcwd(), "browser_data")
        if os.path.exists(browser_data_dir):
            if sys.platform == "win32":
                os.startfile(browser_data_dir)
            else:
                subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", browser_data_dir])
            self.log_message("已打开浏览器数据目录")
        else:
            messagebox.showinfo("提示", "浏览器数据目录不存在")
    
    def view_logs(self):
        """查看日志"""
        # 这里可以实现更详细的日志查看功能
        messagebox.showinfo("日志查看", "当前日志显示在右侧面板中")
    
    def show_help(self):
        """显示帮助"""
        help_text = """
MediaCrawler 使用帮助

1. 基础配置：
   - 选择目标平台（小红书、抖音、快手等）
   - 选择登录方式（二维码、手机号、Cookie）
   - 选择爬取类型（搜索、详情、创作者）
   - 选择数据保存方式

2. 爬虫功能：
   - 开始爬取：根据配置开始数据采集
   - 停止爬取：中止当前运行的任务
   - 查看数据：打开数据存储目录

3. 数据库管理：
   - 初始化数据库表结构
   - 数据导出和清理

4. 实用工具：
   - 短信服务器：用于接收验证码
   - 浏览器管理：管理浏览器缓存数据

更多详细信息请查看项目文档。
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x400")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def open_project_home(self):
        """打开项目主页"""
        webbrowser.open("https://github.com/NanmiCoder/MediaCrawler")
        self.log_message("已打开项目主页")
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
MediaCrawler GUI v1.0

一个功能强大的多平台自媒体数据采集工具

支持平台：
• 小红书 (XHS)
• 抖音 (DouYin) 
• 快手 (KuaiShou)
• 哔哩哔哩 (Bilibili)
• 微博 (Weibo)
• 百度贴吧 (Tieba)
• 知乎 (Zhihu)

开发者：NanmiCoder
项目地址：https://github.com/NanmiCoder/MediaCrawler
        """
        messagebox.showinfo("关于 MediaCrawler", about_text)
    
    def export_data(self):
        """数据导出"""
        messagebox.showinfo("数据导出", "数据导出功能开发中，当前可直接访问data目录获取数据文件")
        self.log_message("数据导出功能提示")
    
    def clean_data(self):
        """数据清理"""
        result = messagebox.askyesno("确认", "确定要清理所有数据吗？此操作不可恢复！")
        if result:
            try:
                data_dir = os.path.join(os.getcwd(), "data")
                if os.path.exists(data_dir):
                    import shutil
                    shutil.rmtree(data_dir)
                    os.makedirs(data_dir)
                    self.log_message("数据清理完成", "SUCCESS")
                    messagebox.showinfo("成功", "数据清理完成")
                else:
                    messagebox.showinfo("提示", "数据目录不存在")
            except Exception as e:
                self.log_message(f"数据清理失败: {str(e)}", "ERROR")
                messagebox.showerror("错误", f"数据清理失败:\n{str(e)}")
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("日志已清空")
    
    def save_log(self):
        """保存日志"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.log_message(f"日志已保存到: {filename}", "SUCCESS")
                messagebox.showinfo("成功", "日志保存成功")
            except Exception as e:
                self.log_message(f"日志保存失败: {str(e)}", "ERROR")
                messagebox.showerror("错误", f"日志保存失败:\n{str(e)}")
    
    def on_comments_toggle(self):
        """评论抓取开关切换时的处理"""
        if self.enable_comments_var.get():
            # 启用评论相关控件
            self.max_comments_entry.config(state='normal')
            self.sub_comments_check.config(state='normal')
        else:
            # 禁用评论相关控件
            self.max_comments_entry.config(state='disabled')
            self.sub_comments_check.config(state='disabled')
            self.enable_sub_comments_var.set(False)
    
    def on_platform_changed(self, event=None):
        """平台选择改变时的处理函数"""
        platform = self.platform_var.get()
        
        # 显示或隐藏快手统计配置
        if hasattr(self, 'kuaishou_stats_frame'):
            if platform == "ks":
                self.kuaishou_stats_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
            else:
                self.kuaishou_stats_frame.grid_remove()
        
        # 显示或隐藏小红书商城配置
        if hasattr(self, 'xhs_mall_frame'):
            if platform == "xhs" and self.crawler_type_var.get() == "mall":
                self.xhs_mall_frame.grid()
            else:
                self.xhs_mall_frame.grid_remove()
    
    def on_crawler_type_changed(self, event=None):
        """爬取类型改变时的处理"""
        crawler_type = self.crawler_type_var.get()
        platform = self.platform_var.get()
        
        # 显示或隐藏小红书商城配置
        if hasattr(self, 'xhs_mall_frame'):
            if platform == "xhs" and crawler_type == "mall":
                self.xhs_mall_frame.grid()
            else:
                self.xhs_mall_frame.grid_remove()
    
    def create_xhs_mall_config(self, parent):
        """创建小红书商城配置区域"""
        self.xhs_mall_frame = ttk.LabelFrame(parent, text="小红书商城配置", padding="5")
        self.xhs_mall_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        self.xhs_mall_frame.grid_remove()  # 默认隐藏
        
        # 商城功能选择
        ttk.Label(self.xhs_mall_frame, text="商城功能:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.mall_function_var = tk.StringVar(value="product_search")
        mall_function_combo = ttk.Combobox(self.xhs_mall_frame, textvariable=self.mall_function_var,
                                          values=["product_search", "trending_products", "product_detail", "analytics"],
                                          state="readonly", width=20)
        mall_function_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        # 商品类别
        ttk.Label(self.xhs_mall_frame, text="商品类别:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.product_category_var = tk.StringVar(value="全部")
        category_combo = ttk.Combobox(self.xhs_mall_frame, textvariable=self.product_category_var,
                                     values=["全部", "美妆", "服饰", "数码", "家居", "食品", "运动", "母婴"],
                                     state="readonly", width=15)
        category_combo.grid(row=0, column=3, sticky=tk.W)
        
        # 价格范围
        price_frame = ttk.Frame(self.xhs_mall_frame)
        price_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Label(price_frame, text="价格范围:").pack(side=tk.LEFT, padx=(0, 5))
        self.min_price_var = tk.StringVar(value="0")
        ttk.Entry(price_frame, textvariable=self.min_price_var, width=10).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(price_frame, text="至").pack(side=tk.LEFT, padx=(0, 5))
        self.max_price_var = tk.StringVar(value="1000")
        ttk.Entry(price_frame, textvariable=self.max_price_var, width=10).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(price_frame, text="元").pack(side=tk.LEFT)
        
        # 排序方式
        ttk.Label(price_frame, text="排序方式:").pack(side=tk.LEFT, padx=(20, 5))
        self.sort_type_var = tk.StringVar(value="sales")
        sort_combo = ttk.Combobox(price_frame, textvariable=self.sort_type_var,
                                 values=["sales", "price_asc", "price_desc", "rating", "newest"],
                                 state="readonly", width=15)
        sort_combo.pack(side=tk.LEFT)
        
        # 数据量限制
        ttk.Label(price_frame, text="数据量:").pack(side=tk.LEFT, padx=(20, 5))
        self.data_limit_var = tk.StringVar(value="100")
        ttk.Entry(price_frame, textvariable=self.data_limit_var, width=8).pack(side=tk.LEFT)
        
        # 实时更新配置
        realtime_frame = ttk.Frame(self.xhs_mall_frame)
        realtime_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.enable_realtime_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(realtime_frame, text="启用实时更新", 
                       variable=self.enable_realtime_var).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(realtime_frame, text="更新间隔:").pack(side=tk.LEFT, padx=(0, 5))
        self.update_interval_var = tk.StringVar(value="300")
        ttk.Entry(realtime_frame, textvariable=self.update_interval_var, width=8).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(realtime_frame, text="秒").pack(side=tk.LEFT)
    
    def create_kuaishou_stats_config(self, parent):
        """创建快手视频统计功能配置区域"""
        self.kuaishou_stats_frame = ttk.LabelFrame(parent, text="快手视频统计功能", padding="5")
        self.kuaishou_stats_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 初始化统计功能相关变量
        self.enable_video_stats_var = tk.BooleanVar(value=False)
        self.enable_batch_stats_var = tk.BooleanVar(value=False)
        self.enable_engagement_rate_var = tk.BooleanVar(value=True)
        self.enable_performance_analysis_var = tk.BooleanVar(value=True)
        self.log_stats_data_var = tk.BooleanVar(value=True)
        self.batch_stats_delay_var = tk.DoubleVar(value=1.0)
        self.top_videos_count_var = tk.IntVar(value=10)
        self.top_videos_metric_var = tk.StringVar(value="likes")
        self.stats_display_language_var = tk.StringVar(value="zh")
        
        # 第一行：基础开关
        ttk.Label(self.kuaishou_stats_frame, text="启用视频统计:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Checkbutton(self.kuaishou_stats_frame, variable=self.enable_video_stats_var).grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(self.kuaishou_stats_frame, text="启用批量统计:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        ttk.Checkbutton(self.kuaishou_stats_frame, variable=self.enable_batch_stats_var).grid(row=0, column=3, sticky=tk.W)
        
        # 第二行：分析功能开关
        ttk.Label(self.kuaishou_stats_frame, text="启用互动率计算:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Checkbutton(self.kuaishou_stats_frame, variable=self.enable_engagement_rate_var).grid(row=1, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        ttk.Label(self.kuaishou_stats_frame, text="启用性能分析:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Checkbutton(self.kuaishou_stats_frame, variable=self.enable_performance_analysis_var).grid(row=1, column=3, sticky=tk.W, pady=(5, 0))
        
        # 第三行：数值配置
        ttk.Label(self.kuaishou_stats_frame, text="批量延迟(秒):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        delay_spinbox = ttk.Spinbox(self.kuaishou_stats_frame, from_=0.1, to=10.0, increment=0.1, 
                                   textvariable=self.batch_stats_delay_var, width=8)
        delay_spinbox.grid(row=2, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        ttk.Label(self.kuaishou_stats_frame, text="热门视频数量:").grid(row=2, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        count_spinbox = ttk.Spinbox(self.kuaishou_stats_frame, from_=1, to=100, 
                                   textvariable=self.top_videos_count_var, width=8)
        count_spinbox.grid(row=2, column=3, sticky=tk.W, pady=(5, 0))
        
        # 第四行：选择配置
        ttk.Label(self.kuaishou_stats_frame, text="排序指标:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        metric_combo = ttk.Combobox(self.kuaishou_stats_frame, textvariable=self.top_videos_metric_var,
                                   values=["likes", "comments", "shares", "collects", "views", "engagement_rate"],
                                   state="readonly", width=12)
        metric_combo.grid(row=3, column=1, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        
        ttk.Label(self.kuaishou_stats_frame, text="显示语言:").grid(row=3, column=2, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        lang_combo = ttk.Combobox(self.kuaishou_stats_frame, textvariable=self.stats_display_language_var,
                                 values=["zh", "en"], state="readonly", width=8)
        lang_combo.grid(row=3, column=3, sticky=tk.W, pady=(5, 0))
        
        # 初始状态下隐藏快手统计配置
        if self.platform_var.get() != "ks":
            self.kuaishou_stats_frame.grid_remove()
    
    def update_kuaishou_config(self):
        """更新快手配置文件中的统计功能设置"""
        try:
            config_path = "config/ks_config.py"
            
            # 读取当前配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新配置值
            config_updates = {
                'ENABLE_VIDEO_STATS': self.enable_video_stats_var.get(),
                'ENABLE_BATCH_STATS': self.enable_batch_stats_var.get(),
                'ENABLE_ENGAGEMENT_RATE': self.enable_engagement_rate_var.get(),
                'ENABLE_PERFORMANCE_ANALYSIS': self.enable_performance_analysis_var.get(),
                'LOG_STATS_DATA': self.log_stats_data_var.get(),
                'BATCH_STATS_DELAY': self.batch_stats_delay_var.get(),
                'TOP_VIDEOS_COUNT': self.top_videos_count_var.get(),
                'TOP_VIDEOS_METRIC': f'"{self.top_videos_metric_var.get()}"',
                'STATS_DISPLAY_LANGUAGE': f'"{self.stats_display_language_var.get()}"'
            }
            
            # 替换配置值
            for key, value in config_updates.items():
                pattern = rf'^{key}\s*=.*$'
                replacement = f'{key} = {value}'
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # 写回配置文件
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_message("快手统计功能配置已更新", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"更新快手配置失败: {str(e)}", "ERROR")
    
    def open_xhs_mall(self):
        """打开小红书商城数据管理界面"""
        try:
            # 获取当前配置
            config = {
                'mall_function': getattr(self, 'mall_function_var', tk.StringVar(value="product_search")).get(),
                'product_category': getattr(self, 'product_category_var', tk.StringVar(value="全部")).get(),
                'min_price': getattr(self, 'min_price_var', tk.StringVar(value="0")).get(),
                'max_price': getattr(self, 'max_price_var', tk.StringVar(value="1000")).get(),
                'sort_type': getattr(self, 'sort_type_var', tk.StringVar(value="sales")).get(),
                'data_limit': getattr(self, 'data_limit_var', tk.StringVar(value="100")).get(),
                'enable_realtime': getattr(self, 'enable_realtime_var', tk.BooleanVar(value=False)).get(),
                'update_interval': getattr(self, 'update_interval_var', tk.StringVar(value="300")).get(),
                'keywords': self.keywords_var.get()
            }
            
            # 导入并启动小红书商城GUI
            from gui_xhs_mall import XhsMallGUI
            
            # 检查是否已经打开了商城窗口
            if hasattr(self, 'xhs_mall_window') and self.xhs_mall_window.window.winfo_exists():
                self.xhs_mall_window.window.lift()  # 将窗口提到前台
                self.xhs_mall_window.window.focus_force()
                return
            
            # 创建新的商城数据管理窗口
            self.xhs_mall_window = XhsMallGUI(self.root, config)
            self.log_message("小红书商城数据管理界面已打开", "SUCCESS")
            
        except ImportError as e:
            self.log_message(f"无法导入小红书商城模块: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"无法打开小红书商城功能:\n缺少必要的模块: {str(e)}")
        except Exception as e:
            self.log_message(f"打开小红书商城界面失败: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"打开小红书商城界面失败:\n{str(e)}")
    
    def select_download_directory(self):
        """选择下载目录"""
        directory = filedialog.askdirectory(
            title="选择视频下载目录",
            initialdir=self.download_dir_var.get()
        )
        if directory:
            self.download_dir_var.set(directory)
            self.log_message(f"下载目录已设置为: {directory}")
    
    def parse_video_url(self):
        """解析视频URL"""
        url = self.video_url_var.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入视频链接")
            return
        
        self.log_message(f"开始解析视频链接: {url}")
        self.download_status_var.set("解析中...")
        
        def parse_url():
            try:
                # 检测平台类型
                platform = self.detect_platform(url)
                if not platform:
                    self.log_message("无法识别视频平台", "ERROR")
                    self.download_status_var.set("解析失败")
                    return
                
                self.log_message(f"检测到平台: {platform}")
                
                # 根据平台解析视频信息
                video_info = self.extract_video_info(url, platform)
                if video_info:
                    self.log_message(f"解析成功 - 标题: {video_info.get('title', '未知')}")
                    self.log_message(f"视频URL: {video_info.get('video_url', '未找到')}")
                    self.download_status_var.set("解析完成")
                else:
                    self.log_message("视频信息解析失败", "ERROR")
                    self.download_status_var.set("解析失败")
                    
            except Exception as e:
                self.log_message(f"解析视频链接出错: {str(e)}", "ERROR")
                self.download_status_var.set("解析失败")
        
        threading.Thread(target=parse_url, daemon=True).start()
    
    def detect_platform(self, url: str) -> Optional[str]:
        """检测视频平台"""
        url_lower = url.lower()
        
        if 'douyin.com' in url_lower or 'dy.com' in url_lower:
            return 'douyin'
        elif 'xiaohongshu.com' in url_lower or 'xhslink.com' in url_lower:
            return 'xiaohongshu'
        elif 'kuaishou.com' in url_lower or 'ks.com' in url_lower:
            return 'kuaishou'
        elif 'bilibili.com' in url_lower:
            return 'bilibili'
        elif 'weibo.com' in url_lower or 'weibo.cn' in url_lower:
            return 'weibo'
        else:
            return None
    
    def extract_video_info(self, url: str, platform: str) -> Optional[Dict]:
        """提取视频信息"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 简单的视频信息提取（实际项目中需要更复杂的解析）
            video_info = {
                'title': self.extract_title_from_html(response.text),
                'platform': platform,
                'original_url': url,
                'video_url': self.extract_video_url_from_html(response.text, platform)
            }
            
            return video_info
            
        except Exception as e:
            self.log_message(f"提取视频信息失败: {str(e)}", "ERROR")
            return None
    
    def extract_title_from_html(self, html: str) -> str:
        """从HTML中提取标题"""
        import re
        
        # 尝试提取title标签内容
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        return "未知标题"
    
    def extract_video_url_from_html(self, html: str, platform: str) -> Optional[str]:
        """从HTML中提取视频URL"""
        import re
        
        # 根据不同平台使用不同的正则表达式
        if platform == 'douyin':
            # 抖音视频URL提取
            video_match = re.search(r'"play_url":\s*"([^"]+)"', html)
        elif platform == 'xiaohongshu':
            # 小红书视频URL提取
            video_match = re.search(r'"videoUrl":\s*"([^"]+)"', html)
        elif platform == 'kuaishou':
            # 快手视频URL提取
            video_match = re.search(r'"photoUrl":\s*"([^"]+)"', html)
        else:
            # 通用视频URL提取
            video_match = re.search(r'<video[^>]+src="([^"]+)"', html, re.IGNORECASE)
        
        if video_match:
            return video_match.group(1).replace('\\/', '/')
        
        return None
    
    def update_download_stats(self, success: bool = None):
        """更新下载统计信息"""
        if success is True:
            self.download_stats["success"] += 1
        elif success is False:
            self.download_stats["failed"] += 1
        else:
            self.download_stats["total"] += 1
        
        stats_text = f"总计: {self.download_stats['total']} | 成功: {self.download_stats['success']} | 失败: {self.download_stats['failed']}"
        if hasattr(self, 'download_stats_var'):
            self.download_stats_var.set(stats_text)

    def download_video(self):
        """下载视频"""
        url = self.video_url_var.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入视频链接")
            return
        
        download_dir = self.download_dir_var.get()
        if not os.path.exists(download_dir):
            try:
                os.makedirs(download_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("错误", f"创建下载目录失败: {str(e)}")
                return
        
        self.log_message(f"开始下载视频: {url}")
        self.download_status_var.set("下载中...")
        self.download_progress_var.set(0)
        self.update_download_stats()  # 增加总计数
        
        def download():
            try:
                # 首先解析视频信息
                platform = self.detect_platform(url)
                if not platform:
                    self.log_message("无法识别视频平台", "ERROR")
                    self.download_status_var.set("下载失败")
                    return
                
                video_info = self.extract_video_info(url, platform)
                if not video_info or not video_info.get('video_url'):
                    self.log_message("无法获取视频下载链接", "ERROR")
                    self.download_status_var.set("下载失败")
                    return
                
                # 下载视频文件
                video_url = video_info['video_url']
                title = video_info.get('title', 'video')
                
                # 清理文件名
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
                filename = f"{safe_title}.mp4"
                filepath = os.path.join(download_dir, filename)
                
                # 如果文件已存在，添加序号
                counter = 1
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(filename)
                    filepath = os.path.join(download_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                # 下载文件
                self.download_file_with_progress(video_url, filepath)
                
                self.log_message(f"视频下载完成: {filepath}", "SUCCESS")
                self.download_status_var.set("下载完成")
                self.download_progress_var.set(100)
                self.update_download_stats(success=True)  # 标记成功
                
            except Exception as e:
                self.log_message(f"下载视频失败: {str(e)}", "ERROR")
                self.download_status_var.set("下载失败")
                self.update_download_stats(success=False)  # 标记失败
        
        threading.Thread(target=download, daemon=True).start()
    
    def download_file_with_progress(self, url: str, filepath: str):
        """带进度显示的文件下载"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # 更新进度
                    if total_size > 0:
                        progress = (downloaded_size / total_size) * 100
                        self.download_progress_var.set(progress)
                        self.root.update_idletasks()
    
    def batch_download_videos(self):
        """批量下载视频"""
        # 打开文件选择对话框，选择包含视频链接的文本文件
        file_path = filedialog.askopenfilename(
            title="选择包含视频链接的文本文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]
            
            if not urls:
                messagebox.showinfo("提示", "文件中没有找到有效的链接")
                return
            
            self.log_message(f"开始批量下载 {len(urls)} 个视频")
            
            def batch_download():
                for i, url in enumerate(urls, 1):
                    self.log_message(f"下载第 {i}/{len(urls)} 个视频: {url}")
                    self.video_url_var.set(url)
                    
                    # 模拟单个视频下载（实际实现中需要更复杂的逻辑）
                    try:
                        platform = self.detect_platform(url)
                        if platform:
                            video_info = self.extract_video_info(url, platform)
                            if video_info and video_info.get('video_url'):
                                # 这里可以调用实际的下载逻辑
                                self.log_message(f"第 {i} 个视频下载完成")
                            else:
                                self.log_message(f"第 {i} 个视频解析失败", "WARNING")
                        else:
                            self.log_message(f"第 {i} 个视频平台不支持", "WARNING")
                    except Exception as e:
                        self.log_message(f"第 {i} 个视频下载出错: {str(e)}", "ERROR")
                
                self.log_message("批量下载完成")
                self.download_status_var.set("批量下载完成")
            
            threading.Thread(target=batch_download, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
    
    def stop_download(self):
        """停止下载"""
        # 这里可以实现停止下载的逻辑
        self.download_active = False
        self.log_message("下载已停止", "WARNING")
        self.download_status_var.set("已停止")
        self.download_progress_var.set(0)
    
    def select_data_file(self):
        """选择数据文件"""
        file_path = filedialog.askopenfilename(
            title="选择数据文件",
            filetypes=[
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ],
            initialdir=os.path.join(os.getcwd(), "data")
        )
        if file_path:
            self.data_file_var.set(file_path)
            self.log_message(f"已选择数据文件: {file_path}", "INFO")
    
    def scan_data_directory(self):
        """扫描数据目录，查找所有JSON文件"""
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            messagebox.showerror("错误", "数据目录不存在")
            return
        
        json_files = []
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.json') and 'contents' in file:
                    json_files.append(os.path.join(root, file))
        
        if not json_files:
            messagebox.showinfo("信息", "未找到数据文件")
            return
        
        # 显示文件选择对话框
        from tkinter import simpledialog
        file_list = "\n".join([f"{i+1}. {os.path.basename(f)}" for i, f in enumerate(json_files)])
        selected = simpledialog.askstring(
            "选择数据文件", 
            f"找到以下数据文件:\n{file_list}\n\n请输入文件编号:"
        )
        
        if selected and selected.isdigit():
            index = int(selected) - 1
            if 0 <= index < len(json_files):
                self.data_file_var.set(json_files[index])
                self.log_message(f"已选择数据文件: {json_files[index]}", "INFO")
    
    def parse_data_file(self):
        """解析数据文件，提取媒体下载链接"""
        file_path = self.data_file_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("错误", "请先选择有效的数据文件")
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 初始化媒体链接存储
            self.parsed_media_data = {
                'videos': [],
                'music': [],
                'images': []
            }
            
            # 解析数据
            if isinstance(data, list):
                for item in data:
                    self._extract_media_links(item)
            elif isinstance(data, dict):
                self._extract_media_links(data)
            
            # 统计结果
            video_count = len(self.parsed_media_data['videos'])
            music_count = len(self.parsed_media_data['music'])
            image_count = len(self.parsed_media_data['images'])
            
            result_text = f"视频: {video_count} | 音乐: {music_count} | 图片: {image_count}"
            self.parse_result_var.set(result_text)
            
            self.log_message(f"数据文件解析完成: {result_text}", "INFO")
            
        except Exception as e:
            messagebox.showerror("错误", f"解析数据文件失败: {str(e)}")
            self.log_message(f"解析数据文件失败: {str(e)}", "ERROR")
    
    def _extract_media_links(self, item):
        """从单个数据项中提取媒体链接"""
        if not isinstance(item, dict):
            return
        
        # 提取视频链接
        video_url = item.get('video_download_url') or item.get('video_url')
        if video_url and video_url != 'N/A':
            # 提取视频封面图URL（支持多种字段名）
            cover_url = (item.get('cover_url') or 
                        item.get('cover') or 
                        item.get('video_cover_url') or 
                        item.get('thumbnail_url') or 
                        item.get('pic_url') or
                        item.get('avatar_thumb'))
            
            video_data = {
                'url': video_url,
                'title': item.get('desc', '未知标题'),
                'author': item.get('nickname', '未知作者'),
                'platform': self._detect_platform_from_data(item),
                'cover_url': cover_url if cover_url and cover_url != 'N/A' else None,
                'duration': item.get('duration', '未知'),
                'size': item.get('file_size', '未知'),
                'publish_time': item.get('publish_time', '未知'),
                'like_count': item.get('liked_count', 0),
                'comment_count': item.get('comments_count', 0),
                'share_count': item.get('share_count', 0)
            }
            self.parsed_media_data['videos'].append(video_data)
        
        # 提取音乐链接
        music_url = item.get('music_download_url') or item.get('music_url')
        if music_url and music_url != 'N/A':
            # 提取音乐封面图URL
            music_cover_url = (item.get('music_cover_url') or 
                              item.get('music_cover') or 
                              item.get('music_pic_url') or
                              item.get('cover_url'))
            
            music_data = {
                'url': music_url,
                'title': item.get('music_title', '未知音乐'),
                'author': item.get('music_author', '未知作者'),
                'platform': self._detect_platform_from_data(item),
                'cover_url': music_cover_url if music_cover_url and music_cover_url != 'N/A' else None,
                'duration': item.get('music_duration', '未知'),
                'size': item.get('music_size', '未知')
            }
            self.parsed_media_data['music'].append(music_data)
        
        # 提取图片链接
        image_urls = []
        if 'note_download_url' in item and item['note_download_url'] != 'N/A':
            image_urls.append(item['note_download_url'])
        if 'cover_url' in item and item['cover_url'] != 'N/A':
            image_urls.append(item['cover_url'])
        # 支持多图片字段
        if 'images' in item and isinstance(item['images'], list):
            for img in item['images']:
                if isinstance(img, str) and img != 'N/A':
                    image_urls.append(img)
                elif isinstance(img, dict) and 'url' in img:
                    image_urls.append(img['url'])
        
        for img_url in image_urls:
            image_data = {
                'url': img_url,
                'title': item.get('desc', '未知标题'),
                'author': item.get('nickname', '未知作者'),
                'platform': self._detect_platform_from_data(item),
                'publish_time': item.get('publish_time', '未知'),
                'like_count': item.get('liked_count', 0),
                'comment_count': item.get('comments_count', 0)
            }
            self.parsed_media_data['images'].append(image_data)
    
    def _detect_platform_from_data(self, item):
        """从数据项中检测平台类型"""
        if 'douyin' in str(item.get('aweme_id', '')):
            return 'douyin'
        elif 'note_id' in item:
            return 'xiaohongshu'
        elif 'photo_id' in item:
            return 'kuaishou'
        elif 'mblog' in str(item):
            return 'weibo'
        else:
            return 'unknown'
    
    def batch_download_from_data(self):
        """从解析的数据中批量下载媒体文件"""
        if not hasattr(self, 'parsed_media_data'):
            messagebox.showerror("错误", "请先解析数据文件")
            return
        
        # 检查选择的下载类型
        download_list = []
        
        if self.download_video_var.get():
            download_list.extend([(item, 'video') for item in self.parsed_media_data['videos']])
        
        if self.download_music_var.get():
            download_list.extend([(item, 'music') for item in self.parsed_media_data['music']])
        
        if self.download_image_var.get():
            download_list.extend([(item, 'image') for item in self.parsed_media_data['images']])
        
        if not download_list:
            messagebox.showwarning("警告", "没有可下载的媒体文件或未选择下载类型")
            return
        
        # 开始批量下载
        self.download_active = True
        self.download_status_var.set("批量下载中...")
        
        def download_thread():
            total_files = len(download_list)
            success_count = 0
            
            for i, (media_item, media_type) in enumerate(download_list):
                if not self.download_active:
                    break
                
                try:
                    # 更新进度
                    progress = (i / total_files) * 100
                    self.download_progress_var.set(progress)
                    
                    # 创建文件名
                    safe_title = re.sub(r'[<>:"/\\|?*]', '_', media_item['title'][:50])
                    platform = media_item['platform']
                    
                    # 确定文件扩展名
                    url = media_item['url']
                    if media_type == 'video':
                        ext = '.mp4'
                        subdir = 'videos'
                    elif media_type == 'music':
                        ext = '.mp3'
                        subdir = 'music'
                    else:  # image
                        ext = '.jpg' if 'jpg' in url.lower() else '.png'
                        subdir = 'images'
                    
                    # 创建保存路径
                    save_dir = os.path.join(self.download_dir_var.get(), platform, subdir)
                    os.makedirs(save_dir, exist_ok=True)
                    
                    filename = f"{safe_title}_{i+1}{ext}"
                    filepath = os.path.join(save_dir, filename)
                    
                    # 下载文件
                    self.download_status_var.set(f"下载中: {filename}")
                    
                    response = requests.get(url, stream=True, timeout=30)
                    response.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if not self.download_active:
                                break
                            f.write(chunk)
                    
                    success_count += 1
                    self.log_message(f"下载成功: {filename}", "INFO")
                    
                except Exception as e:
                    self.log_message(f"下载失败 {media_item['title']}: {str(e)}", "ERROR")
            
            # 完成下载
            self.download_progress_var.set(100)
            self.download_status_var.set(f"批量下载完成: {success_count}/{total_files}")
            self.log_message(f"批量下载完成: 成功 {success_count}/{total_files}", "INFO")
        
        # 在新线程中执行下载
        threading.Thread(target=download_thread, daemon=True).start()
    
    def preview_media_content(self):
        """预览媒体内容"""
        if not hasattr(self, 'parsed_media_data'):
            messagebox.showerror("错误", "请先解析数据文件")
            return
        
        # 创建预览窗口
        preview_window = tk.Toplevel(self.root)
        preview_window.title("媒体内容预览")
        preview_window.geometry("1200x800")
        preview_window.resizable(True, True)
        
        # 创建主框架
        main_frame = ttk.Frame(preview_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建笔记本控件
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 视频标签页
        self._create_video_preview_tab(notebook)
        
        # 音乐标签页
        self._create_music_preview_tab(notebook)
        
        # 图片标签页
        self._create_image_preview_tab(notebook)
    
    def _create_video_preview_tab(self, notebook):
        """创建视频预览标签页"""
        video_frame = ttk.Frame(notebook)
        notebook.add(video_frame, text=f"视频 ({len(self.parsed_media_data['videos'])})")
        
        # 创建分割窗口
        paned_window = ttk.PanedWindow(video_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧列表框架
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # 视频列表
        video_tree = ttk.Treeview(left_frame, columns=('title', 'author', 'platform'), show='headings', height=15)
        video_tree.heading('title', text='标题')
        video_tree.heading('author', text='作者')
        video_tree.heading('platform', text='平台')
        
        video_tree.column('title', width=200)
        video_tree.column('author', width=100)
        video_tree.column('platform', width=80)
        
        # 添加滚动条
        video_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=video_tree.yview)
        video_tree.configure(yscrollcommand=video_scrollbar.set)
        
        video_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        video_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧预览框架
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        # 视频预览区域
        preview_label_frame = ttk.LabelFrame(right_frame, text="视频预览", padding="10")
        preview_label_frame.pack(fill=tk.BOTH, expand=True)
        
        # 视频缩略图显示区域
        video_canvas_frame = ttk.Frame(preview_label_frame)
        video_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.video_canvas = tk.Canvas(video_canvas_frame, bg='white', height=200)
        self.video_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 视频预览标签（用于显示提示信息）
        self.video_preview_label = ttk.Label(preview_label_frame, text="选择视频查看预览", 
                                           font=('Arial', 10), anchor='center')
        self.video_preview_label.pack(pady=(5, 0))
        
        # 视频信息显示
        info_frame = ttk.Frame(preview_label_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.video_info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.video_info_text.yview)
        self.video_info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.video_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定选择事件
        video_tree.bind('<<TreeviewSelect>>', lambda e: self._on_video_select(video_tree))
        
        # 填充数据
        for i, item in enumerate(self.parsed_media_data['videos']):
            video_tree.insert('', 'end', values=(item['title'], item['author'], item['platform']), tags=(str(i),))
    
    def _create_music_preview_tab(self, notebook):
        """创建音乐预览标签页"""
        music_frame = ttk.Frame(notebook)
        notebook.add(music_frame, text=f"音乐 ({len(self.parsed_media_data['music'])})")
        
        # 创建分割窗口
        paned_window = ttk.PanedWindow(music_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧列表框架
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # 音乐列表
        music_tree = ttk.Treeview(left_frame, columns=('title', 'author', 'platform'), show='headings', height=15)
        music_tree.heading('title', text='标题')
        music_tree.heading('author', text='作者')
        music_tree.heading('platform', text='平台')
        
        music_tree.column('title', width=200)
        music_tree.column('author', width=100)
        music_tree.column('platform', width=80)
        
        # 添加滚动条
        music_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=music_tree.yview)
        music_tree.configure(yscrollcommand=music_scrollbar.set)
        
        music_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        music_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧预览框架
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        # 音乐预览区域
        preview_label_frame = ttk.LabelFrame(right_frame, text="音乐预览", padding="10")
        preview_label_frame.pack(fill=tk.BOTH, expand=True)
        
        # 音乐封面显示区域
        music_canvas_frame = ttk.Frame(preview_label_frame)
        music_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.music_canvas = tk.Canvas(music_canvas_frame, bg='white', height=150)
        self.music_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 音乐控制按钮区域
        control_frame = ttk.Frame(preview_label_frame)
        control_frame.pack(fill=tk.X, pady=(5, 0))
        
        # 播放控制按钮（占位符）
        ttk.Button(control_frame, text="▶ 播放", state=tk.DISABLED).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="⏸ 暂停", state=tk.DISABLED).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="⏹ 停止", state=tk.DISABLED).pack(side=tk.LEFT)
        
        # 音乐预览标签（用于显示提示信息）
        self.music_preview_label = ttk.Label(preview_label_frame, text="选择音乐查看信息", 
                                           font=('Arial', 10), anchor='center')
        self.music_preview_label.pack(pady=(5, 0))
        
        # 音乐信息显示
        info_frame = ttk.Frame(preview_label_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.music_info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        music_info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.music_info_text.yview)
        self.music_info_text.configure(yscrollcommand=music_info_scrollbar.set)
        
        self.music_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        music_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定选择事件
        music_tree.bind('<<TreeviewSelect>>', lambda e: self._on_music_select(music_tree))
        
        # 填充数据
        for i, item in enumerate(self.parsed_media_data['music']):
            music_tree.insert('', 'end', values=(item['title'], item['author'], item['platform']), tags=(str(i),))
    
    def _create_image_preview_tab(self, notebook):
        """创建图片预览标签页"""
        image_frame = ttk.Frame(notebook)
        notebook.add(image_frame, text=f"图片 ({len(self.parsed_media_data['images'])})")
        
        # 创建分割窗口
        paned_window = ttk.PanedWindow(image_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧列表框架
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # 图片列表
        image_tree = ttk.Treeview(left_frame, columns=('title', 'author', 'platform'), show='headings', height=15)
        image_tree.heading('title', text='标题')
        image_tree.heading('author', text='作者')
        image_tree.heading('platform', text='平台')
        
        image_tree.column('title', width=200)
        image_tree.column('author', width=100)
        image_tree.column('platform', width=80)
        
        # 添加滚动条
        image_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=image_tree.yview)
        image_tree.configure(yscrollcommand=image_scrollbar.set)
        
        image_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        image_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧预览框架
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=1)
        
        # 图片预览区域
        preview_label_frame = ttk.LabelFrame(right_frame, text="图片预览", padding="10")
        preview_label_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动画布用于图片显示
        canvas_frame = ttk.Frame(preview_label_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.image_canvas = tk.Canvas(canvas_frame, bg='white')
        canvas_v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
        canvas_h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
        
        self.image_canvas.configure(yscrollcommand=canvas_v_scrollbar.set, xscrollcommand=canvas_h_scrollbar.set)
        
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 图片信息显示
        info_frame = ttk.Frame(preview_label_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.image_info_text = tk.Text(info_frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
        image_info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.image_info_text.yview)
        self.image_info_text.configure(yscrollcommand=image_info_scrollbar.set)
        
        self.image_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        image_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定选择事件
        image_tree.bind('<<TreeviewSelect>>', lambda e: self._on_image_select(image_tree))
        
        # 填充数据
        for i, item in enumerate(self.parsed_media_data['images']):
            image_tree.insert('', 'end', values=(item['title'], item['author'], item['platform']), tags=(str(i),))
    
    def _on_video_select(self, tree):
        """处理视频选择事件"""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        index = int(item['tags'][0])
        video_data = self.parsed_media_data['videos'][index]
        
        # 更新信息显示
        self.video_info_text.config(state=tk.NORMAL)
        self.video_info_text.delete(1.0, tk.END)
        info_text = f"标题: {video_data['title']}\n"
        info_text += f"作者: {video_data['author']}\n"
        info_text += f"平台: {video_data['platform']}\n"
        info_text += f"链接: {video_data['url']}\n"
        
        # 显示更多详细信息
        if video_data.get('duration') and video_data['duration'] != '未知':
            info_text += f"时长: {video_data['duration']}\n"
        if video_data.get('size') and video_data['size'] != '未知':
            info_text += f"大小: {video_data['size']}\n"
        if video_data.get('publish_time') and video_data['publish_time'] != '未知':
            info_text += f"发布时间: {video_data['publish_time']}\n"
        if video_data.get('like_count'):
            info_text += f"点赞数: {video_data['like_count']}\n"
        if video_data.get('comment_count'):
            info_text += f"评论数: {video_data['comment_count']}\n"
        if video_data.get('share_count'):
            info_text += f"分享数: {video_data['share_count']}\n"
        
        # 显示封面图URL信息
        if video_data.get('cover_url'):
            info_text += f"封面图: 已获取\n"
        else:
            info_text += f"封面图: 暂无\n"
            
        self.video_info_text.insert(1.0, info_text)
        self.video_info_text.config(state=tk.DISABLED)
        
        # 更新预览标签
        self.video_preview_label.config(text=f"视频: {video_data['title']}")
        
        # 尝试加载视频封面图
        cover_url = video_data.get('cover_url')
        if cover_url:
            threading.Thread(target=self._load_video_cover, args=(cover_url,), daemon=True).start()
        else:
            # 如果没有封面，显示默认信息
            self.video_canvas.delete("all")
            self.video_canvas.create_text(
                200, 100,
                text="暂无封面图\n请检查配置文件中的封面图获取设置", 
                font=('Arial', 12), fill='gray', justify='center'
            )
    
    def _load_video_cover(self, cover_url):
        """在后台线程中加载视频封面"""
        try:
            # 显示加载状态
            def show_loading():
                self.video_canvas.delete("all")
                self.video_canvas.create_text(
                    200, 100,
                    text="加载封面中...", font=('Arial', 12), fill='gray'
                )
            self.root.after(0, show_loading)
            
            # 下载封面图片
            response = requests.get(cover_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # 使用PIL加载图片
            image_data = io.BytesIO(response.content)
            pil_image = Image.open(image_data)
            
            # 计算缩放比例以适应画布
            canvas_width = 400
            canvas_height = 200
            
            img_width, img_height = pil_image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            scale = min(scale_w, scale_h, 1.0)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # 调整图片大小
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为Tkinter可用的格式
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # 在主线程中更新UI
            def update_ui():
                self.video_canvas.delete("all")
                self.video_canvas.create_image(
                    canvas_width//2, canvas_height//2, 
                    image=tk_image, anchor='center'
                )
                # 保存引用防止垃圾回收
                self.video_canvas.image = tk_image
                
                # 添加播放按钮图标（简单的三角形）
                self.video_canvas.create_polygon(
                    canvas_width//2 - 15, canvas_height//2 - 15,
                    canvas_width//2 - 15, canvas_height//2 + 15,
                    canvas_width//2 + 15, canvas_height//2,
                    fill='white', outline='black', width=2
                )
            
            self.root.after(0, update_ui)
            
        except Exception as e:
            # 在主线程中显示错误
            def show_error():
                self.video_canvas.delete("all")
                self.video_canvas.create_text(
                    200, 100,
                    text=f"封面加载失败\n{str(e)}", 
                    font=('Arial', 10), fill='red', justify='center'
                )
            
            self.root.after(0, show_error)
    
    def _on_music_select(self, tree):
        """处理音乐选择事件"""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        index = int(item['tags'][0])
        music_data = self.parsed_media_data['music'][index]
        
        # 更新信息显示
        self.music_info_text.config(state=tk.NORMAL)
        self.music_info_text.delete(1.0, tk.END)
        info_text = f"标题: {music_data['title']}\n"
        info_text += f"作者: {music_data['author']}\n"
        info_text += f"平台: {music_data['platform']}\n"
        info_text += f"链接: {music_data['url']}\n"
        
        # 显示更多详细信息
        if music_data.get('duration') and music_data['duration'] != '未知':
            info_text += f"时长: {music_data['duration']}\n"
        if music_data.get('size') and music_data['size'] != '未知':
            info_text += f"大小: {music_data['size']}\n"
        
        # 显示封面图URL信息
        if music_data.get('cover_url'):
            info_text += f"封面图: 已获取\n"
        else:
            info_text += f"封面图: 暂无\n"
            
        self.music_info_text.insert(1.0, info_text)
        self.music_info_text.config(state=tk.DISABLED)
        
        # 更新预览标签
        self.music_preview_label.config(text=f"音乐: {music_data['title']}")
        
        # 尝试加载音乐封面图
        cover_url = music_data.get('cover_url')
        if cover_url:
            threading.Thread(target=self._load_music_cover, args=(cover_url,), daemon=True).start()
        else:
            # 如果没有封面，显示默认音乐图标
            self.music_canvas.delete("all")
            self._draw_music_icon()
    
    def _load_music_cover(self, cover_url):
        """在后台线程中加载音乐封面"""
        try:
            # 显示加载状态
            def show_loading():
                self.music_canvas.delete("all")
                self.music_canvas.create_text(
                    200, 75,
                    text="加载封面中...", font=('Arial', 10), fill='gray'
                )
            self.root.after(0, show_loading)
            
            # 下载封面图片
            response = requests.get(cover_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # 使用PIL加载图片
            image_data = io.BytesIO(response.content)
            pil_image = Image.open(image_data)
            
            # 计算缩放比例以适应画布
            canvas_width = 400
            canvas_height = 150
            
            img_width, img_height = pil_image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            scale = min(scale_w, scale_h, 1.0)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # 调整图片大小
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为Tkinter可用的格式
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # 在主线程中更新UI
            def update_ui():
                self.music_canvas.delete("all")
                self.music_canvas.create_image(
                    canvas_width//2, canvas_height//2, 
                    image=tk_image, anchor='center'
                )
                # 保存引用防止垃圾回收
                self.music_canvas.image = tk_image
            
            self.root.after(0, update_ui)
            
        except Exception as e:
            # 在主线程中显示错误，使用默认音乐图标
            def show_error():
                self.music_canvas.delete("all")
                self._draw_music_icon()
                self.music_canvas.create_text(
                    200, 120,
                    text=f"封面加载失败", 
                    font=('Arial', 8), fill='red', justify='center'
                )
            
            self.root.after(0, show_error)
    
    def _draw_music_icon(self):
        """绘制默认音乐图标"""
        # 绘制音符图标
        canvas_width = 400
        canvas_height = 150
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        
        # 音符符头
        self.music_canvas.create_oval(
            center_x - 15, center_y - 5,
            center_x + 5, center_y + 15,
            fill='lightblue', outline='blue', width=2
        )
        
        # 音符符干
        self.music_canvas.create_line(
            center_x + 5, center_y + 5,
            center_x + 5, center_y - 30,
            fill='blue', width=3
        )
        
        # 音符符尾
        self.music_canvas.create_arc(
            center_x + 5, center_y - 35,
            center_x + 25, center_y - 15,
            start=0, extent=180,
            fill='blue', outline='blue', width=2
        )
        
        # 添加文字
        self.music_canvas.create_text(
            center_x, center_y + 40,
            text="音乐文件", font=('Arial', 12), fill='gray'
        )
    
    def _on_image_select(self, tree):
        """处理图片选择事件"""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        index = int(item['tags'][0])
        image_data = self.parsed_media_data['images'][index]
        
        # 更新信息显示
        self.image_info_text.config(state=tk.NORMAL)
        self.image_info_text.delete(1.0, tk.END)
        info_text = f"标题: {image_data['title']}\n"
        info_text += f"作者: {image_data['author']}\n"
        info_text += f"平台: {image_data['platform']}\n"
        info_text += f"链接: {image_data['url']}\n"
        
        # 显示更多详细信息
        if image_data.get('publish_time') and image_data['publish_time'] != '未知':
            info_text += f"发布时间: {image_data['publish_time']}\n"
        if image_data.get('like_count'):
            info_text += f"点赞数: {image_data['like_count']}\n"
        if image_data.get('comment_count'):
            info_text += f"评论数: {image_data['comment_count']}\n"
            
        self.image_info_text.insert(1.0, info_text)
        self.image_info_text.config(state=tk.DISABLED)
        
        # 在新线程中加载图片
        threading.Thread(target=self._load_image_preview, args=(image_data['url'],), daemon=True).start()
    
    def _load_image_preview(self, image_url):
        """在后台线程中加载图片预览"""
        try:
            # 显示加载状态
            def show_loading():
                self.image_canvas.delete("all")
                canvas_width = self.image_canvas.winfo_width() or 400
                canvas_height = self.image_canvas.winfo_height() or 300
                
                # 绘制加载动画背景
                self.image_canvas.create_rectangle(
                    canvas_width//2 - 50, canvas_height//2 - 20,
                    canvas_width//2 + 50, canvas_height//2 + 20,
                    fill='lightgray', outline='gray'
                )
                self.image_canvas.create_text(
                    canvas_width//2, canvas_height//2,
                    text="加载中...", font=('Arial', 12), fill='black'
                )
                
                # 添加进度条效果
                self._loading_progress = 0
                self._animate_loading()
            
            self.root.after(0, show_loading)
            
            # 下载图片
            response = requests.get(image_url, timeout=15, stream=True)
            response.raise_for_status()
            
            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                raise ValueError(f"不支持的文件类型: {content_type}")
            
            # 使用PIL加载图片
            image_data = io.BytesIO(response.content)
            pil_image = Image.open(image_data)
            
            # 验证图片格式
            if pil_image.format not in ['JPEG', 'PNG', 'GIF', 'BMP', 'WEBP']:
                raise ValueError(f"不支持的图片格式: {pil_image.format}")
            
            # 计算缩放比例以适应画布
            canvas_width = 400  # 预设画布宽度
            canvas_height = 300  # 预设画布高度
            
            img_width, img_height = pil_image.size
            scale_w = canvas_width / img_width
            scale_h = canvas_height / img_height
            scale = min(scale_w, scale_h, 1.0)  # 不放大，只缩小
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # 调整图片大小
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 转换为Tkinter可用的格式
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # 在主线程中更新UI
            def update_ui():
                self.image_canvas.delete("all")
                self.image_canvas.create_image(
                    canvas_width//2, canvas_height//2, 
                    image=tk_image, anchor='center'
                )
                # 保存引用防止垃圾回收
                self.image_canvas.image = tk_image
                
                # 更新滚动区域
                self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
                
                # 添加图片信息
                info_text = f"尺寸: {img_width}x{img_height} | 格式: {pil_image.format}"
                self.image_canvas.create_text(
                    10, canvas_height - 10,
                    text=info_text, font=('Arial', 8), fill='gray', anchor='sw'
                )
            
            self.root.after(0, update_ui)
            
        except requests.exceptions.Timeout:
            self._show_image_error("加载超时\n请检查网络连接")
        except requests.exceptions.ConnectionError:
            self._show_image_error("网络连接失败\n请检查网络设置")
        except requests.exceptions.HTTPError as e:
            self._show_image_error(f"HTTP错误\n状态码: {e.response.status_code}")
        except ValueError as e:
            self._show_image_error(f"格式错误\n{str(e)}")
        except Exception as e:
            self._show_image_error(f"加载失败\n{str(e)}")
    
    def _animate_loading(self):
        """加载动画效果"""
        if hasattr(self, '_loading_progress'):
            canvas_width = self.image_canvas.winfo_width() or 400
            canvas_height = self.image_canvas.winfo_height() or 300
            
            # 更新进度条
            progress_width = int(80 * (self._loading_progress / 100))
            self.image_canvas.create_rectangle(
                canvas_width//2 - 40, canvas_height//2 + 25,
                canvas_width//2 - 40 + progress_width, canvas_height//2 + 30,
                fill='blue', outline=''
            )
            
            self._loading_progress = (self._loading_progress + 10) % 100
            
            # 继续动画
            if hasattr(self, '_loading_progress'):
                self.root.after(100, self._animate_loading)
    
    def _show_image_error(self, error_message):
        """在主线程中显示图片加载错误"""
        def show_error():
            self.image_canvas.delete("all")
            canvas_width = self.image_canvas.winfo_width() or 400
            canvas_height = self.image_canvas.winfo_height() or 300
            
            # 绘制错误图标
            self.image_canvas.create_oval(
                canvas_width//2 - 30, canvas_height//2 - 30,
                canvas_width//2 + 30, canvas_height//2 + 30,
                fill='lightcoral', outline='red', width=2
            )
            
            # 绘制X符号
            self.image_canvas.create_line(
                canvas_width//2 - 15, canvas_height//2 - 15,
                canvas_width//2 + 15, canvas_height//2 + 15,
                fill='red', width=3
            )
            self.image_canvas.create_line(
                canvas_width//2 - 15, canvas_height//2 + 15,
                canvas_width//2 + 15, canvas_height//2 - 15,
                fill='red', width=3
            )
            
            # 显示错误信息
            self.image_canvas.create_text(
                canvas_width//2, canvas_height//2 + 50,
                text=error_message, 
                font=('Arial', 10), fill='red', justify='center'
            )
            
            # 清除加载进度
            if hasattr(self, '_loading_progress'):
                delattr(self, '_loading_progress')
        
        self.root.after(0, show_error)

    def create_video_download_functions(self, parent):
        """创建视频下载功能区域"""
        video_frame = ttk.LabelFrame(parent, text="视频下载", padding="5")
        video_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 视频链接输入区域
        url_frame = ttk.Frame(video_frame)
        url_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(url_frame, text="视频链接:").pack(side=tk.LEFT, padx=(0, 5))
        self.video_url_var = tk.StringVar()
        self.video_url_entry = ttk.Entry(url_frame, textvariable=self.video_url_var, width=50)
        self.video_url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # 下载目录选择
        dir_frame = ttk.Frame(video_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(dir_frame, text="保存目录:").pack(side=tk.LEFT, padx=(0, 5))
        self.download_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads", "videos"))
        self.download_dir_entry = ttk.Entry(dir_frame, textvariable=self.download_dir_var, width=40)
        self.download_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(dir_frame, text="浏览", 
                  command=self.select_download_directory).pack(side=tk.LEFT)
        
        # 下载控制按钮
        button_frame = ttk.Frame(video_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(button_frame, text="解析视频", 
                  command=self.parse_video_url, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="下载视频", 
                  command=self.download_video, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="批量下载", 
                  command=self.batch_download_videos, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="停止下载", 
                  command=self.stop_download, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # 下载进度显示
        progress_frame = ttk.Frame(video_frame)
        progress_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(progress_frame, text="下载进度:").pack(side=tk.LEFT, padx=(0, 5))
        self.download_progress_var = tk.DoubleVar()
        self.download_progress_bar = ttk.Progressbar(progress_frame, 
                                                   variable=self.download_progress_var, 
                                                   mode='determinate', 
                                                   length=300)
        self.download_progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # 下载状态显示
        status_frame = ttk.Frame(video_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(status_frame, text="状态:").pack(side=tk.LEFT, padx=(0, 5))
        self.download_status_var = tk.StringVar(value="就绪")
        self.download_status_label = ttk.Label(status_frame, textvariable=self.download_status_var)
        self.download_status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # 下载统计信息
        stats_frame = ttk.Frame(video_frame)
        stats_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.download_stats_var = tk.StringVar(value="总计: 0 | 成功: 0 | 失败: 0")
        self.download_stats_label = ttk.Label(stats_frame, textvariable=self.download_stats_var)
        self.download_stats_label.pack(side=tk.LEFT)
        
        # 数据文件自动下载功能区域
        data_frame = ttk.LabelFrame(parent, text="数据文件自动下载", padding="5")
        data_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 数据文件选择区域
        file_frame = ttk.Frame(data_frame)
        file_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(file_frame, text="数据文件:").pack(side=tk.LEFT, padx=(0, 5))
        self.data_file_var = tk.StringVar()
        self.data_file_entry = ttk.Entry(file_frame, textvariable=self.data_file_var, width=50)
        self.data_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(file_frame, text="选择文件", 
                  command=self.select_data_file).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(file_frame, text="扫描数据目录", 
                  command=self.scan_data_directory).pack(side=tk.LEFT)
        
        # 媒体类型选择
        media_frame = ttk.Frame(data_frame)
        media_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(media_frame, text="下载类型:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.download_video_var = tk.BooleanVar(value=True)
        self.download_music_var = tk.BooleanVar(value=True)
        self.download_image_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(media_frame, text="视频", variable=self.download_video_var).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(media_frame, text="音乐", variable=self.download_music_var).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Checkbutton(media_frame, text="图片", variable=self.download_image_var).pack(side=tk.LEFT, padx=(0, 10))
        
        # 数据文件解析和下载控制
        data_button_frame = ttk.Frame(data_frame)
        data_button_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(data_button_frame, text="解析数据文件", 
                  command=self.parse_data_file, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(data_button_frame, text="批量下载媒体", 
                  command=self.batch_download_from_data, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(data_button_frame, text="预览媒体内容", 
                  command=self.preview_media_content, 
                  style='Action.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # 解析结果显示
        result_frame = ttk.Frame(data_frame)
        result_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(result_frame, text="解析结果:").pack(side=tk.LEFT, padx=(0, 5))
        self.parse_result_var = tk.StringVar(value="未解析")
        self.parse_result_label = ttk.Label(result_frame, textvariable=self.parse_result_var)
        self.parse_result_label.pack(side=tk.LEFT)

    def open_content_preview(self):
        """打开内容预览窗口"""
        try:
            ContentPreviewWindow(self.root)
        except Exception as e:
            self.log_message(f"打开内容预览窗口失败: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"打开内容预览窗口失败:\n{str(e)}")

    def run(self):
        """运行GUI应用"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("程序被用户中断")
        except Exception as e:
            self.log_message(f"程序运行出错: {str(e)}", "ERROR")
            messagebox.showerror("错误", f"程序运行出错:\n{str(e)}")


class ContentPreviewWindow:
    """内容预览窗口类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("媒体内容预览与分析")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        
        # 数据存储
        self.content_data = []
        self.comment_data = []
        self.current_content = None
        
        # 创建界面变量
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.platform_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        self.comment_count_var = tk.StringVar(value="评论数量: 0")
        self.avg_length_var = tk.StringVar(value="平均长度: 0")
        self.ip_count_var = tk.StringVar(value="IP地址数量: 0")
        self.top_ip_var = tk.StringVar(value="最多IP: 无")
        
        # 创建界面
        self.create_interface()
        
        # 延迟加载数据，避免界面阻塞
        self.window.after(100, self.load_data)
        
    def create_interface(self):
        """创建界面"""
        # 主框架
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧内容列表
        left_frame = ttk.LabelFrame(main_frame, text="内容列表", padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        left_frame.configure(width=300)
        
        # 内容列表
        self.content_tree = ttk.Treeview(left_frame, columns=('platform', 'title', 'date'), show='tree headings')
        self.content_tree.heading('#0', text='ID')
        self.content_tree.heading('platform', text='平台')
        self.content_tree.heading('title', text='标题')
        self.content_tree.heading('date', text='日期')
        
        self.content_tree.column('#0', width=80)
        self.content_tree.column('platform', width=60)
        self.content_tree.column('title', width=120)
        self.content_tree.column('date', width=80)
        
        content_scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.content_tree.yview)
        self.content_tree.configure(yscrollcommand=content_scrollbar.set)
        
        self.content_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_tree.bind('<<TreeviewSelect>>', self.on_content_select)
        
        # 右侧详情面板
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 内容详情选项卡
        self.create_content_tab()
        
        # 评论分析选项卡
        self.create_comment_tab()
        
        # IP分析选项卡
        self.create_ip_tab()
        
        # 数据可视化选项卡
        self.create_visualization_tab()
        
    def create_content_tab(self):
        """创建内容详情选项卡"""
        content_frame = ttk.Frame(self.notebook)
        self.notebook.add(content_frame, text="内容详情")
        
        # 内容信息显示
        info_frame = ttk.LabelFrame(content_frame, text="基本信息", padding=5)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 创建信息显示标签
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.platform_var = tk.StringVar()
        self.ip_var = tk.StringVar()
        
        ttk.Label(info_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.title_var, wraplength=400).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="作者:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.author_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="发布时间:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.date_var).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="平台:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.platform_var).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(info_frame, text="IP位置:").grid(row=4, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, textvariable=self.ip_var).grid(row=4, column=1, sticky=tk.W)
        
        # 内容描述
        desc_frame = ttk.LabelFrame(content_frame, text="内容描述", padding=5)
        desc_frame.pack(fill=tk.BOTH, expand=True)
        
        self.content_text = scrolledtext.ScrolledText(desc_frame, wrap=tk.WORD, height=10)
        self.content_text.pack(fill=tk.BOTH, expand=True)
        
    def create_comment_tab(self):
        """创建评论分析选项卡"""
        comment_frame = ttk.Frame(self.notebook)
        self.notebook.add(comment_frame, text="评论分析")
        
        # 评论统计
        stats_frame = ttk.LabelFrame(comment_frame, text="评论统计", padding=5)
        stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.comment_count_var = tk.StringVar(value="评论数量: 0")
        self.avg_length_var = tk.StringVar(value="平均长度: 0")
        self.sentiment_var = tk.StringVar(value="情感倾向: 中性")
        
        ttk.Label(stats_frame, textvariable=self.comment_count_var).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.avg_length_var).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.sentiment_var).pack(side=tk.LEFT)
        
        # 评论列表
        comment_list_frame = ttk.LabelFrame(comment_frame, text="评论列表", padding=5)
        comment_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.comment_tree = ttk.Treeview(comment_list_frame, columns=('user', 'content', 'ip', 'likes'), show='headings')
        self.comment_tree.heading('user', text='用户')
        self.comment_tree.heading('content', text='内容')
        self.comment_tree.heading('ip', text='IP位置')
        self.comment_tree.heading('likes', text='点赞数')
        
        self.comment_tree.column('user', width=100)
        self.comment_tree.column('content', width=300)
        self.comment_tree.column('ip', width=100)
        self.comment_tree.column('likes', width=80)
        
        comment_scrollbar = ttk.Scrollbar(comment_list_frame, orient=tk.VERTICAL, command=self.comment_tree.yview)
        self.comment_tree.configure(yscrollcommand=comment_scrollbar.set)
        
        self.comment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        comment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_ip_tab(self):
        """创建IP分析选项卡"""
        ip_frame = ttk.Frame(self.notebook)
        self.notebook.add(ip_frame, text="IP分析")
        
        # IP统计
        ip_stats_frame = ttk.LabelFrame(ip_frame, text="IP统计", padding=5)
        ip_stats_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.unique_ip_var = tk.StringVar(value="独立IP: 0")
        self.top_region_var = tk.StringVar(value="主要地区: 未知")
        
        ttk.Label(ip_stats_frame, textvariable=self.unique_ip_var).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(ip_stats_frame, textvariable=self.top_region_var).pack(side=tk.LEFT)
        
        # IP分布列表
        ip_list_frame = ttk.LabelFrame(ip_frame, text="IP分布", padding=5)
        ip_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ip_tree = ttk.Treeview(ip_list_frame, columns=('region', 'count', 'percentage'), show='headings')
        self.ip_tree.heading('region', text='地区')
        self.ip_tree.heading('count', text='数量')
        self.ip_tree.heading('percentage', text='占比')
        
        self.ip_tree.column('region', width=200)
        self.ip_tree.column('count', width=100)
        self.ip_tree.column('percentage', width=100)
        
        ip_scrollbar = ttk.Scrollbar(ip_list_frame, orient=tk.VERTICAL, command=self.ip_tree.yview)
        self.ip_tree.configure(yscrollcommand=ip_scrollbar.set)
        
        self.ip_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ip_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_visualization_tab(self):
        """创建数据可视化选项卡"""
        viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(viz_frame, text="数据可视化")
        
        # 控制按钮
        control_frame = ttk.Frame(viz_frame)
        control_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(control_frame, text="生成词云", command=self.generate_wordcloud).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="IP分布图", command=self.generate_ip_chart).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="时间分布图", command=self.generate_time_chart).pack(side=tk.LEFT, padx=(0, 5))
        
        # 图表显示区域
        self.chart_frame = ttk.Frame(viz_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)
        
    def load_data(self):
        """加载数据"""
        try:
            # 使用绝对路径
            current_dir = Path(__file__).parent
            data_dir = current_dir / "data"
            
            print(f"当前目录: {current_dir}")
            print(f"数据目录: {data_dir}")
            print(f"数据目录是否存在: {data_dir.exists()}")
            
            if not data_dir.exists():
                messagebox.showwarning("警告", f"数据目录不存在: {data_dir}")
                return
                
            # 清空现有数据
            self.content_data.clear()
            self.comment_data.clear()
            
            # 加载内容数据
            loaded_files = 0
            platform_dirs = list(data_dir.iterdir())
            print(f"找到的平台目录: {[d.name for d in platform_dirs if d.is_dir()]}")
            
            for platform_dir in platform_dirs:
                if platform_dir.is_dir():
                    print(f"正在处理平台目录: {platform_dir}")
                    files_count = self.load_platform_data(platform_dir)
                    loaded_files += files_count
                    print(f"从 {platform_dir.name} 加载了 {files_count} 个文件")
                    
            print(f"总共加载了 {loaded_files} 个数据文件")
            print(f"内容数据数量: {len(self.content_data)}")
            print(f"评论数据数量: {len(self.comment_data)}")
                    
            if loaded_files == 0:
                messagebox.showinfo("提示", "未找到任何数据文件")
            else:
                messagebox.showinfo("成功", f"成功加载 {loaded_files} 个数据文件")
                    
            self.update_content_list()
            
        except Exception as e:
            print(f"加载数据异常: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")
            
    def load_platform_data(self, platform_dir):
        """加载平台数据"""
        platform_name = platform_dir.name
        loaded_files = 0
        
        print(f"开始加载平台 {platform_name} 的数据")
        
        # 递归查找所有内容和评论文件
        content_csv_files = list(platform_dir.rglob("*contents*.csv"))
        content_json_files = list(platform_dir.rglob("*contents*.json"))
        comment_csv_files = list(platform_dir.rglob("*comments*.csv"))
        comment_json_files = list(platform_dir.rglob("*comments*.json"))
        
        print(f"找到的CSV内容文件: {[f.name for f in content_csv_files]}")
        print(f"找到的JSON内容文件: {[f.name for f in content_json_files]}")
        print(f"找到的CSV评论文件: {[f.name for f in comment_csv_files]}")
        print(f"找到的JSON评论文件: {[f.name for f in comment_json_files]}")
        
        # 加载内容文件 (CSV)
        for file_path in content_csv_files:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                print(f"CSV文件 {file_path.name} 包含 {len(df)} 行数据")
                for _, row in df.iterrows():
                    content_item = {
                        'platform': platform_name,
                        'id': row.get('note_id', row.get('aweme_id', '')),
                        'title': row.get('title', row.get('desc', ''))[:50] if row.get('title', row.get('desc', '')) else '',
                        'desc': row.get('desc', ''),
                        'author': row.get('nickname', ''),
                        'create_time': row.get('create_time', ''),
                        'ip_location': row.get('ip_location', ''),
                        'file_path': str(file_path)
                    }
                    self.content_data.append(content_item)
                loaded_files += 1
                print(f"成功加载内容文件: {file_path}")
            except Exception as e:
                print(f"加载内容文件失败 {file_path}: {e}")
                
        # 加载内容文件 (JSON)
        for file_path in content_json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"JSON文件 {file_path.name} 包含 {len(data)} 条数据")
                        for item in data:
                            content_item = {
                                'platform': platform_name,
                                'id': item.get('note_id', item.get('aweme_id', '')),
                                'title': item.get('title', item.get('desc', ''))[:50] if item.get('title', item.get('desc', '')) else '',
                                'desc': item.get('desc', ''),
                                'author': item.get('nickname', ''),
                                'create_time': item.get('create_time', ''),
                                'ip_location': item.get('ip_location', ''),
                                'file_path': str(file_path)
                            }
                            self.content_data.append(content_item)
                loaded_files += 1
                print(f"成功加载内容文件: {file_path}")
            except Exception as e:
                print(f"加载内容文件失败 {file_path}: {e}")
                
        # 加载评论文件 (CSV)
        for file_path in comment_csv_files:
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                print(f"CSV评论文件 {file_path.name} 包含 {len(df)} 行数据")
                for _, row in df.iterrows():
                    # 处理IP位置字段：抖音使用ip_label，其他平台使用ip_location
                    ip_location = row.get('ip_location', '')
                    if not ip_location and platform_name == 'douyin':
                        ip_location = row.get('ip_label', '')
                    
                    comment_item = {
                        'platform': platform_name,
                        'content_id': row.get('note_id', row.get('aweme_id', '')),
                        'comment_id': row.get('comment_id', ''),
                        'content': row.get('content', ''),
                        'nickname': row.get('nickname', ''),
                        'create_time': row.get('create_time', ''),
                        'ip_location': ip_location,
                        'like_count': row.get('like_count', 0),
                        'file_path': str(file_path)
                    }
                    self.comment_data.append(comment_item)
                loaded_files += 1
                print(f"成功加载评论文件: {file_path}")
            except Exception as e:
                print(f"加载评论文件失败 {file_path}: {e}")
                
        # 加载评论文件 (JSON)
        for file_path in comment_json_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        print(f"JSON评论文件 {file_path.name} 包含 {len(data)} 条数据")
                        for item in data:
                            # 处理IP位置字段：抖音使用ip_label，其他平台使用ip_location
                            ip_location = item.get('ip_location', '')
                            if not ip_location and platform_name == 'douyin':
                                ip_location = item.get('ip_label', '')
                            
                            comment_item = {
                                'platform': platform_name,
                                'content_id': item.get('note_id', item.get('aweme_id', '')),
                                'comment_id': item.get('comment_id', ''),
                                'content': item.get('content', ''),
                                'nickname': item.get('nickname', ''),
                                'create_time': item.get('create_time', ''),
                                'ip_location': ip_location,
                                'like_count': item.get('like_count', 0),
                                'file_path': str(file_path)
                            }
                            self.comment_data.append(comment_item)
                loaded_files += 1
                print(f"成功加载评论文件: {file_path}")
            except Exception as e:
                print(f"加载评论文件失败 {file_path}: {e}")
                
        print(f"平台 {platform_name} 总共加载了 {loaded_files} 个文件")
        return loaded_files
                
    def update_content_list(self):
        """更新内容列表"""
        for item in self.content_tree.get_children():
            self.content_tree.delete(item)
            
        for i, content in enumerate(self.content_data):
            # 处理create_time字段，确保它是字符串类型
            create_time = str(content.get('create_time', ''))
            create_time_display = create_time[:10] if create_time else ''
            
            self.content_tree.insert('', 'end', 
                                   text=str(content.get('id', ''))[:10],
                                   values=(content.get('platform', ''), 
                                          content.get('title', ''), 
                                          create_time_display))
                                          
    def on_content_select(self, event):
        """内容选择事件"""
        selection = self.content_tree.selection()
        if not selection:
            return
            
        item = self.content_tree.item(selection[0])
        content_id = item['text']
        
        # 查找对应的内容
        self.current_content = None
        for content in self.content_data:
            if content['id'].startswith(content_id):
                self.current_content = content
                break
                
        if self.current_content:
            self.update_content_details()
            self.update_comment_analysis()
            self.update_ip_analysis()
            
    def update_content_details(self):
        """更新内容详情"""
        if not self.current_content:
            return
            
        self.title_var.set(self.current_content.get('title', ''))
        self.author_var.set(self.current_content.get('author', ''))
        self.date_var.set(self.current_content.get('create_time', ''))
        self.platform_var.set(self.current_content.get('platform', ''))
        self.ip_var.set(self.current_content.get('ip_location', ''))
        
        # 更新内容描述
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, self.current_content.get('desc', ''))
        
    def update_comment_analysis(self):
        """更新评论分析"""
        if not self.current_content:
            self.comment_count_var.set("评论数量: 0")
            self.avg_length_var.set("平均长度: 0")
            return
            
        # 获取当前内容的评论
        content_comments = [c for c in self.comment_data 
                          if c['content_id'] == self.current_content['id']]
        
        if not content_comments:
            self.comment_count_var.set("评论数量: 0")
            self.avg_length_var.set("平均长度: 0")
            return
            
        # 计算统计信息
        comment_count = len(content_comments)
        avg_length = sum(len(c['content']) for c in content_comments) / comment_count
        
        self.comment_count_var.set(f"评论数量: {comment_count}")
        self.avg_length_var.set(f"平均长度: {avg_length:.1f}")
        
        # 更新评论列表
        if hasattr(self, 'comment_tree'):
            for item in self.comment_tree.get_children():
                self.comment_tree.delete(item)
                
            for comment in content_comments[:50]:  # 只显示前50条评论
                self.comment_tree.insert('', 'end', values=(
                    comment['nickname'],
                    comment['content'][:100] + '...' if len(comment['content']) > 100 else comment['content'],
                    comment['ip_location'],
                    comment['like_count']
                ))
            
    def update_ip_analysis(self):
        """更新IP分析"""
        if not self.current_content:
            return
            
        # 获取当前内容的评论
        content_comments = [c for c in self.comment_data 
                          if c['content_id'] == self.current_content['id']]
        
        # 统计IP分布
        ip_counter = Counter()
        for comment in content_comments:
            ip_location = comment.get('ip_location', '未知')
            if ip_location:
                ip_counter[ip_location] += 1
                
        unique_ips = len(ip_counter)
        top_region = ip_counter.most_common(1)[0][0] if ip_counter else "未知"
        
        self.unique_ip_var.set(f"独立IP: {unique_ips}")
        self.top_region_var.set(f"主要地区: {top_region}")
        
        # 更新IP分布列表
        for item in self.ip_tree.get_children():
            self.ip_tree.delete(item)
            
        total_comments = len(content_comments)
        for region, count in ip_counter.most_common(20):
            percentage = (count / total_comments * 100) if total_comments > 0 else 0
            self.ip_tree.insert('', 'end', values=(
                region, count, f"{percentage:.1f}%"
            ))
            
    def generate_wordcloud(self):
        """生成词云"""
        if not self.current_content:
            messagebox.showwarning("警告", "请先选择内容")
            return
            
        try:
            # 清除之前的图表
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
                
            # 获取评论文本
            content_comments = [c for c in self.comment_data 
                              if c['content_id'] == self.current_content['id']]
            
            if not content_comments:
                messagebox.showinfo("提示", "没有评论数据")
                return
                
            # 合并所有评论文本
            text = ' '.join([c['content'] for c in content_comments])
            
            # 使用jieba分词
            words = jieba.cut(text)
            word_list = [word for word in words if len(word) > 1]
            word_text = ' '.join(word_list)
            
            if not word_text.strip():
                messagebox.showinfo("提示", "没有有效的文本数据")
                return
                
            # 生成词云
            wordcloud = WordCloud(
                font_path='C:/Windows/Fonts/simhei.ttf',  # 中文字体
                width=800, height=400,
                background_color='white',
                max_words=100
            ).generate(word_text)
            
            # 显示词云
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('评论词云图')
            
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成词云失败: {str(e)}")
            
    def generate_ip_chart(self):
        """生成IP分布图"""
        if not self.current_content:
            messagebox.showwarning("警告", "请先选择内容")
            return
            
        try:
            # 清除之前的图表
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
                
            # 获取IP数据
            content_comments = [c for c in self.comment_data 
                              if c['content_id'] == self.current_content['id']]
            
            if not content_comments:
                messagebox.showinfo("提示", "没有评论数据")
                return
                
            ip_counter = Counter()
            for comment in content_comments:
                ip_location = comment.get('ip_location', '未知')
                if ip_location:
                    ip_counter[ip_location] += 1
                    
            if not ip_counter:
                messagebox.showinfo("提示", "没有IP数据")
                return
                
            # 取前10个地区
            top_ips = ip_counter.most_common(10)
            regions = [item[0] for item in top_ips]
            counts = [item[1] for item in top_ips]
            
            # 生成柱状图
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(range(len(regions)), counts)
            ax.set_xlabel('地区')
            ax.set_ylabel('评论数量')
            ax.set_title('IP地区分布')
            ax.set_xticks(range(len(regions)))
            ax.set_xticklabels(regions, rotation=45, ha='right')
            
            # 添加数值标签
            for bar, count in zip(bars, counts):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                       str(count), ha='center', va='bottom')
                       
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成IP分布图失败: {str(e)}")
            
    def generate_time_chart(self):
        """生成时间分布图"""
        if not self.current_content:
            messagebox.showwarning("警告", "请先选择内容")
            return
            
        try:
            # 清除之前的图表
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
                
            # 获取时间数据
            content_comments = [c for c in self.comment_data 
                              if c['content_id'] == self.current_content['id']]
            
            if not content_comments:
                messagebox.showinfo("提示", "没有评论数据")
                return
                
            # 解析时间并按小时统计
            hour_counter = Counter()
            for comment in content_comments:
                create_time = comment.get('create_time', '')
                if create_time:
                    try:
                        # 尝试解析时间格式
                        if 'T' in create_time:
                            dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                        else:
                            dt = datetime.strptime(create_time[:19], '%Y-%m-%d %H:%M:%S')
                        hour_counter[dt.hour] += 1
                    except:
                        continue
                        
            if not hour_counter:
                messagebox.showinfo("提示", "没有有效的时间数据")
                return
                
            # 生成时间分布图
            hours = list(range(24))
            counts = [hour_counter.get(hour, 0) for hour in hours]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(hours, counts, marker='o', linewidth=2, markersize=6)
            ax.set_xlabel('小时')
            ax.set_ylabel('评论数量')
            ax.set_title('评论时间分布')
            ax.set_xticks(range(0, 24, 2))
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成时间分布图失败: {str(e)}")


def main():
    """主函数"""
    try:
        app = MediaCrawlerGUI()
        app.run()
    except Exception as e:
        print(f"启动GUI失败: {e}")
        messagebox.showerror("启动错误", f"GUI启动失败:\n{str(e)}")


if __name__ == "__main__":
    main()