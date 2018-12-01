import shutil
import os

# source - top level directories
srcDir = os.path.abspath(os.path.join(__file__, "./../../src/"))
resDir = os.path.abspath(os.path.join(__file__, "./../../resources/"))
manDir = os.path.abspath(os.path.join(__file__, "./../../manuals/"))
installDir = os.path.abspath(os.path.join(__file__, "./../../Install/"))
# source subdirectories
appDir = os.path.abspath(os.path.join(srcDir, "app"))
graphDir = os.path.abspath(os.path.join(srcDir, "graph"))
logDir = os.path.abspath(os.path.join(srcDir, "log"))
sysDir = os.path.abspath(os.path.join(srcDir, "system"))
tableDir = os.path.abspath(os.path.join(srcDir, "table"))
videoDir = os.path.abspath(os.path.join(srcDir, "video"))
# source files to copy
setupFile = os.path.abspath(os.path.join(installDir, "setup.py"))
venvWinFile = os.path.abspath(os.path.join(installDir, "envBuild_Windows.txt"))
venvLinuxFile = os.path.abspath(os.path.join(installDir, "envBuild_Linux.txt"))

# Dest
installDestDir = os.path.abspath(os.path.join(__file__, "./../../bin"))
resDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/resources"))
manDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/manuals"))
srcDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/src"))
venvDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/venv"))

# SubDirectories
appDestDir = os.path.abspath(os.path.join(srcDestDir, "app"))
graphDestDir = os.path.abspath(os.path.join(srcDestDir, "graph"))
logDestDir = os.path.abspath(os.path.join(srcDestDir, "log"))
sysDestDir = os.path.abspath(os.path.join(srcDestDir, "system"))
tableDestDir = os.path.abspath(os.path.join(srcDestDir, "table"))
videoDestDir = os.path.abspath(os.path.join(srcDestDir, "video"))
setupFileDest = os.path.abspath(os.path.join(installDestDir, "setup.py"))


# dest Files
initPyFile = os.path.join("__init__.py")
venvDestWinFile = os.path.abspath(os.path.join(venvDestDir, "envBuild_Windows.txt"))
venvDestLinuxFile = os.path.abspath(os.path.join(venvDestDir, "envBuild_Linux.txt"))
instructFile = os.path.join("Instructions.txt")


def copyDir(dir, dest):
    if os.path.exists(dir):
        dirList = os.listdir(dir)
        for file in dirList:
            if os.path.isfile(os.path.abspath(os.path.join(dir, file))):
                shutil.copy(os.path.abspath(os.path.join(dir, file)), dest)


def createDir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)


def createDirs():
    # create bin folder and subfolders
    createDir(installDestDir)
    createDir(srcDestDir)
    createDir(resDestDir)
    createDir(manDestDir)
    createDir(appDestDir)
    createDir(graphDestDir)
    createDir(logDestDir)
    createDir(sysDestDir)
    createDir(tableDestDir)
    createDir(videoDestDir)
    createDir(venvDestDir)


def copyData():
    # copy all the contents from dev setup to bin
    copyDir(srcDir, srcDestDir)
    copyDir(resDir, resDestDir)
    copyDir(manDir, manDestDir)
    copyDir(appDir, appDestDir)
    copyDir(graphDir, graphDestDir)
    copyDir(logDir, logDestDir)
    copyDir(sysDir, sysDestDir)
    copyDir(tableDir, tableDestDir)
    copyDir(videoDir, videoDestDir)


def copySetup():
    if os.path.exists(installDestDir):
        shutil.copy(os.path.abspath(os.path.join(installDir, instructFile)), os.path.abspath(os.path.join(venvDestDir, instructFile)))
        shutil.copy(venvWinFile, venvDestWinFile)
        shutil.copy(venvLinuxFile, venvDestLinuxFile)
        shutil.copy(setupFile, setupFileDest)


def createPyFile(dirPath):
    if os.path.exists(dirPath):
        initFile = os.path.abspath(os.path.join(dirPath, initPyFile))
        if not os.path.isfile(initFile):
            fp = open(initFile, "w")
            fp.close()


def createPyFiles():
    createPyFile(srcDestDir)
    createPyFile(appDestDir)
    createPyFile(graphDestDir)
    createPyFile(logDestDir)
    createPyFile(sysDestDir)
    createPyFile(tableDestDir)
    createPyFile(videoDestDir)
    createPyFile(venvDestDir)
