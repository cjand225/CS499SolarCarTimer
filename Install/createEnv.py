#!/usr/bin/env python3
from subprocess import call
from sys import platform
import os

if platform == "linux" or platform == "linux2":
    print("Linux")

if platform == "win32":
    print("Windows")
