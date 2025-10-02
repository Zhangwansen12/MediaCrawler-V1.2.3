#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
macOS增强功能模块
提供macOS专用的高级功能和系统集成
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import os
import platform
from typing import Optional, Dict, Any, Tuple


class MacOSEnhancements:
    """macOS系统增强功能类"""
    
    def __init__(self):
        self.system_version = self._get_system_version()
        self.supports_dark_mode = self._check_dark_mode_support()
        self.supports_native_fullscreen = self._check_fullscreen_support()
        
    def _get_system_version(self) -> Tuple[int, int, int]:
        """获取macOS系统版本"""
        try:
            version_str = platform.mac_ver()[0]
            parts = version_str.split('.')
            return (int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) > 2 else 0)
        except:
            return (10, 15, 0)  # 默认版本
    
    def _check_dark_mode_support(self) -> bool:
        """检查是否支持深色模式（macOS 10.14+）"""
        return self.system_version >= (10, 14, 0)
    
    def _check_fullscreen_support(self) -> bool:
        """检查是否支持原生全屏（macOS 10.7+）"""
        return self.system_version >= (10, 7, 0)
    
    def detect_system_appearance(self) -> str:
        """检测系统外观模式"""
        try:
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True, text=True, timeout=5
            )
            return 'dark' if result.stdout.strip() == 'Dark' else 'light'
        except:
            return 'light'
    
    def detect_accent_color(self) -> str:
        """检测系统强调色"""
        try:
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleAccentColor'],
                capture_output=True, text=True, timeout=5
            )
            
            # macOS强调色映射
            accent_colors = {
                '-1': '#007AFF',  # 蓝色（默认）
                '0': '#FF3B30',   # 红色
                '1': '#FF9500',   # 橙色
                '2': '#FFCC00',   # 黄色
                '3': '#34C759',   # 绿色
                '4': '#007AFF',   # 蓝色
                '5': '#5856D6',   # 紫色
                '6': '#FF2D92',   # 粉色
            }
            
            color_code = result.stdout.strip()
            return accent_colors.get(color_code, '#007AFF')
        except:
            return '#007AFF'  # 默认蓝色
    
    def get_system_fonts(self) -> Dict[str, str]:
        """获取系统字体"""
        fonts = {
            'system': 'SF Pro Display',
            'system_mono': 'SF Mono',
            'ui': 'SF Pro Text'
        }
        
        # 检查系统版本以确定可用字体
        if self.system_version >= (10, 11, 0):  # El Capitan+
            fonts['system'] = 'SF Pro Display'
        else:
            fonts['system'] = 'Helvetica Neue'
        
        return fonts
    
    def detect_macos_version(self) -> Tuple[int, int]:
        """检测macOS版本（兼容性方法）"""
        return (self.system_version[0], self.system_version[1])
    
    def detect_dark_mode(self) -> bool:
        """检测深色模式（兼容性方法）"""
        return self.detect_system_appearance() == 'dark'
    
    def detect_retina_display(self) -> bool:
        """检测Retina显示屏"""
        try:
            import tkinter as tk
            test_root = tk.Tk()
            test_root.withdraw()
            
            # 获取DPI，Retina显示通常DPI > 120
            dpi = test_root.winfo_fpixels('1i')
            is_retina = dpi > 120
            
            test_root.destroy()
            return is_retina
        except:
            return False
    
    def setup_native_window_style(self, window: tk.Toplevel) -> bool:
        """设置原生macOS窗口样式"""
        try:
            # 设置窗口样式为文档窗口
            window.tk.call('::tk::unsupported::MacWindowStyle', 
                          window._w, 'document', 'closeBox collapseBox resizable')
            
            # 启用全屏按钮（如果支持）
            if self.supports_native_fullscreen:
                window.tk.call('::tk::unsupported::MacWindowStyle', 
                              window._w, 'fullScreenButton', '1')
            
            # 设置窗口阴影
            window.tk.call('::tk::unsupported::MacWindowStyle', 
                          window._w, 'shadow', '1')
            
            return True
        except tk.TclError:
            return False
    
    def create_native_toolbar(self, window: tk.Toplevel) -> Optional[tk.Frame]:
        """创建原生macOS工具栏"""
        try:
            # 创建工具栏框架
            toolbar = tk.Frame(window, height=44, bg='#f6f6f6')
            
            # 设置工具栏样式
            if self.detect_system_appearance() == 'dark':
                toolbar.configure(bg='#2c2c2c')
            
            return toolbar
        except:
            return None
    
    def apply_vibrancy_effect(self, widget: tk.Widget) -> bool:
        """应用毛玻璃效果（需要macOS 10.10+）"""
        if self.system_version < (10, 10, 0):
            return False
        
        try:
            # 尝试应用毛玻璃效果
            widget.tk.call('::tk::unsupported::MacWindowStyle', 
                          widget._w, 'appearance', 'vibrantLight')
            return True
        except tk.TclError:
            return False
    
    def setup_retina_scaling(self, window: tk.Toplevel) -> Dict[str, Any]:
        """设置Retina显示屏缩放"""
        try:
            # 获取显示器信息
            dpi = window.winfo_fpixels('1i')
            scale_factor = dpi / 72.0  # macOS基准DPI
            
            is_retina = scale_factor > 1.5
            
            return {
                'dpi': dpi,
                'scale_factor': scale_factor,
                'is_retina': is_retina,
                'font_size_multiplier': 1.2 if is_retina else 1.0,
                'spacing_multiplier': 1.1 if is_retina else 1.0
            }
        except:
            return {
                'dpi': 72,
                'scale_factor': 1.0,
                'is_retina': False,
                'font_size_multiplier': 1.0,
                'spacing_multiplier': 1.0
            }
    
    def create_adaptive_style(self, style: ttk.Style) -> Dict[str, str]:
        """创建自适应样式主题"""
        appearance = self.detect_system_appearance()
        accent_color = self.detect_accent_color()
        fonts = self.get_system_fonts()
        
        if appearance == 'dark':
            colors = {
                'bg': '#2c2c2c',
                'fg': '#ffffff',
                'select_bg': accent_color,
                'select_fg': '#ffffff',
                'entry_bg': '#3c3c3c',
                'entry_fg': '#ffffff',
                'button_bg': '#4c4c4c',
                'button_fg': '#ffffff',
                'frame_bg': '#2c2c2c',
                'label_bg': '#2c2c2c',
                'label_fg': '#ffffff'
            }
        else:
            colors = {
                'bg': '#f5f5f5',
                'fg': '#000000',
                'select_bg': accent_color,
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'button_bg': '#e5e5e5',
                'button_fg': '#000000',
                'frame_bg': '#f5f5f5',
                'label_bg': '#f5f5f5',
                'label_fg': '#000000'
            }
        
        # 应用样式
        try:
            # 使用Aqua主题作为基础（如果可用）
            if 'aqua' in style.theme_names():
                style.theme_use('aqua')
            
            # 自定义样式
            style.configure('MacOS.TFrame', background=colors['frame_bg'])
            style.configure('MacOS.TLabel', 
                           background=colors['label_bg'], 
                           foreground=colors['label_fg'],
                           font=(fonts['system'], 11))
            style.configure('MacOS.TButton', 
                           background=colors['button_bg'],
                           foreground=colors['button_fg'],
                           font=(fonts['system'], 11),
                           focuscolor='none')
            style.configure('MacOS.TEntry', 
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['entry_fg'],
                           font=(fonts['system'], 11))
            style.configure('MacOS.TCombobox', 
                           fieldbackground=colors['entry_bg'],
                           foreground=colors['entry_fg'],
                           font=(fonts['system'], 11))
            style.configure('MacOS.TNotebook', 
                           background=colors['bg'])
            style.configure('MacOS.TNotebook.Tab', 
                           font=(fonts['system'], 10),
                           padding=[12, 8])
            style.configure('MacOS.TCheckbutton',
                           background=colors['frame_bg'],
                           foreground=colors['label_fg'],
                           font=(fonts['system'], 11))
            
        except Exception as e:
            print(f"样式配置警告: {e}")
        
        return colors
    
    def setup_gesture_support(self, canvas: tk.Canvas) -> None:
        """设置手势支持"""
        def handle_swipe_left(event):
            """处理左滑手势"""
            canvas.xview_scroll(1, "units")
        
        def handle_swipe_right(event):
            """处理右滑手势"""
            canvas.xview_scroll(-1, "units")
        
        def handle_pinch_zoom(event):
            """处理缩放手势"""
            # 这里可以实现缩放功能
            pass
        
        def handle_scroll(event):
            """处理滚动事件（支持触控板）"""
            # macOS的滚动方向
            canvas.yview_scroll(int(event.delta), "units")
        
        def handle_horizontal_scroll(event):
            """处理水平滚动"""
            canvas.xview_scroll(int(event.delta), "units")
        
        # 绑定事件
        canvas.bind("<MouseWheel>", handle_scroll)
        canvas.bind("<Shift-MouseWheel>", handle_horizontal_scroll)
        
        # 尝试绑定触控板手势（如果支持）
        try:
            canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
            canvas.bind("<Shift-Button-4>", lambda e: canvas.xview_scroll(-1, "units"))
            canvas.bind("<Shift-Button-5>", lambda e: canvas.xview_scroll(1, "units"))
        except:
            pass
    
    def setup_keyboard_shortcuts(self, window: tk.Toplevel, callbacks: Dict[str, callable]) -> None:
        """设置macOS标准键盘快捷键"""
        shortcuts = {
            '<Command-s>': 'save',
            '<Command-o>': 'open',
            '<Command-n>': 'new',
            '<Command-w>': 'close',
            '<Command-q>': 'quit',
            '<Command-z>': 'undo',
            '<Command-Shift-z>': 'redo',
            '<Command-c>': 'copy',
            '<Command-v>': 'paste',
            '<Command-x>': 'cut',
            '<Command-a>': 'select_all',
            '<Command-f>': 'find',
            '<Command-r>': 'refresh',
            '<Command-i>': 'import',
            '<Command-e>': 'export',
            '<Command-comma>': 'preferences',
            '<F11>': 'fullscreen'
        }
        
        for shortcut, action in shortcuts.items():
            if action in callbacks:
                window.bind(shortcut, lambda e, cb=callbacks[action]: cb())
    
    def create_context_menu(self, parent: tk.Widget, items: list) -> tk.Menu:
        """创建macOS风格的上下文菜单"""
        menu = tk.Menu(parent, tearoff=0)
        
        # 设置菜单样式
        appearance = self.detect_system_appearance()
        if appearance == 'dark':
            menu.configure(bg='#3c3c3c', fg='#ffffff', 
                          activebackground='#007AFF', activeforeground='#ffffff')
        else:
            menu.configure(bg='#ffffff', fg='#000000',
                          activebackground='#007AFF', activeforeground='#ffffff')
        
        for item in items:
            if item == 'separator':
                menu.add_separator()
            else:
                menu.add_command(label=item['label'], command=item['command'])
        
        return menu
    
    def show_notification(self, title: str, message: str, sound: bool = True) -> bool:
        """显示macOS系统通知"""
        try:
            cmd = ['osascript', '-e', 
                   f'display notification "{message}" with title "{title}"']
            if sound:
                cmd.extend(['-e', 'beep'])
            
            subprocess.run(cmd, check=True, timeout=5)
            return True
        except:
            return False
    
    def get_system_preferences(self) -> Dict[str, Any]:
        """获取系统偏好设置"""
        prefs = {}
        
        try:
            # 获取滚动方向
            result = subprocess.run(
                ['defaults', 'read', '-g', 'com.apple.swipescrolldirection'],
                capture_output=True, text=True, timeout=5
            )
            prefs['natural_scrolling'] = result.stdout.strip() == '1'
        except:
            prefs['natural_scrolling'] = True
        
        try:
            # 获取双击速度
            result = subprocess.run(
                ['defaults', 'read', '-g', 'com.apple.mouse.doubleClickThreshold'],
                capture_output=True, text=True, timeout=5
            )
            prefs['double_click_speed'] = float(result.stdout.strip())
        except:
            prefs['double_click_speed'] = 0.5
        
        try:
            # 获取菜单栏自动隐藏设置
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleMenuBarVisibleInFullscreen'],
                capture_output=True, text=True, timeout=5
            )
            prefs['menubar_in_fullscreen'] = result.stdout.strip() == '1'
        except:
            prefs['menubar_in_fullscreen'] = False
        
        return prefs
    
    def optimize_for_battery(self) -> Dict[str, Any]:
        """电池优化设置"""
        try:
            # 检查电源状态
            result = subprocess.run(
                ['pmset', '-g', 'batt'],
                capture_output=True, text=True, timeout=5
            )
            
            is_on_battery = 'Battery Power' in result.stdout
            battery_percentage = 100  # 默认值
            
            # 解析电池百分比
            if '%' in result.stdout:
                import re
                match = re.search(r'(\d+)%', result.stdout)
                if match:
                    battery_percentage = int(match.group(1))
            
            return {
                'on_battery': is_on_battery,
                'battery_level': battery_percentage,
                'low_power_mode': is_on_battery and battery_percentage < 20,
                'suggested_refresh_rate': 30 if is_on_battery else 60
            }
        except:
            return {
                'on_battery': False,
                'battery_level': 100,
                'low_power_mode': False,
                'suggested_refresh_rate': 60
            }


