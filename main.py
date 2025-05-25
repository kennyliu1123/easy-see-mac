import subprocess
import os
import sys

def resource_path(filename):
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, "resources", filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    subprocess.Popen(["/usr/local/bin/python3", "-m", "streamlit", "run", app_file])
