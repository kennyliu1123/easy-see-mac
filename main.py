import os
import sys
import subprocess

def resource_path(relative_path):
    """正确获取打包后资源路径（支持 .app 包）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    app_path = resource_path("app.py")
    # 使用完整路径运行 streamlit
    subprocess.run(["streamlit", "run", app_path])
