# -*- coding: utf-8 -*-
"""
小红书商城功能集成测试脚本
测试所有相关模块的集成和功能完整性
"""

import sys
import os
import asyncio
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from media_platform.xhs.mall import XiaoHongShuMallManager, XiaoHongShuMallClient, XiaoHongShuMallDataProcessor
    from model.m_xhs_mall import XhsMallProduct, XhsMallAnalytics, XhsMallReview, XhsMallCategory, XhsMallShop
    from store.xhs import update_xhs_mall_product, update_xhs_mall_analytics
    from realtime_updater import RealtimeUpdater, get_realtime_updater
    from gui_xhs_mall import XhsMallGUI
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有相关模块都已正确创建")
    sys.exit(1)


class XhsMallIntegrationTest:
    """小红书商城集成测试类"""
    
    def __init__(self):
        """初始化测试"""
        self.setup_logging()
        self.test_results = {}
        self.errors = []
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('test_xhs_mall_integration.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_test_result(self, test_name: str, success: bool, message: str = ""):
        """记录测试结果"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if success:
            self.logger.info(f"✅ {test_name}: 通过 - {message}")
        else:
            self.logger.error(f"❌ {test_name}: 失败 - {message}")
            self.errors.append(f"{test_name}: {message}")
    
    def test_model_imports(self):
        """测试数据模型导入"""
        test_name = "数据模型导入测试"
        try:
            # 测试创建模型实例
            product = XhsMallProduct(
                product_id="test_001",
                title="测试商品",
                price=99.99,
                sales_count=100,
                rating=4.5,
                shop_name="测试店铺",
                category="测试分类"
            )
            
            analytics = XhsMallAnalytics(
                analytics_id="test_analytics_001",
                date="2024-01-01",
                total_products=1000,
                total_sales=50000,
                avg_price=125.50,
                top_categories={"美妆": 200, "服装": 150},
                price_distribution={"0-50": 100, "51-100": 200},
                created_time=int(time.time())
            )
            
            review = XhsMallReview(
                review_id="review_001",
                product_id="test_001",
                user_id="user_001",
                user_name="测试用户",
                rating=5,
                content="很好的商品",
                created_time=str(int(time.time()))
            )
            
            category = XhsMallCategory(
                category_id="cat_001",
                name="测试分类",
                parent_id="",
                level=1,
                product_count=100
            )
            
            shop = XhsMallShop(
                shop_id="shop_001",
                name="测试店铺",
                rating=4.8,
                product_count=50,
                follower_count=1000
            )
            
            self.log_test_result(test_name, True, "所有数据模型创建成功")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_mall_client(self):
        """测试商城客户端"""
        test_name = "商城客户端测试"
        try:
            client = XiaoHongShuMallClient()
            
            # 测试客户端方法是否存在
            methods = [
                'get_product_list', 'get_product_detail', 'get_product_reviews',
                'get_categories', 'get_trending_products', 'search_products_by_category'
            ]
            
            for method in methods:
                if not hasattr(client, method):
                    raise AttributeError(f"客户端缺少方法: {method}")
            
            self.log_test_result(test_name, True, "客户端所有方法都存在")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_data_processor(self):
        """测试数据处理器"""
        test_name = "数据处理器测试"
        try:
            processor = XiaoHongShuMallDataProcessor()
            
            # 测试处理器方法
            methods = [
                'process_product_data', 'process_review_data', 'calculate_product_metrics',
                'analyze_price_trends', 'generate_category_stats', 'create_analytics_report'
            ]
            
            for method in methods:
                if not hasattr(processor, method):
                    raise AttributeError(f"处理器缺少方法: {method}")
            
            # 测试数据处理
            test_data = {"product_id": "001", "title": "测试", "price": 100, "sales_count": 50}
            
            processed = processor.process_product_data(test_data)
            if not isinstance(processed, dict):
                raise ValueError("处理后的数据应该是字典")
            
            # 测试空数据处理
            empty_result = processor.process_product_data({})
            if not isinstance(empty_result, dict):
                raise ValueError("空数据处理结果应该是字典")
            
            self.log_test_result(test_name, True, "数据处理器功能正常")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_mall_manager(self):
        """测试商城管理器"""
        test_name = "商城管理器测试"
        try:
            manager = XiaoHongShuMallManager()
            
            # 测试管理器方法
            methods = [
                'get_products', 'get_product_detail', 'get_analytics',
                'search_products', 'get_trending_products', 'cache_data'
            ]
            
            for method in methods:
                if not hasattr(manager, method):
                    raise AttributeError(f"管理器缺少方法: {method}")
            
            self.log_test_result(test_name, True, "商城管理器初始化成功")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_realtime_updater(self):
        """测试实时更新器"""
        test_name = "实时更新器测试"
        try:
            updater = RealtimeUpdater(update_interval=10)
            
            # 测试更新器方法
            methods = [
                'start', 'stop', 'add_update_task', 'add_callback',
                'get_cached_data', 'get_task_status', 'clear_cache'
            ]
            
            for method in methods:
                if not hasattr(updater, method):
                    raise AttributeError(f"更新器缺少方法: {method}")
            
            # 测试回调功能
            callback_called = False
            
            def test_callback(data):
                nonlocal callback_called
                callback_called = True
            
            updater.add_callback('on_data_updated', test_callback)
            
            # 测试任务添加
            updater.add_update_task('test_task', {'param': 'value'})
            
            # 测试状态获取
            status = updater.get_task_status()
            if not isinstance(status, dict):
                raise ValueError("任务状态应该是字典")
            
            self.log_test_result(test_name, True, "实时更新器功能正常")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_store_functions(self):
        """测试存储函数"""
        test_name = "存储函数测试"
        try:
            # 测试存储函数是否可调用
            if not callable(update_xhs_mall_product):
                raise ValueError("update_xhs_mall_product 不可调用")
            
            if not callable(update_xhs_mall_analytics):
                raise ValueError("update_xhs_mall_analytics 不可调用")
            
            self.log_test_result(test_name, True, "存储函数导入成功")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_gui_creation(self):
        """测试GUI创建"""
        test_name = "GUI创建测试"
        try:
            # 在测试环境中，我们只测试类的创建，不实际显示GUI
            gui_class = XhsMallGUI
            
            # 检查GUI类的关键方法
            methods = [
                'create_interface', 'setup_mall_manager', 'setup_realtime_callbacks',
                'toggle_realtime_updates', 'on_realtime_data_updated'
            ]
            
            for method in methods:
                if not hasattr(gui_class, method):
                    raise AttributeError(f"GUI类缺少方法: {method}")
            
            self.log_test_result(test_name, True, "GUI类结构正确")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_integration_workflow(self):
        """测试集成工作流"""
        test_name = "集成工作流测试"
        try:
            # 1. 创建管理器
            manager = XiaoHongShuMallManager()
            
            # 2. 创建实时更新器
            updater = RealtimeUpdater(update_interval=60)
            
            # 3. 测试数据流
            test_products = [
                {"product_id": "test_001", "title": "测试商品1", "price": 99.99},
                {"product_id": "test_002", "title": "测试商品2", "price": 199.99}
            ]
            
            # 4. 处理数据
            processor = XiaoHongShuMallDataProcessor()
            processed_data = []
            for product in test_products:
                processed = processor.process_product_data(product)
                processed_data.append(processed)
            
            # 5. 测试缓存
            updater.data_cache['products']['test'] = {
                'data': processed_data,
                'updated_at': datetime.now()
            }
            
            cached_data = updater.get_cached_data('products', 'test')
            if not cached_data:
                raise ValueError("缓存数据获取失败")
            
            self.log_test_result(test_name, True, "集成工作流测试通过")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def test_error_handling(self):
        """测试错误处理"""
        test_name = "错误处理测试"
        try:
            # 测试无效参数处理
            updater = RealtimeUpdater()
            
            # 测试空数据处理
            processor = XiaoHongShuMallDataProcessor()
            result = processor.process_product_data({})
            if not isinstance(result, dict):
                raise ValueError("空数据处理结果应该是字典")
            
            # 测试无效数据处理
            invalid_data = {"invalid": "data"}
            result = processor.process_product_data(invalid_data)
            if not isinstance(result, dict):
                raise ValueError("处理无效数据应返回字典")
            
            # 测试客户端空产品列表
            client = XiaoHongShuMallClient()
            empty_products = asyncio.run(client.get_product_list())
            if not isinstance(empty_products, list):
                raise ValueError("空产品列表应返回列表")
            
            self.log_test_result(test_name, True, "错误处理机制正常")
            
        except Exception as e:
            self.log_test_result(test_name, False, str(e))
    
    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("开始运行小红书商城集成测试...")
        self.logger.info("=" * 60)
        
        # 运行各项测试
        tests = [
            self.test_model_imports,
            self.test_mall_client,
            self.test_data_processor,
            self.test_mall_manager,
            self.test_realtime_updater,
            self.test_store_functions,
            self.test_gui_creation,
            self.test_integration_workflow,
            self.test_error_handling
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                test_name = test.__name__.replace('test_', '').replace('_', ' ')
                self.log_test_result(test_name, False, f"测试执行异常: {str(e)}")
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        self.logger.info("=" * 60)
        self.logger.info("测试报告")
        self.logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        self.logger.info(f"总测试数: {total_tests}")
        self.logger.info(f"通过测试: {passed_tests}")
        self.logger.info(f"失败测试: {failed_tests}")
        self.logger.info(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if self.errors:
            self.logger.info("\n失败的测试:")
            for error in self.errors:
                self.logger.error(f"  - {error}")
        
        # 保存详细报告到文件
        self.save_detailed_report()
        
        return passed_tests == total_tests
    
    def save_detailed_report(self):
        """保存详细报告到文件"""
        report_file = f"xhs_mall_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        import json
        report_data = {
            'test_summary': {
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for result in self.test_results.values() if result['success']),
                'failed_tests': sum(1 for result in self.test_results.values() if not result['success']),
                'test_time': datetime.now().isoformat()
            },
            'test_results': self.test_results,
            'errors': self.errors
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"详细测试报告已保存到: {report_file}")
            
        except Exception as e:
            self.logger.error(f"保存测试报告失败: {e}")


def main():
    """主函数"""
    print("小红书商城功能集成测试")
    print("=" * 40)
    
    # 创建测试实例
    test_runner = XhsMallIntegrationTest()
    
    # 运行测试
    success = test_runner.run_all_tests()
    
    if success:
        print("\n🎉 所有测试通过！小红书商城功能集成正常。")
        return 0
    else:
        print(f"\n⚠️  有 {len(test_runner.errors)} 个测试失败，请检查日志。")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)