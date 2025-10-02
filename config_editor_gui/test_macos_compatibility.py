#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
macOS兼容性测试脚本
测试macOS版本配置编辑器的功能完整性和界面适配效果
"""

import sys
import os
import platform
import traceback
from typing import Dict, List, Tuple, Any

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class MacOSCompatibilityTester:
    """macOS兼容性测试器"""
    
    def __init__(self):
        self.test_results = {}
        self.errors = []
        self.warnings = []
        
    def log_result(self, test_name: str, success: bool, message: str = "", details: Any = None):
        """记录测试结果"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'details': details
        }
        
        if not success:
            self.errors.append(f"{test_name}: {message}")
        
        print(f"{'✓' if success else '✗'} {test_name}: {message}")
        if details and isinstance(details, dict):
            for key, value in details.items():
                print(f"  {key}: {value}")
    
    def test_system_detection(self) -> bool:
        """测试系统检测功能"""
        print("\n=== 系统检测测试 ===")
        
        try:
            from config_editor_gui.platform_launcher import PlatformLauncher
            
            launcher = PlatformLauncher()
            
            # 测试基本系统信息
            system_info = {
                'system': launcher.system,
                'version': launcher.system_version,
                'architecture': launcher.architecture,
                'python_version': launcher.python_version
            }
            
            self.log_result(
                "系统信息获取",
                True,
                f"检测到 {launcher.system} 系统",
                system_info
            )
            
            # 测试兼容性检查
            compatible, message = launcher.check_compatibility()
            self.log_result(
                "兼容性检查",
                compatible,
                message
            )
            
            # 测试系统能力检测
            capabilities = launcher.detect_system_capabilities()
            self.log_result(
                "系统能力检测",
                capabilities['gui_available'],
                f"GUI可用: {capabilities['gui_available']}",
                {
                    '显示分辨率': f"{capabilities['display_info'].get('screen_width', 'N/A')} × {capabilities['display_info'].get('screen_height', 'N/A')}",
                    'DPI': f"{capabilities['display_info'].get('dpi', 0):.1f}",
                    '特殊功能': len(capabilities.get('special_features', []))
                }
            )
            
            return compatible
            
        except Exception as e:
            self.log_result("系统检测", False, f"导入或执行失败: {e}")
            return False
    
    def test_macos_enhancements(self) -> bool:
        """测试macOS增强功能"""
        print("\n=== macOS增强功能测试 ===")
        
        try:
            from config_editor_gui.macos_enhancements import MacOSEnhancements, MacOSIntegration
            
            # 测试MacOSEnhancements类
            enhancements = MacOSEnhancements()
            
            # 测试系统检测方法
            try:
                macos_version = enhancements.detect_macos_version()
                self.log_result(
                    "macOS版本检测",
                    True,
                    f"版本: {macos_version[0]}.{macos_version[1]}"
                )
            except Exception as e:
                self.log_result("macOS版本检测", False, f"检测失败: {e}")
            
            # 测试深色模式检测
            try:
                dark_mode = enhancements.detect_dark_mode()
                self.log_result(
                    "深色模式检测",
                    True,
                    f"深色模式: {'启用' if dark_mode else '禁用'}"
                )
            except Exception as e:
                self.log_result("深色模式检测", False, f"检测失败: {e}")
            
            # 测试Retina检测
            try:
                is_retina = enhancements.detect_retina_display()
                self.log_result(
                    "Retina显示检测",
                    True,
                    f"Retina显示: {'是' if is_retina else '否'}"
                )
            except Exception as e:
                self.log_result("Retina显示检测", False, f"检测失败: {e}")
            
            # 测试MacOSIntegration类
            try:
                integration = MacOSIntegration()
                self.log_result(
                    "macOS集成模块",
                    True,
                    "集成模块初始化成功"
                )
            except Exception as e:
                self.log_result("macOS集成模块", False, f"初始化失败: {e}")
            
            return True
            
        except ImportError as e:
            self.log_result("macOS增强功能", False, f"模块导入失败: {e}")
            return False
        except Exception as e:
            self.log_result("macOS增强功能", False, f"测试失败: {e}")
            return False
    
    def test_macos_config_editor(self) -> bool:
        """测试macOS配置编辑器"""
        print("\n=== macOS配置编辑器测试 ===")
        
        try:
            from config_editor_gui.config_editor_macos import MacOSConfigEditor
            
            # 测试类初始化（不创建GUI）
            try:
                # 创建一个虚拟的父窗口用于测试
                import tkinter as tk
                test_root = tk.Tk()
                test_root.withdraw()  # 隐藏窗口
                
                editor = MacOSConfigEditor(test_root)
                
                self.log_result(
                    "macOS配置编辑器初始化",
                    True,
                    "编辑器类初始化成功"
                )
                
                # 测试配置文件映射
                config_files = editor.config_files
                self.log_result(
                    "配置文件映射",
                    len(config_files) > 0,
                    f"支持 {len(config_files)} 个配置文件",
                    {name: path for name, path in list(config_files.items())[:3]}  # 只显示前3个
                )
                
                # 测试配置项类型定义
                config_types = editor.config_types
                self.log_result(
                    "配置项类型定义",
                    len(config_types) > 0,
                    f"定义了 {len(config_types)} 种配置项类型",
                    list(config_types.keys())
                )
                
                test_root.destroy()
                return True
                
            except Exception as e:
                self.log_result("macOS配置编辑器初始化", False, f"初始化失败: {e}")
                return False
            
        except ImportError as e:
            self.log_result("macOS配置编辑器", False, f"模块导入失败: {e}")
            return False
        except Exception as e:
            self.log_result("macOS配置编辑器", False, f"测试失败: {e}")
            return False
    
    def test_gui_app_macos(self) -> bool:
        """测试macOS GUI应用"""
        print("\n=== macOS GUI应用测试 ===")
        
        try:
            from config_editor_gui.gui_app_macos import MacOSGUIApp
            
            # 测试应用类初始化（不启动GUI）
            try:
                # 由于MacOSGUIApp会检查系统，我们需要模拟或跳过这个检查
                if platform.system() != 'Darwin':
                    self.log_result(
                        "macOS GUI应用",
                        True,
                        "在非macOS系统上跳过GUI应用测试（设计如此）"
                    )
                    return True
                
                app = MacOSGUIApp()
                self.log_result(
                    "macOS GUI应用初始化",
                    True,
                    "GUI应用类初始化成功"
                )
                
                return True
                
            except SystemExit:
                # 这是预期的，因为在非macOS系统上会退出
                self.log_result(
                    "macOS GUI应用",
                    True,
                    "在非macOS系统上正确退出（设计如此）"
                )
                return True
            except Exception as e:
                self.log_result("macOS GUI应用初始化", False, f"初始化失败: {e}")
                return False
            
        except ImportError as e:
            self.log_result("macOS GUI应用", False, f"模块导入失败: {e}")
            return False
        except Exception as e:
            self.log_result("macOS GUI应用", False, f"测试失败: {e}")
            return False
    
    def test_cross_platform_launcher(self) -> bool:
        """测试跨平台启动器"""
        print("\n=== 跨平台启动器测试 ===")
        
        try:
            from config_editor_gui.platform_launcher import PlatformLauncher, PlatformAwareLauncher
            
            # 测试PlatformLauncher
            launcher = PlatformLauncher()
            
            # 测试编辑器选择
            module_name, class_name = launcher.get_optimal_editor()
            expected_module = 'config_editor_macos' if platform.system() == 'Darwin' else 'config_editor'
            
            self.log_result(
                "编辑器选择",
                module_name == expected_module,
                f"选择了 {module_name}.{class_name}",
                {'期望模块': expected_module, '实际模块': module_name}
            )
            
            # 测试PlatformAwareLauncher
            try:
                aware_launcher = PlatformAwareLauncher()
                self.log_result(
                    "平台感知启动器",
                    True,
                    "平台感知启动器初始化成功"
                )
            except Exception as e:
                self.log_result("平台感知启动器", False, f"初始化失败: {e}")
            
            return True
            
        except ImportError as e:
            self.log_result("跨平台启动器", False, f"模块导入失败: {e}")
            return False
        except Exception as e:
            self.log_result("跨平台启动器", False, f"测试失败: {e}")
            return False
    
    def test_config_file_compatibility(self) -> bool:
        """测试配置文件兼容性"""
        print("\n=== 配置文件兼容性测试 ===")
        
        try:
            # 测试配置文件路径
            config_dir = os.path.join(project_root, 'config')
            
            if not os.path.exists(config_dir):
                self.log_result("配置目录", False, f"配置目录不存在: {config_dir}")
                return False
            
            self.log_result("配置目录", True, f"配置目录存在: {config_dir}")
            
            # 检查主要配置文件
            config_files = [
                'base_config.py',
                'db_config.py',
                'xhs_config.py',
                'dy_config.py',
                'bilibili_config.py',
                'weibo_config.py',
                'tieba_config.py',
                'zhihu_config.py'
            ]
            
            existing_files = []
            missing_files = []
            
            for config_file in config_files:
                file_path = os.path.join(config_dir, config_file)
                if os.path.exists(file_path):
                    existing_files.append(config_file)
                else:
                    missing_files.append(config_file)
            
            self.log_result(
                "配置文件检查",
                len(missing_files) == 0,
                f"找到 {len(existing_files)} 个配置文件",
                {
                    '存在的文件': existing_files[:5],  # 只显示前5个
                    '缺失的文件': missing_files
                }
            )
            
            return len(missing_files) == 0
            
        except Exception as e:
            self.log_result("配置文件兼容性", False, f"测试失败: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("开始macOS兼容性测试...")
        print(f"当前系统: {platform.system()} {platform.version()}")
        print(f"Python版本: {platform.python_version()}")
        print("=" * 60)
        
        # 运行各项测试
        tests = [
            ("系统检测", self.test_system_detection),
            ("macOS增强功能", self.test_macos_enhancements),
            ("macOS配置编辑器", self.test_macos_config_editor),
            ("macOS GUI应用", self.test_gui_app_macos),
            ("跨平台启动器", self.test_cross_platform_launcher),
            ("配置文件兼容性", self.test_config_file_compatibility)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_result(test_name, False, f"测试异常: {e}")
                print(f"详细错误信息:\n{traceback.format_exc()}")
        
        # 生成测试报告
        print("\n" + "=" * 60)
        print("测试报告")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"总体结果: {passed_tests}/{total_tests} 测试通过 ({success_rate:.1f}%)")
        
        if self.errors:
            print(f"\n发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        # 功能完整性评估
        print(f"\n功能完整性评估:")
        if success_rate >= 90:
            print("✓ 优秀 - macOS版本功能完整，可以正常使用")
        elif success_rate >= 75:
            print("⚠ 良好 - macOS版本基本功能正常，部分高级功能可能受限")
        elif success_rate >= 50:
            print("⚠ 一般 - macOS版本核心功能可用，但存在兼容性问题")
        else:
            print("✗ 需要改进 - macOS版本存在严重兼容性问题")
        
        # 系统适配建议
        current_system = platform.system()
        print(f"\n系统适配建议:")
        if current_system == 'Darwin':
            print("• 当前在macOS系统上测试，所有macOS特性都可以正常验证")
            print("• 建议测试触控板手势、Retina显示和系统主题适配")
        elif current_system == 'Windows':
            print("• 当前在Windows系统上测试，macOS特性无法完全验证")
            print("• 建议在实际macOS设备上进行完整测试")
            print("• 跨平台启动器应该能正确检测并选择Windows版本")
        else:
            print(f"• 当前在{current_system}系统上测试")
            print("• 建议在macOS和Windows系统上分别进行测试")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': success_rate,
            'errors': self.errors,
            'warnings': self.warnings,
            'test_results': self.test_results
        }


def main():
    """主函数"""
    tester = MacOSCompatibilityTester()
    results = tester.run_all_tests()
    
    # 返回适当的退出码
    if results['success_rate'] >= 75:
        sys.exit(0)  # 成功
    else:
        sys.exit(1)  # 失败


if __name__ == "__main__":
    main()