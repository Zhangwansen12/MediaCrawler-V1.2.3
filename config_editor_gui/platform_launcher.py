#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MediaCrawler 配置编辑器 - 跨平台启动器
自动检测操作系统并启动相应的配置编辑器版本
"""

import tkinter as tk
from tkinter import messagebox
import platform
import sys
import os
from typing import Optional, Dict, Any


class PlatformLauncher:
    """跨平台启动器类"""
    
    def __init__(self):
        self.system = platform.system()
        self.system_version = platform.version()
        self.architecture = platform.machine()
        self.python_version = platform.python_version()
        
        # 支持的平台配置
        self.supported_platforms = {
            'Windows': {
                'editor_module': 'config_editor',
                'editor_class': 'ConfigEditor',
                'min_version': '10',
                'features': ['Windows原生界面', '系统主题适配', 'Windows手势支持']
            },
            'Darwin': {  # macOS
                'editor_module': 'config_editor_macos',
                'editor_class': 'MacOSConfigEditor',
                'min_version': '10.12',
                'features': ['macOS原生界面', 'Retina显示优化', '触控板手势', '系统主题适配', '毛玻璃效果']
            },
            'Linux': {
                'editor_module': 'config_editor',
                'editor_class': 'ConfigEditor',
                'min_version': '4.0',
                'features': ['GTK主题适配', 'Linux桌面集成']
            }
        }
    
    def detect_system_capabilities(self) -> Dict[str, Any]:
        """检测系统能力和特性"""
        capabilities = {
            'system': self.system,
            'version': self.system_version,
            'architecture': self.architecture,
            'python_version': self.python_version,
            'gui_available': False,
            'display_info': {},
            'special_features': []
        }
        
        # 检测GUI可用性
        try:
            test_root = tk.Tk()
            test_root.withdraw()
            capabilities['gui_available'] = True
            
            # 获取显示信息
            capabilities['display_info'] = {
                'screen_width': test_root.winfo_screenwidth(),
                'screen_height': test_root.winfo_screenheight(),
                'dpi': test_root.winfo_fpixels('1i')
            }
            
            test_root.destroy()
        except Exception as e:
            capabilities['gui_available'] = False
            capabilities['gui_error'] = str(e)
        
        # 系统特定检测
        if self.system == 'Darwin':  # macOS
            capabilities.update(self._detect_macos_features())
        elif self.system == 'Windows':
            capabilities.update(self._detect_windows_features())
        elif self.system == 'Linux':
            capabilities.update(self._detect_linux_features())
        
        return capabilities
    
    def _detect_macos_features(self) -> Dict[str, Any]:
        """检测macOS特性"""
        features = {
            'is_retina': False,
            'dark_mode': False,
            'macos_version': None,
            'supports_gestures': False,
            'supports_vibrancy': False
        }
        
        try:
            # 获取macOS版本
            import subprocess
            
            # 检测macOS版本
            try:
                version_output = subprocess.run(
                    ['sw_vers', '-productVersion'], 
                    capture_output=True, text=True, timeout=5
                )
                features['macos_version'] = version_output.stdout.strip()
                
                # 解析版本号
                version_parts = features['macos_version'].split('.')
                major = int(version_parts[0])
                minor = int(version_parts[1]) if len(version_parts) > 1 else 0
                
                # 检测功能支持
                if (major == 10 and minor >= 14) or major >= 11:
                    features['supports_vibrancy'] = True
                if (major == 10 and minor >= 7) or major >= 11:
                    features['supports_gestures'] = True
                    
            except Exception:
                pass
            
            # 检测深色模式
            try:
                dark_mode_result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True, text=True, timeout=5
                )
                features['dark_mode'] = dark_mode_result.stdout.strip() == 'Dark'
            except Exception:
                features['dark_mode'] = False
            
            # 检测Retina显示
            try:
                test_root = tk.Tk()
                test_root.withdraw()
                dpi = test_root.winfo_fpixels('1i')
                features['is_retina'] = dpi > 120
                test_root.destroy()
            except Exception:
                features['is_retina'] = False
                
        except Exception as e:
            print(f"macOS特性检测警告: {e}")
        
        return features
    
    def _detect_windows_features(self) -> Dict[str, Any]:
        """检测Windows特性"""
        features = {
            'windows_version': platform.win32_ver()[0] if hasattr(platform, 'win32_ver') else 'Unknown',
            'supports_dwm': False,
            'high_dpi': False,
            'dark_mode': False
        }
        
        try:
            # 检测Windows版本和DWM支持
            import winreg
            
            # 检测高DPI支持
            try:
                test_root = tk.Tk()
                test_root.withdraw()
                dpi = test_root.winfo_fpixels('1i')
                features['high_dpi'] = dpi > 96
                test_root.destroy()
            except Exception:
                pass
            
            # 检测深色模式（Windows 10 1903+）
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    features['dark_mode'] = value == 0
            except Exception:
                pass
                
        except ImportError:
            # 不在Windows系统上
            pass
        except Exception as e:
            print(f"Windows特性检测警告: {e}")
        
        return features
    
    def _detect_linux_features(self) -> Dict[str, Any]:
        """检测Linux特性"""
        features = {
            'desktop_environment': os.environ.get('DESKTOP_SESSION', 'unknown'),
            'display_server': os.environ.get('XDG_SESSION_TYPE', 'unknown'),
            'gtk_theme': os.environ.get('GTK_THEME', 'default'),
            'supports_wayland': False
        }
        
        try:
            # 检测Wayland支持
            features['supports_wayland'] = features['display_server'] == 'wayland'
            
            # 检测桌面环境
            if 'GNOME' in features['desktop_environment'].upper():
                features['desktop_type'] = 'GNOME'
            elif 'KDE' in features['desktop_environment'].upper():
                features['desktop_type'] = 'KDE'
            elif 'XFCE' in features['desktop_environment'].upper():
                features['desktop_type'] = 'XFCE'
            else:
                features['desktop_type'] = 'Other'
                
        except Exception as e:
            print(f"Linux特性检测警告: {e}")
        
        return features
    
    def check_compatibility(self) -> tuple[bool, str]:
        """检查系统兼容性"""
        if self.system not in self.supported_platforms:
            return False, f"不支持的操作系统: {self.system}"
        
        platform_config = self.supported_platforms[self.system]
        
        # 检查Python版本
        python_version = tuple(map(int, self.python_version.split('.')))
        if python_version < (3, 7):
            return False, f"需要Python 3.7或更高版本，当前版本: {self.python_version}"
        
        # 检查GUI可用性
        capabilities = self.detect_system_capabilities()
        if not capabilities['gui_available']:
            error_msg = capabilities.get('gui_error', '未知错误')
            return False, f"GUI不可用: {error_msg}"
        
        return True, "系统兼容"
    
    def get_optimal_editor(self) -> tuple[str, str]:
        """获取最优的编辑器配置"""
        if self.system not in self.supported_platforms:
            # 回退到基础版本
            return 'config_editor', 'ConfigEditor'
        
        platform_config = self.supported_platforms[self.system]
        return platform_config['editor_module'], platform_config['editor_class']
    
    def launch_editor(self, parent=None) -> Optional[object]:
        """启动配置编辑器"""
        # 检查兼容性
        compatible, message = self.check_compatibility()
        if not compatible:
            if parent:
                messagebox.showerror("兼容性错误", message)
            else:
                print(f"错误: {message}")
            return None
        
        # 获取编辑器配置
        module_name, class_name = self.get_optimal_editor()
        
        try:
            # 动态导入编辑器模块
            if module_name == 'config_editor_macos':
                from config_editor_macos import MacOSConfigEditor
                editor = MacOSConfigEditor(parent)
            else:
                from config_editor import ConfigEditor
                editor = ConfigEditor(parent)
            
            # 启动编辑器
            editor.open_config_editor()
            
            return editor
            
        except ImportError as e:
            error_msg = f"无法导入编辑器模块 {module_name}: {e}"
            if parent:
                messagebox.showerror("导入错误", error_msg)
            else:
                print(f"错误: {error_msg}")
            return None
        except Exception as e:
            error_msg = f"启动编辑器失败: {e}"
            if parent:
                messagebox.showerror("启动错误", error_msg)
            else:
                print(f"错误: {error_msg}")
            return None
    
    def show_system_info(self, parent=None):
        """显示系统信息对话框"""
        capabilities = self.detect_system_capabilities()
        platform_config = self.supported_platforms.get(self.system, {})
        
        info_text = f"""系统信息:
