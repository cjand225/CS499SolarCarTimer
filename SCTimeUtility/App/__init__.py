import os

resourcesDir = os.path.abspath(os.path.join(__file__, "./../../Resources"))
manualDir = os.path.abspath(os.path.join(__file__, "./../../../Docs"))
settingsDir = os.path.abspath(os.path.join(__file__, "./../../bin/Settings"))

logUIPath = os.path.join(resourcesDir, 'Log.ui')
mainUIPath = os.path.join(resourcesDir, 'AppWindow.ui')
visionUIPath = os.path.join(resourcesDir, 'Video.ui')
quitDialogUIPath = os.path.join(resourcesDir, 'QuitDialog.ui')
helpDialogUIPath = os.path.join(resourcesDir, 'HelpDialog.ui')
aboutDialogUIPath = os.path.join(resourcesDir, 'AboutDialog.ui')
graphUIPath = os.path.join(resourcesDir, 'GraphOptions.ui')
userManPath = os.path.join(manualDir, 'UserManual.html')
aboutPath = os.path.join(manualDir, 'About.html')
