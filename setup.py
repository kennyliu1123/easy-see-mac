from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.py', 'state_init.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['streamlit'],
    'packages': ['pandas', 'chardet'],
    'excludes': ['tkinter', 'unittest', 'email', 'html'],
    'resources': DATA_FILES,
    'optimize': 1
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
