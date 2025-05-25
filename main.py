import os
import subprocess
import sys
import time

def resource_path(filename):
    """获取打包后资源的路径，支持 PyInstaller 打包后资源路径"""
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    
    print(f"Starting Streamlit from {app_file}...")

    # 启动 Streamlit 服务，设置超时机制
    try:
        # 启动 Streamlit 命令
        result = subprocess.run([
            sys.executable,  # 使用当前 Python 解释器
            "-m", "streamlit", "run", app_file,
            "--server.headless=true",  # 不自动打开浏览器
            "--server.port=8502",  # 设置端口为 8502
            "--browser.serverAddress=localhost"  # 限制为 localhost 访问
        ], capture_output=True, text=True, timeout=60)  # 设置 60 秒超时
        
        # 打印调试输出
        print("Streamlit started:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"Error occurred while starting Streamlit: {result.returncode}")
    
    except subprocess.TimeoutExpired:
        print("Streamlit did not start within the expected time frame (60 seconds).")
    
    except Exception as e:
        print(f"An error occurred: {e}")
