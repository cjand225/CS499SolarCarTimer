import os, sys
from SCTimeUtility.Resources import resourceDir

docDir = os.path.abspath(os.path.join(resourceDir, "..", "Docs"))
screensDir = os.path.abspath(os.path.join(docDir, ".", "Screenshots"))

# Docs Path

aboutPath = os.path.abspath(os.path.join(docDir, "About.html"))
adminPath = os.path.abspath(os.path.join(docDir, "AdminManual.html"))
licensePath = os.path.abspath(os.path.join(docDir, "LICENSE"))
userPath = os.path.abspath(os.path.join(docDir, "UserManual.html"))
