# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class XhsMallProduct(BaseModel):
    """小红书商城商品数据模型"""
    
    product_id: str = Field(description="商品ID")
    title: str = Field(description="商品标题")
    price: float = Field(description="商品价格")
    original_price: float = Field(default=0, description="原价")
    discount: float = Field(default=0, description="折扣")
    sales_count: int = Field(default=0, description="销量")
    rating: float = Field(default=0, description="评分")
    review_count: int = Field(default=0, description="评价数量")
    image_url: str = Field(default="", description="商品图片URL")
    shop_name: str = Field(default="", description="店铺名称")
    shop_id: str = Field(default="", description="店铺ID")
    category: str = Field(default="", description="商品分类")
    tags: List[str] = Field(default_factory=list, description="商品标签")
    description: str = Field(default="", description="商品描述")
    created_time: str = Field(default="", description="创建时间")
    updated_time: int = Field(default=0, description="更新时间戳")
    
    class Config:
        table_name = "xhs_mall_products"


class XhsMallReview(BaseModel):
    """小红书商城商品评价数据模型"""
    
    review_id: str = Field(description="评价ID")
    product_id: str = Field(description="商品ID")
    user_id: str = Field(description="用户ID")
    user_name: str = Field(description="用户昵称")
    user_avatar: str = Field(default="", description="用户头像")
    rating: float = Field(description="评分")
    content: str = Field(description="评价内容")
    images: List[str] = Field(default_factory=list, description="评价图片")
    like_count: int = Field(default=0, description="点赞数")
    reply_count: int = Field(default=0, description="回复数")
    created_time: str = Field(description="创建时间")
    updated_time: int = Field(default=0, description="更新时间戳")
    
    class Config:
        table_name = "xhs_mall_reviews"


class XhsMallCategory(BaseModel):
    """小红书商城分类数据模型"""
    
    category_id: str = Field(description="分类ID")
    name: str = Field(description="分类名称")
    parent_id: str = Field(default="", description="父分类ID")
    level: int = Field(default=1, description="分类层级")
    sort_order: int = Field(default=0, description="排序")
    icon_url: str = Field(default="", description="分类图标")
    product_count: int = Field(default=0, description="商品数量")
    created_time: str = Field(default="", description="创建时间")
    updated_time: int = Field(default=0, description="更新时间戳")
    
    class Config:
        table_name = "xhs_mall_categories"


class XhsMallShop(BaseModel):
    """小红书商城店铺数据模型"""
    
    shop_id: str = Field(description="店铺ID")
    name: str = Field(description="店铺名称")
    avatar: str = Field(default="", description="店铺头像")
    description: str = Field(default="", description="店铺描述")
    rating: float = Field(default=0, description="店铺评分")
    follower_count: int = Field(default=0, description="粉丝数")
    product_count: int = Field(default=0, description="商品数量")
    sales_count: int = Field(default=0, description="总销量")
    location: str = Field(default="", description="店铺位置")
    tags: List[str] = Field(default_factory=list, description="店铺标签")
    created_time: str = Field(default="", description="创建时间")
    updated_time: int = Field(default=0, description="更新时间戳")
    
    class Config:
        table_name = "xhs_mall_shops"


class XhsMallAnalytics(BaseModel):
    """小红书商城分析数据模型"""
    analytics_id: str = ""  # 分析ID
    date: str = ""  # 分析日期
    total_products: int = 0  # 总商品数
    total_sales: int = 0  # 总销量
    total_revenue: float = 0.0  # 总收入
    avg_price: float = 0.0  # 平均价格
    top_categories: Dict[str, int] = Field(default_factory=dict)  # 热门分类
    price_distribution: Dict[str, int] = Field(default_factory=dict)  # 价格分布
    sales_trends: Dict[str, int] = Field(default_factory=dict)  # 销售趋势
    created_time: int = 0  # 创建时间戳
    updated_time: int = 0  # 更新时间戳
    
    class Config:
        table_name = "xhs_mall_analytics"


class XhsMallSearchResult(BaseModel):
    """小红书商城搜索结果模型"""
    
    keyword: str = Field(description="搜索关键词")
    category_id: str = Field(default="", description="分类ID")
    total_count: int = Field(default=0, description="总数量")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=20, description="每页数量")
    has_more: bool = Field(default=False, description="是否有更多")
    products: List[XhsMallProduct] = Field(default_factory=list, description="商品列表")
    filters: Dict[str, Any] = Field(default_factory=dict, description="筛选条件")
    sort_type: str = Field(default="default", description="排序类型")
    search_time: float = Field(description="搜索耗时")
    created_time: str = Field(description="创建时间")
    
    class Config:
        table_name = "xhs_mall_search_results"