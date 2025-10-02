# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。

# 快手平台配置

# 指定快手视频ID列表
KS_SPECIFIED_ID_LIST = ["3xf8enb8dbj6uig", "3x6zz972bchmvqe"]

# 指定快手用户ID列表
KS_CREATOR_ID_LIST = [
    "3x4sm73aye7jq7i",
    # ........................
]

# ==================== 视频封面图获取配置 ====================

# 是否启用视频封面图获取
ENABLE_VIDEO_COVER = True

# 封面图质量配置
# 可选值: "default", "medium", "high"
# default: 默认质量封面图
# medium: 中等质量封面图  
# high: 高质量封面图
VIDEO_COVER_QUALITY = "medium"

# 封面图保存配置
# 是否保存封面图到本地
SAVE_VIDEO_COVER = False

# 封面图保存目录（相对于项目根目录）
VIDEO_COVER_SAVE_PATH = "data/kuaishou/covers"

# 封面图文件名格式
# 支持的占位符: {video_id}, {title}, {author}, {timestamp}
VIDEO_COVER_FILENAME_FORMAT = "{video_id}_cover.jpg"

# 封面图获取超时时间（秒）
VIDEO_COVER_TIMEOUT = 10

# 封面图获取重试次数
VIDEO_COVER_RETRY_COUNT = 3

# 是否在数据中包含封面图URL
INCLUDE_COVER_URL_IN_DATA = True

# 视频统计数据功能配置
# 是否启用视频统计数据收集
ENABLE_VIDEO_STATS = False

# 是否启用批量统计数据获取
ENABLE_BATCH_STATS = False

# 批量获取统计数据时的延迟（秒）
BATCH_STATS_DELAY = 1.0

# 是否启用互动率计算
ENABLE_ENGAGEMENT_RATE = True

# 是否启用性能分析报告
ENABLE_PERFORMANCE_ANALYSIS = True

# 热门视频查找的默认指标
TOP_VIDEOS_METRIC = "likes"

# 热门视频查找的默认数量
TOP_VIDEOS_COUNT = 10

# 是否在日志中显示统计数据
LOG_STATS_DATA = True

# 统计数据格式化显示语言 (zh/en)
STATS_DISPLAY_LANGUAGE = "zh"