class MacOSIntegration:
    """macOS系统集成功能"""
    
    def __init__(self, app_name: str = "MediaCrawler Config Editor"):
        self.app_name = app_name
        self.enhancements = MacOSEnhancements()
    
    def setup_app_integration(self, window: tk.Toplevel) -> None:
        """设置应用程序集成"""
        # 设置应用程序名称
        try:
            window.tk.call('::tk::mac::standardAboutPanel')
        except:
            pass
        
        # 设置Dock图标
        self._setup_dock_integration(window)
        
        # 设置菜单栏
        self._setup_menu_bar(window)
    
    def _setup_dock_integration(self, window: tk.Toplevel) -> None:
        """设置Dock集成"""
        try:
            # 设置Dock菜单
            window.createcommand('::tk::mac::ShowPreferences', self._show_preferences)
            window.createcommand('::tk::mac::Quit', lambda: window.quit())
        except:
            pass
    
    def _setup_menu_bar(self, window: tk.Toplevel) -> None:
        """设置菜单栏"""
        try:
            menubar = tk.Menu(window)
            window.config(menu=menubar)
            
            # 应用程序菜单
            app_menu = tk.Menu(menubar, name='apple')
            menubar.add_cascade(menu=app_menu)
            app_menu.add_command(label=f'关于 {self.app_name}', command=self._show_about)
            app_menu.add_separator()
            app_menu.add_command(label='偏好设置...', accelerator='Cmd+,', command=self._show_preferences)
            app_menu.add_separator()
            app_menu.add_command(label=f'退出 {self.app_name}', accelerator='Cmd+Q', command=window.quit)
            
            # 文件菜单
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label='文件', menu=file_menu)
            file_menu.add_command(label='新建', accelerator='Cmd+N')
            file_menu.add_command(label='打开...', accelerator='Cmd+O')
            file_menu.add_separator()
            file_menu.add_command(label='保存', accelerator='Cmd+S')
            file_menu.add_command(label='另存为...', accelerator='Shift+Cmd+S')
            file_menu.add_separator()
            file_menu.add_command(label='导入...', accelerator='Cmd+I')
            file_menu.add_command(label='导出...', accelerator='Cmd+E')
            
            # 编辑菜单
            edit_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label='编辑', menu=edit_menu)
            edit_menu.add_command(label='撤销', accelerator='Cmd+Z')
            edit_menu.add_command(label='重做', accelerator='Shift+Cmd+Z')
            edit_menu.add_separator()
            edit_menu.add_command(label='剪切', accelerator='Cmd+X')
            edit_menu.add_command(label='复制', accelerator='Cmd+C')
            edit_menu.add_command(label='粘贴', accelerator='Cmd+V')
            edit_menu.add_command(label='全选', accelerator='Cmd+A')
            
            # 视图菜单
            view_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label='视图', menu=view_menu)
            view_menu.add_command(label='刷新', accelerator='Cmd+R')
            view_menu.add_separator()
            view_menu.add_command(label='进入全屏', accelerator='F11')
            
            # 窗口菜单
            window_menu = tk.Menu(menubar, name='window', tearoff=0)
            menubar.add_cascade(label='窗口', menu=window_menu)
            window_menu.add_command(label='最小化', accelerator='Cmd+M')
            window_menu.add_command(label='缩放')
            window_menu.add_separator()
            window_menu.add_command(label='前置全部窗口')
            
            # 帮助菜单
            help_menu = tk.Menu(menubar, name='help', tearoff=0)
            menubar.add_cascade(label='帮助', menu=help_menu)
            help_menu.add_command(label=f'{self.app_name} 帮助')
            
        except Exception as e:
            print(f"菜单栏设置警告: {e}")
    
    def _show_about(self):
        """显示关于对话框"""
        from tkinter import messagebox
        messagebox.showinfo("关于", f"{self.app_name}\n\n专为macOS优化的配置编辑器\n版本 1.0")
    
    def _show_preferences(self):
        """显示偏好设置"""
        # 这里可以实现偏好设置窗口
        pass