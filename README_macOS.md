# MediaCrawler - macOS版本使用指南

## 概述

MediaCrawler macOS版本是专为苹果macOS系统优化的媒体爬虫工具配置编辑器。该版本完全兼容Windows版本的所有功能，同时针对macOS系统特性进行了深度优化。

## 系统要求

- **操作系统**: macOS 10.12 (Sierra) 或更高版本
- **Python版本**: Python 3.7 或更高版本
- **内存**: 至少 4GB RAM
- **存储空间**: 至少 100MB 可用空间

## macOS专属特性

### 🎨 界面设计
- **Apple Human Interface Guidelines**: 严格遵循苹果人机界面指南
- **原生macOS外观**: 使用系统原生控件和样式
- **自适应主题**: 自动适配浅色/深色模式
- **毛玻璃效果**: 支持macOS Mojave+的毛玻璃视觉效果

### 📱 Retina显示优化
- **高DPI支持**: 完美支持Retina显示屏
- **矢量图标**: 使用SVG图标确保清晰显示
- **字体优化**: 使用SF Pro Display系统字体
- **自动缩放**: 根据显示器DPI自动调整界面元素

### 🖱️ 触控板手势支持
- **双指滚动**: 支持触控板双指滚动
- **捏合缩放**: 支持双指捏合缩放（在支持的区域）
- **三指拖拽**: 支持三指拖拽操作
- **智能滚动**: 支持惯性滚动和边界反弹

### 🔧 系统集成
- **Dock集成**: 应用图标显示在Dock中
- **菜单栏**: 标准macOS菜单栏布局
- **全屏支持**: 支持macOS原生全屏模式
- **通知中心**: 集成系统通知

## 安装和启动

### 方法一：跨平台启动器（推荐）
```bash
cd MediaCrawler/config_editor_gui
python platform_launcher.py
```

### 方法二：直接启动macOS版本
```bash
cd MediaCrawler/config_editor_gui
python gui_app_macos.py
```

### 方法三：命令行直接启动
```bash
cd MediaCrawler/config_editor_gui
python platform_launcher.py --direct
```

## 功能特性

### 📋 配置文件管理
支持以下配置文件的编辑：
- **基础配置** (`base_config.py`)
- **数据库配置** (`db_config.py`)
- **小红书配置** (`xhs_config.py`)
- **抖音配置** (`dy_config.py`)
- **哔哩哔哩配置** (`bilibili_config.py`)
- **微博配置** (`weibo_config.py`)
- **贴吧配置** (`tieba_config.py`)
- **知乎配置** (`zhihu_config.py`)

### 🎛️ 配置项类型
支持51种不同类型的配置项：
- 文本输入、数字输入、布尔选择
- 文件路径选择、日期时间选择
- 下拉菜单、多选框、密码输入
- 颜色选择、范围滑块等

### 💾 数据操作
- **加载配置**: 从文件加载现有配置
- **保存配置**: 保存修改到配置文件
- **重置配置**: 恢复到默认设置
- **导入/导出**: 支持配置的导入和导出
- **实时预览**: 配置修改的实时预览

## macOS专属界面元素

### 🔧 工具栏
- 原生macOS样式工具栏
- 支持工具栏自定义
- 图标使用SF Symbols风格

### 📑 标签页
- 原生NSTabView样式
- 支持标签页拖拽重排
- 标签页关闭按钮

### 📊 状态栏
- 显示当前系统信息
- 实时更新状态
- macOS风格状态指示器

### 🎨 主题适配
- **浅色模式**: 适配macOS浅色主题
- **深色模式**: 适配macOS深色主题
- **自动切换**: 跟随系统主题自动切换
- **强调色**: 使用系统强调色

## 键盘快捷键

### 应用程序
- `Cmd + O`: 打开配置编辑器
- `Cmd + Q`: 退出应用
- `Cmd + ,`: 打开偏好设置
- `Cmd + H`: 隐藏应用

### 编辑操作
- `Cmd + S`: 保存配置
- `Cmd + Z`: 撤销操作
- `Cmd + Shift + Z`: 重做操作
- `Cmd + A`: 全选

### 视图操作
- `Cmd + 0`: 实际大小
- `Cmd + +`: 放大
- `Cmd + -`: 缩小
- `Ctrl + Cmd + F`: 全屏模式

## 兼容性测试

运行兼容性测试以验证功能：
```bash
cd MediaCrawler/config_editor_gui
python test_macos_compatibility.py
```

测试内容包括：
- ✅ 系统检测功能
- ✅ macOS增强功能
- ✅ 配置编辑器核心功能
- ✅ GUI应用启动
- ✅ 跨平台启动器
- ✅ 配置文件兼容性

## 故障排除

### 常见问题

**Q: 应用无法启动**
A: 检查Python版本是否为3.7+，确保所有依赖已安装

**Q: 界面显示异常**
A: 尝试重启应用，或检查系统显示设置

**Q: 触控板手势不工作**
A: 确保在系统偏好设置中启用了相关手势

**Q: 深色模式不生效**
A: 检查macOS版本是否为10.14+，重启应用

### 日志和调试
```bash
# 启用详细日志
python platform_launcher.py --verbose

# 查看系统信息
python -c "from platform_launcher import PlatformLauncher; PlatformLauncher().show_system_info()"
```

## 版本历史

### v1.0.0 (当前版本)
- ✅ 完整的macOS界面适配
- ✅ Retina显示优化
- ✅ 触控板手势支持
- ✅ 系统主题自动适配
- ✅ 跨平台启动器
- ✅ 完整功能兼容性

## 技术架构

### 核心模块
- `config_editor_macos.py`: macOS专用配置编辑器
- `macos_enhancements.py`: macOS系统增强功能
- `platform_launcher.py`: 跨平台启动器
- `gui_app_macos.py`: macOS GUI应用

### 设计模式
- **适配器模式**: 跨平台兼容性
- **工厂模式**: 动态组件创建
- **观察者模式**: 主题变化响应
- **策略模式**: 不同平台策略

## 贡献指南

欢迎为macOS版本贡献代码：

1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 运行兼容性测试
5. 提交Pull Request

### 开发环境设置
```bash
# 克隆仓库
git clone <repository-url>
cd MediaCrawler

# 安装依赖
pip install -r requirements.txt

# 运行测试
python config_editor_gui/test_macos_compatibility.py
```

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 联系我们

- **项目主页**: [GitHub Repository]
- **问题反馈**: [GitHub Issues]
- **功能建议**: [GitHub Discussions]

---

**MediaCrawler macOS版本** - 为Mac用户打造的专业媒体爬虫配置工具 🍎