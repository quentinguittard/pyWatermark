# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['F:\\Workspaces\\devenv\\qt_for_python\\pyWatermark\\src\\main\\python\\main.py'],
             pathex=['F:\\Workspaces\\devenv\\qt_for_python\\pyWatermark\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['F:\\Workspaces\\devenv\\qt_for_python\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['F:\\Workspaces\\devenv\\qt_for_python\\pyWatermark\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='pyWatermark',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='F:\\Workspaces\\devenv\\qt_for_python\\pyWatermark\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='pyWatermark')
