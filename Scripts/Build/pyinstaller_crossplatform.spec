# -*- mode: python -*-
#To generate run: pyinstaller --clean --windowed pyinstaller_crossplatform.spec
# or use the buildExecutable scripts for your OS
#for terminal output remove --windowed
block_cipher = None

import os
resource_path = os.path.abspath(os.path.join(".","..", "..", "SCTimeUtility", "Resources"))
ui_path = os.path.abspath(os.path.join(resource_path, "UI", "*.*"))
docs_path = os.path.abspath(os.path.join(resource_path, "Docs", "*.*"))
icons_path = os.path.abspath(os.path.join(resource_path, "Icons", "*.*"))
script_path = os.path.abspath(os.path.join(".","..", "..", "SCTimeUtility", "__main__.py"))
project_path = os.path.abspath(os.path.join("."))
dist_path = os.path.join(".",  "SCTimeUtility", "Resources")
ui_dist_path = os.path.join(dist_path, "UI")
docs_dist_path = os.path.join(dist_path, "Docs")
icons_dist_path = os.path.join(dist_path, "Icons")

a = Analysis([script_path],
             pathex=[project_path],
             binaries=[],
             datas=[( ui_path , ui_dist_path), (docs_path, docs_dist_path), (icons_path, icons_dist_path)],
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
