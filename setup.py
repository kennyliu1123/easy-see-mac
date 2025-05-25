from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.py', 'state_init.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['streamlit', 'pandas', 'chardet'],
    'packages': ['streamlit', 'pandas', 'chardet'],
    'resources': DATA_FILES,  # 指定需打包进去的文件
}

setup(
    app=APP,
    data_files=[],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
