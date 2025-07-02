#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata, collect_data_files

# 复制streamlit的元数据
datas = copy_metadata("streamlit")

# 收集streamlit的数据文件
datas += collect_data_files("streamlit")

# 添加streamlit需要的核心隐藏导入
hiddenimports = [
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.runtime.caching',
    'streamlit.runtime.state',
    'streamlit.components.v1',
    'streamlit.delta_generator',
    'streamlit.elements',
    'streamlit.elements.widgets',
    'streamlit.elements.text',
    'streamlit.elements.markdown',
    'streamlit.elements.button',
    'streamlit.elements.selectbox',
    'streamlit.elements.text_input',
    'streamlit.elements.number_input',
    'streamlit.elements.checkbox',
    'streamlit.elements.columns',
    'streamlit.elements.tabs',
    'streamlit.elements.expander',
    'streamlit.elements.sidebar',
    'streamlit.elements.empty',
    'streamlit.elements.spinner',
    'streamlit.elements.progress',
    'streamlit.elements.success',
    'streamlit.elements.error',
    'streamlit.elements.warning',
    'streamlit.elements.info',
    'streamlit.elements.download_button',
    'streamlit.elements.image',
    'streamlit.elements.container',
    'streamlit.logger',
    'streamlit.config',
    'streamlit.util',
    'streamlit.errors',
    'click',
    'tornado',
    'tornado.web',
    'tornado.ioloop',
    'tornado.httpserver',
    'tornado.websocket',
]