操作系统: {self.system} {self.system_version}
架构: {self.architecture}
Python版本: {self.python_version}

显示信息:
分辨率: {capabilities['display_info'].get('screen_width', 'N/A')} x {capabilities['display_info'].get('screen_height', 'N/A')}
DPI: {capabilities['display_info'].get('dpi', 'N/A'):.1f}

支持的特性:
{chr(10).join('• ' + feature for feature in platform_config.get('features', ['基础功能']))}

GUI可用性: {'是' if capabilities['gui_available'] else '否'}
"""
        
        # 添加系统特定信息
        if self.system == 'Darwin':
            macos_info = capabilities
            info_text += f"""
macOS特性:
版本: {macos_info.get('macos_version', 'Unknown')}
Retina显示: {'是' if macos_info.get('is_retina', False) else '否'}
深色模式: {'是' if macos_info.get('dark_mode', False) else '否'}
手势支持: {'是' if macos_info.get('supports_gestures', False) else '否'}
毛玻璃效果: {'是' if macos_info.get('supports_vibrancy', False) else '否'}
"""
        elif self.system == 'Windows':
            windows_info = capabilities
            info_text += f"""
Windows特性:
版本: {windows_info.get('windows_version', 'Unknown')}
高DPI: {'是' if windows_info.get('high_dpi', False) else '否'}
深色模式: {'是' if windows_info.get('dark_mode', False) else '否'}
"""
        elif self.system == 'Linux':
            linux_info = capabilities
            info_text += f"""
