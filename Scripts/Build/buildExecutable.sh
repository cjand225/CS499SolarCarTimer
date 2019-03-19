#!/usr/bin/env bash
# set seed to a known repeatable integer value
PYTHONHASHSEED=1
export PYTHONHASHSEED
pyinstaller --clean --windowed ./Scripts/Build/pyinstaller_crossplatform.spec
# make checksum
cksum ./dist/SCTimeUtility-PyInstaller/SCT | awk '{print $1}' > ./dist/SCT.checksum
# let Python be unpredictable again
unset PYTHONHASHSEED