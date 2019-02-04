# -*- mode: python -*-
#To generate run: pyinstaller --clean --windowed pyinstaller_crossplatform.spec
# or use the buildExecutable scripts for your OS
#for terminal output remove --windowed
block_cipher = None

import os
resource_path = os.path.abspath("./../SCTimeUtility/resources/*.ui")
script_path = os.path.abspath("./../SCTimeUtility/__main__.py")
project_path = os.path.abspath(".")
dist_path = os.path.join("./../SCTimeUtility/resources/")

a = Analysis([script_path],
             pathex=[project_path],
             binaries=[],
             datas=[( resource_path , dist_path)],
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
          [],
          exclude_binaries=True,
          name='SCT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SCTimeUtility')
