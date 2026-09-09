# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for a standalone FetchCord binary.

Build with:  pyinstaller fetchcord.spec
Used by the GitHub "release" workflow to produce a Windows .exe
(and is testable on Linux, where it produces a native Linux binary).
"""
from PyInstaller.utils.hooks import collect_data_files

# Bundle every non-code resource (the *.yml / *.json / *.conf config files and
# the Windows native package) so importlib.resources finds them in the exe.
datas = collect_data_files("fetch_cord", include_py_files=True)

a = Analysis(
    ["run_fetchcord.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=["pypresence", "psutil", "yaml"],
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
    name="FetchCord",
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
