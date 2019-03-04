import os

resourcesDir = os.path.abspath(os.path.join(__file__, "./../../Resources"))
manualDir = os.path.abspath(os.path.join(__file__, "./../../../Docs"))
settingsDir = os.path.abspath(os.path.join(__file__, "./../../bin/Settings"))
uiDir = os.path.join(resourcesDir, './UI')

# ui file paths
mainUIPath = os.path.join(uiDir, 'AppWindow.ui')

# ui Dialog paths
quitDialogUIPath = os.path.join(uiDir, 'QuitDialog.ui')
helpDialogUIPath = os.path.join(uiDir, 'HelpDialog.ui')
aboutDialogUIPath = os.path.join(uiDir, 'AboutDialog.ui')

# resource manual paths
userManPath = os.path.join(manualDir, 'UserManual.html')
aboutPath = os.path.join(manualDir, 'About.html')
