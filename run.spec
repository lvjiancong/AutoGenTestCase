# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('page.py', '.'),
        ('llms.py', '.'),
        ('config.ini', '.'),
        ('TESTCASE_READER_SYSTEM_MESSAGE.txt', '.'),
        ('TESTCASE_WRITER_SYSTEM_MESSAGE.txt', '.'),
        ('需求文档示例.txt', '.'),
        ('img', 'img')
    ],
    hiddenimports=[
        # Streamlit核心模块
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.components.v1',
        'streamlit.components.v1.html',
        'streamlit.components.v1.iframe',
        'streamlit.runtime.state',
        'streamlit.runtime.caching',
        'streamlit.runtime.secrets',
        'streamlit.delta_generator',
        'streamlit.elements',
        'streamlit.elements.form',
        'streamlit.elements.widgets',
        'streamlit.elements.widgets.button',
        'streamlit.elements.widgets.checkbox',
        'streamlit.elements.widgets.selectbox',
        'streamlit.elements.widgets.text_input',
        'streamlit.elements.widgets.number_input',
        'streamlit.elements.widgets.slider',
        'streamlit.elements.text',
        'streamlit.elements.markdown',
        'streamlit.elements.container',
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
        
        # AutoGen相关模块
        'autogen',
        'autogen.agentchat',
        'autogen.agentchat.assistant_agent',
        'autogen.agentchat.user_proxy_agent',
        'autogen.agentchat.groupchat',
        'autogen.coding',
        'autogen.oai',
        'autogen.runtime_logging',
        'autogen_agentchat',
        'autogen_agentchat.agents',
        'autogen_agentchat.base',
        'autogen_agentchat.messages',
        'autogen_core',
        'autogen_ext',
        
        # OpenAI和HTTP客户端
        'openai',
        'openai.types',
        'openai.types.chat',
        'openai._client',
        'openai._base_client',
        'openai._response',
        'openai._streaming',
        'openai._utils',
        'openai._compat',
        'openai._constants',
        'openai._exceptions',
        'openai.resources',
        'openai.resources.chat',
        'openai.resources.chat.completions',
        'httpx',
        'httpx._client',
        'httpx._config',
        'httpx._models',
        'httpx._types',
        'httpx._utils',
        'httpx._auth',
        'httpx._exceptions',
        'httpcore',
        'httpcore._backends',
        'httpcore._sync',
        'httpcore._async',
        
        # tiktoken
        'tiktoken',
        'tiktoken.core',
        'tiktoken.encoding',
        'tiktoken_ext',
        'tiktoken_ext.openai_public',
        
        # 其他必要模块
        'configparser',
        'pathlib',
        'xlsxwriter',
        'xlsxwriter.workbook',
        'xlsxwriter.worksheet',
        'base64',
        'platform',
        'json',
        'urllib3',
        'requests',
        'certifi',
        'charset_normalizer',
        'idna',
        
        # 数据处理
        'pandas',
        'numpy',
        'pyarrow',
        'pyarrow.parquet',
        'pyarrow.csv',
        'pyarrow.json',
        
        # 时间和日期
        'datetime',
        'time',
        'pytz',
        'dateutil',
        'dateutil.parser',
        'dateutil.tz',
        
        # 正则表达式和文本处理
        're',
        'string',
        'textwrap',
        
        # 系统和文件操作
        'os',
        'sys',
        'io',
        'tempfile',
        'shutil',
        'glob',
        
        # 网络和并发
        'threading',
        'multiprocessing',
        'concurrent',
        'concurrent.futures',
        'asyncio',
        
        # 加密和哈希
        'hashlib',
        'hmac',
        'secrets',
        
        # 类型提示
        'typing',
        'typing_extensions',
        
        # 日志
        'logging',
        'logging.handlers',
        
        # 数学和统计
        'math',
        'statistics',
        'random',
        
        # 序列化
        'pickle',
        'marshal',
        
        # 压缩
        'gzip',
        'zipfile',
        'tarfile',
        
        # URL和HTML
        'urllib',
        'urllib.parse',
        'urllib.request',
        'html',
        'html.parser',
        
        # XML
        'xml',
        'xml.etree',
        'xml.etree.ElementTree',
        
        # 集合和迭代工具
        'collections',
        'collections.abc',
        'itertools',
        'functools',
        
        # 文件格式
        'csv',
        'email',
        'email.mime',
        'email.mime.text',
        'email.mime.multipart',
        
        # 调试和检查
        'inspect',
        'traceback',
        'warnings',
        
        # 包管理
        'pkg_resources',
        'importlib',
        'importlib.metadata',
        'importlib.util',
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run',
)
