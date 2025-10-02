# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

import asyncio
import json
import logging
import time
from typing import Dict, List, Optional, Any, Callable
from urllib.parse import urlencode

from playwright.async_api import Page, BrowserContext
from tenacity import retry, stop_after_attempt, wait_fixed

from tools import utils
from .client import XiaoHongShuClient
from .exception import DataFetchError


class XiaoHongShuMallClient:
    """小红书商城数据客户端"""
    
    def __init__(self, xhs_client: XiaoHongShuClient = None, playwright_page: Page = None):
        """
        初始化小红书商城客户端
        
        Args:
            xhs_client: 小红书客户端实例
            playwright_page: Playwright页面实例
        """
        self.xhs_client = xhs_client
        self.playwright_page = playwright_page
        self.logger = logging.getLogger(__name__)
        self._mall_host = "https://ark.xiaohongshu.com"
        self._product_host = "https://www.xiaohongshu.com"
        
    async def get_categories(self) -> List[Dict]:
        """
        获取商品分类列表
        
        Returns:
            分类列表
        """
        try:
            # 模拟获取分类数据
            categories = [
                {"category_id": "cat_001", "name": "美妆护肤", "parent_id": "", "level": 1},
                {"category_id": "cat_002", "name": "服装鞋包", "parent_id": "", "level": 1},
                {"category_id": "cat_003", "name": "家居生活", "parent_id": "", "level": 1},
                {"category_id": "cat_004", "name": "数码电器", "parent_id": "", "level": 1},
                {"category_id": "cat_005", "name": "食品饮料", "parent_id": "", "level": 1},
                {"category_id": "cat_006", "name": "面部护理", "parent_id": "cat_001", "level": 2},
                {"category_id": "cat_007", "name": "彩妆", "parent_id": "cat_001", "level": 2},
                {"category_id": "cat_008", "name": "女装", "parent_id": "cat_002", "level": 2},
                {"category_id": "cat_009", "name": "男装", "parent_id": "cat_002", "level": 2},
                {"category_id": "cat_010", "name": "鞋靴", "parent_id": "cat_002", "level": 2}
            ]
            
            return categories
        except Exception as e:
            self.logger.error(f"获取分类列表失败: {e}")
            return []
    async def get_mall_products(
        self, 
        keyword: str = "", 
        category_id: str = "", 
        page: int = 1, 
        page_size: int = 20,
        sort_type: str = "default"
    ) -> Dict:
        """
        获取商城商品列表
        Args:
            keyword: 搜索关键词
            category_id: 商品分类ID
            page: 页码
            page_size: 每页数量
            sort_type: 排序类型 (default, price_asc, price_desc, sales, newest)
        Returns:
            商品列表数据
        """
        uri = "/api/sns/web/v1/mall/search"
        params = {
            "keyword": keyword,
            "category_id": category_id,
            "page": page,
            "page_size": page_size,
            "sort": sort_type,
            "image_formats": "jpg,webp,avif"
        }
        
        try:
            return await self.xhs_client.get(uri, params)
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallClient.get_mall_products] 获取商品列表失败: {e}")
            return {"items": [], "has_more": False, "total": 0}
    
    async def get_product_list(self, category: str = "", keyword: str = "", page: int = 1, limit: int = 20) -> List[Dict]:
        """
        获取商品列表
        
        Args:
            category: 商品分类
            keyword: 搜索关键词
            page: 页码
            limit: 每页数量
            
        Returns:
            商品列表
        """
        try:
            # 模拟获取商品列表数据
            products = []
            for i in range(limit):
                product = {
                    "product_id": f"product_{page}_{i+1}",
                    "title": f"商品 {keyword or category} {i+1}",
                    "price": 99.99 + i * 10,
                    "sales_count": 100 + i * 5,
                    "rating": 4.0 + (i % 5) * 0.2,
                    "shop_name": f"店铺{i+1}",
                    "category": category or "默认分类",
                    "image_url": f"https://example.com/image_{i+1}.jpg",
                    "description": f"这是商品{i+1}的描述",
                    "created_time": int(time.time()),
                    "updated_time": int(time.time())
                }
                products.append(product)
            
            return products
        except Exception as e:
            self.logger.error(f"获取商品列表失败: {e}")
            return []
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def get_product_detail(self, product_id: str) -> Dict:
        """
        获取商品详情
        Args:
            product_id: 商品ID
        Returns:
            商品详情数据
        """
        uri = f"/api/sns/web/v1/mall/product/{product_id}"
        params = {
            "image_formats": "jpg,webp,avif"
        }
        
        try:
            return await self.xhs_client.get(uri, params)
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallClient.get_product_detail] 获取商品详情失败: {e}")
            return {}
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def get_product_reviews(
        self, 
        product_id: str, 
        page: int = 1, 
        page_size: int = 20
    ) -> Dict:
        """
        获取商品评价
        Args:
            product_id: 商品ID
            page: 页码
            page_size: 每页数量
        Returns:
            评价数据
        """
        uri = "/api/sns/web/v1/mall/product/reviews"
        params = {
            "product_id": product_id,
            "page": page,
            "page_size": page_size,
            "image_formats": "jpg,webp,avif"
        }
        
        try:
            return await self.xhs_client.get(uri, params)
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallClient.get_product_reviews] 获取商品评价失败: {e}")
            return {"items": [], "has_more": False, "total": 0}
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def get_mall_categories(self) -> Dict:
        """
        获取商城分类列表
        Returns:
            分类数据
        """
        uri = "/api/sns/web/v1/mall/categories"
        
        try:
            return await self.xhs_client.get(uri, {})
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallClient.get_mall_categories] 获取商城分类失败: {e}")
            return {"categories": []}
    
    async def get_trending_products(self, limit: int = 50) -> List[Dict]:
        """
        获取热门商品
        Args:
            limit: 获取数量限制
        Returns:
            热门商品列表
        """
        try:
            # 获取热门商品，按销量排序
            result = await self.get_mall_products(
                keyword="",
                page=1,
                page_size=limit,
                sort_type="sales"
            )
            return result.get("items", [])
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallClient.get_trending_products] 获取热门商品失败: {e}")
            return []
    
    async def search_products_by_category(
        self, 
        category_id: str, 
        max_pages: int = 5
    ) -> List[Dict]:
        """
        按分类搜索商品
        Args:
            category_id: 分类ID
            max_pages: 最大页数
        Returns:
            商品列表
        """
        all_products = []
        page = 1
        
        while page <= max_pages:
            try:
                result = await self.get_mall_products(
                    category_id=category_id,
                    page=page,
                    page_size=20
                )
                
                products = result.get("items", [])
                if not products:
                    break
                    
                all_products.extend(products)
                
                if not result.get("has_more", False):
                    break
                    
                page += 1
                await asyncio.sleep(1)  # 控制请求频率
                
            except Exception as e:
                utils.logger.error(f"[XiaoHongShuMallClient.search_products_by_category] 第{page}页获取失败: {e}")
                break
        
        return all_products


