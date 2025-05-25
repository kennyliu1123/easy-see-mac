import os
import subprocess

def resource_path(filename):
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    subprocess.Popen(["/usr/bin/env", "streamlit", "run", app_file])
