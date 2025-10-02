#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手视频统计数据功能测试脚本
测试新增的评论数、分享数、收藏数抓取功能
"""

import asyncio
import json
import sys
import os
from typing import Dict, List

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from media_platform.kuaishou.field import VideoStats
from media_platform.kuaishou.video_stats_extractor import VideoStatsExtractor
from media_platform.kuaishou.stats_analyzer import StatsAnalyzer


def test_video_stats_extractor():
    """测试视频统计数据提取器"""
    print("=== 测试 VideoStatsExtractor ===")
    
    # 模拟视频详情数据
    mock_video_detail = {
        "visionVideoDetail": {
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
                "name": "测试用户"
            }
        }
    }
    
    try:
        # 测试统计数据提取
        stats = VideoStatsExtractor.extract_video_stats(mock_video_detail)
        print(f"✓ 统计数据提取成功: {stats}")
        
        # 将VideoStats转换为字典用于格式化显示测试
        stats_dict = {
            "video_id": stats.video_id,
            "like_count": stats.like_count,
            "real_like_count": stats.real_like_count,
            "comment_count": stats.comment_count,
            "share_count": stats.share_count,
            "collect_count": stats.collect_count,
            "view_count": stats.view_count,
            "duration": stats.duration,
            "timestamp": stats.timestamp
        }
        
        # 测试格式化显示
        formatted = VideoStatsExtractor.format_stats_for_display(stats_dict)
        print(f"✓ 格式化显示: {formatted}")
        
        # 测试互动率计算
        engagement_rate = VideoStatsExtractor.get_engagement_rate(stats_dict)
        print(f"✓ 互动率计算: {engagement_rate:.2f}%")
        
        return True
        
    except Exception as e:
        print(f"✗ VideoStatsExtractor 测试失败: {e}")
        return False


def test_stats_analyzer():
    """测试统计数据分析器"""
    print("\n=== 测试 StatsAnalyzer ===")
    
    # 模拟多个视频的统计数据
    mock_stats_list = [
        VideoStats(
            video_id="video_1",
            like_count=1500,
            real_like_count=1450,
            comment_count=89,
            share_count=234,
            collect_count=156,
            view_count=12500,
            duration=45000,
            timestamp=1640995200
        ),
        VideoStats(
            video_id="video_2",
            like_count=2300,
            real_like_count=2250,
            comment_count=145,
            share_count=378,
            collect_count=289,
            view_count=18900,
            duration=62000,
            timestamp=1641081600
        ),
        VideoStats(
            video_id="video_3",
            like_count=890,
            real_like_count=850,
            comment_count=56,
            share_count=123,
            collect_count=78,
            view_count=7800,
            duration=38000,
            timestamp=1641168000
        )
    ]
    
    try:
        # 测试性能分析
        performance = StatsAnalyzer.analyze_video_performance(mock_stats_list)
        print(f"✓ 性能分析成功:")
        print(f"  - 总点赞数: {performance['like_stats']['total']}")
        print(f"  - 平均观看数: {performance['view_stats']['average']:.0f}")
        print(f"  - 最高互动率: {performance['engagement_stats']['max']:.2f}%")
        
        # 测试热门视频查找
        top_videos = StatsAnalyzer.find_top_performing_videos(mock_stats_list, "like_count", 2)
        print(f"✓ 热门视频查找成功: 找到 {len(top_videos)} 个热门视频")
        
        # 测试视频对比
        comparison = StatsAnalyzer.compare_video_stats(mock_stats_list[0], mock_stats_list[1])
        print(f"✓ 视频对比成功: {comparison['summary']}")
        
        # 测试报告生成
        report = StatsAnalyzer.generate_stats_report(mock_stats_list)
        print(f"✓ 报告生成成功:")
        print(report[:200] + "..." if len(report) > 200 else report)
        
        return True
        
    except Exception as e:
        print(f"✗ StatsAnalyzer 测试失败: {e}")
        return False


def test_video_stats_namedtuple():
    """测试 VideoStats NamedTuple"""
    print("\n=== 测试 VideoStats NamedTuple ===")
    
    try:
        # 创建 VideoStats 实例
        stats = VideoStats(
            video_id="test_123",
            like_count=1000,
            real_like_count=950,
            comment_count=50,
            share_count=100,
            collect_count=75,
            view_count=5000,
            duration=30000,
            timestamp=1640995200
        )
        
        print(f"✓ VideoStats 创建成功: {stats}")
        print(f"  - 视频ID: {stats.video_id}")
        print(f"  - 点赞数: {stats.like_count}")
        print(f"  - 评论数: {stats.comment_count}")
        print(f"  - 分享数: {stats.share_count}")
        print(f"  - 收藏数: {stats.collect_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ VideoStats 测试失败: {e}")
        return False


def test_integration():
    """集成测试"""
    print("\n=== 集成测试 ===")
    
    try:
        # 模拟完整的数据处理流程
        mock_video_detail = {
            "visionVideoDetail": {
                "photo": {
                    "id": "integration_test_456",
                    "likeCount": 3200,
                    "realLikeCount": 3100,
                    "commentCount": 180,
                    "shareCount": 450,
                    "collectCount": 320,
                    "viewCount": 25000,
                    "duration": 55000,
                    "timestamp": 1641254400,
                    "caption": "集成测试视频"
                },
                "author": {
                    "name": "集成测试用户"
                }
            }
        }
        
        # 1. 提取统计数据
        stats_dict = VideoStatsExtractor.extract_video_stats(mock_video_detail)
        print(f"✓ 步骤1 - 数据提取: {stats_dict.video_id}")
        
        # 2. 转换为 NamedTuple
        stats = VideoStats(**{
            "video_id": stats_dict.video_id,
            "like_count": stats_dict.like_count,
            "real_like_count": stats_dict.real_like_count,
            "comment_count": stats_dict.comment_count,
            "share_count": stats_dict.share_count,
            "collect_count": stats_dict.collect_count,
            "view_count": stats_dict.view_count,
            "duration": stats_dict.duration,
            "timestamp": stats_dict.timestamp
        })
        print(f"✓ 步骤2 - 数据转换: {stats.video_id}")
        
        # 3. 计算互动率
        engagement_rate = VideoStatsExtractor.get_engagement_rate({
            "video_id": stats_dict.video_id,
            "like_count": stats_dict.like_count,
            "real_like_count": stats_dict.real_like_count,
            "comment_count": stats_dict.comment_count,
            "share_count": stats_dict.share_count,
            "collect_count": stats_dict.collect_count,
            "view_count": stats_dict.view_count,
            "duration": stats_dict.duration,
            "timestamp": stats_dict.timestamp
        })
        print(f"✓ 步骤3 - 互动率计算: {engagement_rate:.2f}%")
        
        # 4. 格式化显示
        formatted = VideoStatsExtractor.format_stats_for_display({
            "video_id": stats_dict.video_id,
            "like_count": stats_dict.like_count,
            "real_like_count": stats_dict.real_like_count,
            "comment_count": stats_dict.comment_count,
            "share_count": stats_dict.share_count,
            "collect_count": stats_dict.collect_count,
            "view_count": stats_dict.view_count,
            "duration": stats_dict.duration,
            "timestamp": stats_dict.timestamp
        })
        print(f"✓ 步骤4 - 格式化显示: {formatted}")
        
        print("✓ 集成测试通过!")
        return True
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("快手视频统计数据功能测试")
    print("=" * 50)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("VideoStats NamedTuple", test_video_stats_namedtuple()))
    test_results.append(("VideoStatsExtractor", test_video_stats_extractor()))
    test_results.append(("StatsAnalyzer", test_stats_analyzer()))
    test_results.append(("集成测试", test_integration()))
    
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
        print("🎉 所有测试通过! 快手视频统计数据功能已就绪。")
        return True
    else:
        print("❌ 部分测试失败，请检查相关功能。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)