import os
import sys
import streamlit.web.bootstrap

def resource_path(filename):
    # 如果使用 PyInstaller 打包，_MEIPASS 是临时目录
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    streamlit.web.bootstrap.run(
        app_file,
        f"run.py {app_file}",
        [],
        flag_options={}
    )
