import os, datetime

resourceDir = os.path.abspath(os.path.join(__file__, "."))
settingsDir = os.path.abspath(os.path.join(resourceDir, "../Settings"))
logDir = os.path.abspath(os.path.join(settingsDir, "./Logs"))
logFilePath = os.path.abspath(
    os.path.join(logDir, str(datetime.datetime.now()).strip().replace(':', '-') + '.log')).strip()
