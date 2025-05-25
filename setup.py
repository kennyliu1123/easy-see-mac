from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.py', 'state_init.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['streamlit'],
    'excludes': ['tkinter', 'email', 'unittest', 'pydevd'],
    'packages': ['pandas', 'chardet'],
    'resources': ['app.py', 'state_init.py']
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
