#!/usr/bin/env bash
# set seed to a known repeatable integer value
PYTHONHASHSEED=1
export PYTHONHASHSEED
pyinstaller --clean --windowed --workpath=../../bin/ --distpath=../../bin/ pyinstaller_crossplatform.spec
# make checksum
cksum ./../../bin/SCTimeUtility/SCT | awk '{print $1}' > ./../../bin/SCT.checksum
# let Python be unpredictable again
unset PYTHONHASHSEED