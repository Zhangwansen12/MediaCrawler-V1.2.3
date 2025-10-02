# -*- coding: utf-8 -*-
"""
MediaCrawler 配置编辑器GUI包

这个包提供了一个图形化的配置编辑器，用于编辑MediaCrawler的各种配置文件。

主要功能：
- 可视化配置编辑
- 多配置文件支持
- 实时验证
- 导入/导出功能
"""

__version__ = "1.0.0"
__author__ = "MediaCrawler Team"

# 导入主要类
from .config_editor import ConfigEditor

__all__ = ["ConfigEditor"]