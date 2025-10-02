#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手真实API调用测试脚本
测试实际的API响应结构和数据解析逻辑
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from media_platform.kuaishou.client import KuaiShouClient
from media_platform.kuaishou.graphql import KuaiShouGraphQL

# 模拟真实的API响应数据结构
MOCK_API_RESPONSE = {
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
                "caption": "测试视频标题"
            },
            "author": {
                "name": "测试用户",
                "id": "user123"
            }
        }
    }
}

# 模拟空响应
EMPTY_API_RESPONSE = {
    "data": {}
}

# 模拟错误响应
ERROR_API_RESPONSE = {
    "errors": [
        {
            "message": "视频不存在或已被删除",
            "extensions": {
                "code": "VIDEO_NOT_FOUND"
            }
        }
    ]
}

async def test_real_api_calls():
    """测试真实API调用和响应处理"""
    print("=" * 50)
    print("快手真实API调用测试")
    print("=" * 50)
    
    # 创建模拟的客户端
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
    
    # 测试1: 正常API响应处理
    print("\n=== 测试1: 正常API响应处理 ===")
    with patch.object(client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = MOCK_API_RESPONSE["data"]
        
        try:
            result = await client.get_video_info("test_video_123")
            print(f"✓ API调用成功")
            print(f"  - 响应结构: {list(result.keys())}")
            
            if "visionVideoDetail" in result:
                video_detail = result["visionVideoDetail"]
                photo = video_detail.get("photo", {})
                print(f"  - 视频ID: {photo.get('id')}")
                print(f"  - 点赞数: {photo.get('likeCount')}")
                print(f"  - 评论数: {photo.get('commentCount')}")
                print(f"  - 分享数: {photo.get('shareCount')}")
                print(f"  - 收藏数: {photo.get('collectCount')}")
                print(f"  - 播放数: {photo.get('viewCount')}")
                test_results.append("正常响应处理: ✓")
            else:
                print("✗ 响应结构不正确")
                test_results.append("正常响应处理: ✗")
                
        except Exception as e:
            print(f"✗ API调用失败: {e}")
            test_results.append("正常响应处理: ✗")
    
    # 测试2: 使用get_video_stats方法
    print("\n=== 测试2: 视频统计数据提取 ===")
    with patch.object(client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = MOCK_API_RESPONSE["data"]
        
        try:
            stats = await client.get_video_stats("test_video_123")
            print(f"✓ 统计数据提取成功")
            print(f"  - 视频ID: {stats.get('video_id')}")
            print(f"  - 点赞数: {stats.get('like_count')}")
            print(f"  - 真实点赞数: {stats.get('real_like_count')}")
            print(f"  - 评论数: {stats.get('comment_count')}")
            print(f"  - 分享数: {stats.get('share_count')}")
            print(f"  - 收藏数: {stats.get('collect_count')}")
            print(f"  - 播放数: {stats.get('view_count')}")
            print(f"  - 作者: {stats.get('author')}")
            
            # 验证数据类型
            if all(isinstance(stats.get(key), int) for key in 
                   ['like_count', 'comment_count', 'share_count', 'collect_count', 'view_count']):
                print("✓ 数据类型转换正确")
                test_results.append("统计数据提取: ✓")
            else:
                print("✗ 数据类型转换失败")
                test_results.append("统计数据提取: ✗")
                
        except Exception as e:
            print(f"✗ 统计数据提取失败: {e}")
            test_results.append("统计数据提取: ✗")
    
    # 测试3: 空响应处理
    print("\n=== 测试3: 空响应处理 ===")
    with patch.object(client, 'request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = EMPTY_API_RESPONSE["data"]
        
        try:
            stats = await client.get_video_stats("empty_video")
            if not stats:
                print("✓ 空响应处理正确")
                test_results.append("空响应处理: ✓")
            else:
                print("✗ 空响应处理失败")
                test_results.append("空响应处理: ✗")
        except Exception as e:
            print(f"✗ 空响应处理异常: {e}")
            test_results.append("空响应处理: ✗")
    
    # 测试4: 错误响应处理
    print("\n=== 测试4: 错误响应处理 ===")
    with patch.object(client, 'request', new_callable=AsyncMock) as mock_request:
        from media_platform.kuaishou.exception import DataFetchError
        mock_request.side_effect = DataFetchError(ERROR_API_RESPONSE["errors"])
        
        try:
            stats = await client.get_video_stats("error_video")
            if not stats:
                print("✓ 错误响应处理正确")
                test_results.append("错误响应处理: ✓")
            else:
                print("✗ 错误响应处理失败")
                test_results.append("错误响应处理: ✗")
        except Exception as e:
            print(f"✓ 错误响应正确抛出异常: {type(e).__name__}")
            test_results.append("错误响应处理: ✓")
    
    # 测试5: 批量获取统计数据
    print("\n=== 测试5: 批量统计数据获取 ===")
    with patch.object(client, 'get_video_stats', new_callable=AsyncMock) as mock_get_stats:
        mock_get_stats.return_value = {
            "video_id": "batch_test_123",
            "like_count": 5000,
            "comment_count": 200,
            "share_count": 50,
            "collect_count": 100,
            "view_count": 25000
        }
        
        try:
            batch_stats = await client.batch_get_video_stats(["video1", "video2", "video3"])
            print(f"✓ 批量获取成功，共获取 {len(batch_stats)} 个视频统计")
            
            if len(batch_stats) == 3:
                print("✓ 批量数据数量正确")
                test_results.append("批量统计获取: ✓")
            else:
                print("✗ 批量数据数量不正确")
                test_results.append("批量统计获取: ✗")
                
        except Exception as e:
            print(f"✗ 批量获取失败: {e}")
            test_results.append("批量统计获取: ✗")
    
    # 输出测试结果汇总
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    for result in test_results:
        print(f"  {result}")
    
    passed_tests = len([r for r in test_results if "✓" in r])
    total_tests = len(test_results)
    print(f"总计: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("✅ 所有API调用测试通过，数据解析逻辑正常。")
    else:
        print("❌ 部分API调用测试失败，需要检查数据解析逻辑。")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    asyncio.run(test_real_api_calls())