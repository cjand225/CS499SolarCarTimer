#!/usr/bin/env python3

from distutils.core import setup
import shutil
import os


#source
srcDir = os.path.abspath(os.path.join(__file__,"./../../src/"))
resDir = os.path.abspath(os.path.join(__file__,"./../../resources/"))
manDir = os.path.abspath(os.path.join(__file__,"./../../manuals/"))


#Dest
installDir = os.path.abspath(os.path.join(__file__, "./../../bin"))
srcDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/src"))
logDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/logs"))
resDestDir = os.path.abspath(os.path.join(__file__, "./../../bin/resources"))


if not os.path.exists(installDir):
      os.mkdir(installDir)



#setup(name='SC_TimerUtility',
#      version='1.0',
#      description='Timing Utility for Solar Car Team',
#      author='Charles Andrews, Andrew Tapia, Tanner Coffman, Parker Back',
#      url='Team3.me')