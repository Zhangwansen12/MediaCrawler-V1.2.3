#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手完整数据流程测试脚本
测试从API调用到数据解析、统计分析的完整流程
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from media_platform.kuaishou.client import KuaiShouClient
from media_platform.kuaishou.video_stats_extractor import VideoStatsExtractor
from media_platform.kuaishou.stats_analyzer import StatsAnalyzer
from media_platform.kuaishou.field import VideoStats

# 模拟真实的快手API响应数据
MOCK_VIDEO_RESPONSES = [
    {
        "data": {
            "visionVideoDetail": {
                "photo": {
                    "id": "3xf6q2z8abc123",
                    "likeCount": 12345,
                    "realLikeCount": 12300,
                    "commentCount": 567,
                    "shareCount": 89,
                    "collectCount": 234,
                    "viewCount": 98765,
                    "duration": 15000,
                    "timestamp": 1640995200000,
                    "caption": "热门视频1"
                },
                "author": {
                    "name": "用户A",
                    "id": "userA123"
                }
            }
        }
    },
    {
        "data": {
            "visionVideoDetail": {
                "photo": {
                    "id": "3xf6q2z8def456",
                    "likeCount": 8900,
                    "realLikeCount": 8850,
                    "commentCount": 234,
                    "shareCount": 45,
                    "collectCount": 123,
                    "viewCount": 45678,
                    "duration": 12000,
                    "timestamp": 1640995300000,
                    "caption": "热门视频2"
                },
                "author": {
                    "name": "用户B",
                    "id": "userB456"
                }
            }
        }
    },
    {
        "data": {
            "visionVideoDetail": {
                "photo": {
                    "id": "3xf6q2z8ghi789",
                    "likeCount": 5600,
                    "realLikeCount": 5580,
                    "commentCount": 156,
                    "shareCount": 23,
                    "collectCount": 67,
                    "viewCount": 23456,
                    "duration": 18000,
                    "timestamp": 1640995400000,
                    "caption": "热门视频3"
                },
                "author": {
                    "name": "用户C",
                    "id": "userC789"
                }
            }
        }
    }
]

