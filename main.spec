# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['C:\\Users\\nico_000\\Documents\\Floatmotion'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
