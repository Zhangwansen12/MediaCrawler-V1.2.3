#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手数据获取功能测试脚本
专门测试点赞数、分享数、评论数等关键数据指标的获取
"""

import asyncio
import json
import sys
import os
from typing import Dict, List

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

from media_platform.kuaishou.video_stats_extractor import VideoStatsExtractor
from media_platform.kuaishou.field import VideoStats
from tools import utils


def test_data_extraction_with_mock_data():
    """使用模拟数据测试数据提取功能"""
    print("=== 测试数据提取功能 ===")
    
    # 模拟快手API返回的数据结构
    mock_video_detail = {
        "visionVideoDetail": {
            "status": 1,
            "photo": {
                "id": "test_video_123",
                "likeCount": 1500,
                "realLikeCount": 1450,
                "commentCount": 89,
                "shareCount": 234,
                "collectCount": 156,
                "viewCount": 12500,
                "duration": 45000,
                "timestamp": 1640995200,
                "caption": "测试视频标题"
            },
            "author": {
                "name": "测试用户",
                "id": "test_user_456"
            }
        }
    }
    
    # 测试数据提取
    print("1. 测试VideoStatsExtractor.extract_video_stats()...")
    video_stats = VideoStatsExtractor.extract_video_stats(mock_video_detail)
    
    if video_stats:
        print(f"✓ 数据提取成功:")
        print(f"  - 视频ID: {video_stats.video_id}")
        print(f"  - 点赞数: {video_stats.like_count}")
        print(f"  - 真实点赞数: {video_stats.real_like_count}")
        print(f"  - 评论数: {video_stats.comment_count}")
        print(f"  - 分享数: {video_stats.share_count}")
        print(f"  - 收藏数: {video_stats.collect_count}")
        print(f"  - 观看数: {video_stats.view_count}")
        print(f"  - 时长: {video_stats.duration}ms")
        
        # 验证数据正确性
        assert video_stats.like_count == 1500, f"点赞数不匹配: 期望1500, 实际{video_stats.like_count}"
        assert video_stats.comment_count == 89, f"评论数不匹配: 期望89, 实际{video_stats.comment_count}"
        assert video_stats.share_count == 234, f"分享数不匹配: 期望234, 实际{video_stats.share_count}"
        assert video_stats.collect_count == 156, f"收藏数不匹配: 期望156, 实际{video_stats.collect_count}"
        assert video_stats.view_count == 12500, f"观看数不匹配: 期望12500, 实际{video_stats.view_count}"
        
        print("✓ 所有数据字段验证通过!")
        
        # 测试互动率计算
        stats_dict = video_stats._asdict()
        engagement_rate = VideoStatsExtractor.get_engagement_rate(stats_dict)
        print(f"  - 互动率: {engagement_rate}%")
        
        # 测试格式化显示
        formatted_stats = VideoStatsExtractor.format_stats_for_display(stats_dict)
        print(f"✓ 格式化显示: {formatted_stats}")
        
        return True
    else:
        print("✗ 数据提取失败")
        return False


def test_edge_cases():
    """测试边界情况和错误处理"""
    print("\n=== 测试边界情况 ===")
    
    # 测试空数据
    print("1. 测试空数据处理...")
    result = VideoStatsExtractor.extract_video_stats({})
    if result is None:
        print("✓ 空数据处理正确")
    else:
        print("✗ 空数据处理失败")
        return False
    
    # 测试缺少字段的数据
    print("2. 测试缺少字段的数据...")
    incomplete_data = {
        "visionVideoDetail": {
            "photo": {
                "id": "incomplete_test",
                "likeCount": 100
                # 缺少其他字段
            }
        }
    }
    
    result = VideoStatsExtractor.extract_video_stats(incomplete_data)
    if result and result.like_count == 100:
        print("✓ 缺少字段的数据处理正确，使用默认值")
        print(f"  - 点赞数: {result.like_count}")
        print(f"  - 评论数: {result.comment_count} (默认值)")
        print(f"  - 分享数: {result.share_count} (默认值)")
    else:
        print("✗ 缺少字段的数据处理失败")
        return False
    
    # 测试不同数据结构
    print("3. 测试直接photo数据结构...")
    direct_photo_data = {
        "photo": {
            "id": "direct_test",
            "likeCount": 500,
            "commentCount": 25,
            "shareCount": 50,
            "collectCount": 30,
            "viewCount": 2000,
            "duration": 30000,
            "timestamp": 1640995200
        }
    }
    
    result = VideoStatsExtractor.extract_video_stats(direct_photo_data)
    if result and result.like_count == 500:
        print("✓ 直接photo数据结构处理正确")
    else:
        print("✗ 直接photo数据结构处理失败")
        return False
    
    return True


def test_data_validation():
    """测试数据验证和类型转换"""
    print("\n=== 测试数据验证 ===")
    
    # 测试字符串数字转换
    string_number_data = {
        "visionVideoDetail": {
            "photo": {
                "id": "string_test",
                "likeCount": "1500",  # 字符串格式
                "commentCount": "89",
                "shareCount": "234",
                "collectCount": "156",
                "viewCount": "12500",
                "duration": "45000",
                "timestamp": "1640995200"
            }
        }
    }
    
    result = VideoStatsExtractor.extract_video_stats(string_number_data)
    if result and isinstance(result.like_count, int) and result.like_count == 1500:
        print("✓ 字符串数字转换正确")
    else:
        print("✗ 字符串数字转换失败")
        return False
    
    return True


def main():
    """主测试函数"""
    print("开始快手数据获取功能测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("数据提取功能", test_data_extraction_with_mock_data()))
    test_results.append(("边界情况处理", test_edge_cases()))
    test_results.append(("数据验证", test_data_validation()))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过! 快手数据获取功能正常。")
        return True
    else:
        print("❌ 部分测试失败，需要检查数据获取逻辑。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)