# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


# -*- coding: utf-8 -*-

import sys
import os
from typing import Dict, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from tools import utils
from media_platform.kuaishou.field import VideoStats


class VideoStatsExtractor:
    """视频统计数据提取器"""
    
    @staticmethod
    def extract_video_stats(video_detail: Dict) -> Optional[VideoStats]:
        """
        从视频详情数据中提取统计信息
        
        Args:
            video_detail: 视频详情数据字典
            
        Returns:
            VideoStats: 视频统计数据对象，如果提取失败返回None
        """
        try:
            if not video_detail or not isinstance(video_detail, dict):
                utils.logger.warning("[VideoStatsExtractor] Invalid video_detail data")
                return None
            
            # 处理两种数据结构：直接的photo数据或包含visionVideoDetail的完整结构
            if "visionVideoDetail" in video_detail:
                vision_detail = video_detail.get("visionVideoDetail", {})
                photo_data = vision_detail.get("photo", {})
            else:
                photo_data = video_detail.get("photo", {})
                
            if not photo_data:
                utils.logger.warning("[VideoStatsExtractor] No photo data found in video_detail")
                return None
            
            # 提取基本统计数据
            video_id = photo_data.get("id", "")
            like_count = int(photo_data.get("likeCount", 0))
            real_like_count = int(photo_data.get("realLikeCount", 0))
            comment_count = int(photo_data.get("commentCount", 0))
            share_count = int(photo_data.get("shareCount", 0))
            collect_count = int(photo_data.get("collectCount", 0))
            view_count = int(photo_data.get("viewCount", 0))
            duration = int(photo_data.get("duration", 0))
            timestamp = int(photo_data.get("timestamp", 0))
            
            # 创建VideoStats对象
            video_stats = VideoStats(
                video_id=video_id,
                like_count=like_count,
                real_like_count=real_like_count,
                comment_count=comment_count,
                share_count=share_count,
                collect_count=collect_count,
                view_count=view_count,
                duration=duration,
                timestamp=timestamp
            )
            
            utils.logger.info(
                f"[VideoStatsExtractor] Extracted stats for video {video_id}: "
                f"likes={like_count}, comments={comment_count}, shares={share_count}, collects={collect_count}"
            )
            
            return video_stats
            
        except Exception as e:
            utils.logger.error(f"[VideoStatsExtractor] Error extracting video stats: {e}")
            return None

    @staticmethod
    def format_stats_for_display(video_stats) -> Dict[str, str]:
        """
        格式化视频统计数据用于显示
        
        Args:
            video_stats: 视频统计数据（可以是字典或VideoStats对象）
            
        Returns:
            Dict[str, str]: 格式化后的显示数据
        """
        try:
            # 计算互动率
            engagement_rate = VideoStatsExtractor.get_engagement_rate(video_stats)
            
            def format_number(num):
                """格式化数字显示"""
                if num >= 10000:
                    return f"{num/10000:.1f}万"
                elif num >= 1000:
                    return f"{num/1000:.1f}k"
                else:
                    return str(num)
            
            # 处理不同类型的输入（字典或NamedTuple）
            if hasattr(video_stats, '_asdict'):
                # VideoStats NamedTuple
                stats_dict = video_stats._asdict()
            elif isinstance(video_stats, dict):
                # 字典类型
                stats_dict = video_stats
            else:
                # 尝试通过属性访问
                stats_dict = {
                    'video_id': getattr(video_stats, 'video_id', ''),
                    'like_count': getattr(video_stats, 'like_count', 0),
                    'real_like_count': getattr(video_stats, 'real_like_count', 0),
                    'comment_count': getattr(video_stats, 'comment_count', 0),
                    'share_count': getattr(video_stats, 'share_count', 0),
                    'collect_count': getattr(video_stats, 'collect_count', 0),
                    'view_count': getattr(video_stats, 'view_count', 0),
                    'duration': getattr(video_stats, 'duration', 0),
                }
            
            formatted_data = {
                "视频ID": stats_dict.get("video_id", ""),
                "点赞数": format_number(stats_dict.get("like_count", 0)),
                "真实点赞数": format_number(stats_dict.get("real_like_count", 0)),
                "评论数": format_number(stats_dict.get("comment_count", 0)),
                "分享数": format_number(stats_dict.get("share_count", 0)),
                "收藏数": format_number(stats_dict.get("collect_count", 0)),
                "观看数": format_number(stats_dict.get("view_count", 0)),
                "时长": f"{stats_dict.get('duration', 0)//1000}秒",
                "互动率": f"{engagement_rate:.2f}%"
            }
            
            return formatted_data
            
        except Exception as e:
            utils.logger.error(f"[VideoStatsExtractor] Error formatting stats for display: {e}")
            return {"error": f"格式化失败: {str(e)}"}
    
    @staticmethod
    def get_engagement_rate(video_stats) -> float:
        """
        计算视频互动率
        
        Args:
            video_stats: 视频统计数据（可以是字典或VideoStats对象）
            
        Returns:
            float: 互动率（点赞+评论+分享+收藏）/播放量
        """
        # 处理不同类型的输入（字典或NamedTuple）
        if hasattr(video_stats, '_asdict'):
            # VideoStats NamedTuple
            stats_dict = video_stats._asdict()
        elif isinstance(video_stats, dict):
            # 字典类型
            stats_dict = video_stats
        else:
            # 尝试通过属性访问
            stats_dict = {
                'view_count': getattr(video_stats, 'view_count', 0),
                'like_count': getattr(video_stats, 'like_count', 0),
                'comment_count': getattr(video_stats, 'comment_count', 0),
                'share_count': getattr(video_stats, 'share_count', 0),
                'collect_count': getattr(video_stats, 'collect_count', 0),
            }
        
        view_count = stats_dict.get("view_count", 0)
        if view_count == 0:
            return 0.0
        
        total_engagement = (
            stats_dict.get("like_count", 0) + 
            stats_dict.get("comment_count", 0) + 
            stats_dict.get("share_count", 0) + 
            stats_dict.get("collect_count", 0)
        )
        
        engagement_rate = total_engagement / view_count
        return round(engagement_rate * 100, 2)  # 返回百分比