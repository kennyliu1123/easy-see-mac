import os
import sys
import streamlit.web.bootstrap

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

if __name__ == "__main__":
    app_file = resource_path("app.py")
    streamlit.web.bootstrap.run(
        app_file,
        f"streamlit run {app_file}",
        [],
        {}  # flag_options，如有需要可加 e.g. {"server.headless": True}
    )
