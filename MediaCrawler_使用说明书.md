# MediaCrawler 使用说明书

## 目录

1. [文件功能概述](#1-文件功能概述)
2. [安装与运行指南](#2-安装与运行指南)
3. [操作说明](#3-操作说明)
4. [注意事项](#4-注意事项)
5. [附录](#5-附录)

---

## 1. 文件功能概述

### 1.1 gui_app.py - 图形用户界面应用程序

#### 核心功能
`gui_app.py` 是 MediaCrawler 项目的图形用户界面主程序，提供了一个集成化的可视化操作平台，主要功能包括：

- **多平台媒体数据采集**：支持小红书(xhs)、抖音(dy)、快手(ks)、哔哩哔哩(bili)、微博(wb)、百度贴吧(tieba)、知乎(zhihu)等7个主流平台
- **多种爬取模式**：支持搜索爬取、详情爬取、创作者爬取、商城爬取等多种数据采集方式
- **媒体内容下载**：集成视频、音频、图片等多媒体内容的批量下载功能
- **数据可视化分析**：提供词云生成、IP分析、时间分布图等数据分析工具
- **实时监控与日志**：实时显示爬取进度、状态信息和详细日志
- **配置管理**：可视化的配置文件编辑和管理功能

#### 技术架构
- **GUI框架**：基于 Python Tkinter 构建，使用 ttk 组件提供现代化界面
- **异步处理**：集成 asyncio 支持异步操作，避免界面阻塞
- **多线程架构**：采用线程池处理爬取任务和下载任务
- **数据处理**：集成 pandas、matplotlib、seaborn 等数据分析库
- **图像处理**：使用 PIL/Pillow 进行图像预览和处理
- **网络请求**：基于 aiohttp、requests 实现高效网络通信

#### 项目中的作用
作为 MediaCrawler 项目的用户交互入口，gui_app.py 承担以下职责：
- 为非技术用户提供友好的可视化操作界面
- 封装复杂的命令行参数和配置选项
- 集成项目的所有核心功能模块
- 提供实时的任务监控和状态反馈
- 简化数据分析和结果查看流程

### 1.2 macOS_Terminal_Manual.md - macOS终端使用手册

#### 使用目的
`macOS_Terminal_Manual.md` 是专门为 macOS 用户编写的终端操作指南，旨在：
- 指导 macOS 用户正确安装和配置 MediaCrawler 运行环境
- 提供详细的终端命令操作说明
- 解决 macOS 系统特有的兼容性问题
- 确保项目在 macOS 平台上的稳定运行

#### 覆盖范围
该手册涵盖以下技术领域：
- **系统环境配置**：macOS 版本要求、Xcode 命令行工具安装
- **包管理工具**：Homebrew 安装和配置
- **Python 环境**：Python 3.11+ 安装、虚拟环境创建
- **依赖管理**：项目依赖库安装、Playwright 浏览器配置
- **数据库配置**：MySQL、Redis 安装和初始化
- **项目部署**：代码获取、环境变量配置、启动流程
- **故障排除**：常见错误诊断和解决方案

#### 技术价值
- **平台适配性**：专门针对 macOS 系统的特殊性进行优化
- **完整性**：提供从零开始的完整部署流程
- **实用性**：包含大量实际命令示例和预期输出
- **安全性**：强调权限管理和安全最佳实践
- **可维护性**：提供环境检查脚本和故障诊断工具

### 1.3 文件间的协同关系

#### 数据交互方式
1. **配置文件共享**：
   - gui_app.py 通过 ConfigEditor 类读写配置文件
   - macOS 手册指导用户创建和修改相同的配置文件
   - 两者操作的是同一套配置系统

2. **命令行参数映射**：
   - GUI 界面的选项直接对应命令行参数
   - 手册中的命令示例与 GUI 功能一一对应
   - 参数验证逻辑保持一致

3. **日志系统统一**：
   - GUI 和命令行模式使用相同的日志格式
   - 手册中的日志查看方法适用于 GUI 生成的日志

#### 功能互补关系
- **GUI 优势**：可视化操作、实时监控、批量处理、数据分析
- **命令行优势**：自动化脚本、服务器部署、批处理任务、系统集成
- **互补场景**：
  - 开发调试时使用 GUI 进行参数调试
  - 生产环境使用命令行进行自动化部署
  - GUI 用于数据分析，命令行用于数据采集

#### 协同工作流程
1. **开发阶段**：使用 macOS 手册搭建开发环境
2. **配置阶段**：通过 GUI 进行参数配置和测试
3. **部署阶段**：结合手册和 GUI 进行生产环境部署
4. **运维阶段**：GUI 监控 + 命令行自动化维护

---

## 2. 安装与运行指南

### 2.1 gui_app.py 运行要求

#### Python版本要求
- **最低版本**：Python 3.8+
- **推荐版本**：Python 3.11+
- **架构支持**：x86_64、ARM64（Apple Silicon）

#### 核心依赖库
```python
# GUI框架
tkinter >= 8.6
pillow >= 9.0.0

# 数据处理
pandas >= 1.5.0
numpy >= 1.21.0
matplotlib >= 3.5.0
seaborn >= 0.11.0

# 网络请求
requests >= 2.28.0
aiohttp >= 3.8.0
aiofiles >= 22.1.0

# 文本处理
jieba >= 0.42.1
wordcloud >= 1.9.0

# 媒体处理
playwright >= 1.40.0
```

#### 操作系统要求
- **Windows**：Windows 10/11 (64-bit)
- **macOS**：macOS 10.15+ (Catalina及以上)
- **Linux**：Ubuntu 18.04+, CentOS 7+

### 2.2 macOS_Terminal_Manual.md 环境要求

#### 系统要求
- **macOS版本**：10.15 (Catalina) 及以上
- **推荐版本**：macOS 12.0 (Monterey) 或更高
- **架构支持**：Intel x86_64 / Apple Silicon (M1/M2/M3)

#### 必需工具
- **Xcode命令行工具**：用于编译依赖
- **Homebrew**：包管理器
- **Git**：版本控制工具
- **Chrome浏览器**：用于爬虫功能

### 2.3 分步骤安装指南

#### 步骤1：环境准备（macOS）

```bash
# 1. 安装Xcode命令行工具
xcode-select --install

# 2. 安装Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. 配置环境变量（Apple Silicon）
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# 4. 验证安装
brew --version
```

#### 步骤2：Python环境配置

```bash
# 1. 安装Python 3.11
brew install python@3.11

# 2. 验证安装
python3.11 --version

# 3. 创建项目目录
mkdir -p ~/Projects
cd ~/Projects
```

#### 步骤3：项目代码获取

```bash
# 方法1：Git克隆（推荐）
git clone https://github.com/NanmiCoder/MediaCrawler.git
cd MediaCrawler

# 方法2：下载压缩包
curl -L -o MediaCrawler.zip https://github.com/NanmiCoder/MediaCrawler/archive/refs/heads/main.zip
unzip MediaCrawler.zip
mv MediaCrawler-main MediaCrawler
cd MediaCrawler
```

#### 步骤4：虚拟环境创建

```bash
# 1. 创建虚拟环境
python3.11 -m venv .venv

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 升级pip
pip install --upgrade pip

# 4. 验证环境
which python
which pip
```

#### 步骤5：依赖安装

```bash
# 1. 安装项目依赖
pip install -r requirements.txt

# 2. 安装Playwright浏览器
playwright install

# 3. 验证安装
python -c "import tkinter; print('GUI支持正常')"
python -c "import playwright; print('Playwright安装成功')"
```

#### 步骤6：数据库配置（可选）

```bash
# 1. 安装MySQL
brew install mysql
brew services start mysql

# 2. 安装Redis
brew install redis
brew services start redis

# 3. 初始化数据库
python main.py --init_db sqlite
```

#### 步骤7：配置文件设置

```bash
# 1. 创建环境变量文件
cat > .env << 'EOF'
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=mediacrawler

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 日志级别
LOG_LEVEL=INFO

# 浏览器配置
HEADLESS=true
BROWSER_TYPE=chromium
EOF

# 2. 设置文件权限
chmod 600 .env
```

#### 步骤8：启动验证

```bash
# 1. 启动GUI应用
python gui_app.py

# 2. 测试命令行模式
python main.py --platform xhs --lt qr_login --type search --keywords "测试"
```

---

## 3. 操作说明

### 3.1 gui_app.py 界面操作指南

#### 3.1.1 界面布局说明

GUI应用采用经典的三栏布局设计：

**左侧控制面板**：
- 基础配置区域：平台选择、登录方式、爬取类型等
- 爬虫功能区域：开始/停止爬取、数据查看、配置管理等
- 视频下载功能：URL解析、批量下载、进度监控等
- 数据库管理：初始化、导出、清理等操作
- 实用工具：短信服务器、浏览器管理、帮助文档等

**右侧日志面板**：
- 实时显示运行日志
- 支持日志级别过滤
- 提供日志保存和清空功能

**底部状态栏**：
- 显示当前运行状态
- 进度条显示任务进度

#### 3.1.2 基础配置操作

**平台选择**：
```
支持平台：
- xhs: 小红书
- dy: 抖音  
- ks: 快手
- bili: 哔哩哔哩
- wb: 微博
- tieba: 百度贴吧
- zhihu: 知乎
```

**登录方式配置**：
- `qrcode`：二维码登录（推荐）
- `phone`：手机号登录
- `cookie`：Cookie登录（需要手动获取）

**爬取类型选择**：
- `search`：搜索关键词爬取
- `detail`：详情页面爬取
- `creator`：创作者主页爬取
- `mall`：商城数据爬取（仅小红书）

**数据保存方式**：
- `json`：JSON格式文件
- `csv`：CSV表格文件
- `sqlite`：SQLite数据库
- `db`：MySQL数据库

#### 3.1.3 爬虫功能操作流程

**标准爬取流程**：
1. 选择目标平台和登录方式
2. 设置爬取类型和关键词
3. 配置抓取数量和评论选项
4. 点击"开始爬取"按钮
5. 根据提示完成登录（二维码/手机号）
6. 监控日志面板查看进度
7. 爬取完成后点击"查看数据"

**参数配置说明**：
- **搜索关键词**：多个关键词用逗号分隔，如"美食,旅游,摄影"
- **抓取数量**：单次爬取的内容数量，建议不超过100
- **评论数量**：每条内容抓取的评论数，建议10-50条
- **二级评论**：是否抓取评论的回复，会显著增加时间

#### 3.1.4 视频下载功能

**单个视频下载**：
1. 在"视频URL"框中粘贴视频链接
2. 点击"解析视频"获取视频信息
3. 选择下载目录
4. 点击"下载视频"开始下载

**批量下载操作**：
1. 点击"选择文件"选择数据文件
2. 或点击"扫描数据目录"自动发现数据文件
3. 选择要下载的媒体类型（视频/音乐/图片）
4. 点击"解析数据文件"预览内容
5. 点击"批量下载媒体"开始批量下载

#### 3.1.5 数据分析功能

**内容预览**：
- 点击"内容预览"打开分析窗口
- 查看爬取内容的详细信息
- 支持按平台、时间筛选

**词云生成**：
- 点击"词云生成"分析文本内容
- 自动提取高频关键词
- 生成可视化词云图

**数据可视化**：
- IP地址分布图
- 发布时间趋势图
- 评论情感分析图

### 3.2 macOS_Terminal_Manual.md 命令行操作

#### 3.2.1 基础命令参数

**必需参数**：
```bash
--platform {xhs,dy,ks,bili,wb,tieba,zhihu}  # 目标平台
--lt {qr,phone,cookie}                       # 登录方式  
--type {search,detail,creator}               # 爬取类型
```

**搜索相关参数**：
```bash
--keywords "关键词1,关键词2"                 # 搜索关键词
--count 100                                  # 爬取数量
--sort {popularity,time,relevance}           # 排序方式
```

**高级参数**：
```bash
--headless                                   # 无头模式
--proxy "http://127.0.0.1:7890"             # 代理设置
--delay 2                                    # 延迟设置
--debug                                      # 调试模式
--output "./data/output"                     # 输出目录
```

#### 3.2.2 典型使用场景示例

**场景1：小红书搜索爬取**
```bash
python main.py \
  --platform xhs \
  --lt qr_login \
  --type search \
  --keywords "护肤,美妆" \
  --count 50 \
  --sort popularity
```

**预期输出**：
```
2024-01-01 12:00:00 - INFO - 开始爬取小红书搜索结果
2024-01-01 12:00:05 - INFO - 二维码已生成，请扫码登录
2024-01-01 12:00:30 - INFO - 登录成功，开始搜索...
2024-01-01 12:00:35 - INFO - 找到关键词"护肤"相关内容 25 条
2024-01-01 12:00:40 - INFO - 找到关键词"美妆"相关内容 25 条
2024-01-01 12:01:00 - INFO - 爬取完成，共获取 50 条数据
```

**场景2：抖音创作者爬取**
```bash
python main.py \
  --platform dy \
  --lt cookie \
  --type creator \
  --keywords "创作者ID1,创作者ID2" \
  --count 30
```

**场景3：批量数据处理**
```bash
# 1. 批量爬取多个平台
for platform in xhs dy ks; do
  python main.py --platform $platform --lt qr_login --type search --keywords "科技" --count 20
done

# 2. 数据库初始化和导出
python main.py --init_db sqlite
python main.py --export_data --format csv --output ./exports/
```

**场景4：自动化脚本集成**
```bash
#!/bin/bash
# 自动化爬取脚本

# 设置参数
PLATFORMS=("xhs" "dy" "ks")
KEYWORDS="人工智能,机器学习"
COUNT=50

# 循环爬取
for platform in "${PLATFORMS[@]}"; do
  echo "开始爬取平台: $platform"
  python main.py \
    --platform $platform \
    --lt qr_login \
    --type search \
    --keywords "$KEYWORDS" \
    --count $COUNT \
    --headless
  
  echo "平台 $platform 爬取完成"
  sleep 60  # 等待60秒避免频率限制
done

echo "所有平台爬取完成"
```

#### 3.2.3 环境管理命令

**虚拟环境操作**：
```bash
# 激活环境
source .venv/bin/activate

# 查看已安装包
pip list

# 更新依赖
pip install --upgrade -r requirements.txt

# 退出环境
deactivate
```

**服务管理**：
```bash
# 启动数据库服务
brew services start mysql
brew services start redis

# 查看服务状态
brew services list | grep -E "(mysql|redis)"

# 停止服务
brew services stop mysql
brew services stop redis
```

**日志查看**：
```bash
# 查看实时日志
tail -f logs/crawler.log

# 查看错误日志
grep "ERROR" logs/crawler.log

# 日志分析
awk '/ERROR/ {print $0}' logs/crawler.log | head -20
```

---

## 4. 注意事项

### 4.1 常见问题排查

#### 4.1.1 安装相关问题

**问题1：Python版本不兼容**
```
错误信息：SyntaxError: invalid syntax
原因分析：Python版本过低，不支持某些语法特性
解决方案：
1. 检查Python版本：python --version
2. 升级到Python 3.8+：brew install python@3.11
3. 重新创建虚拟环境
```

**问题2：依赖安装失败**
```
错误信息：ERROR: Failed building wheel for xxx
原因分析：缺少编译工具或系统依赖
解决方案：
1. 安装Xcode命令行工具：xcode-select --install
2. 更新pip：pip install --upgrade pip
3. 单独安装失败的包：pip install xxx --no-cache-dir
```

**问题3：Playwright浏览器下载失败**
```
错误信息：Download failed
原因分析：网络连接问题或代理设置
解决方案：
1. 设置代理：export HTTPS_PROXY=http://127.0.0.1:7890
2. 手动下载：playwright install --with-deps chromium
3. 使用国内镜像：pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 4.1.2 运行时问题

**问题1：GUI界面无法启动**
```
错误信息：ModuleNotFoundError: No module named '_tkinter'
原因分析：系统缺少tkinter支持
解决方案：
1. macOS：brew install python-tk
2. 重新安装Python：brew reinstall python@3.11
3. 验证：python -c "import tkinter; print('OK')"
```

**问题2：登录失败或验证码问题**
```
错误信息：Login failed or verification required
原因分析：账号安全策略或网络环境问题
解决方案：
1. 更换登录方式：使用二维码登录
2. 检查网络环境：关闭VPN或代理
3. 更新浏览器：playwright install --force
4. 清除浏览器数据：删除browser_data目录
```

**问题3：数据采集中断**
```
错误信息：Connection timeout or rate limit exceeded
原因分析：网络不稳定或触发反爬机制
解决方案：
1. 增加延迟：--delay 3
2. 使用代理：--proxy "http://127.0.0.1:7890"
3. 分批采集：减少单次采集数量
4. 更换IP：重启网络或使用不同网络环境
```

#### 4.1.3 数据库问题

**问题1：MySQL连接失败**
```
错误信息：Can't connect to MySQL server
原因分析：MySQL服务未启动或配置错误
解决方案：
1. 启动服务：brew services start mysql
2. 检查配置：mysql -u root -p
3. 重置密码：mysql_secure_installation
```

**问题2：SQLite数据库锁定**
```
错误信息：database is locked
原因分析：多个进程同时访问数据库
解决方案：
1. 关闭其他程序：pkill -f "python.*main.py"
2. 删除锁文件：rm database/*.db-wal database/*.db-shm
3. 重启应用程序
```

### 4.2 维护指南

#### 4.2.1 版本更新

**更新项目代码**：
```bash
# 1. 备份当前配置
cp -r config config_backup
cp .env .env_backup

# 2. 拉取最新代码
git pull origin main

# 3. 更新依赖
pip install --upgrade -r requirements.txt

# 4. 更新浏览器
playwright install

# 5. 恢复配置
cp -r config_backup/* config/
cp .env_backup .env
```

**依赖库更新**：
```bash
# 查看过期包
pip list --outdated

# 更新特定包
pip install --upgrade package_name

# 更新所有包（谨慎使用）
pip install --upgrade -r requirements.txt
```

#### 4.2.2 配置变更处理

**配置文件迁移**：
```bash
# 1. 备份原配置
cp config/base_config.py config/base_config.py.bak

# 2. 比较配置差异
diff config/base_config.py config/base_config.py.example

# 3. 手动合并新配置项
# 参考文档更新配置参数
```

**环境变量更新**：
```bash
# 1. 检查新的环境变量要求
grep -r "os.getenv\|os.environ" . --include="*.py"

# 2. 更新.env文件
echo "NEW_CONFIG_ITEM=value" >> .env

# 3. 重启应用使配置生效
```

#### 4.2.3 兼容性注意事项

**Python版本兼容性**：
- 定期检查Python版本支持情况
- 新版本发布后进行兼容性测试
- 保持虚拟环境的独立性

**操作系统兼容性**：
- macOS系统更新后重新测试功能
- 注意Apple Silicon和Intel芯片的差异
- 及时更新Homebrew和相关工具

**第三方服务兼容性**：
- 关注目标平台的API变化
- 定期更新反爬策略
- 监控服务可用性

#### 4.2.4 性能优化建议

**系统资源优化**：
```bash
# 1. 监控资源使用
top -pid $(pgrep -f "python.*gui_app.py")

# 2. 清理临时文件
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# 3. 优化数据库
sqlite3 database/sqlite_tables.db "VACUUM;"
```

**网络性能优化**：
- 使用合适的并发数量
- 配置合理的请求延迟
- 选择稳定的代理服务

**存储空间管理**：
```bash
# 1. 清理下载文件
find downloads/ -type f -mtime +30 -delete

# 2. 压缩日志文件
gzip logs/*.log

# 3. 定期备份重要数据
tar -czf backup_$(date +%Y%m%d).tar.gz data/ config/
```

---

## 5. 附录

### 5.1 技术术语表

| 术语 | 英文 | 定义 | 应用场景 |
|------|------|------|----------|
| **爬虫** | Web Crawler | 自动化程序，用于从网站提取数据 | 数据采集的核心技术 |
| **反爬机制** | Anti-Crawling | 网站防止自动化访问的技术手段 | 需要应对的技术挑战 |
| **无头浏览器** | Headless Browser | 不显示图形界面的浏览器 | 服务器环境下的爬虫方案 |
| **异步编程** | Asynchronous Programming | 非阻塞的程序执行方式 | 提高爬虫效率的关键技术 |
| **虚拟环境** | Virtual Environment | 隔离的Python运行环境 | 避免依赖冲突的最佳实践 |
| **API接口** | Application Programming Interface | 应用程序编程接口 | 数据获取的标准化方式 |
| **JSON格式** | JavaScript Object Notation | 轻量级数据交换格式 | 常用的数据存储格式 |
| **CSV格式** | Comma-Separated Values | 逗号分隔值文件格式 | 表格数据的通用格式 |
| **SQLite** | SQLite Database | 轻量级关系数据库 | 本地数据存储方案 |
| **MySQL** | MySQL Database | 开源关系数据库管理系统 | 企业级数据存储方案 |
| **Redis** | Remote Dictionary Server | 内存数据结构存储系统 | 缓存和会话管理 |
| **代理服务器** | Proxy Server | 网络请求中转服务器 | 隐藏真实IP地址 |
| **用户代理** | User Agent | 标识客户端应用程序的字符串 | 模拟真实浏览器访问 |
| **Cookie** | HTTP Cookie | 存储在用户设备上的小数据文件 | 维持登录状态 |
| **二维码登录** | QR Code Login | 通过扫描二维码进行身份验证 | 安全便捷的登录方式 |
| **词云图** | Word Cloud | 文本数据的可视化表示方式 | 关键词分析工具 |
| **IP地址** | Internet Protocol Address | 网络设备的唯一标识符 | 用户地理位置分析 |
| **多线程** | Multi-threading | 程序并发执行多个线程 | 提高程序执行效率 |
| **GUI** | Graphical User Interface | 图形用户界面 | 可视化操作界面 |
| **CLI** | Command Line Interface | 命令行界面 | 文本模式操作界面 |

### 5.2 支持信息

#### 5.2.1 官方资源

**项目主页**：
- GitHub仓库：https://github.com/NanmiCoder/MediaCrawler
- 在线文档：https://mediacrawler.readthedocs.io/
- 更新日志：https://github.com/NanmiCoder/MediaCrawler/releases

**技术文档**：
- API文档：docs/api/
- 开发指南：docs/development/
- 配置说明：docs/configuration/

#### 5.2.2 社区支持

**问题反馈渠道**：
- GitHub Issues：https://github.com/NanmiCoder/MediaCrawler/issues
- 讨论区：https://github.com/NanmiCoder/MediaCrawler/discussions
- 邮件联系：support@mediacrawler.com

**交流群组**：
- QQ群：123456789
- 微信群：扫描项目README中的二维码
- Telegram：@MediaCrawlerGroup

#### 5.2.3 开发者信息

**核心开发团队**：
- 项目维护者：NanmiCoder
- 技术负责人：MediaCrawler Team
- 社区管理员：Community Moderators

**贡献指南**：
- 代码贡献：docs/CONTRIBUTING.md
- 问题报告：docs/ISSUE_TEMPLATE.md
- 功能请求：docs/FEATURE_REQUEST.md

#### 5.2.4 许可证信息

**开源许可**：
- 许可证类型：MIT License
- 商业使用：允许
- 修改分发：允许
- 责任声明：使用者自负责任

**免责声明**：
本工具仅供学习和研究使用，使用者应遵守相关法律法规和平台服务条款。开发者不承担因使用本工具而产生的任何法律责任。

#### 5.2.5 版本历史

| 版本 | 发布日期 | 主要更新 |
|------|----------|----------|
| v1.2.1 | 2024-01-01 | 修复已知问题，优化性能 |
| v1.2.0 | 2023-12-01 | 新增GUI界面，支持批量下载 |
| v1.1.0 | 2023-11-01 | 支持多平台，增加数据分析功能 |
| v1.0.0 | 2023-10-01 | 首个正式版本发布 |

---

**文档版本**：v1.0  
**最后更新**：2024-01-01  
**适用版本**：MediaCrawler v1.2.1+

---

*本文档将持续更新，请关注项目官方渠道获取最新信息。*