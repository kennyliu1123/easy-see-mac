import os
import subprocess
import sys
import pathlib

def resource_path(filename):
    base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    streamlit_path = resource_path("venv/bin/streamlit")
    subprocess.Popen([streamlit_path, "run", app_file])
