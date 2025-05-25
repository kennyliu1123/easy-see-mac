import subprocess
import os
import sys

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_file])
