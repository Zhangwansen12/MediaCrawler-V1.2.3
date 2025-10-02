#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平台切换功能测试脚本
测试当平台选择改变时，快手统计配置的显示/隐藏功能
"""

import tkinter as tk
from tkinter import ttk
import sys
import time

def test_platform_switching():
    """测试平台切换功能"""
    print("=" * 60)
    print("测试平台切换功能")
    print("=" * 60)
    
    try:
        # 导入GUI应用程序
        from gui_app import MediaCrawlerGUI
        
        # 创建应用程序实例
        app = MediaCrawlerGUI()
        print("✓ GUI应用程序初始化成功")
        
        # 检查快手统计框架是否存在
        if not hasattr(app, 'kuaishou_stats_frame'):
            print("✗ 快手统计配置框架不存在")
            return False
        
        print("✓ 快手统计配置框架存在")
        
        # 测试不同平台的切换
        platforms = ["dy", "xhs", "ks", "bili", "wb", "tieba", "zhihu"]
        
        for platform in platforms:
            print(f"\n测试切换到平台: {platform}")
            
            # 设置平台
            app.platform_var.set(platform)
            
            # 调用平台切换事件处理函数
            app.on_platform_changed()
            
            # 检查快手统计配置的可见性
            try:
                # 获取框架的grid信息
                grid_info = app.kuaishou_stats_frame.grid_info()
                is_visible = bool(grid_info)  # 如果有grid信息说明是可见的
                
                if platform == "ks":
                    if is_visible:
                        print(f"  ✓ 快手平台时统计配置可见")
                    else:
                        print(f"  ✗ 快手平台时统计配置应该可见但实际不可见")
                        return False
                else:
                    if not is_visible:
                        print(f"  ✓ 非快手平台时统计配置隐藏")
                    else:
                        print(f"  ✗ 非快手平台时统计配置应该隐藏但实际可见")
                        return False
                        
            except tk.TclError:
                # 如果获取grid_info失败，说明框架被隐藏了
                if platform == "ks":
                    print(f"  ✗ 快手平台时统计配置应该可见但实际隐藏")
                    return False
                else:
                    print(f"  ✓ 非快手平台时统计配置隐藏")
        
        print("\n✓ 所有平台切换测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 平台切换测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_kuaishou_config_widgets():
    """测试快手配置组件"""
    print("\n" + "=" * 60)
    print("测试快手配置组件")
    print("=" * 60)
    
    try:
        from gui_app import MediaCrawlerGUI
        
        app = MediaCrawlerGUI()
        print("✓ GUI应用程序初始化成功")
        
        # 切换到快手平台
        app.platform_var.set("ks")
        app.on_platform_changed()
        
        # 检查所有快手统计相关的变量是否有默认值
        config_vars = {
            'enable_video_stats_var': bool,
            'enable_batch_stats_var': bool,
            'enable_engagement_rate_var': bool,
            'enable_performance_analysis_var': bool,
            'log_stats_data_var': bool,
            'batch_stats_delay_var': (int, float),
            'top_videos_count_var': int,
            'top_videos_metric_var': str,
            'stats_display_language_var': str
        }
        
        all_vars_ok = True
        for var_name, expected_type in config_vars.items():
            if hasattr(app, var_name):
                var = getattr(app, var_name)
                try:
                    value = var.get()
                    if isinstance(expected_type, tuple):
                        type_ok = any(isinstance(value, t) for t in expected_type)
                    else:
                        type_ok = isinstance(value, expected_type)
                    
                    if type_ok:
                        print(f"✓ {var_name} = {value} (类型: {type(value).__name__})")
                    else:
                        print(f"✗ {var_name} = {value} (期望类型: {expected_type}, 实际类型: {type(value)})")
                        all_vars_ok = False
                except Exception as e:
                    print(f"✗ {var_name} 获取值失败: {e}")
                    all_vars_ok = False
            else:
                print(f"✗ {var_name} 不存在")
                all_vars_ok = False
        
        if all_vars_ok:
            print("\n✓ 所有快手配置变量都正常")
        else:
            print("\n✗ 部分快手配置变量有问题")
        
        return all_vars_ok
        
    except Exception as e:
        print(f"✗ 快手配置组件测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("平台切换功能测试")
    print("=" * 60)
    
    tests = [
        ("快手配置组件测试", test_kuaishou_config_widgets),
        ("平台切换功能测试", test_platform_switching),
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
        print("🎉 所有平台切换测试都通过了！")
        return 0
    else:
        print("❌ 部分测试失败，请检查相关功能")
        return 1

if __name__ == "__main__":
    sys.exit(main())