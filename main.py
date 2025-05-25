import os
import subprocess
import sys

def resource_path(filename):
    base = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base, filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    
    # Start Streamlit using subprocess and capture output
    result = subprocess.run([
        sys.executable,  # Use the current Python interpreter
        "-m", "streamlit", "run", app_file,
        "--server.headless=true",  # Run without opening a browser
        "--server.port=5000",  # Set the desired port
        "--browser.serverAddress=localhost"
    ], capture_output=True, text=True)
    
    # Print stdout and stderr to help debug
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    
    # Check if process was successful
    if result.returncode != 0:
        print(f"Error occurred while starting Streamlit: {result.returncode}")
