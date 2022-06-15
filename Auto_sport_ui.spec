# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Auto_sport_ui.py'],
             pathex=['C:\\Users\\user\\PycharmProjects\\Sport_Auto_gambling_bet',
                     'C:\\Users\\user\\PycharmProjects\\Sport_Auto_gambling_bet\\venv\\Lib\\site-packages\\PyQt5',
                     'C:\\Users\\user\\PycharmProjects\\Sport_Auto_gambling_bet\\venv\\Lib\\site-packages\\PyQt5\\Qt5\\bin',
                     'C:\\Users\\user\\PycharmProjects\\Sport_Auto_gambling_bet\\venv\\Lib\\site-packages\\PyQt5\\Qt5\\plugins'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Auto_sport_ui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
