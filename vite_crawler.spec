# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['vite_crawler.py'],
    pathex=[],
    binaries=[],
    datas=[('config.ini', '.'), ('E:\Program Files\Python\Python312\Lib\site-packages\pathvalidate', 'pathvalidate')],
    hiddenimports=['pathvalidate'],
    hookspath=[],
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
    a.binaries,
    a.datas,
    [],
    name='vite_crawler',
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
)
