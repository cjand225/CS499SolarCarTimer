import os, sys, platform

PROJ_PATH = os.path.join("../SCTimeUtility/__main__.py")
DESKTOP_DIR = os.path.join(os.environ["HOMEPATH"], "Desktop")
FILE_PATH = os.path.join(DESKTOP_DIR, "__main__.py")
SHORTCUT_PATH = os.path.join(DESKTOP_DIR, "SCTime.lnk")
SHORTCUT_NAME = "SCTime"
ARGS = os.path.join("-mSCTimeUtility")
TARGET = os.path.join(sys.executable)
TARGET_PATH = os.path.join(sys.path[2][:-12])

def createLinuxShortcut():
  print('PH')

def createWindowsShortcut():
  print("PH")

def createMacShortcut():
  print('PH')




if platform.system() == "Windows":
  createWindowsShortcut()
elif platform.system() == "Linux":
  createLinuxShortcut()
elif platform.system() == "MacOS":
  createMacShortcut()