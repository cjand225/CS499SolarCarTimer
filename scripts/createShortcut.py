import os
import shutil
import platform
from win32com.client import Dispatch


def createShortcut(path, target='', wDir='', icon=''):
  ext = path[-3:]
  if ext == 'url':
    shortcut = open(path, 'w')
    shortcut.write('[InternetShortcut]\n')
    shortcut.write('URL=%s' % target)
    shortcut.close()
  else:
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    if icon == '':
      pass
    else:
      shortcut.IconLocation = icon
    shortcut.save()

PROJ_PATH = os.path.join("../SCTimeUtility/__main__.py")
DESKTOP_PATH = os.path.join(os.environ["HOMEPATH"], "Desktop")
FILE_PATH = os.path.join(DESKTOP_PATH, "__main__.py")
PYTHON_PATH = os.path.join("C:/Users/cjan225/Anaconda3/envs/playground/python.exe ", FILE_PATH)

SHORTCUT_PATH = os.path.join(DESKTOP_PATH, "SCTime.url")



if platform.system() == "Windows":
  shutil.copy(PROJ_PATH, FILE_PATH)
  createShortcut(SHORTCUT_PATH, PYTHON_PATH, DESKTOP_PATH, '')
elif platform.system() == "Linux":
  shutil.copy(PROJ_PATH, FILE_PATH)


