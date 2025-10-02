# -*- coding: utf-8 -*-
"""
配置编辑器独立测试脚本
用于在不依赖包结构的情况下测试配置编辑器功能
"""

import sys
import os
import tkinter as tk

# 添加父目录到路径，以便导入配置编辑器
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_editor import ConfigEditor

def test_config_editor():
    """测试配置编辑器功能"""
    print("开始测试配置编辑器...")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("配置编辑器独立测试")
    root.geometry("800x600")
    
    # 创建配置编辑器实例
    config_editor = ConfigEditor(root)
    
    # 创建测试按钮
    test_frame = tk.Frame(root)
    test_frame.pack(pady=20)
    
    # 打开配置编辑器按钮
    open_btn = tk.Button(
        test_frame, 
        text="打开配置编辑器", 
        command=config_editor.open_config_editor,
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10
    )
    open_btn.pack(pady=10)
    
    # 检查配置文件按钮
    def check_config_files():
        config_dir = os.path.join(os.getcwd(), "config")
        if os.path.exists(config_dir):
            files = [f for f in os.listdir(config_dir) if f.endswith('.py')]
            print(f"找到配置文件: {files}")
            tk.messagebox.showinfo("配置文件检查", f"找到 {len(files)} 个配置文件:\n" + "\n".join(files))
        else:
            print("配置目录不存在")
            tk.messagebox.showerror("错误", "配置目录不存在")
    
    check_btn = tk.Button(
        test_frame,
        text="检查配置文件",
        command=check_config_files,
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        padx=20,
        pady=10
    )
    check_btn.pack(pady=10)
    
    # 退出按钮
    quit_btn = tk.Button(
        test_frame,
        text="退出测试",
        command=root.quit,
        font=("Arial", 12),
        bg="#f44336",
        fg="white",
        padx=20,
        pady=10
    )
    quit_btn.pack(pady=10)
    
    # 状态标签
    status_label = tk.Label(
        root,
        text="配置编辑器独立测试就绪",
        font=("Arial", 10),
        fg="green"
    )
    status_label.pack(side=tk.BOTTOM, pady=10)
    
    print("配置编辑器测试界面已创建")
    print("请点击'打开配置编辑器'按钮测试功能")
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    test_config_editor()