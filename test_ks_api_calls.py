#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手API调用测试脚本
测试API调用接口和响应处理逻辑
"""

import asyncio
import json
import sys
import os
from typing import Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

# 添加项目根目录到路径
sys.path.append(os.path.dirname(__file__))

from media_platform.kuaishou.client import KuaiShouClient
from media_platform.kuaishou.graphql import KuaiShouGraphQL
from tools import utils


def create_mock_client():
    """创建模拟的KuaiShouClient"""
    # 创建模拟的页面和cookie
    mock_page = MagicMock()
    mock_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    mock_cookies = {"sessionid": "test_session"}
    
    # 创建客户端实例
    client = KuaiShouClient(
        headers=mock_headers,
        playwright_page=mock_page,
        cookie_dict=mock_cookies
    )
    
    return client


def test_graphql_queries():
    """测试GraphQL查询配置"""
    print("=== 测试GraphQL查询配置 ===")
    
    try:
        graphql = KuaiShouGraphQL()
        
        # 检查关键查询是否存在
        required_queries = [
            "search_query",
            "video_detail", 
            "comment_list",
            "vision_profile",
            "vision_profile_photo_list"
        ]
        
        for query_name in required_queries:
            query = graphql.get(query_name)
            if query and query != "Query not found":
                print(f"✓ {query_name} 查询配置正确")
                
                # 检查video_detail查询是否包含必要字段
                if query_name == "video_detail":
                    required_fields = ["likeCount", "commentCount", "shareCount", "collectCount", "viewCount"]
                    for field in required_fields:
                        if field in query:
                            print(f"  ✓ 包含字段: {field}")
                        else:
                            print(f"  ✗ 缺少字段: {field}")
                            return False
            else:
                print(f"✗ {query_name} 查询配置缺失")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ GraphQL查询配置测试失败: {e}")
        return False


async def test_api_request_structure():
    """测试API请求结构"""
    print("\n=== 测试API请求结构 ===")
    
    try:
        client = create_mock_client()
        
        # 模拟成功的API响应
        mock_response = {
            "data": {
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
                        "caption": "测试视频"
                    },
                    "author": {
                        "name": "测试用户",
                        "id": "test_user"
                    }
                }
            }
        }
        
        # 模拟post方法
        with patch.object(client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            # 测试get_video_info方法
            print("1. 测试get_video_info API调用...")
            result = await client.get_video_info("test_video_123")
            
            # 验证调用参数
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            post_data = call_args[0][1]  # 第二个参数是data
            
            # 检查请求结构
            assert post_data["operationName"] == "visionVideoDetail", "operationName不正确"
            assert post_data["variables"]["photoId"] == "test_video_123", "photoId参数不正确"
            assert "query" in post_data, "缺少query字段"
            
            print("✓ API请求结构正确")
            print(f"  - operationName: {post_data['operationName']}")
            print(f"  - photoId: {post_data['variables']['photoId']}")
            print(f"  - 包含GraphQL查询: {'query' in post_data}")
            
            # 验证响应处理
            if result == mock_response:
                print("✓ API响应处理正确")
                return True
            else:
                print("✗ API响应处理失败")
                return False
                
    except Exception as e:
        print(f"✗ API请求结构测试失败: {e}")
        return False


async def test_video_stats_extraction():
    """测试视频统计数据提取"""
    print("\n=== 测试视频统计数据提取 ===")
    
    try:
        client = create_mock_client()
        
        # 模拟API响应
        mock_api_response = {
            "data": {
                "visionVideoDetail": {
                    "status": 1,
                    "photo": {
                        "id": "stats_test_456",
                        "likeCount": 2500,
                        "realLikeCount": 2400,
                        "commentCount": 150,
                        "shareCount": 300,
                        "collectCount": 200,
                        "viewCount": 18000,
                        "duration": 60000,
                        "timestamp": 1640995200,
                        "caption": "统计测试视频"
                    },
                    "author": {
                        "name": "统计测试用户",
                        "id": "stats_user"
                    }
                }
            }
        }
        
        with patch.object(client, 'get_video_info', new_callable=AsyncMock) as mock_get_info:
            mock_get_info.return_value = mock_api_response
            
            # 测试get_video_stats方法
            print("1. 测试get_video_stats方法...")
            stats = await client.get_video_stats("stats_test_456")
            
            if stats:
                print("✓ 统计数据提取成功")
                print(f"  - 视频ID: {stats.get('video_id')}")
                print(f"  - 点赞数: {stats.get('like_count')}")
                print(f"  - 评论数: {stats.get('comment_count')}")
                print(f"  - 分享数: {stats.get('share_count')}")
                print(f"  - 收藏数: {stats.get('collect_count')}")
                print(f"  - 观看数: {stats.get('view_count')}")
                
                # 验证数据正确性
                expected_values = {
                    'video_id': 'stats_test_456',
                    'like_count': 2500,
                    'comment_count': 150,
                    'share_count': 300,
                    'collect_count': 200,
                    'view_count': 18000
                }
                
                for key, expected in expected_values.items():
                    if stats.get(key) == expected:
                        print(f"  ✓ {key}: {stats.get(key)} (正确)")
                    else:
                        print(f"  ✗ {key}: 期望{expected}, 实际{stats.get(key)}")
                        return False
                
                return True
            else:
                print("✗ 统计数据提取失败")
                return False
                
    except Exception as e:
        print(f"✗ 视频统计数据提取测试失败: {e}")
        return False


async def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        client = create_mock_client()
        
        # 测试空响应处理
        print("1. 测试空响应处理...")
        with patch.object(client, 'get_video_info', new_callable=AsyncMock) as mock_get_info:
            mock_get_info.return_value = {}
            
            stats = await client.get_video_stats("empty_test")
            if stats == {}:
                print("✓ 空响应处理正确")
            else:
                print("✗ 空响应处理失败")
                return False
        
        # 测试异常处理
        print("2. 测试异常处理...")
        with patch.object(client, 'get_video_info', new_callable=AsyncMock) as mock_get_info:
            mock_get_info.side_effect = Exception("网络错误")
            
            stats = await client.get_video_stats("error_test")
            if stats == {}:
                print("✓ 异常处理正确")
            else:
                print("✗ 异常处理失败")
                return False
        
        # 测试无效数据结构处理
        print("3. 测试无效数据结构处理...")
        with patch.object(client, 'get_video_info', new_callable=AsyncMock) as mock_get_info:
            mock_get_info.return_value = {"data": {"invalid": "structure"}}
            
            stats = await client.get_video_stats("invalid_test")
            if stats == {}:
                print("✓ 无效数据结构处理正确")
                return True
            else:
                print("✗ 无效数据结构处理失败")
                return False
                
    except Exception as e:
        print(f"✗ 错误处理测试失败: {e}")
        return False


async def main():
    """主测试函数"""
    print("开始快手API调用测试...")
    print("=" * 50)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(("GraphQL查询配置", test_graphql_queries()))
    test_results.append(("API请求结构", await test_api_request_structure()))
    test_results.append(("视频统计数据提取", await test_video_stats_extraction()))
    test_results.append(("错误处理", await test_error_handling()))
    
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
        print("🎉 所有API调用测试通过! 快手API接口正常。")
        return True
    else:
        print("❌ 部分API调用测试失败，需要检查接口逻辑。")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)