class XiaoHongShuMallDataProcessor:
    """小红书商城数据处理器"""
    
    @staticmethod
    def process_product_data(raw_product: Dict) -> Dict:
        """
        处理原始商品数据
        Args:
            raw_product: 原始商品数据
        Returns:
            处理后的商品数据
        """
        try:
            return {
                "product_id": raw_product.get("id", ""),
                "title": raw_product.get("title", ""),
                "price": raw_product.get("price", 0),
                "original_price": raw_product.get("original_price", 0),
                "discount": raw_product.get("discount", 0),
                "sales_count": raw_product.get("sales_count", 0),
                "rating": raw_product.get("rating", 0),
                "review_count": raw_product.get("review_count", 0),
                "image_url": raw_product.get("cover_image", ""),
                "shop_name": raw_product.get("shop", {}).get("name", ""),
                "shop_id": raw_product.get("shop", {}).get("id", ""),
                "category": raw_product.get("category", ""),
                "tags": raw_product.get("tags", []),
                "description": raw_product.get("description", ""),
                "created_time": raw_product.get("created_time", ""),
                "updated_time": int(time.time())
            }
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallDataProcessor.process_product_data] 处理商品数据失败: {e}")
            return {}
    
    @staticmethod
    def process_review_data(raw_review: Dict) -> Dict:
        """
        处理原始评价数据
        Args:
            raw_review: 原始评价数据
        Returns:
            处理后的评价数据
        """
        try:
            return {
                "review_id": raw_review.get("id", ""),
                "product_id": raw_review.get("product_id", ""),
                "user_id": raw_review.get("user", {}).get("id", ""),
                "user_name": raw_review.get("user", {}).get("nickname", ""),
                "user_avatar": raw_review.get("user", {}).get("avatar", ""),
                "rating": raw_review.get("rating", 0),
                "content": raw_review.get("content", ""),
                "images": raw_review.get("images", []),
                "like_count": raw_review.get("like_count", 0),
                "reply_count": raw_review.get("reply_count", 0),
                "created_time": raw_review.get("created_time", ""),
                "updated_time": int(time.time())
            }
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallDataProcessor.process_review_data] 处理评价数据失败: {e}")
            return {}
    
    @staticmethod
    def calculate_product_metrics(products: List[Dict]) -> Dict:
        """
        计算商品指标
        Args:
            products: 商品列表
        Returns:
            指标数据
        """
        if not products:
            return {}
        
        try:
            total_products = len(products)
            total_sales = sum(p.get("sales_count", 0) for p in products)
            avg_price = sum(p.get("price", 0) for p in products) / total_products
            avg_rating = sum(p.get("rating", 0) for p in products) / total_products
            
            # 价格区间分布
            price_ranges = {
                "0-50": 0,
                "50-100": 0,
                "100-200": 0,
                "200-500": 0,
                "500+": 0
            }
            
            for product in products:
                price = product.get("price", 0)
                if price <= 50:
                    price_ranges["0-50"] += 1
                elif price <= 100:
                    price_ranges["50-100"] += 1
                elif price <= 200:
                    price_ranges["100-200"] += 1
                elif price <= 500:
                    price_ranges["200-500"] += 1
                else:
                    price_ranges["500+"] += 1
            
            return {
                "total_products": total_products,
                "total_sales": total_sales,
                "avg_price": round(avg_price, 2),
                "avg_rating": round(avg_rating, 2),
                "price_distribution": price_ranges,
                "top_selling": sorted(products, key=lambda x: x.get("sales_count", 0), reverse=True)[:10],
                "highest_rated": sorted(products, key=lambda x: x.get("rating", 0), reverse=True)[:10]
            }
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallDataProcessor.calculate_product_metrics] 计算商品指标失败: {e}")
            return {}

    @staticmethod
    def analyze_price_trends(products_data: List[Dict]) -> Dict:
        """
        分析价格趋势
        
        Args:
            products_data: 商品数据列表
            
        Returns:
            价格趋势分析结果
        """
        if not products_data:
            return {}
        
        prices = [product.get('price', 0) for product in products_data if product.get('price')]
        
        if not prices:
            return {}
        
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'price_range': max(prices) - min(prices),
            'total_products': len(products_data)
        }

    @staticmethod
    def generate_category_stats(products_data: List[Dict]) -> Dict:
        """
        生成分类统计
        
        Args:
            products_data: 商品数据列表
            
        Returns:
            分类统计结果
        """
        if not products_data:
            return {}
        
        category_stats = {}
        
        for product in products_data:
            category = product.get('category', '未分类')
            if category not in category_stats:
                category_stats[category] = {
                    'count': 0,
                    'total_sales': 0,
                    'avg_price': 0,
                    'product_ids': []
                }
            
            category_stats[category]['count'] += 1
            category_stats[category]['total_sales'] += product.get('sales_count', 0)
            category_stats[category]['product_ids'].append(product.get('product_id', ''))
        
        # 计算平均价格
        for category, stats in category_stats.items():
            category_products = [p for p in products_data if p.get('category') == category]
            prices = [p.get('price', 0) for p in category_products if p.get('price')]
            if prices:
                stats['avg_price'] = sum(prices) / len(prices)
        
        return category_stats

    @staticmethod
    def create_analytics_report(products_data: List[Dict]) -> Dict:
        """
        创建分析报告
        
        Args:
            products_data: 商品数据列表
            
        Returns:
            分析报告
        """
        if not products_data:
            return {
                'total_products': 0,
                'total_sales': 0,
                'avg_price': 0,
                'price_trends': {},
                'category_stats': {},
                'top_products': [],
                'report_time': time.time()
            }
        
        # 基础统计
        total_products = len(products_data)
        total_sales = sum(product.get('sales_count', 0) for product in products_data)
        prices = [product.get('price', 0) for product in products_data if product.get('price')]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # 价格趋势分析
        price_trends = XiaoHongShuMallDataProcessor.analyze_price_trends(products_data)
        
        # 分类统计
        category_stats = XiaoHongShuMallDataProcessor.generate_category_stats(products_data)
        
        # 热门商品（按销量排序）
        top_products = sorted(
            products_data, 
            key=lambda x: x.get('sales_count', 0), 
            reverse=True
        )[:10]
        
        return {
            'total_products': total_products,
            'total_sales': total_sales,
            'avg_price': avg_price,
            'price_trends': price_trends,
            'category_stats': category_stats,
            'top_products': [
                {
                    'product_id': p.get('product_id', ''),
                    'title': p.get('title', ''),
                    'price': p.get('price', 0),
                    'sales_count': p.get('sales_count', 0)
                } for p in top_products
            ],
            'report_time': time.time()
        }


