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

from typing import Dict, List, Optional, Tuple
from statistics import mean, median
from tools import utils
from .field import VideoStats


class StatsAnalyzer:
    """视频统计数据分析器"""
    
    @staticmethod
    def analyze_video_performance(video_stats_list: List[VideoStats]) -> Dict:
        """
        分析视频表现数据
        
        Args:
            video_stats_list: 视频统计数据列表
            
        Returns:
            Dict: 分析结果
        """
        if not video_stats_list:
            return {"error": "No video stats data provided"}
        
        try:
            # 基础统计
            total_videos = len(video_stats_list)
            
            # 各项指标的统计
            like_counts = [stats.like_count for stats in video_stats_list]
            comment_counts = [stats.comment_count for stats in video_stats_list]
            share_counts = [stats.share_count for stats in video_stats_list]
            collect_counts = [stats.collect_count for stats in video_stats_list]
            view_counts = [stats.view_count for stats in video_stats_list]
            
            # 计算平均值和中位数
            analysis_result = {
                "total_videos": total_videos,
                "like_stats": {
                    "total": sum(like_counts),
                    "average": round(mean(like_counts), 2),
                    "median": median(like_counts),
                    "max": max(like_counts),
                    "min": min(like_counts)
                },
                "comment_stats": {
                    "total": sum(comment_counts),
                    "average": round(mean(comment_counts), 2),
                    "median": median(comment_counts),
                    "max": max(comment_counts),
                    "min": min(comment_counts)
                },
                "share_stats": {
                    "total": sum(share_counts),
                    "average": round(mean(share_counts), 2),
                    "median": median(share_counts),
                    "max": max(share_counts),
                    "min": min(share_counts)
                },
                "collect_stats": {
                    "total": sum(collect_counts),
                    "average": round(mean(collect_counts), 2),
                    "median": median(collect_counts),
                    "max": max(collect_counts),
                    "min": min(collect_counts)
                },
                "view_stats": {
                    "total": sum(view_counts),
                    "average": round(mean(view_counts), 2),
                    "median": median(view_counts),
                    "max": max(view_counts),
                    "min": min(view_counts)
                }
            }
            
            # 计算互动率统计
            from .video_stats_extractor import VideoStatsExtractor
            engagement_rates = []
            for stats in video_stats_list:
                stats_dict = {
                    "video_id": stats.video_id,
                    "like_count": stats.like_count,
                    "comment_count": stats.comment_count,
                    "share_count": stats.share_count,
                    "collect_count": stats.collect_count,
                    "view_count": stats.view_count
                }
                engagement_rates.append(VideoStatsExtractor.get_engagement_rate(stats_dict))
                
            analysis_result["engagement_stats"] = {
                "average": round(mean(engagement_rates), 2),
                "median": round(median(engagement_rates), 2),
                "max": round(max(engagement_rates), 2),
                "min": round(min(engagement_rates), 2)
            }
            
            utils.logger.info(f"[StatsAnalyzer] Analyzed {total_videos} videos performance")
            return analysis_result
            
        except Exception as e:
            utils.logger.error(f"[StatsAnalyzer] Error analyzing video performance: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def find_top_performing_videos(video_stats_list: List[VideoStats], 
                                 metric: str = "like_count", 
                                 top_n: int = 10) -> List[VideoStats]:
        """
        找出表现最好的视频
        
        Args:
            video_stats_list: 视频统计数据列表
            metric: 排序指标 (like_count, comment_count, share_count, collect_count, view_count)
            top_n: 返回前N个视频
            
        Returns:
            List[VideoStats]: 排序后的前N个视频统计数据
        """
        if not video_stats_list:
            return []
        
        try:
            # 根据指定指标排序
            if metric == "engagement_rate":
                from .video_stats_extractor import VideoStatsExtractor
                sorted_videos = sorted(
                    video_stats_list, 
                    key=lambda x: VideoStatsExtractor.get_engagement_rate(x), 
                    reverse=True
                )
            else:
                sorted_videos = sorted(
                    video_stats_list, 
                    key=lambda x: getattr(x, metric, 0), 
                    reverse=True
                )
            
            top_videos = sorted_videos[:top_n]
            utils.logger.info(f"[StatsAnalyzer] Found top {len(top_videos)} videos by {metric}")
            return top_videos
            
        except Exception as e:
            utils.logger.error(f"[StatsAnalyzer] Error finding top performing videos: {e}")
            return []
    
    @staticmethod
    def compare_video_stats(video_stats1: VideoStats, video_stats2: VideoStats) -> Dict:
        """
        比较两个视频的统计数据
        
        Args:
            video_stats1: 第一个视频统计数据
            video_stats2: 第二个视频统计数据
            
        Returns:
            Dict: 比较结果
        """
        try:
            from .video_stats_extractor import VideoStatsExtractor
            
            # 转换为字典格式以供get_engagement_rate使用
            stats1_dict = {
                "video_id": video_stats1.video_id,
                "like_count": video_stats1.like_count,
                "comment_count": video_stats1.comment_count,
                "share_count": video_stats1.share_count,
                "collect_count": video_stats1.collect_count,
                "view_count": video_stats1.view_count
            }
            
            stats2_dict = {
                "video_id": video_stats2.video_id,
                "like_count": video_stats2.like_count,
                "comment_count": video_stats2.comment_count,
                "share_count": video_stats2.share_count,
                "collect_count": video_stats2.collect_count,
                "view_count": video_stats2.view_count
            }
            
            comparison = {
                "video1_id": video_stats1.video_id,
                "video2_id": video_stats2.video_id,
                "like_count_diff": video_stats1.like_count - video_stats2.like_count,
                "comment_count_diff": video_stats1.comment_count - video_stats2.comment_count,
                "share_count_diff": video_stats1.share_count - video_stats2.share_count,
                "collect_count_diff": video_stats1.collect_count - video_stats2.collect_count,
                "view_count_diff": video_stats1.view_count - video_stats2.view_count,
                "engagement_rate_diff": round(
                    VideoStatsExtractor.get_engagement_rate(stats1_dict) - 
                    VideoStatsExtractor.get_engagement_rate(stats2_dict), 2
                )
            }
            
            # 判断哪个视频表现更好
            better_video = "video1" if comparison["like_count_diff"] > 0 else "video2"
            comparison["better_performing"] = better_video
            
            # 添加摘要信息
            comparison["summary"] = f"视频{comparison['video1_id']}与视频{comparison['video2_id']}对比，{better_video}表现更好"
            
            utils.logger.info(f"[StatsAnalyzer] Compared videos {video_stats1.video_id} vs {video_stats2.video_id}")
            return comparison
            
        except Exception as e:
            utils.logger.error(f"[StatsAnalyzer] Error comparing video stats: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def generate_stats_report(video_stats_list: List[VideoStats]) -> str:
        """
        生成统计报告
        
        Args:
            video_stats_list: 视频统计数据列表
            
        Returns:
            str: 格式化的统计报告
        """
        if not video_stats_list:
            return "没有可用的视频统计数据"
        
        try:
            analysis = StatsAnalyzer.analyze_video_performance(video_stats_list)
            
            report = f"""
快手视频统计分析报告
==================

总体概况:
- 分析视频数量: {analysis['total_videos']}

点赞数据:
- 总点赞数: {analysis['like_stats']['total']:,}
- 平均点赞数: {analysis['like_stats']['average']:,}
- 中位数: {analysis['like_stats']['median']:,}
- 最高: {analysis['like_stats']['max']:,}
- 最低: {analysis['like_stats']['min']:,}

评论数据:
- 总评论数: {analysis['comment_stats']['total']:,}
- 平均评论数: {analysis['comment_stats']['average']:,}
- 中位数: {analysis['comment_stats']['median']:,}
- 最高: {analysis['comment_stats']['max']:,}
- 最低: {analysis['comment_stats']['min']:,}

分享数据:
- 总分享数: {analysis['share_stats']['total']:,}
- 平均分享数: {analysis['share_stats']['average']:,}
- 中位数: {analysis['share_stats']['median']:,}
- 最高: {analysis['share_stats']['max']:,}
- 最低: {analysis['share_stats']['min']:,}

收藏数据:
- 总收藏数: {analysis['collect_stats']['total']:,}
- 平均收藏数: {analysis['collect_stats']['average']:,}
- 中位数: {analysis['collect_stats']['median']:,}
- 最高: {analysis['collect_stats']['max']:,}
- 最低: {analysis['collect_stats']['min']:,}

播放数据:
- 总播放数: {analysis['view_stats']['total']:,}
- 平均播放数: {analysis['view_stats']['average']:,}
- 中位数: {analysis['view_stats']['median']:,}
- 最高: {analysis['view_stats']['max']:,}
- 最低: {analysis['view_stats']['min']:,}

互动率数据:
- 平均互动率: {analysis['engagement_stats']['average']}%
- 中位数: {analysis['engagement_stats']['median']}%
- 最高: {analysis['engagement_stats']['max']}%
- 最低: {analysis['engagement_stats']['min']}%
"""
            
            utils.logger.info("[StatsAnalyzer] Generated comprehensive stats report")
            return report
            
        except Exception as e:
            utils.logger.error(f"[StatsAnalyzer] Error generating stats report: {e}")
            return f"生成报告时出错: {str(e)}"