async def test_complete_data_flow():
    """测试完整的数据流程"""
    print("=" * 60)
    print("快手完整数据流程测试")
    print("=" * 60)
    
    # 创建模拟客户端
    mock_page = MagicMock()
    mock_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    mock_cookies = {"kpn": "KUAISHOU_VISION"}
    
    client = KuaiShouClient(
        headers=mock_headers,
        playwright_page=mock_page,
        cookie_dict=mock_cookies
    )
    
    test_results = []
    video_stats_list = []
    
    print("\n=== 步骤1: 批量获取视频数据 ===")
    
    # 模拟批量获取视频统计数据
    video_ids = ["3xf6q2z8abc123", "3xf6q2z8def456", "3xf6q2z8ghi789"]
    
    with patch.object(client, 'request', new_callable=AsyncMock) as mock_request:
        # 设置不同的响应数据
        mock_request.side_effect = [resp["data"] for resp in MOCK_VIDEO_RESPONSES]
        
        try:
            batch_stats = []
            for i, video_id in enumerate(video_ids):
                stats = await client.get_video_stats(video_id)
                if stats:
                    batch_stats.append(stats)
                    print(f"✓ 获取视频 {video_id} 统计数据成功")
                    print(f"  - 点赞: {stats['like_count']:,}")
                    print(f"  - 评论: {stats['comment_count']:,}")
                    print(f"  - 分享: {stats['share_count']:,}")
                    print(f"  - 收藏: {stats['collect_count']:,}")
                    print(f"  - 播放: {stats['view_count']:,}")
                else:
                    print(f"✗ 获取视频 {video_id} 统计数据失败")
            
            if len(batch_stats) == len(video_ids):
                print(f"✓ 批量获取成功，共获取 {len(batch_stats)} 个视频统计")
                test_results.append("批量数据获取: ✓")
            else:
                print(f"✗ 批量获取部分失败，期望 {len(video_ids)} 个，实际 {len(batch_stats)} 个")
                test_results.append("批量数据获取: ✗")
                
        except Exception as e:
            print(f"✗ 批量获取异常: {e}")
            test_results.append("批量数据获取: ✗")
            batch_stats = []
    
    print("\n=== 步骤2: 数据结构转换 ===")
    
    try:
        # 将字典数据转换为VideoStats对象
        for stats_dict in batch_stats:
            video_stats = VideoStats(
                video_id=stats_dict['video_id'],
                like_count=stats_dict['like_count'],
                real_like_count=stats_dict['real_like_count'],
                comment_count=stats_dict['comment_count'],
                share_count=stats_dict['share_count'],
                collect_count=stats_dict['collect_count'],
                view_count=stats_dict['view_count'],
                duration=stats_dict['duration'],
                timestamp=stats_dict['timestamp']
            )
            video_stats_list.append(video_stats)
        
        print(f"✓ 成功转换 {len(video_stats_list)} 个VideoStats对象")
        test_results.append("数据结构转换: ✓")
        
    except Exception as e:
        print(f"✗ 数据结构转换失败: {e}")
        test_results.append("数据结构转换: ✗")
    
    print("\n=== 步骤3: 统计分析 ===")
    
    if video_stats_list:
        try:
            # 进行统计分析
            analysis = StatsAnalyzer.analyze_video_performance(video_stats_list)
            
            print("✓ 统计分析完成")
            print(f"  - 分析视频数量: {analysis['total_videos']}")
            print(f"  - 总点赞数: {analysis['like_stats']['total']:,}")
            print(f"  - 平均点赞数: {analysis['like_stats']['average']:,}")
            print(f"  - 总评论数: {analysis['comment_stats']['total']:,}")
            print(f"  - 平均评论数: {analysis['comment_stats']['average']:,}")
            print(f"  - 总分享数: {analysis['share_stats']['total']:,}")
            print(f"  - 平均分享数: {analysis['share_stats']['average']:,}")
            print(f"  - 总收藏数: {analysis['collect_stats']['total']:,}")
            print(f"  - 平均收藏数: {analysis['collect_stats']['average']:,}")
            
            test_results.append("统计分析: ✓")
            
        except Exception as e:
            print(f"✗ 统计分析失败: {e}")
            test_results.append("统计分析: ✗")
    else:
        print("✗ 无数据可供分析")
        test_results.append("统计分析: ✗")
    
    print("\n=== 步骤4: 数据格式化显示 ===")
    
    if video_stats_list:
        try:
            for stats in video_stats_list:
                formatted_display = VideoStatsExtractor.format_stats_for_display(stats)
                engagement_rate = VideoStatsExtractor.get_engagement_rate(stats)
                
                print(f"✓ 视频 {stats.video_id}:")
                print(f"  - 格式化显示: {formatted_display}")
                print(f"  - 互动率: {engagement_rate}%")
            
            test_results.append("数据格式化: ✓")
            
        except Exception as e:
            print(f"✗ 数据格式化失败: {e}")
            test_results.append("数据格式化: ✗")
    else:
        print("✗ 无数据可供格式化")
        test_results.append("数据格式化: ✗")
    
    print("\n=== 步骤5: 生成统计报告 ===")
    
    if video_stats_list:
        try:
            report = StatsAnalyzer.generate_stats_report(video_stats_list)
            print("✓ 统计报告生成成功")
            print("报告预览:")
            print("-" * 40)
            # 只显示报告的前几行
            report_lines = report.split('\n')[:15]
            for line in report_lines:
                print(line)
            print("... (报告内容已截断)")
            print("-" * 40)
            
            test_results.append("统计报告: ✓")
            
        except Exception as e:
            print(f"✗ 统计报告生成失败: {e}")
            test_results.append("统计报告: ✗")
    else:
        print("✗ 无数据可生成报告")
        test_results.append("统计报告: ✗")
    
    print("\n=== 步骤6: 数据验证 ===")
    
    try:
        # 验证数据的完整性和准确性
        validation_passed = True
        
        for stats in video_stats_list:
            # 检查所有统计数据都是非负整数
            if not all(isinstance(getattr(stats, field), int) and getattr(stats, field) >= 0 
                      for field in ['like_count', 'comment_count', 'share_count', 'collect_count', 'view_count']):
                validation_passed = False
                print(f"✗ 视频 {stats.video_id} 数据类型验证失败")
                break
            
            # 检查播放量应该大于等于点赞数（合理性检查）
            if stats.view_count < stats.like_count:
                print(f"⚠ 视频 {stats.video_id} 播放量({stats.view_count})小于点赞数({stats.like_count})，可能存在数据异常")
        
        if validation_passed:
            print("✓ 数据验证通过")
            test_results.append("数据验证: ✓")
        else:
            print("✗ 数据验证失败")
            test_results.append("数据验证: ✗")
            
    except Exception as e:
        print(f"✗ 数据验证异常: {e}")
        test_results.append("数据验证: ✗")
    
    # 输出最终测试结果
    print("\n" + "=" * 60)
    print("完整流程测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for result in test_results:
        status = "✓" if "✓" in result else "✗"
        print(f"  {result}")
        if "✓" in result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 完整数据流程测试全部通过！")
        print("✅ 快手社交互动数据获取功能已完全就绪。")
        return True
    else:
        print("❌ 部分流程测试失败，需要进一步检查。")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_complete_data_flow())
    exit(0 if success else 1)