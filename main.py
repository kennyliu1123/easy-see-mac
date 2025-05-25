import os
import subprocess
import sys

def resource_path(filename):
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    subprocess.run([
        sys.executable,
        "-m", "streamlit", "run", app_file,
        "--server.headless=true",
        "--server.port=3000",
        "--browser.serverAddress=localhost"
    ])
