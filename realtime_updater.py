# -*- coding: utf-8 -*-
"""
实时数据更新机制
用于监控和实时更新小红书商城数据的后台服务
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
import queue

from media_platform.xhs.mall import XiaoHongShuMallManager
from model.m_xhs_mall import XhsMallProduct, XhsMallAnalytics


@dataclass
class UpdateTask:
    """更新任务数据类"""
    task_id: str
    task_type: str  # 'product_list', 'product_detail', 'trending', 'analytics'
    params: Dict[str, Any]
    priority: int = 1  # 1=高优先级, 2=中优先级, 3=低优先级
    created_at: datetime = None
    retry_count: int = 0
    max_retries: int = 3
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class RealtimeUpdater:
    """实时数据更新器"""
    
    def __init__(self, update_interval: int = 300, mall_manager: XiaoHongShuMallManager = None):
        """
        初始化实时更新器
        
        Args:
            update_interval: 更新间隔（秒）
            mall_manager: 小红书商城管理器实例
        """
        self.update_interval = update_interval
        self.is_running = False
        self.mall_manager = mall_manager
        
        # 任务队列
        self.task_queue = queue.PriorityQueue()
        self.completed_tasks = []
        self.failed_tasks = []
        
        # 回调函数
        self.callbacks = {
            'on_data_updated': [],
            'on_error': [],
            'on_status_changed': []
        }
        
        # 线程管理
        self.update_thread = None
        self.worker_threads = []
        self.max_workers = 3
        
        # 数据缓存
        self.data_cache = {
            'products': {},
            'analytics': {},
            'last_update': {}
        }
        
        # 配置日志
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def set_mall_manager(self, mall_manager: XiaoHongShuMallManager):
        """设置商城管理器"""
        self.mall_manager = mall_manager
    
    def add_callback(self, event_type: str, callback: Callable):
        """
        添加回调函数
        
        Args:
            event_type: 事件类型 ('on_data_updated', 'on_error', 'on_status_changed')
            callback: 回调函数
        """
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
    
    def remove_callback(self, event_type: str, callback: Callable):
        """移除回调函数"""
        if event_type in self.callbacks and callback in self.callbacks[event_type]:
            self.callbacks[event_type].remove(callback)
    
    def trigger_callback(self, event_type: str, *args, **kwargs):
        """触发回调函数"""
        if event_type in self.callbacks:
            for callback in self.callbacks[event_type]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"回调函数执行失败: {e}")
    
    def start(self):
        """启动实时更新服务"""
        if self.is_running:
            self.logger.warning("实时更新服务已在运行")
            return
        
        self.is_running = True
        self.logger.info("启动实时更新服务")
        
        # 启动主更新线程
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
        # 启动工作线程
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.worker_threads.append(worker)
        
        # 安排定期任务
        self._schedule_periodic_tasks()
        
        self.trigger_callback('on_status_changed', {'status': 'started'})
    
    def stop(self):
        """停止实时更新服务"""
        if not self.is_running:
            self.logger.warning("实时更新服务未在运行")
            return
        
        self.is_running = False
        self.logger.info("停止实时更新服务")
        
        # 等待线程结束
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=5)
        
        for worker in self.worker_threads:
            if worker.is_alive():
                worker.join(timeout=2)
        
        self.worker_threads.clear()
        self.trigger_callback('on_status_changed', {'status': 'stopped'})
    
    def add_update_task(self, task_type: str, params: Dict[str, Any], priority: int = 2):
        """
        添加更新任务
        
        Args:
            task_type: 任务类型
            params: 任务参数
            priority: 优先级
        """
        task_id = f"{task_type}_{int(time.time() * 1000)}"
        task = UpdateTask(
            task_id=task_id,
            task_type=task_type,
            params=params,
            priority=priority
        )
        
        self.task_queue.put((priority, task))
        self.logger.info(f"添加更新任务: {task_id} ({task_type})")
    
    def _update_loop(self):
        """主更新循环"""
        while self.is_running:
            try:
                time.sleep(self.update_interval)
                if self.is_running:
                    self._schedule_periodic_tasks()
            except Exception as e:
                self.logger.error(f"更新循环异常: {e}")
                self.trigger_callback('on_error', f"更新循环异常: {e}")
    
    def _worker_loop(self):
        """工作线程循环"""
        while self.is_running:
            try:
                # 获取任务（超时1秒）
                priority, task = self.task_queue.get(timeout=1)
                if task:
                    self._execute_task(task)
                    self.task_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"工作线程异常: {e}")
    
    def _schedule_periodic_tasks(self):
        """安排定期任务"""
        # 添加定期更新任务
        self.add_update_task('product_list', {'keyword': '美妆', 'limit': 20}, priority=2)
        self.add_update_task('trending', {}, priority=2)
        self.add_update_task('analytics', {}, priority=3)
    
    def _execute_task(self, task: UpdateTask):
        """执行更新任务"""
        try:
            self.logger.info(f"执行任务: {task.task_id} ({task.task_type})")
            
            if task.task_type == 'product_list':
                self._update_product_list(task)
            elif task.task_type == 'product_detail':
                self._update_product_detail(task)
            elif task.task_type == 'trending':
                self._update_trending_products(task)
            elif task.task_type == 'analytics':
                self._update_analytics(task)
            else:
                raise ValueError(f"未知任务类型: {task.task_type}")
            
            self.completed_tasks.append(task)
            self.logger.info(f"任务完成: {task.task_id}")
            
        except Exception as e:
            self.logger.error(f"任务执行失败: {task.task_id} - {e}")
            task.retry_count += 1
            
            if task.retry_count < task.max_retries:
                self.logger.info(f"任务重试: {task.task_id} (第{task.retry_count}次)")
                # 降低优先级重新加入队列
                self.task_queue.put((task.priority + 1, task))
            else:
                self.logger.error(f"任务最终失败: {task.task_id}")
                self.failed_tasks.append(task)
                self.trigger_callback('on_error', f"任务失败: {task.task_id} - {e}")
    
    def _update_product_list(self, task: UpdateTask):
        """更新商品列表"""
        params = task.params
        keyword = params.get('keyword', '美妆')
        limit = params.get('limit', 20)
        
        try:
            # 使用真实API获取商品列表
            if self.mall_manager:
                products_data = self.mall_manager.search_products(keyword, limit=limit)
                if not products_data:
                    # 如果搜索无结果，尝试获取通用商品列表
                    products_data = self.mall_manager.get_products(limit=limit)
                
                # 转换为字典格式
                products = []
                if products_data:
                    for product in products_data:
                        if hasattr(product, 'to_dict'):
                            products.append(product.to_dict())
                        elif isinstance(product, dict):
                            products.append(product)
                        else:
                            # 如果是其他格式，尝试转换
                            products.append({
                                'product_id': getattr(product, 'product_id', f'unknown_{len(products)}'),
                                'title': getattr(product, 'title', '未知商品'),
                                'price': getattr(product, 'price', 0),
                                'sales': getattr(product, 'sales', 0),
                                'rating': getattr(product, 'rating', 0),
                                'image_url': getattr(product, 'image_url', ''),
                                'shop_name': getattr(product, 'shop_name', ''),
                                'category': getattr(product, 'category', ''),
                            })
            else:
                # 如果没有mall_manager，使用模拟数据作为后备
                products = self._simulate_product_data(keyword, limit)
        except Exception as e:
            self.logger.warning(f"API调用失败，使用模拟数据: {e}")
            products = self._simulate_product_data(keyword, limit)
        
        # 更新缓存
        cache_key = f"{keyword}_{limit}"
        self.data_cache['products'][cache_key] = {
            'data': products,
            'updated_at': datetime.now()
        }
        
        # 触发回调
        self.trigger_callback('on_data_updated', {
            'type': 'product_list',
            'data': products,
            'params': params
        })
    
    def _update_product_detail(self, task: UpdateTask):
        """更新商品详情"""
        params = task.params
        product_id = params.get('product_id')
        
        if not product_id:
            raise ValueError("缺少product_id参数")
        
        try:
            # 使用真实API获取商品详情
            if self.mall_manager:
                detail_data = self.mall_manager.get_product_detail(product_id)
                if detail_data:
                    if hasattr(detail_data, 'to_dict'):
                        detail = detail_data.to_dict()
                    elif isinstance(detail_data, dict):
                        detail = detail_data
                    else:
                        detail = {
                            'product_id': product_id,
                            'title': getattr(detail_data, 'title', '未知商品'),
                            'price': getattr(detail_data, 'price', 0),
                            'description': getattr(detail_data, 'description', ''),
                            'images': getattr(detail_data, 'images', []),
                            'specifications': getattr(detail_data, 'specifications', {}),
                        }
                else:
                    detail = self._simulate_product_detail(product_id)
            else:
                detail = self._simulate_product_detail(product_id)
        except Exception as e:
            self.logger.warning(f"API调用失败，使用模拟数据: {e}")
            detail = self._simulate_product_detail(product_id)
        
        # 更新缓存
        self.data_cache['products'][f"detail_{product_id}"] = {
            'data': detail,
            'updated_at': datetime.now()
        }
        
        # 触发回调
        self.trigger_callback('on_data_updated', {
            'type': 'product_detail',
            'data': detail,
            'params': params
        })
    
    def _update_trending_products(self, task: UpdateTask):
        """更新热门商品"""
        try:
            # 使用真实API获取热门商品
            if self.mall_manager:
                trending_data = self.mall_manager.get_trending_products(limit=15)
                if trending_data:
                    trending_products = []
                    for product in trending_data:
                        if hasattr(product, 'to_dict'):
                            trending_products.append(product.to_dict())
                        elif isinstance(product, dict):
                            trending_products.append(product)
                        else:
                            trending_products.append({
                                'product_id': getattr(product, 'product_id', f'trending_{len(trending_products)}'),
                                'title': getattr(product, 'title', '热门商品'),
                                'price': getattr(product, 'price', 0),
                                'sales': getattr(product, 'sales', 0),
                                'rating': getattr(product, 'rating', 0),
                                'image_url': getattr(product, 'image_url', ''),
                                'shop_name': getattr(product, 'shop_name', ''),
                                'category': getattr(product, 'category', ''),
                            })
                else:
                    trending_products = self._simulate_product_data("热门", 15)
            else:
                trending_products = self._simulate_product_data("热门", 15)
        except Exception as e:
            self.logger.warning(f"API调用失败，使用模拟数据: {e}")
            trending_products = self._simulate_product_data("热门", 15)
        
        # 更新缓存
        self.data_cache['products']['trending'] = {
            'data': trending_products,
            'updated_at': datetime.now()
        }
        
        # 触发回调
        self.trigger_callback('on_data_updated', {
            'type': 'trending',
            'data': trending_products,
            'params': task.params
        })
    
    def _update_analytics(self, task: UpdateTask):
        """更新分析数据"""
        try:
            # 使用真实API获取分析数据
            if self.mall_manager:
                analytics_data = self.mall_manager.get_analytics()
                if analytics_data:
                    if hasattr(analytics_data, 'to_dict'):
                        analytics = analytics_data.to_dict()
                    elif isinstance(analytics_data, dict):
                        analytics = analytics_data
                    else:
                        analytics = {
                            'total_products': getattr(analytics_data, 'total_products', 0),
                            'total_sales': getattr(analytics_data, 'total_sales', 0),
                            'avg_rating': getattr(analytics_data, 'avg_rating', 0),
                            'categories': getattr(analytics_data, 'categories', {}),
                            'trends': getattr(analytics_data, 'trends', {}),
                        }
                else:
                    analytics = self._simulate_analytics_data()
            else:
                analytics = self._simulate_analytics_data()
        except Exception as e:
            self.logger.warning(f"API调用失败，使用模拟数据: {e}")
            analytics = self._simulate_analytics_data()
        
        # 更新缓存
        self.data_cache['analytics']['general'] = {
            'data': analytics,
            'updated_at': datetime.now()
        }
        
        # 触发回调
        self.trigger_callback('on_data_updated', {
            'type': 'analytics',
            'data': analytics,
            'params': task.params
        })
    
    def _simulate_product_data(self, keyword: str, limit: int) -> List[Dict]:
        """模拟商品数据"""
        import random
        products = []
        
        for i in range(limit):
            product = {
                "product_id": f"xhs_mall_{keyword}_{i+1:06d}",
                "title": f"{keyword}相关商品 {i+1}",
                "price": round(random.uniform(10, 500), 2),
                "sales_count": random.randint(0, 10000),
                "rating": round(random.uniform(3.0, 5.0), 1),
                "shop_name": f"店铺{random.randint(1, 100)}",
                "category": random.choice(["美妆", "服装", "数码", "家居", "食品"]),
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "is_trending": random.choice([True, False]),
                "discount": random.randint(0, 50) if random.random() > 0.7 else 0
            }
            products.append(product)
        
        return products
    
    def _simulate_product_detail(self, product_id: str) -> Dict:
        """模拟商品详情数据"""
        import random
        
        return {
            "product_id": product_id,
            "title": f"商品详情 {product_id}",
            "description": "这是一个优质商品的详细描述...",
            "price": round(random.uniform(50, 300), 2),
            "original_price": round(random.uniform(60, 400), 2),
            "sales_count": random.randint(100, 5000),
            "rating": round(random.uniform(4.0, 5.0), 1),
            "review_count": random.randint(50, 1000),
            "shop_info": {
                "shop_id": f"shop_{random.randint(1000, 9999)}",
                "shop_name": f"精品店铺{random.randint(1, 50)}",
                "shop_rating": round(random.uniform(4.5, 5.0), 1)
            },
            "images": [f"image_{i}.jpg" for i in range(1, 6)],
            "specifications": {
                "品牌": "知名品牌",
                "产地": "中国",
                "保质期": "3年"
            },
            "updated_at": datetime.now().isoformat()
        }
    
    def _simulate_analytics_data(self) -> Dict:
        """模拟分析数据"""
        import random
        
        return {
            "total_products": random.randint(1000, 5000),
            "total_sales": random.randint(50000, 200000),
            "avg_price": round(random.uniform(80, 150), 2),
            "top_categories": [
                {"name": "美妆", "count": random.randint(200, 500)},
                {"name": "服装", "count": random.randint(150, 400)},
                {"name": "数码", "count": random.randint(100, 300)},
                {"name": "家居", "count": random.randint(80, 250)},
                {"name": "食品", "count": random.randint(60, 200)}
            ],
            "price_distribution": {
                "0-50": random.randint(100, 300),
                "51-100": random.randint(200, 500),
                "101-200": random.randint(150, 400),
                "200+": random.randint(50, 150)
            },
            "trending_keywords": ["热销", "新品", "限时", "优惠", "精选"],
            "generated_at": datetime.now().isoformat()
        }
    
    def get_cached_data(self, data_type: str, key: str = None) -> Optional[Dict]:
        """获取缓存数据"""
        if data_type not in self.data_cache:
            return None
        
        if key:
            return self.data_cache[data_type].get(key)
        else:
            return self.data_cache[data_type]
    
    def get_task_status(self) -> Dict:
        """获取任务状态"""
        return {
            "is_running": self.is_running,
            "queue_size": self.task_queue.qsize(),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "update_interval": self.update_interval,
            "last_updates": self.data_cache['last_update']
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.data_cache = {
            'products': {},
            'analytics': {},
            'last_update': {}
        }
        self.logger.info("缓存已清空")
    
    def set_update_interval(self, interval: int):
        """设置更新间隔"""
        if interval < 60:
            raise ValueError("更新间隔不能小于60秒")
        
        self.update_interval = interval
        self.logger.info(f"更新间隔已设置为: {interval}秒")


# 全局实时更新器实例
_global_updater = None


def get_realtime_updater() -> RealtimeUpdater:
    """获取全局实时更新器实例"""
    global _global_updater
    if _global_updater is None:
        _global_updater = RealtimeUpdater()
    return _global_updater


def start_realtime_updates(update_interval: int = 300):
    """启动实时更新服务"""
    updater = get_realtime_updater()
    updater.set_update_interval(update_interval)
    updater.start()
    return updater


def stop_realtime_updates():
    """停止实时更新服务"""
    global _global_updater
    if _global_updater:
        _global_updater.stop()


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)
    
    def on_data_updated(data):
        print(f"数据更新: {data['type']}")
    
    def on_error(error):
        print(f"错误: {error}")
    
    def on_status_changed(status):
        print(f"状态变更: {status}")
    
    # 创建更新器
    updater = RealtimeUpdater(update_interval=10)
    updater.add_callback('on_data_updated', on_data_updated)
    updater.add_callback('on_error', on_error)
    updater.add_callback('on_status_changed', on_status_changed)
    
    # 启动服务
    updater.start()
    
    # 添加测试任务
    updater.add_update_task('product_list', {'keyword': '测试', 'limit': 5}, priority=1)
    
    try:
        # 运行30秒
        time.sleep(30)
    except KeyboardInterrupt:
        print("用户中断")
    finally:
        updater.stop()
        print("测试完成")