Linux特性:
桌面环境: {linux_info.get('desktop_environment', 'Unknown')}
显示服务器: {linux_info.get('display_server', 'Unknown')}
GTK主题: {linux_info.get('gtk_theme', 'Default')}
Wayland支持: {'是' if linux_info.get('supports_wayland', False) else '否'}
"""
        
        if parent:
            messagebox.showinfo("系统信息", info_text)
        else:
            print(info_text)


class PlatformAwareLauncher:
    """平台感知启动器 - 提供统一的启动接口"""
    
    def __init__(self):
        self.launcher = PlatformLauncher()
        self.root = None
        self.editor = None
    
    def create_launcher_gui(self):
        """创建启动器GUI"""
        self.root = tk.Tk()
        self.root.title("MediaCrawler 配置编辑器启动器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # 居中窗口
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_height()) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # 创建主框架
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="MediaCrawler 配置编辑器",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # 系统信息
        system_info = f"检测到系统: {self.launcher.system}"
        if self.launcher.system == 'Darwin':
            capabilities = self.launcher.detect_system_capabilities()
            macos_version = capabilities.get('macos_version', 'Unknown')
            system_info += f" {macos_version}"
        
        info_label = tk.Label(main_frame, text=system_info, font=('Arial', 10))
        info_label.pack(pady=(0, 20))
        
        # 检查兼容性
        compatible, message = self.launcher.check_compatibility()
        
        if compatible:
            # 显示支持的特性
            platform_config = self.launcher.supported_platforms.get(self.launcher.system, {})
            features_text = "支持的特性:\n" + "\n".join(f"• {feature}" for feature in platform_config.get('features', []))
            
            features_label = tk.Label(
                main_frame, 
                text=features_text, 
                font=('Arial', 9),
                justify=tk.LEFT,
                anchor='w'
            )
            features_label.pack(pady=(0, 20), fill=tk.X)
            
            # 启动按钮
            launch_btn = tk.Button(
                main_frame,
                text="启动配置编辑器",
                font=('Arial', 12, 'bold'),
                bg='#007AFF',
                fg='white',
                padx=20,
                pady=10,
                command=self.launch_and_close
            )
            launch_btn.pack(pady=(0, 10))
            
        else:
            # 显示错误信息
            error_label = tk.Label(
                main_frame,
                text=f"兼容性问题:\n{message}",
                font=('Arial', 10),
                fg='red',
                justify=tk.LEFT
            )
            error_label.pack(pady=(0, 20))
        
        # 系统信息按钮
        info_btn = tk.Button(
            main_frame,
            text="查看系统信息",
            font=('Arial', 10),
            command=lambda: self.launcher.show_system_info(self.root)
        )
        info_btn.pack(pady=(0, 10))
        
        # 退出按钮
        quit_btn = tk.Button(
            main_frame,
            text="退出",
            font=('Arial', 10),
            command=self.root.quit
        )
        quit_btn.pack()
    
    def launch_and_close(self):
        """启动编辑器并关闭启动器"""
        self.editor = self.launcher.launch_editor(self.root)
        if self.editor:
            self.root.withdraw()  # 隐藏启动器窗口
    
    def run(self):
        """运行启动器"""
        # 检查是否可以直接启动（命令行模式）
        if len(sys.argv) > 1 and '--direct' in sys.argv:
            return self.launcher.launch_editor()
        
        # 创建GUI启动器
        self.create_launcher_gui()
        self.root.mainloop()
        
        return self.editor


def main():
    """主函数"""
    try:
        launcher = PlatformAwareLauncher()
        launcher.run()
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"启动器错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()