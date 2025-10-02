#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MediaCrawler 配置编辑器
提供图形化界面来编辑各种配置文件
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re
import json
from typing import Dict, Any, List, Tuple
import importlib.util


class ConfigEditor:
    """配置编辑器主类"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.config_window = None
        self.config_data = {}
        self.config_widgets = {}
        self.current_config_file = None
        
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
        
        # 配置项类型定义
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
            
            # 快手视频统计功能配置
            "ENABLE_VIDEO_STATS": {"type": "boolean"},
            "ENABLE_BATCH_STATS": {"type": "boolean"},
            "ENABLE_ENGAGEMENT_RATE": {"type": "boolean"},
            "ENABLE_PERFORMANCE_ANALYSIS": {"type": "boolean"},
            "LOG_STATS_DATA": {"type": "boolean"},
            
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
            
            # 快手统计功能数字配置
            "BATCH_STATS_DELAY": {"type": "float", "min": 0.1, "max": 10.0},
            "TOP_VIDEOS_COUNT": {"type": "integer", "min": 1, "max": 100},
            
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
            
            # 快手统计功能字符串配置
            "TOP_VIDEOS_METRIC": {"type": "choice", "choices": ["likes", "comments", "shares", "collects", "views", "engagement_rate"]},
            "STATS_DISPLAY_LANGUAGE": {"type": "choice", "choices": ["zh", "en"]},
            
            # 列表类型
            "DY_SPECIFIED_ID_LIST": {"type": "list"},
            "DY_CREATOR_ID_LIST": {"type": "list"},
            "KS_SPECIFIED_ID_LIST": {"type": "list"},
            "KS_CREATOR_ID_LIST": {"type": "list"},
            "XHS_SPECIFIED_NOTE_URL_LIST": {"type": "list"},
            "XHS_CREATOR_ID_LIST": {"type": "list"},
            "BILI_SPECIFIED_ID_LIST": {"type": "list"},
            "BILI_CREATOR_ID_LIST": {"type": "list"},
            "WEIBO_SPECIFIED_ID_LIST": {"type": "list"},
            "WEIBO_CREATOR_ID_LIST": {"type": "list"},
            "TIEBA_SPECIFIED_ID_LIST": {"type": "list"},
            "TIEBA_NAME_LIST": {"type": "list"},
            "TIEBA_CREATOR_URL_LIST": {"type": "list"},
            "ZHIHU_CREATOR_URL_LIST": {"type": "list"},
            "ZHIHU_SPECIFIED_ID_LIST": {"type": "list"},
            
            # 字典类型
            "CUSTOM_WORDS": {"type": "dict"}
        }
    
    def open_config_editor(self):
        """打开配置编辑器窗口"""
        if self.config_window and self.config_window.winfo_exists():
            self.config_window.lift()
            return
        
        self.config_window = tk.Toplevel(self.parent)
        self.config_window.title("MediaCrawler 配置编辑器")
        self.config_window.geometry("1000x700")
        self.config_window.resizable(True, True)
        
        # 设置窗口图标和样式
        self.setup_config_window_style()
        
        # 创建主界面
        self.create_config_interface()
    
    def setup_config_window_style(self):
        """设置配置窗口样式"""
        self.config_window.configure(bg='#f0f0f0')
        
        # 创建样式
        style = ttk.Style()
        style.configure('Config.TFrame', background='#f0f0f0')
        style.configure('Config.TLabel', background='#f0f0f0', font=('Microsoft YaHei', 9))
        style.configure('Config.TButton', font=('Microsoft YaHei', 9))
    
    def create_config_interface(self):
        """创建配置编辑界面"""
        # 主框架
        main_frame = ttk.Frame(self.config_window, style='Config.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部工具栏
        toolbar_frame = ttk.Frame(main_frame, style='Config.TFrame')
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 配置文件选择
        ttk.Label(toolbar_frame, text="选择配置文件:", style='Config.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        
        self.config_file_var = tk.StringVar()
        config_combo = ttk.Combobox(toolbar_frame, textvariable=self.config_file_var, 
                                   values=list(self.config_files.keys()), 
                                   state="readonly", width=15)
        config_combo.pack(side=tk.LEFT, padx=(0, 10))
        config_combo.bind('<<ComboboxSelected>>', self.on_config_file_selected)
        
        # 操作按钮
        ttk.Button(toolbar_frame, text="加载配置", command=self.load_config, 
                  style='Config.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="保存配置", command=self.save_config, 
                  style='Config.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="重置配置", command=self.reset_config, 
                  style='Config.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="导入配置", command=self.import_config, 
                  style='Config.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="导出配置", command=self.export_config, 
                  style='Config.TButton').pack(side=tk.LEFT, padx=(0, 5))
        
        # 配置编辑区域
        self.create_config_edit_area(main_frame)
        
        # 默认选择基础配置
        self.config_file_var.set("基础配置")
        self.load_config()
    
    def create_config_edit_area(self, parent):
        """创建配置编辑区域"""
        # 创建滚动框架
        canvas = tk.Canvas(parent, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Config.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def on_config_file_selected(self, event=None):
        """配置文件选择事件"""
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        selected_config = self.config_file_var.get()
        if not selected_config or selected_config not in self.config_files:
            return
        
        config_file = self.config_files[selected_config]
        # 修复路径计算：从config_editor_gui文件夹回到项目根目录
        project_root = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(project_root, config_file)
        
        if not os.path.exists(config_path):
            messagebox.showerror("错误", f"配置文件不存在: {config_path}")
            return
        
        try:
            # 解析配置文件
            self.config_data = self.parse_config_file(config_path)
            self.current_config_file = config_path
            
            # 创建配置编辑界面
            self.create_config_widgets()
            
        except Exception as e:
            messagebox.showerror("错误", f"加载配置文件失败: {str(e)}")
    
    def parse_config_file(self, config_path: str) -> Dict[str, Any]:
        """解析配置文件"""
        config_data = {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取配置项
        patterns = [
            r'^([A-Z_]+)\s*=\s*"([^"]*)"',  # 字符串
            r'^([A-Z_]+)\s*=\s*\'([^\']*)\'',  # 单引号字符串
            r'^([A-Z_]+)\s*=\s*(\d+)',  # 数字
            r'^([A-Z_]+)\s*=\s*(True|False)',  # 布尔值
            r'^([A-Z_]+)\s*=\s*\[(.*?)\]',  # 列表（单行）
            r'^([A-Z_]+)\s*=\s*\{(.*?)\}',  # 字典（单行）
        ]
        
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过注释和空行
            if not line or line.startswith('#'):
                i += 1
                continue
            
            # 尝试匹配各种模式
            matched = False
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    
                    # 根据模式处理值
                    if 'True|False' in pattern:
                        config_data[key] = value == 'True'
                    elif r'\d+' in pattern:
                        config_data[key] = int(value)
                    elif r'\[.*?\]' in pattern:
                        # 处理列表
                        config_data[key] = self.parse_list_value(value)
                    elif r'\{.*?\}' in pattern:
                        # 处理字典
                        config_data[key] = self.parse_dict_value(value)
                    else:
                        config_data[key] = value
                    
                    matched = True
                    break
            
            # 处理多行列表和字典
            if not matched and '=' in line:
                key_part, value_part = line.split('=', 1)
                key = key_part.strip()
                value_part = value_part.strip()
                
                if value_part.startswith('[') and not value_part.endswith(']'):
                    # 多行列表
                    list_content = value_part[1:]  # 去掉开头的 [
                    i += 1
                    while i < len(lines) and not lines[i].strip().endswith(']'):
                        list_content += '\n' + lines[i].strip()
                        i += 1
                    if i < len(lines):
                        list_content += '\n' + lines[i].strip()[:-1]  # 去掉结尾的 ]
                    
                    config_data[key] = self.parse_list_value(list_content)
                    matched = True
                
                elif value_part.startswith('{') and not value_part.endswith('}'):
                    # 多行字典
                    dict_content = value_part[1:]  # 去掉开头的 {
                    i += 1
                    while i < len(lines) and not lines[i].strip().endswith('}'):
                        dict_content += '\n' + lines[i].strip()
                        i += 1
                    if i < len(lines):
                        dict_content += '\n' + lines[i].strip()[:-1]  # 去掉结尾的 }
                    
                    config_data[key] = self.parse_dict_value(dict_content)
                    matched = True
            
            i += 1
        
        return config_data
    
    def parse_list_value(self, value: str) -> List[str]:
        """解析列表值"""
        if not value.strip():
            return []
        
        # 简单的列表解析
        items = []
        for item in value.split(','):
            item = item.strip()
            if item:
                # 去掉引号
                item = item.strip('"\'')
                if item and not item.startswith('#'):
                    items.append(item)
        
        return items
    
    def parse_dict_value(self, value: str) -> Dict[str, str]:
        """解析字典值"""
        if not value.strip():
            return {}
        
        # 简单的字典解析
        result = {}
        for item in value.split(','):
            item = item.strip()
            if ':' in item:
                key, val = item.split(':', 1)
                key = key.strip().strip('"\'')
                val = val.strip().strip('"\'')
                if key and val:
                    result[key] = val
        
        return result
    
    def create_config_widgets(self):
        """创建配置编辑控件"""
        # 清空现有控件
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.config_widgets = {}
        
        if not self.config_data:
            ttk.Label(self.scrollable_frame, text="没有找到配置项", 
                     style='Config.TLabel').pack(pady=20)
            return
        
        # 按类别分组配置项
        categories = self.categorize_config_items()
        
        for category, items in categories.items():
            if not items:
                continue
            
            # 创建分类标题
            category_frame = ttk.LabelFrame(self.scrollable_frame, text=category, 
                                          style='Config.TFrame')
            category_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # 创建配置项控件
            for key in items:
                self.create_config_widget(category_frame, key, self.config_data[key])
    
    def categorize_config_items(self) -> Dict[str, List[str]]:
        """将配置项按类别分组"""
        categories = {
            "基础设置": [],
            "爬虫设置": [],
            "浏览器设置": [],
            "数据库设置": [],
            "代理设置": [],
            "平台特定设置": [],
            "视频统计功能": [],
            "其他设置": []
        }
        
        for key in self.config_data.keys():
            if key in ["PLATFORM", "LOGIN_TYPE", "CRAWLER_TYPE", "KEYWORDS", "COOKIES"]:
                categories["基础设置"].append(key)
            elif key.startswith(("CRAWLER_", "SAVE_DATA", "START_PAGE", "MAX_NOTES", "ENABLE_GET")):
                categories["爬虫设置"].append(key)
            elif key.startswith(("HEADLESS", "CDP_", "BROWSER_", "AUTO_CLOSE", "CUSTOM_BROWSER", "USER_DATA")):
                categories["浏览器设置"].append(key)
            elif key.startswith(("MYSQL_", "REDIS_", "SQLITE_", "CACHE_TYPE")):
                categories["数据库设置"].append(key)
            elif key.startswith(("IP_PROXY", "ENABLE_IP_PROXY")):
                categories["代理设置"].append(key)
            elif key.startswith(("ENABLE_VIDEO_STATS", "ENABLE_BATCH_STATS", "BATCH_STATS_DELAY", "ENABLE_ENGAGEMENT_RATE", "ENABLE_PERFORMANCE_ANALYSIS", "TOP_VIDEOS_", "LOG_STATS_DATA", "STATS_DISPLAY_LANGUAGE")):
                categories["视频统计功能"].append(key)
            elif any(key.startswith(prefix) for prefix in ["DY_", "XHS_", "KS_", "BILI_", "WEIBO_", "TIEBA_", "ZHIHU_", "SORT_TYPE", "SEARCH_TYPE", "PUBLISH_TIME"]):
                categories["平台特定设置"].append(key)
            else:
                categories["其他设置"].append(key)
        
        return categories
    
    def create_config_widget(self, parent, key: str, value: Any):
        """创建单个配置项的编辑控件"""
        frame = ttk.Frame(parent, style='Config.TFrame')
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        # 标签
        label = ttk.Label(frame, text=f"{key}:", style='Config.TLabel', width=30)
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 根据配置类型创建相应控件
        config_type = self.config_types.get(key, {"type": "string"})
        widget_type = config_type["type"]
        
        if widget_type == "boolean":
            var = tk.BooleanVar(value=value)
            widget = ttk.Checkbutton(frame, variable=var)
            self.config_widgets[key] = var
        
        elif widget_type == "choice":
            var = tk.StringVar(value=str(value))
            widget = ttk.Combobox(frame, textvariable=var, 
                                 values=config_type["choices"], 
                                 state="readonly", width=20)
            self.config_widgets[key] = var
        
        elif widget_type == "integer":
            var = tk.StringVar(value=str(value))
            widget = ttk.Entry(frame, textvariable=var, width=20)
            self.config_widgets[key] = var
        
        elif widget_type == "password":
            var = tk.StringVar(value=str(value))
            widget = ttk.Entry(frame, textvariable=var, show="*", width=20)
            self.config_widgets[key] = var
        
        elif widget_type == "file":
            var = tk.StringVar(value=str(value))
            entry_frame = ttk.Frame(frame)
            entry = ttk.Entry(entry_frame, textvariable=var, width=30)
            entry.pack(side=tk.LEFT)
            ttk.Button(entry_frame, text="浏览", 
                      command=lambda: self.browse_file(var)).pack(side=tk.LEFT, padx=(5, 0))
            widget = entry_frame
            self.config_widgets[key] = var
        
        elif widget_type == "text":
            var = tk.StringVar(value=str(value))
            widget = tk.Text(frame, height=3, width=40)
            widget.insert('1.0', str(value))
            self.config_widgets[key] = widget
        
        elif widget_type == "list":
            widget = tk.Text(frame, height=5, width=40)
            if isinstance(value, list):
                widget.insert('1.0', '\n'.join(value))
            else:
                widget.insert('1.0', str(value))
            self.config_widgets[key] = widget
        
        elif widget_type == "dict":
            widget = tk.Text(frame, height=5, width=40)
            if isinstance(value, dict):
                dict_text = '\n'.join([f"{k}: {v}" for k, v in value.items()])
                widget.insert('1.0', dict_text)
            else:
                widget.insert('1.0', str(value))
            self.config_widgets[key] = widget
        
        else:  # string
            var = tk.StringVar(value=str(value))
            widget = ttk.Entry(frame, textvariable=var, width=40)
            self.config_widgets[key] = var
        
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def browse_file(self, var):
        """浏览文件"""
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)
    
    def save_config(self):
        """保存配置"""
        if not self.current_config_file or not self.config_widgets:
            messagebox.showwarning("警告", "没有加载的配置文件")
            return
        
        try:
            # 收集配置值
            new_config = {}
            for key, widget in self.config_widgets.items():
                if isinstance(widget, tk.BooleanVar) or isinstance(widget, tk.StringVar):
                    new_config[key] = widget.get()
                elif isinstance(widget, tk.Text):
                    content = widget.get('1.0', tk.END).strip()
                    if key in self.config_types and self.config_types[key]["type"] == "list":
                        new_config[key] = [line.strip() for line in content.split('\n') if line.strip()]
                    elif key in self.config_types and self.config_types[key]["type"] == "dict":
                        new_config[key] = {}
                        for line in content.split('\n'):
                            if ':' in line:
                                k, v = line.split(':', 1)
                                new_config[key][k.strip()] = v.strip()
                    else:
                        new_config[key] = content
            
            # 验证配置
            if self.validate_config(new_config):
                # 写入配置文件
                self.write_config_file(new_config)
                messagebox.showinfo("成功", "配置保存成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证配置"""
        for key, value in config.items():
            if key in self.config_types:
                config_type = self.config_types[key]
                
                if config_type["type"] == "integer":
                    try:
                        int_val = int(value)
                        if "min" in config_type and int_val < config_type["min"]:
                            messagebox.showerror("验证错误", f"{key} 的值不能小于 {config_type['min']}")
                            return False
                        if "max" in config_type and int_val > config_type["max"]:
                            messagebox.showerror("验证错误", f"{key} 的值不能大于 {config_type['max']}")
                            return False
                    except ValueError:
                        messagebox.showerror("验证错误", f"{key} 必须是整数")
                        return False
                
                elif config_type["type"] == "choice":
                    if str(value) not in config_type["choices"]:
                        messagebox.showerror("验证错误", f"{key} 的值必须是 {config_type['choices']} 中的一个")
                        return False
        
        return True
    
    def write_config_file(self, config: Dict[str, Any]):
        """写入配置文件"""
        with open(self.current_config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换配置值
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            original_line = line
            stripped_line = line.strip()
            
            # 跳过注释和空行
            if not stripped_line or stripped_line.startswith('#'):
                new_lines.append(original_line)
                continue
            
            # 查找配置项
            updated = False
            for key, value in config.items():
                if stripped_line.startswith(f"{key} ="):
                    # 构造新的配置行
                    indent = len(line) - len(line.lstrip())
                    new_value = self.format_config_value(value)
                    new_line = ' ' * indent + f"{key} = {new_value}"
                    new_lines.append(new_line)
                    updated = True
                    break
            
            if not updated:
                new_lines.append(original_line)
        
        # 写入文件
        with open(self.current_config_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
    
    def format_config_value(self, value: Any) -> str:
        """格式化配置值"""
        if isinstance(value, bool):
            return str(value)
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, list):
            if not value:
                return "[]"
            formatted_items = [f'    "{item}",' for item in value]
            return "[\n" + '\n'.join(formatted_items) + "\n]"
        elif isinstance(value, dict):
            if not value:
                return "{}"
            formatted_items = [f'    "{k}": "{v}",' for k, v in value.items()]
            return "{\n" + '\n'.join(formatted_items) + "\n}"
        else:
            return f'"{value}"'
    
    def reset_config(self):
        """重置配置"""
        if messagebox.askyesno("确认", "确定要重置配置吗？这将丢失所有未保存的更改。"):
            self.load_config()
    
    def import_config(self):
        """导入配置"""
        filename = filedialog.askopenfilename(
            title="导入配置文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_config = json.load(f)
                
                # 更新配置
                for key, value in imported_config.items():
                    if key in self.config_widgets:
                        widget = self.config_widgets[key]
                        if isinstance(widget, tk.BooleanVar) or isinstance(widget, tk.StringVar):
                            widget.set(value)
                        elif isinstance(widget, tk.Text):
                            widget.delete('1.0', tk.END)
                            if isinstance(value, list):
                                widget.insert('1.0', '\n'.join(value))
                            elif isinstance(value, dict):
                                dict_text = '\n'.join([f"{k}: {v}" for k, v in value.items()])
                                widget.insert('1.0', dict_text)
                            else:
                                widget.insert('1.0', str(value))
                
                messagebox.showinfo("成功", "配置导入成功！")
                
            except Exception as e:
                messagebox.showerror("错误", f"导入配置失败: {str(e)}")
    
    def export_config(self):
        """导出配置"""
        if not self.config_widgets:
            messagebox.showwarning("警告", "没有可导出的配置")
            return
        
        filename = filedialog.asksaveasfilename(
            title="导出配置文件",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # 收集当前配置
                export_config = {}
                for key, widget in self.config_widgets.items():
                    if isinstance(widget, tk.BooleanVar) or isinstance(widget, tk.StringVar):
                        export_config[key] = widget.get()
                    elif isinstance(widget, tk.Text):
                        content = widget.get('1.0', tk.END).strip()
                        if key in self.config_types and self.config_types[key]["type"] == "list":
                            export_config[key] = [line.strip() for line in content.split('\n') if line.strip()]
                        elif key in self.config_types and self.config_types[key]["type"] == "dict":
                            dict_config = {}
                            for line in content.split('\n'):
                                if ':' in line:
                                    k, v = line.split(':', 1)
                                    dict_config[k.strip()] = v.strip()
                            export_config[key] = dict_config
                        else:
                            export_config[key] = content
                
                # 写入JSON文件
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_config, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("成功", "配置导出成功！")
                
            except Exception as e:
                messagebox.showerror("错误", f"导出配置失败: {str(e)}")


if __name__ == "__main__":
    # 测试配置编辑器
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    editor = ConfigEditor(root)
    editor.open_config_editor()
    
    root.mainloop()