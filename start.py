#!/usr/bin/env python3
"""
游戏项目启动脚本
自动启动后端和前端服务器
"""
import subprocess
import sys
import os
import time
import platform


def is_windows():
    """判断是否为Windows系统"""
    return platform.system() == 'Windows'


def start_backend():
    """启动后端服务器"""
    print("启动后端服务器...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')

    if is_windows():
        # Windows系统使用start命令在新窗口启动
        cmd = f'start cmd /k "cd /d {backend_dir} && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"'
        subprocess.Popen(cmd, shell=True)
    else:
        # Linux/Mac系统使用后台进程
        cmd = ['python', '-m', 'uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000']
        subprocess.Popen(cmd, cwd=backend_dir)

    print("后端服务器启动中...")


def start_frontend():
    """启动前端服务器"""
    print("启动前端服务器...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')

    if is_windows():
        # Windows系统使用start命令在新窗口启动
        cmd = f'start cmd /k "cd /d {frontend_dir} && npm run dev"'
        subprocess.Popen(cmd, shell=True)
    else:
        # Linux/Mac系统使用后台进程
        cmd = ['npm', 'run', 'dev']
        subprocess.Popen(cmd, cwd=frontend_dir)

    print("前端服务器启动中...")


def main():
    """主函数"""
    print("=" * 50)
    print("游戏服务器启动脚本")
    print("=" * 50)

    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)

    # 启动后端
    start_backend()

    # 等待后端启动
    print("\n等待后端启动...")
    time.sleep(3)

    # 启动前端
    start_frontend()

    # 显示访问信息
    print("\n" + "=" * 50)
    print("游戏服务器正在启动...")
    print("后端地址: http://localhost:8000")
    print("前端地址: http://localhost:5173")
    print("API文档: http://localhost:8000/docs")
    print("=" * 50)
    print("\n提示: 请保持此窗口打开")

    if not is_windows():
        print("\n按 Ctrl+C 停止所有服务")
        try:
            # 在非Windows系统上保持脚本运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n正在停止服务器...")
            sys.exit(0)


if __name__ == '__main__':
    main()
