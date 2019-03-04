import os, logging

from SCTimeUtility.App import uiDir

logUIPath = os.path.join(uiDir, 'LogWidget.ui')
defaultLogFormat = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