class XiaoHongShuMallManager:
    """小红书商城管理器"""
    
    def __init__(self, xhs_client=None, playwright_page=None):
        self.mall_client = XiaoHongShuMallClient(xhs_client, playwright_page)
        self.data_processor = XiaoHongShuMallDataProcessor()
        self.cache = {}
        self.cache_expire_time = 300  # 5分钟缓存
    
    async def get_products_with_processing(
        self, 
        keyword: str = "", 
        category_id: str = "", 
        max_count: int = 100
    ) -> List[Dict]:
        """
        获取并处理商品数据
        Args:
            keyword: 搜索关键词
            category_id: 分类ID
            max_count: 最大获取数量
        Returns:
            处理后的商品列表
        """
        cache_key = f"products_{keyword}_{category_id}_{max_count}"
        
        # 检查缓存
        if cache_key in self.cache:
            cache_data = self.cache[cache_key]
            if time.time() - cache_data["timestamp"] < self.cache_expire_time:
                return cache_data["data"]
        
        try:
            all_products = []
            page = 1
            page_size = 20
            
            while len(all_products) < max_count:
                result = await self.mall_client.get_mall_products(
                    keyword=keyword,
                    category_id=category_id,
                    page=page,
                    page_size=page_size
                )
                
                raw_products = result.get("items", [])
                if not raw_products:
                    break
                
                # 处理商品数据
                processed_products = []
                for raw_product in raw_products:
                    processed = self.data_processor.process_product_data(raw_product)
                    if processed:
                        processed_products.append(processed)
                
                all_products.extend(processed_products)
                
                if not result.get("has_more", False) or len(all_products) >= max_count:
                    break
                
                page += 1
                await asyncio.sleep(0.5)  # 控制请求频率
            
            # 限制返回数量
            final_products = all_products[:max_count]
            
            # 更新缓存
            self.cache[cache_key] = {
                "data": final_products,
                "timestamp": time.time()
            }
            
            return final_products
            
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallManager.get_products_with_processing] 获取商品数据失败: {e}")
            return []
    
    async def get_product_analytics(self, products: List[Dict]) -> Dict:
        """
        获取商品分析数据
        Args:
            products: 商品列表
        Returns:
            分析数据
        """
        try:
            return self.data_processor.calculate_product_metrics(products)
        except Exception as e:
            utils.logger.error(f"[XiaoHongShuMallManager.get_product_analytics] 获取商品分析失败: {e}")
            return {}
    
    async def monitor_products(
        self, 
        product_ids: List[str], 
        callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        监控商品数据变化
        Args:
            product_ids: 商品ID列表
            callback: 回调函数
        Returns:
            商品数据列表
        """
        monitored_products = []
        
        for product_id in product_ids:
            try:
                raw_detail = await self.mall_client.get_product_detail(product_id)
                if raw_detail:
                    processed_detail = self.data_processor.process_product_data(raw_detail)
                    if processed_detail:
                        monitored_products.append(processed_detail)
                        
                        if callback:
                            await callback(processed_detail)
                
                await asyncio.sleep(0.5)  # 控制请求频率
                
            except Exception as e:
                utils.logger.error(f"[XiaoHongShuMallManager.monitor_products] 监控商品{product_id}失败: {e}")
        
        return monitored_products

    def generate_category_stats(self, products_data: List[Dict]) -> Dict:
        """
        生成分类统计
        
        Args:
            products_data: 商品数据列表
            
        Returns:
            分类统计结果
        """
        if not products_data:
            return {}
        
        category_stats = {}
        for product in products_data:
            category = product.get('category', '未分类')
            if category not in category_stats:
                category_stats[category] = {
                    'count': 0,
                    'total_sales': 0,
                    'avg_price': 0,
                    'products': []
                }
            
            category_stats[category]['count'] += 1
            category_stats[category]['total_sales'] += product.get('sales_count', 0)
            category_stats[category]['products'].append(product.get('product_id', ''))
        
        # 计算平均价格
        for category, stats in category_stats.items():
            category_products = [p for p in products_data if p.get('category') == category]
            prices = [p.get('price', 0) for p in category_products if p.get('price')]
            stats['avg_price'] = sum(prices) / len(prices) if prices else 0
        
        return category_stats
    
    async def get_products(self, category: str = "", keyword: str = "", page: int = 1, limit: int = 20) -> List[Dict]:
        """
        获取商品列表
        
        Args:
            category: 商品分类
            keyword: 搜索关键词
            page: 页码
            limit: 每页数量
            
        Returns:
            商品列表
        """
        try:
            return await self.mall_client.get_product_list(category, keyword, page, limit)
        except Exception as e:
            self.logger.error(f"获取商品列表失败: {e}")
            return []

    async def get_product_detail(self, product_id: str) -> Optional[Dict]:
        """
        获取商品详情
        
        Args:
            product_id: 商品ID
            
        Returns:
            商品详情
        """
        try:
            return await self.mall_client.get_product_detail(product_id)
        except Exception as e:
            self.logger.error(f"获取商品详情失败: {e}")
            return None

    async def get_analytics(self) -> Dict:
        """
        获取分析数据
        
        Returns:
            分析数据
        """
        try:
            # 获取商品数据进行分析
            products = await self.get_products(limit=100)
            return self.data_processor.create_analytics_report(products)
        except Exception as e:
            self.logger.error(f"获取分析数据失败: {e}")
            return {}

    async def search_products(self, keyword: str, page: int = 1, limit: int = 20) -> List[Dict]:
        """
        搜索商品
        
        Args:
            keyword: 搜索关键词
            page: 页码
            limit: 每页数量
            
        Returns:
            搜索结果
        """
        try:
            return await self.mall_client.search_products(keyword, page, limit)
        except Exception as e:
            self.logger.error(f"搜索商品失败: {e}")
            return []

    async def get_trending_products(self, limit: int = 20) -> List[Dict]:
        """
        获取热门商品
        
        Args:
            limit: 数量限制
            
        Returns:
            热门商品列表
        """
        try:
            return await self.mall_client.get_trending_products(limit)
        except Exception as e:
            self.logger.error(f"获取热门商品失败: {e}")
            return []

    def cache_data(self, key: str, data: Any, ttl: int = 3600):
        """
        缓存数据
        
        Args:
            key: 缓存键
            data: 数据
            ttl: 过期时间（秒）
        """
        self.cache[key] = {
            'data': data,
            'timestamp': time.time(),
            'ttl': ttl
        }
    
    def clear_cache(self):
        """清除缓存"""
        self.cache.clear()
        utils.logger.info("[XiaoHongShuMallManager.clear_cache] 缓存已清除")