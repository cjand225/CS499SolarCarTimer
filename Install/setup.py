#!/usr/bin/env python3

from distutils.core import setup
import os

logDir = os.path.abspath(os.path.join(__file__, "./../../bin/"))

setup(name='SC_TimerUtility',
      version='1.0',
      description='Timing Utility for Solar Car Team',
      author='Charles Andrews, Andrew Tapia, Tanner Coffman, Parker Back',
      url='Team3.me')