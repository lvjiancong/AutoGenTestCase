# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [("D:/Python311/Lib/site-packages/streamlit/runtime","./streamlit/runtime")]
datas += collect_data_files("streamlit")
datas += collect_data_files("autogen_agentchat")
datas += collect_data_files("autogen_ext")
datas += collect_data_files("autogen_core")
datas += copy_metadata("streamlit")
datas += copy_metadata("autogen_agentchat")
datas += copy_metadata("autogen_ext")
datas += copy_metadata("autogen_core")

block_cipher = None

a = Analysis(
    [
        'run.py',
        'D:\\Python311\\Lib\\site-packages\\streamlit\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_agentchat\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_agentchat\\conditions\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_agentchat\\teams\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_agentchat\\agents\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_ext\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_ext\\models\\openai\\__init__.py',
        'D:\\Python311\\Lib\\site-packages\\autogen_core\\__init__.py'
    ],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=
    [
        'autogen_agentchat',
        'autogen_agentchat.conditions',
        'autogen_agentchat.teams',
        'autogen_agentchat.agents',
        'autogen_ext',
        'autogen_ext.models.openai',
        'autogen_core'
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\IMRMToolsLibrary\\deepseek\\img\\favicon.ico'],
)
