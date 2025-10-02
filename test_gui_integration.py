#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手视频统计功能GUI集成测试脚本
测试配置文件更新功能和平台切换功能
"""

import os
import re
import sys
import tempfile
import shutil
from pathlib import Path

def test_config_update_functionality():
    """测试配置文件更新功能"""
    print("=" * 60)
    print("测试配置文件更新功能")
    print("=" * 60)
    
    # 备份原始配置文件
    config_path = "config/ks_config.py"
    backup_path = "config/ks_config.py.backup"
    
    if os.path.exists(config_path):
        shutil.copy2(config_path, backup_path)
        print(f"✓ 已备份原始配置文件到 {backup_path}")
    else:
        print(f"✗ 配置文件 {config_path} 不存在")
        return False
    
    try:
        # 模拟GUI应用程序的配置更新逻辑
        print("\n正在测试配置更新逻辑...")
        
        # 读取当前配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        print("✓ 成功读取配置文件")
        
        # 模拟配置更新
        test_config_updates = {
            'ENABLE_VIDEO_STATS': True,
            'ENABLE_BATCH_STATS': False,
            'ENABLE_ENGAGEMENT_RATE': True,
            'ENABLE_PERFORMANCE_ANALYSIS': True,
            'LOG_STATS_DATA': False,
            'BATCH_STATS_DELAY': 2.5,
            'TOP_VIDEOS_COUNT': 15,
            'TOP_VIDEOS_METRIC': '"likes"',
            'STATS_DISPLAY_LANGUAGE': '"en"'
        }
        
        # 应用配置更新
        updated_content = original_content
        for key, value in test_config_updates.items():
            pattern = rf'^{key}\s*=.*$'
            replacement = f'{key} = {value}'
            updated_content = re.sub(pattern, replacement, updated_content, flags=re.MULTILINE)
        
        # 写入更新后的配置
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✓ 成功写入更新后的配置")
        
        # 验证配置更新
        with open(config_path, 'r', encoding='utf-8') as f:
            updated_file_content = f.read()
        
        # 检查每个配置项是否正确更新
        all_updated = True
        for key, expected_value in test_config_updates.items():
            pattern = rf'^{key}\s*=\s*(.+)$'
            match = re.search(pattern, updated_file_content, flags=re.MULTILINE)
            if match:
                actual_value = match.group(1).strip()
                if str(expected_value) == actual_value:
                    print(f"✓ {key} = {actual_value} (正确)")
                else:
                    print(f"✗ {key} = {actual_value} (期望: {expected_value})")
                    all_updated = False
            else:
                print(f"✗ 未找到配置项 {key}")
                all_updated = False
        
        if all_updated:
            print("\n✓ 所有配置项都已正确更新")
        else:
            print("\n✗ 部分配置项更新失败")
        
        return all_updated
        
    except Exception as e:
        print(f"✗ 配置更新测试失败: {e}")
        return False
    
    finally:
        # 恢复原始配置文件
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, config_path)
            os.remove(backup_path)
            print(f"✓ 已恢复原始配置文件")

def test_gui_variables_initialization():
    """测试GUI变量初始化"""
    print("\n" + "=" * 60)
    print("测试GUI变量初始化")
    print("=" * 60)
    
    try:
        # 导入GUI应用程序
        from gui_app import MediaCrawlerGUI
        
        # 创建应用程序实例
        app = MediaCrawlerGUI()
        print("✓ GUI应用程序初始化成功")
        
        # 检查所有必需的变量
        required_vars = [
            'platform_var',
            'enable_video_stats_var',
            'enable_batch_stats_var',
            'enable_engagement_rate_var',
            'enable_performance_analysis_var',
            'log_stats_data_var',
            'batch_stats_delay_var',
            'top_videos_count_var',
            'top_videos_metric_var',
            'stats_display_language_var'
        ]
        
        missing_vars = []
        for var in required_vars:
            if hasattr(app, var):
                print(f"✓ {var} 存在")
            else:
                missing_vars.append(var)
                print(f"✗ {var} 不存在")
        
        # 检查方法
        required_methods = [
            'on_platform_changed',
            'create_kuaishou_stats_config',
            'update_kuaishou_config'
        ]
        
        missing_methods = []
        for method in required_methods:
            if hasattr(app, method) and callable(getattr(app, method)):
                print(f"✓ 方法 {method} 存在")
            else:
                missing_methods.append(method)
                print(f"✗ 方法 {method} 不存在")
        
        success = len(missing_vars) == 0 and len(missing_methods) == 0
        
        if success:
            print("\n✓ 所有GUI变量和方法都已正确初始化")
        else:
            print(f"\n✗ 缺少变量: {missing_vars}")
            print(f"✗ 缺少方法: {missing_methods}")
        
        return success
        
    except Exception as e:
        print(f"✗ GUI变量初始化测试失败: {e}")
        return False

def test_config_file_structure():
    """测试配置文件结构"""
    print("\n" + "=" * 60)
    print("测试配置文件结构")
    print("=" * 60)
    
    config_path = "config/ks_config.py"
    
    if not os.path.exists(config_path):
        print(f"✗ 配置文件 {config_path} 不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查必需的配置项
        required_configs = [
            'ENABLE_VIDEO_STATS',
            'ENABLE_BATCH_STATS',
            'BATCH_STATS_DELAY',
            'ENABLE_ENGAGEMENT_RATE',
            'ENABLE_PERFORMANCE_ANALYSIS',
            'TOP_VIDEOS_METRIC',
            'TOP_VIDEOS_COUNT',
            'LOG_STATS_DATA',
            'STATS_DISPLAY_LANGUAGE'
        ]
        
        missing_configs = []
        for config in required_configs:
            pattern = rf'^{config}\s*='
            if re.search(pattern, content, flags=re.MULTILINE):
                print(f"✓ 配置项 {config} 存在")
            else:
                missing_configs.append(config)
                print(f"✗ 配置项 {config} 不存在")
        
        success = len(missing_configs) == 0
        
        if success:
            print("\n✓ 所有必需的配置项都存在")
        else:
            print(f"\n✗ 缺少配置项: {missing_configs}")
        
        return success
        
    except Exception as e:
        print(f"✗ 配置文件结构测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("快手视频统计功能GUI集成测试")
    print("=" * 60)
    
    tests = [
        ("配置文件结构测试", test_config_file_structure),
        ("GUI变量初始化测试", test_gui_variables_initialization),
        ("配置文件更新功能测试", test_config_update_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n开始执行: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} 执行失败: {e}")
            results.append((test_name, False))
    
    # 输出测试结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！快手视频统计功能GUI集成成功！")
        return 0
    else:
        print("❌ 部分测试失败，请检查相关功能")
        return 1

if __name__ == "__main__":
    sys.exit(main())