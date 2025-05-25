from setuptools import setup

APP = ['main.py']
DATA_FILES = [('resources', ['app.py', 'state_init.py'])]  # 指定资源文件目录
OPTIONS = {
    'argv_emulation': True,
    'includes': ['streamlit', 'pandas', 'chardet'],
    'packages': ['streamlit', 'pandas', 'chardet'],
    'resources': ['resources']  # 显式打包资源
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
