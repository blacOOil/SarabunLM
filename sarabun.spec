# sarabun.spec
import sys
from pathlib import Path
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
         ('api/Tools',  'api/Tools'),   # Tools folder (SarabunLM.py, DocFormat.py, etc.)
        ('api/Ui',     'api/Ui'),      # Ui folder is INSIDE api/, not root
        ('api/snippets.txt', 'api/snippets.txt'),
    ],
    hiddenimports=[
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.loops.auto',
        'uvicorn.logging',
        'fastapi',
        'starlette',
        'jinja2',
        'webview',
        'anyio',
        'anyio._backends._asyncio',
        'anyio._backends._trio',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,      
    a.zipfiles,      
    a.datas,         
    [],
    exclude_binaries=True,
    name='SarabunLM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,        # Set True if you want a debug console window
    icon=None,            # Add 'your_icon.ico' path here if you have one
    onefile=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SarabunLM',
)