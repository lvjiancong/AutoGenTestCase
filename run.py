#!/usr/bin/python
# -*- coding: utf-8 -*-
import streamlit.web.cli as stcli
import os, sys


def resolve_path(path):
    # 检测是否在PyInstaller打包环境中
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # 在打包环境中，使用_MEIPASS目录
        resolved_path = os.path.join(sys._MEIPASS, path)
    else:
        # 在开发环境中，使用相对路径
        resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
    return resolved_path


if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        resolve_path("page.py"),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
