from distutils.core import setup
from sys import platform

setup(name='SC_TimerUtility',
      version='1.0',
      description='Timing Utility for Solar Car Team',
      author='Charles Andrews, Andrew Tapia, Tanner Coffman, Parker Back',
      author_email='N/A',
      url='Team3.me',
      platform=platform,
      packages=['src', 'src/app', 'src/graph', 'src/log', 'src/system', 'src/table', 'src/video']
      )
