#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终GUI集成测试脚本
测试快手视频统计功能的完整集成
"""

import tkinter as tk
import sys
import os
import re

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui_app import MediaCrawlerGUI

def test_complete_integration():
    """测试完整的GUI集成功能"""
    print("最终GUI集成测试")
    print("=" * 60)
    
    try:
        # 创建GUI应用程序
        app = MediaCrawlerGUI()
        root = app.root
        print("✓ GUI应用程序初始化成功")
        
        # 测试1: 验证所有快手统计相关的GUI组件
        print("\n测试1: 验证快手统计GUI组件")
        print("-" * 40)
        
        # 检查所有必需的变量
        required_vars = [
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
        
        for var_name in required_vars:
            if hasattr(app, var_name):
                var_obj = getattr(app, var_name)
                value = var_obj.get()
                print(f"✓ {var_name} = {value}")
            else:
                print(f"✗ 缺少变量: {var_name}")
                return False
        
        # 测试2: 验证方法存在
        print("\n测试2: 验证关键方法")
        print("-" * 40)
        
        required_methods = [
            'on_platform_changed',
            'create_kuaishou_stats_config', 
            'update_kuaishou_config'
        ]
        
        for method_name in required_methods:
            if hasattr(app, method_name):
                print(f"✓ 方法 {method_name} 存在")
            else:
                print(f"✗ 缺少方法: {method_name}")
                return False
        
        # 测试3: 测试平台切换功能
        print("\n测试3: 测试平台切换功能")
        print("-" * 40)
        
        # 切换到快手平台
        app.platform_var.set("ks")
        app.on_platform_changed()
        
        # 检查快手统计配置是否可见
        if hasattr(app, 'kuaishou_stats_frame'):
            try:
                grid_info = app.kuaishou_stats_frame.grid_info()
                if grid_info:
                    print("✓ 切换到快手平台时，统计配置可见")
                else:
                    print("✗ 切换到快手平台时，统计配置不可见")
                    return False
            except tk.TclError:
                print("✗ 快手统计配置框架状态异常")
                return False
        else:
            print("✗ 快手统计配置框架不存在")
            return False
        
        # 切换到其他平台
        app.platform_var.set("dy")
        app.on_platform_changed()
        
        try:
            grid_info = app.kuaishou_stats_frame.grid_info()
            if not grid_info:
                print("✓ 切换到其他平台时，统计配置隐藏")
            else:
                print("✗ 切换到其他平台时，统计配置仍然可见")
                return False
        except tk.TclError:
            print("✓ 切换到其他平台时，统计配置隐藏")
        
        # 测试4: 测试配置更新功能
        print("\n测试4: 测试配置更新功能")
        print("-" * 40)
        
        # 切换回快手平台并设置一些配置值
        app.platform_var.set("ks")
        app.on_platform_changed()
        
        # 设置测试值
        app.enable_video_stats_var.set(True)
        app.batch_stats_delay_var.set(2.5)
        app.top_videos_count_var.set(20)
        app.top_videos_metric_var.set("comments")
        app.stats_display_language_var.set("en")
        
        print("✓ 设置测试配置值")
        
        # 测试配置更新方法
        try:
            app.update_kuaishou_config()
            print("✓ 配置更新方法执行成功")
            
            # 验证配置文件是否更新
            config_file = os.path.join(os.path.dirname(__file__), "config", "ks_config.py")
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查关键配置是否更新
                if "ENABLE_VIDEO_STATS = True" in content:
                    print("✓ ENABLE_VIDEO_STATS 配置更新成功")
                else:
                    print("✗ ENABLE_VIDEO_STATS 配置更新失败")
                    return False
                
                if "BATCH_STATS_DELAY = 2.5" in content:
                    print("✓ BATCH_STATS_DELAY 配置更新成功")
                else:
                    print("✗ BATCH_STATS_DELAY 配置更新失败")
                    return False
                    
                if "TOP_VIDEOS_COUNT = 20" in content:
                    print("✓ TOP_VIDEOS_COUNT 配置更新成功")
                else:
                    print("✗ TOP_VIDEOS_COUNT 配置更新失败")
                    return False
                    
            else:
                print("✗ 配置文件不存在")
                return False
                
        except Exception as e:
            print(f"✗ 配置更新失败: {e}")
            return False
        
        # 测试5: 测试GUI布局
        print("\n测试5: 测试GUI布局")
        print("-" * 40)
        
        # 检查主要组件是否正确布局
        try:
            # 强制更新GUI
            root.update_idletasks()
            
            # 检查快手统计配置框架的子组件
            if hasattr(app, 'kuaishou_stats_frame'):
                children = app.kuaishou_stats_frame.winfo_children()
                if len(children) > 0:
                    print(f"✓ 快手统计配置包含 {len(children)} 个子组件")
                else:
                    print("✗ 快手统计配置没有子组件")
                    return False
            
            print("✓ GUI布局测试通过")
            
        except Exception as e:
            print(f"✗ GUI布局测试失败: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 所有集成测试都通过了！")
        print("快手视频统计功能已成功集成到GUI中")
        
        # 清理
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_integration()
    if success:
        print("\n✅ 最终集成测试: 成功")
        sys.exit(0)
    else:
        print("\n❌ 最终集成测试: 失败")
        sys.exit(1)