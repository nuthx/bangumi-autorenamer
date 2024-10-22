# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/style', 'src/style'), ('src/font', 'src/font'), ('src/image', 'src/image')],
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
    [],
    exclude_binaries=True,
    name='BangumiRenamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BangumiRenamer',
)

app = BUNDLE(
    coll,
    name='BangumiRenamer.app',
    icon='image/icon.icns',
    bundle_identifier=None,
    version='2.1.0',
)
