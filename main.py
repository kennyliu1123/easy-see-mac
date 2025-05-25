import os
import streamlit.web.bootstrap

def resource_path(filename):
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, filename)

if __name__ == "__main__":
    app_path = resource_path("app.py")
    streamlit.web.bootstrap.run(app_path, f"streamlit run {app_path}", [])
