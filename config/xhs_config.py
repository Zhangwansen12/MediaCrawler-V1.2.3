# -*- coding: utf-8 -*-
# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


# 小红书平台配置

# 排序方式，具体的枚举值在media_platform/xhs/field.py中
SORT_TYPE = "popularity_descending"

# 指定笔记URL列表, 必须要携带xsec_token参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/66fad51c000000001b0224b8?xsec_token=AB3rO-QopW5sgrJ41GwN01WCXh6yWPxjSoFI9D5JIMgKw=&xsec_source=pc_search"
    # ........................
]

# 指定用户ID列表
XHS_CREATOR_ID_LIST = [
    "63e36c9a000000002703502b",
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
VIDEO_COVER_SAVE_PATH = "data/xiaohongshu/covers"

# 封面图文件名格式
# 支持的占位符: {video_id}, {title}, {author}, {timestamp}
VIDEO_COVER_FILENAME_FORMAT = "{video_id}_cover.jpg"

# 封面图获取超时时间（秒）
VIDEO_COVER_TIMEOUT = 10

# 封面图获取重试次数
VIDEO_COVER_RETRY_COUNT = 3

# 是否在数据中包含封面图URL
INCLUDE_COVER_URL_IN_DATA = True
