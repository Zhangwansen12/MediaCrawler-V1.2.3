#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MediaCrawler 配置编辑器 - macOS版本
专为macOS系统优化的图形化配置编辑器
支持macOS原生手势、Retina显示优化、系统主题适配
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re
import json
import platform
from typing import Dict, Any, List, Tuple
import importlib.util

# 导入macOS增强功能
try:
    from .macos_enhancements import MacOSEnhancements, MacOSIntegration
except ImportError:
    from macos_enhancements import MacOSEnhancements, MacOSIntegration


class MacOSConfigEditor:
    """macOS专用配置编辑器"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.config_window = None
        self.config_data = {}
        self.config_widgets = {}
        self.current_config_file = None
        
        # 初始化macOS增强功能
        self.macos_enhancements = MacOSEnhancements()
        self.macos_integration = MacOSIntegration("MediaCrawler 配置编辑器")
        
        # 检测macOS版本和特性
        self.macos_version = self._get_macos_version()
        self.is_retina = self._detect_retina_display()
        self.dark_mode = self._detect_dark_mode()
        
        # 配置文件映射
        self.config_files = {
            "基础配置": "config/base_config.py",
            "数据库配置": "config/db_config.py",
            "小红书配置": "config/xhs_config.py",
            "抖音配置": "config/dy_config.py",
            "快手配置": "config/ks_config.py",
            "B站配置": "config/bilibili_config.py",
            "微博配置": "config/weibo_config.py",
            "贴吧配置": "config/tieba_config.py",
            "知乎配置": "config/zhihu_config.py"
        }
        
        # macOS专用配置项类型定义
        self.config_types = {
            # 基础配置类型
            "PLATFORM": {"type": "choice", "choices": ["xhs", "dy", "ks", "bili", "wb", "tieba", "zhihu"]},
            "LOGIN_TYPE": {"type": "choice", "choices": ["qrcode", "phone", "cookie"]},
            "CRAWLER_TYPE": {"type": "choice", "choices": ["search", "detail", "creator"]},
            "SAVE_DATA_OPTION": {"type": "choice", "choices": ["csv", "db", "json", "sqlite"]},
            "IP_PROXY_PROVIDER_NAME": {"type": "choice", "choices": ["kuaidaili", "wandouhttp"]},
            
            # 布尔类型
            "ENABLE_IP_PROXY": {"type": "boolean"},
            "HEADLESS": {"type": "boolean"},
            "SAVE_LOGIN_STATE": {"type": "boolean"},
            "ENABLE_CDP_MODE": {"type": "boolean"},
            "CDP_HEADLESS": {"type": "boolean"},
            "AUTO_CLOSE_BROWSER": {"type": "boolean"},
            "ENABLE_GET_MEIDAS": {"type": "boolean"},
            "ENABLE_GET_COMMENTS": {"type": "boolean"},
            "ENABLE_GET_SUB_COMMENTS": {"type": "boolean"},
            "ENABLE_GET_WORDCLOUD": {"type": "boolean"},
            "CREATOR_MODE": {"type": "boolean"},
            
            # 数字类型
            "IP_PROXY_POOL_COUNT": {"type": "integer", "min": 1, "max": 10},
            "CDP_DEBUG_PORT": {"type": "integer", "min": 1024, "max": 65535},
            "BROWSER_LAUNCH_TIMEOUT": {"type": "integer", "min": 10, "max": 300},
            "START_PAGE": {"type": "integer", "min": 1, "max": 1000},
            "CRAWLER_MAX_NOTES_COUNT": {"type": "integer", "min": 1, "max": 10000},
            "MAX_CONCURRENCY_NUM": {"type": "integer", "min": 1, "max": 10},
            "CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES": {"type": "integer", "min": 1, "max": 1000},
            "CRAWLER_MAX_SLEEP_SEC": {"type": "integer", "min": 1, "max": 60},
            "MYSQL_DB_PORT": {"type": "integer", "min": 1, "max": 65535},
            "REDIS_DB_PORT": {"type": "integer", "min": 1, "max": 65535},
            "REDIS_DB_NUM": {"type": "integer", "min": 0, "max": 15},
            "PUBLISH_TIME_TYPE": {"type": "integer", "min": 0, "max": 10},
            "MAX_NOTES_PER_DAY": {"type": "integer", "min": 1, "max": 1000},
            "BILI_QN": {"type": "choice", "choices": ["16", "32", "64", "80", "112", "116", "120"]},
            "START_CONTACTS_PAGE": {"type": "integer", "min": 1, "max": 100},
            "CRAWLER_MAX_CONTACTS_COUNT_SINGLENOTES": {"type": "integer", "min": 1, "max": 1000},
            "CRAWLER_MAX_DYNAMICS_COUNT_SINGLENOTES": {"type": "integer", "min": 1, "max": 1000},
            
            # 字符串类型
            "KEYWORDS": {"type": "string"},
            "COOKIES": {"type": "text"},
            "CUSTOM_BROWSER_PATH": {"type": "file"},
            "USER_DATA_DIR": {"type": "string"},
            "STOP_WORDS_FILE": {"type": "file"},
            "FONT_PATH": {"type": "file"},
            "MYSQL_DB_PWD": {"type": "password"},
            "MYSQL_DB_USER": {"type": "string"},
            "MYSQL_DB_HOST": {"type": "string"},
            "MYSQL_DB_NAME": {"type": "string"},
            "REDIS_DB_HOST": {"type": "string"},
            "REDIS_DB_PWD": {"type": "password"},
            "SQLITE_DB_PATH": {"type": "file"},
            "SORT_TYPE": {"type": "string"},
            "WEIBO_SEARCH_TYPE": {"type": "string"},
            "BILI_SEARCH_MODE": {"type": "string"},
            "START_DAY": {"type": "date"},
            "END_DAY": {"type": "date"},
        }
    
    def _get_macos_version(self):
        """获取macOS版本信息"""
        try:
            version = platform.mac_ver()[0]
            return version
        except:
            return "Unknown"
    
    def _detect_retina_display(self):
        """检测是否为Retina显示屏"""
        try:
            # 通过检测屏幕分辨率和DPI来判断
            root = tk.Tk()
            root.withdraw()
            dpi = root.winfo_fpixels('1i')
            root.destroy()
            return dpi > 120  # Retina显示屏通常DPI > 120
        except:
            return False
    
    def _detect_dark_mode(self):
        """检测系统是否启用深色模式"""
        try:
            import subprocess
            result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], 
                                  capture_output=True, text=True)
            return result.stdout.strip() == 'Dark'
        except:
            return False
    
    def open_config_editor(self):
        """打开macOS配置编辑器窗口"""
        if self.config_window and self.config_window.winfo_exists():
            self.config_window.lift()
            return
        
        # 创建顶级窗口
        self.config_window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.config_window.title("MediaCrawler 配置编辑器 - macOS版")
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以设置应用程序图标
            pass
        except:
            pass
        
        # 获取Retina显示信息
        self.retina_info = self.macos_enhancements.setup_retina_scaling(self.config_window)
        
        # 计算窗口大小（适配Retina显示）
        base_width = 1000
        base_height = 700
        
        if self.retina_info['is_retina']:
            width = int(base_width * self.retina_info['spacing_multiplier'])
            height = int(base_height * self.retina_info['spacing_multiplier'])
        else:
            width = base_width
            height = base_height
        
        # 设置窗口几何属性
        screen_width = self.config_window.winfo_screenwidth()
        screen_height = self.config_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.config_window.geometry(f"{width}x{height}+{x}+{y}")
        self.config_window.minsize(800, 600)
        
        # 设置macOS原生窗口样式
        self.macos_enhancements.setup_native_window_style(self.config_window)
        
        # 设置应用程序集成
        self.macos_integration.setup_app_integration(self.config_window)
        
        # 设置窗口样式和界面
        self.setup_macos_window_style()
        self.create_macos_interface()
        
        # 设置键盘快捷键
        self.setup_macos_shortcuts()
        
        # 绑定窗口关闭事件
        self.config_window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # 显示窗口
        self.config_window.focus_set()
        
        # 显示欢迎通知
        self.macos_enhancements.show_notification(
            "配置编辑器", 
            "macOS版配置编辑器已启动", 
            sound=False
        )
    
    def setup_macos_window_style(self):
        """设置macOS窗口样式"""
        # 创建样式对象
        self.style = ttk.Style()
        
        # 应用自适应主题
        self.system_colors = self.macos_enhancements.create_adaptive_style(self.style)
        self.system_fonts = self.macos_enhancements.get_system_fonts()
        
        # 设置窗口背景
        self.config_window.configure(bg=self.system_colors['bg'])
        
        # 应用毛玻璃效果（如果支持）
        self.macos_enhancements.apply_vibrancy_effect(self.config_window)
    
    def create_macos_interface(self):
        """创建macOS界面"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.config_window, style='MacOS.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建工具栏
        self.create_macos_toolbar()
        
        # 创建内容区域
        self.create_content_area()
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_macos_toolbar(self):
        """创建macOS风格工具栏"""
        # 使用原生工具栏（如果支持）
        self.toolbar = self.macos_enhancements.create_native_toolbar(self.config_window)
        
        if not self.toolbar:
            # 回退到标准工具栏
            self.toolbar = ttk.Frame(self.main_frame, style='MacOS.TFrame', height=44)
        
        self.toolbar.pack(fill=tk.X, padx=0, pady=0)
        self.toolbar.pack_propagate(False)
        
        # 工具栏内容框架
        toolbar_content = ttk.Frame(self.toolbar, style='MacOS.TFrame')
        toolbar_content.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        
        # 配置文件选择
        config_frame = ttk.Frame(toolbar_content, style='MacOS.TFrame')
        config_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Label(config_frame, text="配置文件:", style='MacOS.TLabel').pack(side=tk.LEFT, padx=(0, 8))
        
        self.config_var = tk.StringVar()
        self.config_combobox = ttk.Combobox(
            config_frame, 
            textvariable=self.config_var,
            values=list(self.config_files.keys()),
            state="readonly",
            style='MacOS.TCombobox',
            width=15
        )
        self.config_combobox.pack(side=tk.LEFT)
        self.config_combobox.bind('<<ComboboxSelected>>', self.on_config_selected)
        
        # 操作按钮
        button_frame = ttk.Frame(toolbar_content, style='MacOS.TFrame')
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮样式配置
        button_config = {
            'style': 'MacOS.TButton',
            'width': 8
        }
        
        # 加载按钮
        self.load_btn = ttk.Button(
            button_frame, 
            text="加载", 
            command=self.load_config,
            **button_config
        )
        self.load_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 保存按钮
        self.save_btn = ttk.Button(
            button_frame, 
            text="保存", 
            command=self.save_config,
            **button_config
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 重置按钮
        self.reset_btn = ttk.Button(
            button_frame, 
            text="重置", 
            command=self.reset_config,
            **button_config
        )
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 更多操作菜单按钮
        self.more_btn = ttk.Button(
            button_frame, 
            text="更多", 
            command=self.show_more_menu,
            **button_config
        )
        self.more_btn.pack(side=tk.LEFT)
    
    def create_content_area(self):
        """创建内容区域"""
        # 创建分隔线
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 1))
        
        # 创建内容框架
        content_frame = ttk.Frame(self.main_frame, style='MacOS.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 创建选项卡式界面
        self.notebook = ttk.Notebook(content_frame, style='MacOS.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # 配置编辑选项卡
        self.config_tab = ttk.Frame(self.notebook, style='MacOS.TFrame')
        self.notebook.add(self.config_tab, text="配置编辑")
        
        # 预览选项卡
        self.preview_tab = ttk.Frame(self.notebook, style='MacOS.TFrame')
        self.notebook.add(self.preview_tab, text="配置预览")
        
        # 创建配置编辑区域
        self.create_config_edit_area()
        
        # 创建预览区域
        self.create_preview_area()
    
    def create_config_edit_area(self):
        """创建配置编辑区域"""
        # 创建滚动框架
        self.canvas = tk.Canvas(
            self.config_tab, 
            bg=self.system_colors['bg'],
            highlightthickness=0
        )
        
        # 设置手势支持
        self.macos_enhancements.setup_gesture_support(self.canvas)
        
        self.scrollbar = ttk.Scrollbar(
            self.config_tab, 
            orient="vertical", 
            command=self.canvas.yview
        )
        
        self.scrollable_frame = ttk.Frame(self.canvas, style='MacOS.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 布局滚动组件
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮事件
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
    
    def create_preview_area(self):
        """创建预览区域"""
        # 创建文本预览区域
        preview_frame = ttk.Frame(self.preview_tab, style='MacOS.TFrame')
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # 预览文本框
        self.preview_text = tk.Text(
            preview_frame,
            bg=self.system_colors['entry_bg'],
            fg=self.system_colors['entry_fg'],
            font=(self.system_fonts['system_mono'], 11),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        
        # 预览滚动条
        preview_scrollbar = ttk.Scrollbar(
            preview_frame,
            orient="vertical",
            command=self.preview_text.yview
        )
        
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        # 布局预览组件
        self.preview_text.pack(side="left", fill="both", expand=True)
        preview_scrollbar.pack(side="right", fill="y")
    
    def create_status_bar(self):
        """创建状态栏"""
        # 创建分隔线
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(1, 0))
        
        # 状态栏框架
        self.status_bar = ttk.Frame(self.main_frame, style='MacOS.TFrame', height=24)
        self.status_bar.pack(fill=tk.X, padx=0, pady=0)
        self.status_bar.pack_propagate(False)
        
        # 状态栏内容
        status_content = ttk.Frame(self.status_bar, style='MacOS.TFrame')
        status_content.pack(fill=tk.BOTH, expand=True, padx=16, pady=4)
        
        # 状态标签
        self.status_label = ttk.Label(
            status_content, 
            text="就绪", 
            style='MacOS.TLabel',
            font=(self.system_fonts['system'], 9)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 系统信息标签
        system_info = f"macOS {'.'.join(map(str, self.macos_enhancements.system_version))}"
        if self.retina_info['is_retina']:
            system_info += " • Retina"
        
        self.system_info_label = ttk.Label(
            status_content,
            text=system_info,
            style='MacOS.TLabel',
            font=(self.system_fonts['system'], 9)
        )
        self.system_info_label.pack(side=tk.RIGHT)


if __name__ == "__main__":
    # 检查是否在macOS上运行
    if platform.system() != 'Darwin':
        print("此版本专为macOS设计，当前系统不支持。")
        exit(1)
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    editor = MacOSConfigEditor(root)
    editor.open_config_editor()
    
    root.mainloop()