# macOS终端模拟器使用手册 - MediaCrawler项目运行指南

## 📋 目录
1. [安装配置部分](#1-安装配置部分)
2. [项目部署部分](#2-项目部署部分)
3. [操作使用部分](#3-操作使用部分)
4. [故障处理部分](#4-故障处理部分)
5. [安全警告与最佳实践](#5-安全警告与最佳实践)

---

## 1. 安装配置部分

### 1.1 系统环境要求

#### 🖥️ macOS版本要求
- **最低版本**: macOS 10.15 (Catalina)
- **推荐版本**: macOS 12.0 (Monterey) 或更高
- **架构支持**: Intel x86_64 / Apple Silicon (M1/M2)

#### 🔧 必需工具检查
在开始之前，请确认系统已安装以下工具：

```bash
# 检查系统版本
sw_vers

# 预期输出示例：
# ProductName:    macOS
# ProductVersion: 13.0
# BuildVersion:   22A380
```

```bash
# 检查Xcode命令行工具
xcode-select --version

# 预期输出示例：
# xcode-select version 2395.
```

### 1.2 终端模拟器安装

#### 🍺 方法一：使用Homebrew安装（推荐）

**步骤1：安装Homebrew**
```bash
# ⚠️ 无需sudo权限
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 预期输出示例：
# ==> Installation successful!
# ==> Homebrew has enabled anonymous aggregate formulae and cask analytics.
```

**步骤2：配置环境变量**
```bash
# 对于Intel Mac
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc

# 对于Apple Silicon Mac
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

**步骤3：验证Homebrew安装**
```bash
# ⚠️ 无需sudo权限
brew --version

# 预期输出示例：
# Homebrew 4.0.0
# Homebrew/homebrew-core (git revision 1234567; last commit 2023-01-01)
```

#### 🔨 方法二：手动安装终端增强工具

**安装iTerm2（可选但推荐）**
```bash
# ⚠️ 无需sudo权限
brew install --cask iterm2

# 预期输出示例：
# ==> Downloading https://iterm2.com/downloads/stable/iTerm2-3_4_19.zip
# ==> Installing Cask iterm2
# ==> Moving App 'iTerm.app' to '/Applications/iTerm.app'
```

### 1.3 必要依赖组件安装

#### 🐍 Python环境配置

**步骤1：安装Python 3.11+**
```bash
# ⚠️ 无需sudo权限
brew install python@3.11

# 预期输出示例：
# ==> Downloading https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
# ==> Installing python@3.11
# ==> Summary
# 🍺  python@3.11 was successfully installed!
```

**步骤2：验证Python安装**
```bash
# 检查Python版本
python3.11 --version

# 预期输出示例：
# Python 3.11.0
```

**步骤3：安装pip包管理器**
```bash
# ⚠️ 无需sudo权限
python3.11 -m ensurepip --upgrade

# 预期输出示例：
# Looking in links: /tmp/tmpxxxxxxx
# Requirement already satisfied: setuptools in /usr/local/lib/python3.11/site-packages
# Requirement already satisfied: pip in /usr/local/lib/python3.11/site-packages
```

#### 🌐 Git版本控制工具

**安装Git**
```bash
# ⚠️ 无需sudo权限
brew install git

# 预期输出示例：
# ==> Downloading https://github.com/git/git/archive/v2.39.0.tar.gz
# ==> Installing git
# 🍺  git was successfully installed!
```

**配置Git用户信息**
```bash
# ⚠️ 无需sudo权限 - 替换为您的信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 验证配置
git config --list | grep user

# 预期输出示例：
# user.name=Your Name
# user.email=your.email@example.com
```

#### 🔧 其他必需工具

**安装Node.js（用于某些功能）**
```bash
# ⚠️ 无需sudo权限
brew install node

# 预期输出示例：
# ==> Downloading https://nodejs.org/dist/v18.12.1/node-v18.12.1.tar.xz
# ==> Installing node
# 🍺  node was successfully installed!
```

**安装Chrome浏览器（用于爬虫功能）**
```bash
# ⚠️ 无需sudo权限
brew install --cask google-chrome

# 预期输出示例：
# ==> Downloading https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg
# ==> Installing Cask google-chrome
# ==> Moving App 'Google Chrome.app' to '/Applications/Google Chrome.app'
```

#### ✅ 环境验证脚本

创建并运行环境检查脚本：
```bash
# 创建检查脚本
cat > check_environment.sh << 'EOF'
#!/bin/bash
echo "🔍 检查macOS环境配置..."
echo "================================"

# 检查macOS版本
echo "📱 macOS版本:"
sw_vers

# 检查Python
echo -e "\n🐍 Python版本:"
python3.11 --version 2>/dev/null || echo "❌ Python 3.11 未安装"

# 检查pip
echo -e "\n📦 pip版本:"
python3.11 -m pip --version 2>/dev/null || echo "❌ pip 未安装"

# 检查Git
echo -e "\n🌐 Git版本:"
git --version 2>/dev/null || echo "❌ Git 未安装"

# 检查Node.js
echo -e "\n🟢 Node.js版本:"
node --version 2>/dev/null || echo "❌ Node.js 未安装"

# 检查Chrome
echo -e "\n🌐 Chrome浏览器:"
if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✅ Chrome 已安装"
else
    echo "❌ Chrome 未安装"
fi

# 检查Homebrew
echo -e "\n🍺 Homebrew版本:"
brew --version 2>/dev/null || echo "❌ Homebrew 未安装"

echo -e "\n✅ 环境检查完成!"
EOF

# 赋予执行权限并运行
chmod +x check_environment.sh
./check_environment.sh
```

**预期输出示例：**
```
🔍 检查macOS环境配置...
================================
📱 macOS版本:
ProductName:    macOS
ProductVersion: 13.0
BuildVersion:   22A380

🐍 Python版本:
Python 3.11.0

📦 pip版本:
pip 22.3 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)

🌐 Git版本:
git version 2.39.0

🟢 Node.js版本:
v18.12.1

🌐 Chrome浏览器:
✅ Chrome 已安装

🍺 Homebrew版本:
Homebrew 4.0.0

✅ 环境检查完成!
```

---

## ⚠️ 安全警告

### 🔒 权限管理注意事项
- **避免使用sudo**: 大部分操作无需管理员权限
- **仅在必要时使用sudo**: 系统级配置或安装时才需要
- **验证脚本来源**: 运行任何脚本前请确认其来源可信

### 🛡️ 系统安全建议
- 定期更新Homebrew: `brew update && brew upgrade`
- 保持系统更新: 及时安装macOS安全更新
- 使用虚拟环境: 避免全局安装Python包污染系统环境

---

## 2. 项目部署部分

### 2.1 项目代码获取

#### 🌐 方法一：Git克隆（推荐）

**步骤1：选择项目目录**
```bash
# ⚠️ 无需sudo权限
# 创建项目目录
mkdir -p ~/Projects
cd ~/Projects

# 预期输出：进入Projects目录
pwd
# 预期输出示例：
# /Users/username/Projects
```

**步骤2：克隆项目代码**
```bash
# ⚠️ 无需sudo权限
git clone https://github.com/NanmiCoder/MediaCrawler.git
cd MediaCrawler

# 预期输出示例：
# Cloning into 'MediaCrawler'...
# remote: Enumerating objects: 1234, done.
# remote: Counting objects: 100% (1234/1234), done.
# remote: Compressing objects: 100% (567/567), done.
# remote: Total 1234 (delta 890), reused 1100 (delta 780)
# Receiving objects: 100% (1234/1234), 2.34 MiB | 1.23 MiB/s, done.
# Resolving deltas: 100% (890/890), done.
```

**步骤3：验证项目结构**
```bash
# ⚠️ 无需sudo权限
ls -la

# 预期输出示例：
# total 64
# drwxr-xr-x  15 username  staff   480 Jan  1 12:00 .
# drwxr-xr-x   3 username  staff    96 Jan  1 12:00 ..
# -rw-r--r--   1 username  staff   123 Jan  1 12:00 .gitignore
# -rw-r--r--   1 username  staff  1234 Jan  1 12:00 README.md
# -rw-r--r--   1 username  staff   567 Jan  1 12:00 requirements.txt
# -rw-r--r--   1 username  staff   890 Jan  1 12:00 main.py
# -rw-r--r--   1 username  staff   456 Jan  1 12:00 gui_app.py
# drwxr-xr-x   5 username  staff   160 Jan  1 12:00 config
# drwxr-xr-x   8 username  staff   256 Jan  1 12:00 media_platform
```

#### 📦 方法二：下载压缩包

**步骤1：下载项目压缩包**
```bash
# ⚠️ 无需sudo权限
cd ~/Projects
curl -L -o MediaCrawler.zip https://github.com/NanmiCoder/MediaCrawler/archive/refs/heads/main.zip

# 预期输出示例：
# % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                Dload  Upload   Total   Spent    Left  Speed
# 100 2340k  100 2340k    0     0  1234k      0  0:00:01  0:00:01 --:--:-- 1234k
```

**步骤2：解压项目文件**
```bash
# ⚠️ 无需sudo权限
unzip MediaCrawler.zip
mv MediaCrawler-main MediaCrawler
cd MediaCrawler

# 预期输出示例：
# Archive:  MediaCrawler.zip
# creating: MediaCrawler-main/
# inflating: MediaCrawler-main/README.md
# inflating: MediaCrawler-main/main.py
# ...
```

### 2.2 Python虚拟环境配置

#### 🐍 创建虚拟环境

**步骤1：创建虚拟环境**
```bash
# ⚠️ 无需sudo权限
python3.11 -m venv .venv

# 预期输出：创建.venv目录
ls -la .venv/
# 预期输出示例：
# total 8
# drwxr-xr-x  6 username  staff  192 Jan  1 12:00 .
# drwxr-xr-x 15 username  staff  480 Jan  1 12:00 ..
# drwxr-xr-x  3 username  staff   96 Jan  1 12:00 bin
# drwxr-xr-x  2 username  staff   64 Jan  1 12:00 include
# drwxr-xr-x  3 username  staff   96 Jan  1 12:00 lib
# -rw-r--r--  1 username  staff   75 Jan  1 12:00 pyvenv.cfg
```

**步骤2：激活虚拟环境**
```bash
# ⚠️ 无需sudo权限
source .venv/bin/activate

# 预期输出：命令提示符前出现(.venv)
# (.venv) username@MacBook-Pro MediaCrawler %
```

**步骤3：验证虚拟环境**
```bash
# ⚠️ 无需sudo权限
which python
which pip

# 预期输出示例：
# /Users/username/Projects/MediaCrawler/.venv/bin/python
# /Users/username/Projects/MediaCrawler/.venv/bin/pip
```

### 2.3 依赖库安装

#### 📦 安装Python依赖

**步骤1：升级pip**
```bash
# ⚠️ 无需sudo权限（虚拟环境中）
pip install --upgrade pip

# 预期输出示例：
# Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (22.3)
# Collecting pip
# Downloading pip-23.0-py3-none-any.whl (2.1 MB)
# Successfully installed pip-23.0
```

**步骤2：安装项目依赖**
```bash
# ⚠️ 无需sudo权限（虚拟环境中）
pip install -r requirements.txt

# 预期输出示例：
# Collecting playwright>=1.40.0
# Downloading playwright-1.40.0-py3-none-macosx_10_13_x86_64.whl (34.5 MB)
# Collecting asyncio>=3.4.3
# Downloading asyncio-3.4.3-py3-none-any.whl (101 kB)
# ...
# Successfully installed playwright-1.40.0 asyncio-3.4.3 ...
```

**步骤3：安装Playwright浏览器**
```bash
# ⚠️ 无需sudo权限（虚拟环境中）
playwright install

# 预期输出示例：
# Downloading Chromium 109.0.5414.74 (playwright build v1045) from https://playwright.azureedge.net/builds/chromium/1045/chromium-mac.zip
# 130.2 Mb [====================] 100% 0.0s
# Chromium 109.0.5414.74 (playwright build v1045) downloaded to /Users/username/Library/Caches/ms-playwright/chromium-1045
# Downloading Firefox 108.0.2 (playwright build v1378) from https://playwright.azureedge.net/builds/firefox/1378/firefox-mac.zip
# ...
```

### 2.4 环境变量配置

#### ⚙️ 创建配置文件

**步骤1：复制配置模板**
```bash
# ⚠️ 无需sudo权限
# 检查是否存在配置模板
ls config/

# 预期输出示例：
# base_config.py    dy_config.py      ks_config.py      weibo_config.py
# bilibili_config.py    db_config.py      tieba_config.py   xhs_config.py
```

**步骤2：创建环境变量文件**
```bash
# ⚠️ 无需sudo权限
cat > .env << 'EOF'
# MediaCrawler 环境配置文件

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=mediacrawler

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 代理配置（可选）
PROXY_HOST=
PROXY_PORT=
PROXY_USER=
PROXY_PASSWORD=

# 日志级别
LOG_LEVEL=INFO

# 浏览器配置
HEADLESS=true
BROWSER_TYPE=chromium
EOF

echo "✅ 环境变量文件已创建: .env"
```

**步骤3：设置文件权限**
```bash
# ⚠️ 无需sudo权限
chmod 600 .env

# 验证权限设置
ls -la .env
# 预期输出示例：
# -rw-------  1 username  staff  456 Jan  1 12:00 .env
```

### 2.5 数据库配置（可选）

#### 🗄️ MySQL安装配置

**步骤1：安装MySQL**
```bash
# ⚠️ 无需sudo权限
brew install mysql

# 预期输出示例：
# ==> Downloading https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.32-macos13-x86_64.tar.gz
# ==> Installing mysql
# ==> Starting mysql
# 🍺  mysql was successfully installed!
```

**步骤2：启动MySQL服务**
```bash
# ⚠️ 无需sudo权限
brew services start mysql

# 预期输出示例：
# ==> Successfully started `mysql` (label: homebrew.mxcl.mysql)
```

**步骤3：安全配置MySQL**
```bash
# ⚠️ 需要交互式配置
mysql_secure_installation

# 预期交互示例：
# Securing the MySQL server deployment.
# Enter password for user root: [输入密码]
# Would you like to setup VALIDATE PASSWORD component? (Press y|Y for Yes, any other key for No): n
# Change the password for root ? ((Press y|Y for Yes, any other key for No): n
# Remove anonymous users? (Press y|Y for Yes, any other key for No): y
# Disallow root login remotely? (Press y|Y for Yes, any other key for No): y
# Remove test database and access to it? (Press y|Y for Yes, any other key for No): y
# Reload privilege tables now? (Press y|Y for Yes, any other key for No): y
```

#### 🔴 Redis安装配置

**步骤1：安装Redis**
```bash
# ⚠️ 无需sudo权限
brew install redis

# 预期输出示例：
# ==> Downloading https://download.redis.io/redis-stable.tar.gz
# ==> Installing redis
# 🍺  redis was successfully installed!
```

**步骤2：启动Redis服务**
```bash
# ⚠️ 无需sudo权限
brew services start redis

# 预期输出示例：
# ==> Successfully started `redis` (label: homebrew.mxcl.redis)
```

### 2.6 项目配置验证

#### ✅ 创建配置验证脚本

```bash
# ⚠️ 无需sudo权限
cat > verify_setup.py << 'EOF'
#!/usr/bin/env python3
"""
MediaCrawler 项目配置验证脚本
"""
import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    print(f"🐍 Python版本: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 11:
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，需要3.11+")
        return False

def check_virtual_env():
    """检查虚拟环境"""
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"✅ 虚拟环境已激活: {venv_path}")
        return True
    else:
        print("❌ 虚拟环境未激活")
        return False

def check_dependencies():
    """检查依赖包"""
    required_packages = [
        'playwright',
        'asyncio',
        'aiofiles',
        'httpx',
        'fake-useragent'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_config_files():
    """检查配置文件"""
    config_files = [
        'config/base_config.py',
        'config/dy_config.py',
        'config/ks_config.py',
        'config/xhs_config.py'
    ]
    
    all_exist = True
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"✅ {config_file} 存在")
        else:
            print(f"❌ {config_file} 不存在")
            all_exist = False
    
    return all_exist

def check_project_structure():
    """检查项目结构"""
    required_dirs = [
        'media_platform',
        'config',
        'tools',
        'cache',
        'database'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/ 目录存在")
        else:
            print(f"❌ {directory}/ 目录不存在")
            all_exist = False
    
    return all_exist

def main():
    """主验证函数"""
    print("🔍 MediaCrawler 项目配置验证")
    print("=" * 40)
    
    checks = [
        ("Python版本", check_python_version),
        ("虚拟环境", check_virtual_env),
        ("依赖包", check_dependencies),
        ("配置文件", check_config_files),
        ("项目结构", check_project_structure)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 检查 {name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 所有检查通过！项目配置完成。")
        return 0
    else:
        print("⚠️  部分检查未通过，请根据上述提示进行修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

# 运行验证脚本
python verify_setup.py
```

**预期输出示例：**
```
🔍 MediaCrawler 项目配置验证
========================================

📋 检查 Python版本:
🐍 Python版本: 3.11.0
✅ Python版本符合要求

📋 检查 虚拟环境:
✅ 虚拟环境已激活: /Users/username/Projects/MediaCrawler/.venv

📋 检查 依赖包:
✅ playwright 已安装
✅ asyncio 已安装
✅ aiofiles 已安装
✅ httpx 已安装
✅ fake-useragent 已安装

📋 检查 配置文件:
✅ config/base_config.py 存在
✅ config/dy_config.py 存在
✅ config/ks_config.py 存在
✅ config/xhs_config.py 存在

📋 检查 项目结构:
✅ media_platform/ 目录存在
✅ config/ 目录存在
✅ tools/ 目录存在
✅ cache/ 目录存在
✅ database/ 目录存在

========================================
🎉 所有检查通过！项目配置完成。
```

---

## 3. 操作使用部分

### 3.1 项目启动命令

#### 🚀 基础启动方式

**步骤1：激活虚拟环境**
```bash
# ⚠️ 无需sudo权限
cd ~/Projects/MediaCrawler
source .venv/bin/activate

# 预期输出：命令提示符显示(.venv)
# (.venv) username@MacBook-Pro MediaCrawler %
```

**步骤2：启动GUI界面（推荐）**
```bash
# ⚠️ 无需sudo权限
python gui_app.py

# 预期输出示例：
# 2024-01-01 12:00:00,123 - INFO - GUI应用启动中...
# 2024-01-01 12:00:01,456 - INFO - 加载配置文件完成
# 2024-01-01 12:00:02,789 - INFO - GUI界面已启动，监听端口: http://localhost:8080
```

**步骤3：启动命令行模式**
```bash
# ⚠️ 无需sudo权限
python main.py --platform xhs --lt qr_login --type search --keywords "美食"

# 预期输出示例：
# 2024-01-01 12:00:00,123 - INFO - MediaCrawler 启动
# 2024-01-01 12:00:01,456 - INFO - 平台: 小红书 (xhs)
# 2024-01-01 12:00:02,789 - INFO - 登录方式: 二维码登录
# 2024-01-01 12:00:03,012 - INFO - 爬取类型: 搜索
# 2024-01-01 12:00:04,345 - INFO - 关键词: 美食
```

#### 📋 命令行参数详解

**基础参数**
```bash
# 平台选择 (必需)
--platform {xhs,dy,ks,bili,wb,tieba,zhihu}
# xhs: 小红书, dy: 抖音, ks: 快手, bili: 哔哩哔哩
# wb: 微博, tieba: 百度贴吧, zhihu: 知乎

# 登录方式 (必需)
--lt {qr,phone,cookie}
# qr: 二维码登录, phone: 手机号登录, cookie: Cookie登录

# 爬取类型 (必需)
--type {search,detail,creator}
# search: 搜索爬取, detail: 详情爬取, creator: 创作者爬取
```

**搜索相关参数**
```bash
# 搜索关键词
--keywords "关键词1,关键词2"

# 爬取数量限制
--count 100

# 排序方式
--sort {popularity,time,relevance}
# popularity: 热度排序, time: 时间排序, relevance: 相关性排序
```

**高级参数**
```bash
# 启用无头模式
--headless

# 设置代理
--proxy "http://127.0.0.1:7890"

# 设置延迟（秒）
--delay 2

# 启用调试模式
--debug

# 指定输出目录
--output "./data/output"
```

#### 🎯 常用启动命令示例

**小红书搜索爬取**
```bash
# ⚠️ 无需sudo权限
python main.py \
  --platform xhs \
  --lt qr_login \
  --type search \
  --keywords "护肤,美妆" \
  --count 50 \
  --sort popularity

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始爬取小红书搜索结果
# 2024-01-01 12:00:05 - INFO - 二维码已生成，请扫码登录
# 2024-01-01 12:00:30 - INFO - 登录成功，开始搜索...
# 2024-01-01 12:00:35 - INFO - 找到关键词"护肤"相关内容 25 条
# 2024-01-01 12:00:40 - INFO - 找到关键词"美妆"相关内容 25 条
# 2024-01-01 12:01:00 - INFO - 爬取完成，共获取 50 条数据
```

**抖音创作者爬取**
```bash
# ⚠️ 无需sudo权限
python main.py \
  --platform dy \
  --lt cookie \
  --type creator \
  --keywords "创作者ID1,创作者ID2" \
  --count 30

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始爬取抖音创作者内容
# 2024-01-01 12:00:02 - INFO - 使用Cookie登录
# 2024-01-01 12:00:05 - INFO - 登录验证成功
# 2024-01-01 12:00:10 - INFO - 开始爬取创作者: 创作者ID1
# 2024-01-01 12:00:45 - INFO - 创作者ID1 爬取完成，获取 15 条视频
# 2024-01-01 12:01:20 - INFO - 创作者ID2 爬取完成，获取 15 条视频
```

**快手批量爬取**
```bash
# ⚠️ 无需sudo权限
python main.py \
  --platform ks \
  --lt phone \
  --type search \
  --keywords "科技,数码" \
  --count 100 \
  --headless \
  --delay 3

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始爬取快手搜索结果
# 2024-01-01 12:00:02 - INFO - 启用无头模式
# 2024-01-01 12:00:03 - INFO - 设置延迟: 3秒
# 2024-01-01 12:00:05 - INFO - 请输入手机号进行登录
# 2024-01-01 12:00:30 - INFO - 手机号登录成功
# 2024-01-01 12:02:00 - INFO - 爬取完成，共获取 100 条数据
```

### 3.2 常用功能指令

#### 📊 数据管理命令

**查看爬取数据**
```bash
# ⚠️ 无需sudo权限
# 查看最近爬取的数据
ls -la data/

# 预期输出示例：
# total 1024
# drwxr-xr-x  8 username  staff   256 Jan  1 12:00 .
# drwxr-xr-x 15 username  staff   480 Jan  1 12:00 ..
# drwxr-xr-x  3 username  staff    96 Jan  1 12:00 xhs
# drwxr-xr-x  3 username  staff    96 Jan  1 12:00 douyin
# drwxr-xr-x  3 username  staff    96 Jan  1 12:00 kuaishou
# -rw-r--r--  1 username  staff 12345 Jan  1 12:00 crawl_log.txt
```

**数据统计分析**
```bash
# ⚠️ 无需sudo权限
# 统计各平台数据量
find data/ -name "*.json" | wc -l

# 预期输出示例：
# 1250

# 查看具体平台数据
find data/xhs/ -name "*.json" | wc -l
# 预期输出示例：
# 450
```

**数据格式转换**
```bash
# ⚠️ 无需sudo权限
# 将JSON数据转换为CSV格式
python tools/data_converter.py --input data/xhs/ --output data/xhs_export.csv --format csv

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始转换数据格式
# 2024-01-01 12:00:05 - INFO - 读取JSON文件: 450个
# 2024-01-01 12:00:10 - INFO - 转换完成，输出文件: data/xhs_export.csv
# 2024-01-01 12:00:11 - INFO - 共转换 450 条记录
```

#### 🔧 配置管理命令

**查看当前配置**
```bash
# ⚠️ 无需sudo权限
python -c "
import config.base_config as config
print('当前配置:')
print(f'数据存储路径: {config.DATA_SAVE_PATH}')
print(f'日志级别: {config.LOG_LEVEL}')
print(f'浏览器类型: {config.BROWSER_TYPE}')
"

# 预期输出示例：
# 当前配置:
# 数据存储路径: ./data
# 日志级别: INFO
# 浏览器类型: chromium
```

**修改配置文件**
```bash
# ⚠️ 无需sudo权限
# 使用内置配置编辑器
python config_editor.py

# 预期输出示例：
# MediaCrawler 配置编辑器
# ========================
# 1. 基础配置
# 2. 平台配置
# 3. 数据库配置
# 4. 代理配置
# 请选择要编辑的配置类型 (1-4):
```

**重置配置到默认值**
```bash
# ⚠️ 无需sudo权限
python tools/reset_config.py --platform xhs

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 重置小红书配置到默认值
# 2024-01-01 12:00:01 - INFO - 备份当前配置到: config/backup/xhs_config_20240101.py
# 2024-01-01 12:00:02 - INFO - 配置重置完成
```

#### 🗄️ 数据库操作命令

**初始化数据库**
```bash
# ⚠️ 无需sudo权限
python database/init_db.py

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始初始化数据库
# 2024-01-01 12:00:01 - INFO - 创建数据库表: posts
# 2024-01-01 12:00:02 - INFO - 创建数据库表: users
# 2024-01-01 12:00:03 - INFO - 创建数据库表: comments
# 2024-01-01 12:00:04 - INFO - 数据库初始化完成
```

**数据库备份**
```bash
# ⚠️ 无需sudo权限
python database/backup_db.py --output backup/db_backup_$(date +%Y%m%d).sql

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始数据库备份
# 2024-01-01 12:00:30 - INFO - 备份完成: backup/db_backup_20240101.sql
# 2024-01-01 12:00:31 - INFO - 备份文件大小: 15.6 MB
```

**数据库清理**
```bash
# ⚠️ 无需sudo权限
python database/cleanup_db.py --days 30

# 预期输出示例：
# 2024-01-01 12:00:00 - INFO - 开始清理30天前的数据
# 2024-01-01 12:00:05 - INFO - 清理posts表: 删除 1250 条记录
# 2024-01-01 12:00:10 - INFO - 清理comments表: 删除 3750 条记录
# 2024-01-01 12:00:15 - INFO - 数据库清理完成
```

### 3.3 运行状态监控

#### 📈 实时监控命令

**查看运行状态**
```bash
# ⚠️ 无需sudo权限
# 查看Python进程
ps aux | grep python | grep -v grep

# 预期输出示例：
# username  12345   0.5  2.1  123456  67890 s001  S+   12:00PM   0:01.23 python gui_app.py
# username  12346   1.2  3.4  234567  89012 s002  S+   12:01PM   0:02.34 python main.py --platform xhs
```

**监控系统资源使用**
```bash
# ⚠️ 无需sudo权限
# 监控CPU和内存使用
top -pid $(pgrep -f "python.*main.py")

# 预期输出示例：
# PID    COMMAND      %CPU TIME     #TH   #WQ  #PORT MEM    PURG   CMPRS  PGRP
# 12346  python       15.2 00:05.67 8     0    25    234M   0B     0B     12346
```

**查看网络连接状态**
```bash
# ⚠️ 无需sudo权限
# 查看程序的网络连接
lsof -i -P | grep python

# 预期输出示例：
# python  12345 username   3u  IPv4 0x1234567890abcdef      0t0  TCP localhost:8080 (LISTEN)
# python  12346 username   4u  IPv4 0x1234567890abcdef      0t0  TCP *:443->api.xiaohongshu.com:443 (ESTABLISHED)
```

#### 📊 性能监控脚本

**创建监控脚本**
```bash
# ⚠️ 无需sudo权限
cat > monitor_crawler.sh << 'EOF'
#!/bin/bash

# MediaCrawler 性能监控脚本

echo "🔍 MediaCrawler 运行状态监控"
echo "================================"

# 检查进程状态
echo "📋 进程状态:"
PIDS=$(pgrep -f "python.*main.py\|python.*gui_app.py")
if [ -n "$PIDS" ]; then
    for PID in $PIDS; do
        PROCESS_INFO=$(ps -p $PID -o pid,ppid,%cpu,%mem,time,command --no-headers)
        echo "✅ PID: $PROCESS_INFO"
    done
else
    echo "❌ 未发现运行中的MediaCrawler进程"
fi

# 检查内存使用
echo -e "\n💾 内存使用情况:"
if [ -n "$PIDS" ]; then
    for PID in $PIDS; do
        MEMORY=$(ps -p $PID -o rss --no-headers)
        MEMORY_MB=$((MEMORY / 1024))
        echo "📊 PID $PID: ${MEMORY_MB}MB"
    done
fi

# 检查磁盘使用
echo -e "\n💿 数据目录磁盘使用:"
if [ -d "data" ]; then
    DATA_SIZE=$(du -sh data/ | cut -f1)
    echo "📁 data/ 目录大小: $DATA_SIZE"
else
    echo "❌ data/ 目录不存在"
fi

# 检查日志文件
echo -e "\n📝 最新日志:"
if [ -f "logs/crawler.log" ]; then
    echo "📄 最新10条日志:"
    tail -n 10 logs/crawler.log
else
    echo "❌ 日志文件不存在"
fi

# 检查网络连接
echo -e "\n🌐 网络连接状态:"
if [ -n "$PIDS" ]; then
    CONNECTIONS=$(lsof -i -P | grep python | wc -l)
    echo "🔗 活跃网络连接数: $CONNECTIONS"
fi

echo -e "\n✅ 监控完成 - $(date)"
EOF

# 赋予执行权限
chmod +x monitor_crawler.sh

# 运行监控脚本
./monitor_crawler.sh
```

**预期输出示例：**
```
🔍 MediaCrawler 运行状态监控
================================
📋 进程状态:
✅ PID: 12345     1  15.2  2.1 00:05:67 python gui_app.py
✅ PID: 12346     1   8.5  3.4 00:03:45 python main.py --platform xhs

💾 内存使用情况:
📊 PID 12345: 234MB
📊 PID 12346: 345MB

💿 数据目录磁盘使用:
📁 data/ 目录大小: 1.2G

📝 最新日志:
📄 最新10条日志:
2024-01-01 12:00:00,123 - INFO - 开始爬取小红书数据
2024-01-01 12:00:05,456 - INFO - 登录验证成功
2024-01-01 12:00:10,789 - INFO - 搜索关键词: 美食
2024-01-01 12:00:15,012 - INFO - 获取到 25 条搜索结果
2024-01-01 12:00:20,345 - INFO - 开始详情页爬取
2024-01-01 12:00:25,678 - INFO - 爬取进度: 10/25
2024-01-01 12:00:30,901 - INFO - 爬取进度: 20/25
2024-01-01 12:00:35,234 - INFO - 爬取完成
2024-01-01 12:00:40,567 - INFO - 数据保存到: data/xhs/20240101/
2024-01-01 12:00:45,890 - INFO - 本次爬取获取 25 条有效数据

🌐 网络连接状态:
🔗 活跃网络连接数: 5

✅ 监控完成 - Mon Jan  1 12:00:45 CST 2024
```

#### ⏰ 定时监控设置

**设置定时监控任务**
```bash
# ⚠️ 无需sudo权限
# 编辑crontab
crontab -e

# 添加以下内容（每5分钟执行一次监控）
# */5 * * * * cd ~/Projects/MediaCrawler && ./monitor_crawler.sh >> logs/monitor.log 2>&1

# 验证crontab设置
crontab -l

# 预期输出示例：
# */5 * * * * cd ~/Projects/MediaCrawler && ./monitor_crawler.sh >> logs/monitor.log 2>&1
```

**查看监控日志**
```bash
# ⚠️ 无需sudo权限
tail -f logs/monitor.log

# 预期输出示例：
# 🔍 MediaCrawler 运行状态监控
# ================================
# 📋 进程状态:
# ✅ PID: 12345     1  15.2  2.1 00:05:67 python gui_app.py
# ...
```

---

## 4. 故障处理部分

### 4.1 常见错误代码解决方案

#### 🚨 Python环境相关错误

**错误1：ModuleNotFoundError**
```bash
# 错误信息示例：
# ModuleNotFoundError: No module named 'playwright'

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 确认虚拟环境已激活
source .venv/bin/activate

# 2. 重新安装依赖
pip install -r requirements.txt

# 3. 验证模块安装
python -c "import playwright; print('✅ playwright 安装成功')"

# 预期输出：
# ✅ playwright 安装成功
```

**错误2：Permission Denied**
```bash
# 错误信息示例：
# PermissionError: [Errno 13] Permission denied: '/usr/local/lib/python3.11/site-packages'

# 解决方案：
# ⚠️ 无需sudo权限 - 使用虚拟环境
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 预期输出：
# Successfully installed playwright-1.40.0 ...
```

**错误3：Python版本不兼容**
```bash
# 错误信息示例：
# SyntaxError: invalid syntax (match statement requires Python 3.10+)

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 检查Python版本
python --version

# 2. 安装正确版本
brew install python@3.11

# 3. 重新创建虚拟环境
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate

# 预期输出：
# Python 3.11.0
```

#### 🌐 网络连接相关错误

**错误4：网络超时**
```bash
# 错误信息示例：
# TimeoutError: Navigation timeout of 30000ms exceeded

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 检查网络连接
ping -c 3 www.xiaohongshu.com

# 2. 增加超时时间
python main.py --platform xhs --timeout 60

# 3. 使用代理（如需要）
python main.py --platform xhs --proxy "http://127.0.0.1:7890"

# 预期输出：
# PING www.xiaohongshu.com: 56 data bytes
# 64 bytes from xxx.xxx.xxx.xxx: icmp_seq=0 time=45.123 ms
```

**错误5：SSL证书错误**
```bash
# 错误信息示例：
# SSL: CERTIFICATE_VERIFY_FAILED

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 更新证书
/Applications/Python\ 3.11/Install\ Certificates.command

# 2. 或者在代码中忽略SSL验证（仅用于测试）
export PYTHONHTTPSVERIFY=0

# 预期输出：
# -- pip install --upgrade certifi
# Requirement already satisfied: certifi in ...
```

#### 🎭 浏览器相关错误

**错误6：浏览器启动失败**
```bash
# 错误信息示例：
# playwright._impl._api_types.Error: Executable doesn't exist

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 重新安装浏览器
playwright install

# 2. 检查浏览器安装
playwright install --dry-run

# 3. 清理并重新安装
rm -rf ~/.cache/ms-playwright
playwright install

# 预期输出：
# Downloading Chromium 109.0.5414.74 ...
# Chromium 109.0.5414.74 downloaded to ~/.cache/ms-playwright/chromium-1045
```

**错误7：浏览器权限问题**
```bash
# 错误信息示例：
# Error: Failed to launch browser: spawn EACCES

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 修复浏览器权限
find ~/.cache/ms-playwright -name "chrome*" -exec chmod +x {} \;

# 2. 重新安装浏览器
playwright install chromium

# 预期输出：
# Chromium 109.0.5414.74 is already installed
```

#### 🗄️ 数据库相关错误

**错误8：数据库连接失败**
```bash
# 错误信息示例：
# sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server")

# 解决方案：
# ⚠️ 无需sudo权限
# 1. 检查MySQL服务状态
brew services list | grep mysql

# 2. 启动MySQL服务
brew services start mysql

# 3. 测试连接
mysql -u root -p -e "SELECT 1;"

# 预期输出：
# mysql      started username ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
```

**错误9：数据库权限错误**
```bash
# 错误信息示例：
# Access denied for user 'root'@'localhost'

# 解决方案：
# ⚠️ 需要交互式操作
# 1. 重置MySQL密码
mysql_secure_installation

# 2. 创建新用户
mysql -u root -p -e "
CREATE USER 'mediacrawler'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mediacrawler.* TO 'mediacrawler'@'localhost';
FLUSH PRIVILEGES;
"

# 预期输出：
# Query OK, 0 rows affected (0.01 sec)
```

### 4.2 日志查看方法

#### 📝 日志文件位置

**系统日志结构**
```bash
# ⚠️ 无需sudo权限
# 查看日志目录结构
tree logs/ 2>/dev/null || find logs/ -type f

# 预期输出示例：
# logs/
# ├── crawler.log          # 主要爬虫日志
# ├── error.log           # 错误日志
# ├── debug.log           # 调试日志
# ├── network.log         # 网络请求日志
# └── performance.log     # 性能监控日志
```

**实时查看日志**
```bash
# ⚠️ 无需sudo权限
# 实时查看主日志
tail -f logs/crawler.log

# 实时查看错误日志
tail -f logs/error.log

# 查看最近100行日志
tail -n 100 logs/crawler.log

# 预期输出示例：
# 2024-01-01 12:00:00,123 - INFO - 开始爬取任务
# 2024-01-01 12:00:01,456 - INFO - 登录验证成功
# 2024-01-01 12:00:02,789 - WARNING - 请求频率过快，等待2秒
# 2024-01-01 12:00:05,012 - INFO - 获取数据成功
```

#### 🔍 日志分析工具

**创建日志分析脚本**
```bash
# ⚠️ 无需sudo权限
cat > analyze_logs.sh << 'EOF'
#!/bin/bash

# MediaCrawler 日志分析脚本

LOG_FILE=${1:-"logs/crawler.log"}

if [ ! -f "$LOG_FILE" ]; then
    echo "❌ 日志文件不存在: $LOG_FILE"
    exit 1
fi

echo "📊 日志分析报告 - $(basename $LOG_FILE)"
echo "================================"

# 统计日志级别
echo "📋 日志级别统计:"
echo "INFO:    $(grep -c "INFO" $LOG_FILE)"
echo "WARNING: $(grep -c "WARNING" $LOG_FILE)"
echo "ERROR:   $(grep -c "ERROR" $LOG_FILE)"
echo "DEBUG:   $(grep -c "DEBUG" $LOG_FILE)"

# 最近的错误
echo -e "\n🚨 最近10个错误:"
grep "ERROR" $LOG_FILE | tail -n 10

# 最频繁的警告
echo -e "\n⚠️  最频繁的警告:"
grep "WARNING" $LOG_FILE | cut -d'-' -f4- | sort | uniq -c | sort -nr | head -5

# 性能统计
echo -e "\n⏱️  性能相关:"
grep -E "(耗时|timeout|slow)" $LOG_FILE | tail -n 5

echo -e "\n✅ 分析完成"
EOF

chmod +x analyze_logs.sh

# 使用示例
./analyze_logs.sh logs/crawler.log
```

**预期输出示例：**
```
📊 日志分析报告 - crawler.log
================================
📋 日志级别统计:
INFO:    1250
WARNING: 45
ERROR:   8
DEBUG:   234

🚨 最近10个错误:
2024-01-01 12:00:00,123 - ERROR - 网络请求失败: Connection timeout
2024-01-01 12:05:30,456 - ERROR - 解析数据失败: Invalid JSON format
2024-01-01 12:10:15,789 - ERROR - 保存文件失败: Permission denied

⚠️  最频繁的警告:
   15  请求频率过快，等待中
    8  Cookie即将过期
    5  内存使用率较高
    3  磁盘空间不足
    2  网络连接不稳定

⏱️  性能相关:
2024-01-01 12:00:00 - INFO - 页面加载耗时: 2.34秒
2024-01-01 12:05:00 - WARNING - 请求响应较慢: 5.67秒

✅ 分析完成
```

#### 📈 日志监控设置

**设置日志轮转**
```bash
# ⚠️ 无需sudo权限
# 创建logrotate配置
cat > logrotate.conf << 'EOF'
logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 username staff
}
EOF

# 手动执行日志轮转
logrotate -f logrotate.conf

# 预期输出：
# 日志文件已轮转并压缩
```

### 4.3 环境检查脚本

#### 🔧 综合环境检查

**创建完整的环境检查脚本**
```bash
# ⚠️ 无需sudo权限
cat > full_environment_check.py << 'EOF'
#!/usr/bin/env python3
"""
MediaCrawler 完整环境检查脚本
"""
import sys
import os
import subprocess
import json
from pathlib import Path
import importlib.util

class EnvironmentChecker:
    def __init__(self):
        self.results = {}
        self.issues = []
        
    def check_system_info(self):
        """检查系统信息"""
        print("🖥️  系统信息检查:")
        try:
            # macOS版本
            result = subprocess.run(['sw_vers'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ macOS版本信息:")
                for line in result.stdout.strip().split('\n'):
                    print(f"   {line}")
                self.results['system'] = True
            else:
                print("❌ 无法获取系统版本信息")
                self.results['system'] = False
                self.issues.append("系统版本信息获取失败")
        except Exception as e:
            print(f"❌ 系统检查失败: {e}")
            self.results['system'] = False
            self.issues.append(f"系统检查异常: {e}")
    
    def check_python_environment(self):
        """检查Python环境"""
        print("\n🐍 Python环境检查:")
        
        # Python版本
        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
        if version.major == 3 and version.minor >= 11:
            print("✅ Python版本符合要求")
            self.results['python_version'] = True
        else:
            print("❌ Python版本过低，需要3.11+")
            self.results['python_version'] = False
            self.issues.append("Python版本不符合要求")
        
        # 虚拟环境
        venv_path = os.environ.get('VIRTUAL_ENV')
        if venv_path:
            print(f"✅ 虚拟环境: {venv_path}")
            self.results['virtual_env'] = True
        else:
            print("❌ 虚拟环境未激活")
            self.results['virtual_env'] = False
            self.issues.append("虚拟环境未激活")
    
    def check_dependencies(self):
        """检查依赖包"""
        print("\n📦 依赖包检查:")
        
        required_packages = [
            'playwright', 'asyncio', 'aiofiles', 'httpx', 
            'fake_useragent', 'pymysql', 'redis', 'pandas'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                spec = importlib.util.find_spec(package)
                if spec is not None:
                    print(f"✅ {package}")
                else:
                    print(f"❌ {package} 未安装")
                    missing_packages.append(package)
            except ImportError:
                print(f"❌ {package} 导入失败")
                missing_packages.append(package)
        
        if not missing_packages:
            self.results['dependencies'] = True
        else:
            self.results['dependencies'] = False
            self.issues.extend([f"缺少依赖包: {pkg}" for pkg in missing_packages])
    
    def check_project_structure(self):
        """检查项目结构"""
        print("\n📁 项目结构检查:")
        
        required_dirs = [
            'media_platform', 'config', 'tools', 'cache', 
            'database', 'logs', 'data'
        ]
        
        required_files = [
            'main.py', 'gui_app.py', 'requirements.txt',
            'config/base_config.py'
        ]
        
        missing_items = []
        
        # 检查目录
        for directory in required_dirs:
            if Path(directory).exists():
                print(f"✅ {directory}/")
            else:
                print(f"❌ {directory}/ 不存在")
                missing_items.append(f"目录: {directory}")
        
        # 检查文件
        for file_path in required_files:
            if Path(file_path).exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path} 不存在")
                missing_items.append(f"文件: {file_path}")
        
        if not missing_items:
            self.results['project_structure'] = True
        else:
            self.results['project_structure'] = False
            self.issues.extend([f"缺少{item}" for item in missing_items])
    
    def check_services(self):
        """检查外部服务"""
        print("\n🔧 外部服务检查:")
        
        # 检查MySQL
        try:
            result = subprocess.run(['brew', 'services', 'list'], 
                                  capture_output=True, text=True)
            if 'mysql' in result.stdout and 'started' in result.stdout:
                print("✅ MySQL服务运行中")
                self.results['mysql'] = True
            else:
                print("⚠️  MySQL服务未启动")
                self.results['mysql'] = False
                self.issues.append("MySQL服务未启动")
        except Exception as e:
            print(f"❌ MySQL检查失败: {e}")
            self.results['mysql'] = False
            self.issues.append(f"MySQL检查异常: {e}")
        
        # 检查Redis
        try:
            result = subprocess.run(['redis-cli', 'ping'], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and 'PONG' in result.stdout:
                print("✅ Redis服务运行中")
                self.results['redis'] = True
            else:
                print("⚠️  Redis服务未启动")
                self.results['redis'] = False
                self.issues.append("Redis服务未启动")
        except Exception as e:
            print(f"❌ Redis检查失败: {e}")
            self.results['redis'] = False
            self.issues.append(f"Redis检查异常: {e}")
    
    def check_browser_setup(self):
        """检查浏览器设置"""
        print("\n🌐 浏览器环境检查:")
        
        # 检查Playwright浏览器
        try:
            result = subprocess.run(['playwright', 'install', '--dry-run'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Playwright浏览器已安装")
                self.results['playwright_browsers'] = True
            else:
                print("❌ Playwright浏览器未安装")
                self.results['playwright_browsers'] = False
                self.issues.append("Playwright浏览器未安装")
        except Exception as e:
            print(f"❌ 浏览器检查失败: {e}")
            self.results['playwright_browsers'] = False
            self.issues.append(f"浏览器检查异常: {e}")
    
    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*50)
        print("📋 环境检查报告")
        print("="*50)
        
        total_checks = len(self.results)
        passed_checks = sum(1 for result in self.results.values() if result)
        
        print(f"总检查项: {total_checks}")
        print(f"通过检查: {passed_checks}")
        print(f"失败检查: {total_checks - passed_checks}")
        print(f"通过率: {passed_checks/total_checks*100:.1f}%")
        
        if self.issues:
            print("\n🚨 发现的问题:")
            for i, issue in enumerate(self.issues, 1):
                print(f"{i}. {issue}")
            
            print("\n💡 建议解决方案:")
            self.suggest_solutions()
        else:
            print("\n🎉 所有检查通过！环境配置完美。")
        
        # 保存报告到文件
        report_data = {
            'timestamp': subprocess.run(['date'], capture_output=True, text=True).stdout.strip(),
            'results': self.results,
            'issues': self.issues,
            'pass_rate': passed_checks/total_checks*100
        }
        
        with open('environment_check_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 详细报告已保存到: environment_check_report.json")
    
    def suggest_solutions(self):
        """提供解决方案建议"""
        solutions = {
            "Python版本不符合要求": "运行: brew install python@3.11",
            "虚拟环境未激活": "运行: source .venv/bin/activate",
            "缺少依赖包": "运行: pip install -r requirements.txt",
            "MySQL服务未启动": "运行: brew services start mysql",
            "Redis服务未启动": "运行: brew services start redis",
            "Playwright浏览器未安装": "运行: playwright install"
        }
        
        for issue in self.issues:
            for problem, solution in solutions.items():
                if problem in issue:
                    print(f"• {issue} -> {solution}")
                    break
    
    def run_all_checks(self):
        """运行所有检查"""
        print("🔍 开始完整环境检查...")
        print("="*50)
        
        self.check_system_info()
        self.check_python_environment()
        self.check_dependencies()
        self.check_project_structure()
        self.check_services()
        self.check_browser_setup()
        self.generate_report()

if __name__ == "__main__":
    checker = EnvironmentChecker()
    checker.run_all_checks()
EOF

# 运行完整环境检查
python full_environment_check.py
```

**预期输出示例：**
```
🔍 开始完整环境检查...
==================================================
🖥️  系统信息检查:
✅ macOS版本信息:
   ProductName:    macOS
   ProductVersion: 13.0
   BuildVersion:   22A380

🐍 Python环境检查:
Python版本: 3.11.0
✅ Python版本符合要求
✅ 虚拟环境: /Users/username/Projects/MediaCrawler/.venv

📦 依赖包检查:
✅ playwright
✅ asyncio
✅ aiofiles
✅ httpx
✅ fake_useragent
✅ pymysql
✅ redis
✅ pandas

📁 项目结构检查:
✅ media_platform/
✅ config/
✅ tools/
✅ cache/
✅ database/
✅ logs/
✅ data/
✅ main.py
✅ gui_app.py
✅ requirements.txt
✅ config/base_config.py

🔧 外部服务检查:
✅ MySQL服务运行中
✅ Redis服务运行中

🌐 浏览器环境检查:
✅ Playwright浏览器已安装

==================================================
📋 环境检查报告
==================================================
总检查项: 6
通过检查: 6
失败检查: 0
通过率: 100.0%

🎉 所有检查通过！环境配置完美。

📄 详细报告已保存到: environment_check_report.json
```

---

## 5. 安全警告与最佳实践

### 🔒 系统安全警告

#### ⚠️ 重要安全提醒

**1. sudo权限使用原则**
```bash
# ❌ 错误做法 - 避免不必要的sudo使用
sudo pip install package_name

# ✅ 正确做法 - 使用虚拟环境
source .venv/bin/activate
pip install package_name

# 🚨 警告：只有在以下情况才使用sudo：
# - 安装系统级软件包（如Homebrew、Xcode工具）
# - 修改系统配置文件
# - 安装需要系统权限的服务
```

**2. 网络安全注意事项**
```bash
# ⚠️ 代理配置安全
# 确保代理服务器可信
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890

# ⚠️ SSL证书验证
# 仅在测试环境中禁用SSL验证
export PYTHONHTTPSVERIFY=0  # 仅用于测试！

# ✅ 生产环境应始终验证SSL证书
unset PYTHONHTTPSVERIFY
```

**3. 数据安全保护**
```bash
# ⚠️ 敏感信息保护
# 永远不要在代码中硬编码密码
# 使用环境变量存储敏感信息

# ✅ 正确的密码管理
echo 'export MYSQL_PASSWORD="your_secure_password"' >> ~/.zshrc
echo 'export REDIS_PASSWORD="your_redis_password"' >> ~/.zshrc
source ~/.zshrc

# 🚨 警告：定期更换密码，使用强密码策略
```

### 🛡️ 最佳实践建议

#### 📋 开发环境最佳实践

**1. 虚拟环境管理**
```bash
# ✅ 为每个项目创建独立的虚拟环境
python3.11 -m venv .venv

# ✅ 始终激活虚拟环境后再工作
source .venv/bin/activate

# ✅ 定期更新pip和依赖包
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# ✅ 导出依赖包版本
pip freeze > requirements.txt
```

**2. 代码版本控制**
```bash
# ✅ 使用Git进行版本控制
git init
git add .
git commit -m "Initial commit"

# ✅ 创建.gitignore文件
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
.venv/

# 敏感信息
.env
config/secrets.py
*.log

# 系统文件
.DS_Store
Thumbs.db

# 数据文件
data/
cache/
*.db
EOF

# ✅ 定期备份重要数据
git push origin main
```

**3. 性能优化建议**
```bash
# ✅ 监控系统资源使用
# 创建性能监控脚本
cat > monitor_performance.sh << 'EOF'
#!/bin/bash

echo "📊 系统性能监控 - $(date)"
echo "================================"

# CPU使用率
echo "💻 CPU使用率:"
top -l 1 | grep "CPU usage"

# 内存使用情况
echo -e "\n🧠 内存使用情况:"
vm_stat | head -5

# 磁盘使用情况
echo -e "\n💾 磁盘使用情况:"
df -h | head -5

# 网络连接状态
echo -e "\n🌐 网络连接状态:"
netstat -an | grep LISTEN | wc -l | xargs echo "监听端口数量:"

# Python进程监控
echo -e "\n🐍 Python进程:"
ps aux | grep python | grep -v grep | wc -l | xargs echo "Python进程数量:"

echo -e "\n✅ 监控完成"
EOF

chmod +x monitor_performance.sh
./monitor_performance.sh
```

#### 🔧 运维最佳实践

**1. 日志管理策略**
```bash
# ✅ 设置日志轮转
cat > setup_log_rotation.sh << 'EOF'
#!/bin/bash

# 创建日志轮转配置
mkdir -p logs/archive

# 设置日志轮转脚本
cat > rotate_logs.sh << 'INNER_EOF'
#!/bin/bash

LOG_DIR="logs"
ARCHIVE_DIR="logs/archive"
MAX_SIZE="100M"

for log_file in $LOG_DIR/*.log; do
    if [ -f "$log_file" ]; then
        file_size=$(stat -f%z "$log_file" 2>/dev/null || echo 0)
        max_size_bytes=$((100 * 1024 * 1024))  # 100MB
        
        if [ $file_size -gt $max_size_bytes ]; then
            timestamp=$(date +"%Y%m%d_%H%M%S")
            base_name=$(basename "$log_file" .log)
            
            # 压缩并归档
            gzip -c "$log_file" > "$ARCHIVE_DIR/${base_name}_${timestamp}.log.gz"
            
            # 清空原日志文件
            > "$log_file"
            
            echo "✅ 已轮转日志: $log_file"
        fi
    fi
done
INNER_EOF

chmod +x rotate_logs.sh
echo "✅ 日志轮转脚本已创建"
EOF

chmod +x setup_log_rotation.sh
./setup_log_rotation.sh
```

**2. 数据备份策略**
```bash
# ✅ 创建自动备份脚本
cat > backup_data.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="backups"
DATE=$(date +"%Y%m%d_%H%M%S")

mkdir -p $BACKUP_DIR

echo "🔄 开始数据备份 - $DATE"

# 备份配置文件
echo "📁 备份配置文件..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" config/

# 备份数据库（如果使用SQLite）
if [ -f "database/mediacrawler.db" ]; then
    echo "🗄️ 备份数据库..."
    cp "database/mediacrawler.db" "$BACKUP_DIR/database_$DATE.db"
fi

# 备份重要数据
if [ -d "data" ]; then
    echo "📊 备份数据文件..."
    tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" data/
fi

# 清理旧备份（保留最近7天）
echo "🧹 清理旧备份..."
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.db" -mtime +7 -delete

echo "✅ 备份完成"
EOF

chmod +x backup_data.sh

# 设置定时备份（可选）
echo "⏰ 设置定时备份任务:"
echo "# 每天凌晨2点执行备份"
echo "0 2 * * * cd $(pwd) && ./backup_data.sh >> logs/backup.log 2>&1"
```

#### 🚀 性能调优建议

**1. 爬虫性能优化**
```bash
# ✅ 创建性能调优配置
cat > performance_tuning.py << 'EOF'
#!/usr/bin/env python3
"""
MediaCrawler 性能调优建议
"""

# 推荐的性能配置
PERFORMANCE_CONFIG = {
    # 并发设置
    "max_concurrent_tasks": 5,  # 根据系统性能调整
    "request_delay": 1.0,       # 请求间隔（秒）
    "timeout": 30,              # 请求超时时间
    
    # 内存管理
    "max_memory_usage": "1GB",  # 最大内存使用
    "cache_size": 1000,         # 缓存大小
    
    # 网络优化
    "connection_pool_size": 10, # 连接池大小
    "retry_attempts": 3,        # 重试次数
    
    # 数据库优化
    "batch_size": 100,          # 批量插入大小
    "connection_timeout": 30,   # 数据库连接超时
}

def apply_performance_settings():
    """应用性能设置"""
    print("🚀 应用性能优化设置...")
    
    # 设置环境变量
    import os
    os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '~/.cache/ms-playwright'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # 优化Python垃圾回收
    import gc
    gc.set_threshold(700, 10, 10)
    
    print("✅ 性能设置已应用")

if __name__ == "__main__":
    apply_performance_settings()
EOF

python performance_tuning.py
```

### 📚 快速参考指南

#### 🔗 常用命令速查

```bash
# 🚀 快速启动
source .venv/bin/activate && python gui_app.py

# 📊 状态检查
python full_environment_check.py

# 📝 查看日志
tail -f logs/crawler.log

# 🔄 重启服务
brew services restart mysql redis

# 🧹 清理缓存
rm -rf cache/* && rm -rf __pycache__

# 📦 更新依赖
pip install --upgrade -r requirements.txt

# 🔍 性能监控
./monitor_performance.sh

# 💾 数据备份
./backup_data.sh
```

#### 📞 技术支持

**遇到问题时的处理流程：**

1. **🔍 首先检查日志**
   ```bash
   tail -n 50 logs/error.log
   ```

2. **🔧 运行环境检查**
   ```bash
   python full_environment_check.py
   ```

3. **📊 分析系统状态**
   ```bash
   ./monitor_performance.sh
   ```

4. **🔄 尝试重启相关服务**
   ```bash
   brew services restart mysql redis
   ```

5. **📚 查阅本手册相关章节**
   - 安装配置问题 → 第1章
   - 部署相关问题 → 第2章
   - 运行时问题 → 第3章
   - 错误排查 → 第4章

---

## 📋 总结

本手册详细介绍了MediaCrawler项目在macOS系统上的完整部署和使用流程，涵盖了从环境准备到故障排查的所有关键环节。

### ✅ 手册要点回顾

1. **🔧 环境配置**：系统要求、依赖安装、环境验证
2. **🚀 项目部署**：代码获取、环境配置、依赖安装
3. **💻 操作使用**：启动命令、功能使用、状态监控
4. **🛠️ 故障处理**：错误解决、日志分析、环境检查
5. **🔒 安全实践**：权限管理、数据保护、性能优化

### 🎯 成功部署检查清单

- [ ] ✅ macOS系统版本兼容（10.15+）
- [ ] ✅ Python 3.11+ 已安装
- [ ] ✅ 虚拟环境已创建并激活
- [ ] ✅ 所有依赖包已安装
- [ ] ✅ Playwright浏览器已安装
- [ ] ✅ MySQL/Redis服务已启动（可选）
- [ ] ✅ 环境检查脚本通过
- [ ] ✅ GUI界面可正常启动
- [ ] ✅ 命令行模式可正常运行

### 🚀 开始使用

完成所有配置后，您可以通过以下命令启动项目：

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动GUI界面
python gui_app.py

# 或使用命令行模式
python main.py --platform xhs --keywords "美食"
```

**祝您使用愉快！** 🎉

---

*MediaCrawler macOS终端使用手册 v1.0*  
*最后更新：2024年1月*