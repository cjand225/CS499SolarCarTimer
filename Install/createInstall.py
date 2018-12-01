#!/usr/bin/env python3
import createBin

# create bin folder tree
createBin.createDirs()
createBin.copyData()
createBin.copySetup()
createBin.createPyFiles()
