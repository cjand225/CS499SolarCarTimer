#!/usr/bin/env bash
# set seed to a known repeatable integer value
PYTHONHASHSEED=1
export PYTHONHASHSEED
pyinstaller --clean --windowed pyinstaller_crossplatform.spec
# make checksum
cksum ./../dist/SCTimeUtility/SCT | awk '{print $1}' > ./dist/SCT.checksum
# let Python be unpredictable again
unset PYTHONHASHSEED