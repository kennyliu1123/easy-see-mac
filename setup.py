from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.py', 'state_init.py']

OPTIONS = {
    'argv_emulation': True,
    'packages': ['streamlit', 'pandas', 'chardet'],
    'includes': ['streamlit'],
    'plist': {
        'CFBundleName': 'EasySee',
        'CFBundleIdentifier': 'com.kennyliu.easysee',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
