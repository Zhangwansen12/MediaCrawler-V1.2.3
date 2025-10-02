#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MediaCrawler GUI应用 - macOS版本
专为macOS系统优化的GUI启动器
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import platform
from typing import Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from config_editor_gui.platform_launcher import PlatformLauncher, PlatformAwareLauncher
    from config_editor_gui.config_editor_macos import MacOSConfigEditor
    from config_editor_gui.macos_enhancements import MacOSEnhancements, MacOSIntegration
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)


class MacOSGUIApp:
    """macOS专用GUI应用类"""
    
    def __init__(self):
        self.root = None
        self.config_editor = None
        self.platform_launcher = PlatformLauncher()
        self.macos_enhancements = None
        self.macos_integration = None
        
        # 检查是否在macOS上运行
        if platform.system() != 'Darwin':
            messagebox.showerror("系统错误", "此版本仅支持macOS系统")
            sys.exit(1)
    
    def setup_macos_app(self):
        """设置macOS应用特性"""
        try:
            self.macos_enhancements = MacOSEnhancements()
            self.macos_integration = MacOSIntegration()
            
            # 设置应用集成
            if self.root:
                self.macos_integration.setup_app_integration(self.root)
                
        except Exception as e:
            print(f"macOS特性设置警告: {e}")
    
    def create_main_window(self):
        """创建主窗口"""
        self.root = tk.Tk()
        self.root.title("MediaCrawler - macOS版")
        
        # 设置窗口属性
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 设置macOS特性
        self.setup_macos_app()
        
        # 应用macOS样式
        if self.macos_enhancements:
            try:
                # 检测并应用系统主题
                is_dark = self.macos_enhancements.detect_dark_mode()
                theme = self.macos_enhancements.create_adaptive_theme(is_dark)
                
                # 设置窗口样式
                self.macos_enhancements.set_native_window_style(self.root)
                
                # 应用毛玻璃效果（如果支持）
                if self.macos_enhancements.detect_macos_version()[0] >= 10.14:
                    self.macos_enhancements.apply_vibrancy_effect(self.root)
                    
            except Exception as e:
                print(f"macOS样式应用警告: {e}")
        
        # 居中窗口
        self.center_window()
        
        return self.root
    
    def center_window(self):
        """居中窗口"""
        if not self.root:
            return
            
        self.root.update_idletasks()
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口尺寸
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"+{x}+{y}")
    
    def create_main_interface(self):
        """创建主界面"""
        if not self.root:
            return
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="MediaCrawler",
            font=('SF Pro Display', 24, 'bold') if self.macos_enhancements else ('Arial', 24, 'bold')
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="媒体爬虫工具 - macOS版",
            font=('SF Pro Display', 12) if self.macos_enhancements else ('Arial', 12)
        )
        subtitle_label.pack(pady=(5, 0))
        
        # 系统信息区域
        info_frame = ttk.LabelFrame(main_frame, text="系统信息", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 获取系统信息
        capabilities = self.platform_launcher.detect_system_capabilities()
        
        info_text = f"""系统版本: {capabilities.get('macos_version', 'macOS')}
架构: {capabilities['architecture']}
Python版本: {capabilities['python_version']}
显示分辨率: {capabilities['display_info'].get('screen_width', 'N/A')} × {capabilities['display_info'].get('screen_height', 'N/A')}
DPI: {capabilities['display_info'].get('dpi', 0):.1f}
Retina显示: {'是' if capabilities.get('is_retina', False) else '否'}
深色模式: {'是' if capabilities.get('dark_mode', False) else '否'}"""
        
        info_label = ttk.Label(info_frame, text=info_text, font=('SF Mono', 10) if self.macos_enhancements else ('Courier', 10))
        info_label.pack(anchor='w')
        
        # 功能按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 配置编辑器按钮
        config_btn = ttk.Button(
            button_frame,
            text="打开配置编辑器",
            command=self.open_config_editor,
            style='Accent.TButton' if self.macos_enhancements else None
        )
        config_btn.pack(pady=(0, 10), fill=tk.X)
        
        # 系统信息按钮
        sysinfo_btn = ttk.Button(
            button_frame,
            text="详细系统信息",
            command=self.show_system_info
        )
        sysinfo_btn.pack(pady=(0, 10), fill=tk.X)
        
        # 关于按钮
        about_btn = ttk.Button(
            button_frame,
            text="关于",
            command=self.show_about
        )
        about_btn.pack(fill=tk.X)
        
        # 状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            status_frame,
            text="就绪",
            font=('SF Pro Display', 10) if self.macos_enhancements else ('Arial', 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 设置macOS手势支持
        if self.macos_enhancements:
            try:
                self.macos_enhancements.setup_gesture_support(self.root)
            except Exception as e:
                print(f"手势支持设置警告: {e}")
    
    def open_config_editor(self):
        """打开配置编辑器"""
        try:
            self.status_label.config(text="正在启动配置编辑器...")
            self.root.update()
            
            # 创建macOS配置编辑器
            self.config_editor = MacOSConfigEditor(self.root)
            self.config_editor.open_config_editor()
            
            self.status_label.config(text="配置编辑器已启动")
            
        except Exception as e:
            error_msg = f"启动配置编辑器失败: {e}"
            messagebox.showerror("错误", error_msg)
            self.status_label.config(text="启动失败")
            print(error_msg)
    
    def show_system_info(self):
        """显示详细系统信息"""
        self.platform_launcher.show_system_info(self.root)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """MediaCrawler - macOS版

专为macOS系统优化的媒体爬虫工具

特性:
• 原生macOS界面设计
• Retina显示屏优化
• 触控板手势支持
• 系统主题自动适配
• 毛玻璃视觉效果

版本: 1.0.0
系统要求: macOS 10.12+
Python要求: 3.7+

© 2024 MediaCrawler Team"""
        
        messagebox.showinfo("关于 MediaCrawler", about_text)
    
    def setup_menu_bar(self):
        """设置macOS菜单栏"""
        if not self.root or not self.macos_integration:
            return
        
        try:
            # 创建菜单栏
            menubar = tk.Menu(self.root)
            self.root.config(menu=menubar)
            
            # 应用程序菜单
            app_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="MediaCrawler", menu=app_menu)
            app_menu.add_command(label="关于 MediaCrawler", command=self.show_about)
            app_menu.add_separator()
            app_menu.add_command(label="偏好设置...", command=self.open_preferences, accelerator="Cmd+,")
            app_menu.add_separator()
            app_menu.add_command(label="隐藏 MediaCrawler", accelerator="Cmd+H")
            app_menu.add_command(label="隐藏其他", accelerator="Cmd+Opt+H")
            app_menu.add_command(label="显示全部")
            app_menu.add_separator()
            app_menu.add_command(label="退出 MediaCrawler", command=self.quit_app, accelerator="Cmd+Q")
            
            # 文件菜单
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="文件", menu=file_menu)
            file_menu.add_command(label="打开配置编辑器", command=self.open_config_editor, accelerator="Cmd+O")
            file_menu.add_separator()
            file_menu.add_command(label="关闭窗口", accelerator="Cmd+W")
            
            # 编辑菜单
            edit_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="编辑", menu=edit_menu)
            edit_menu.add_command(label="撤销", accelerator="Cmd+Z")
            edit_menu.add_command(label="重做", accelerator="Cmd+Shift+Z")
            edit_menu.add_separator()
            edit_menu.add_command(label="剪切", accelerator="Cmd+X")
            edit_menu.add_command(label="复制", accelerator="Cmd+C")
            edit_menu.add_command(label="粘贴", accelerator="Cmd+V")
            edit_menu.add_command(label="全选", accelerator="Cmd+A")
            
            # 视图菜单
            view_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="视图", menu=view_menu)
            view_menu.add_command(label="进入全屏", accelerator="Ctrl+Cmd+F")
            view_menu.add_separator()
            view_menu.add_command(label="实际大小", accelerator="Cmd+0")
            view_menu.add_command(label="放大", accelerator="Cmd++")
            view_menu.add_command(label="缩小", accelerator="Cmd+-")
            
            # 窗口菜单
            window_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="窗口", menu=window_menu)
            window_menu.add_command(label="最小化", accelerator="Cmd+M")
            window_menu.add_command(label="缩放")
            window_menu.add_separator()
            window_menu.add_command(label="前置全部窗口")
            
            # 帮助菜单
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="帮助", menu=help_menu)
            help_menu.add_command(label="MediaCrawler 帮助")
            help_menu.add_command(label="系统信息", command=self.show_system_info)
            
            # 绑定键盘快捷键
            self.root.bind('<Command-o>', lambda e: self.open_config_editor())
            self.root.bind('<Command-q>', lambda e: self.quit_app())
            self.root.bind('<Command-comma>', lambda e: self.open_preferences())
            
        except Exception as e:
            print(f"菜单栏设置警告: {e}")
    
    def open_preferences(self):
        """打开偏好设置"""
        messagebox.showinfo("偏好设置", "偏好设置功能即将推出")
    
    def quit_app(self):
        """退出应用"""
        if messagebox.askokcancel("退出", "确定要退出 MediaCrawler 吗？"):
            self.root.quit()
    
    def run(self):
        """运行应用"""
        try:
            # 创建主窗口
            self.create_main_window()
            
            # 设置菜单栏
            self.setup_menu_bar()
            
            # 创建界面
            self.create_main_interface()
            
            # 设置窗口关闭事件
            self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
            
            # 启动主循环
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\n用户中断")
        except Exception as e:
            print(f"应用运行错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    # 检查系统
    if platform.system() != 'Darwin':
        print("错误: 此版本仅支持macOS系统")
        print("请使用通用版本或对应系统的版本")
        sys.exit(1)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    # 启动应用
    app = MacOSGUIApp()
    app.run()


if __name__ == "__main__":
    main()