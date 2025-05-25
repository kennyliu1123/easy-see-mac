from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.py', 'state_init.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['streamlit', 'pandas', 'chardet'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
