# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\maced\\PycharmProjects\\M.IA\\main.py'],
    pathex=['C:\\Users\\maced\\PycharmProjects\\M.IA\\src', 'C:\\Users\\maced\\PycharmProjects\\M.IA\\UI'],
    binaries=[],
    datas=[('C:\\Users\\maced\\PycharmProjects\\M.IA\\UI\\image', 'UI/image/')],
    hiddenimports=[],
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
    name='M.IA 1.1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\maced\\PycharmProjects\\M.IA\\UI\\image\\icone_MIA.ico'],
)
