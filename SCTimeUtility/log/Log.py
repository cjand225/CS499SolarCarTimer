import logging, os

logDir = os.path.abspath(os.path.join(__file__, "./../../settings/logs"))
infoLogPath = os.path.abspath(os.path.join(logDir, 'SCT.log'))


def checkDirs():
    if not os.path.exists(logDir):
        os.makedirs(logDir)


def getLog():
    return logging.getLogger("SCT")


def initLogs():
    checkDirs()
    initLog()


def initLog():
    infoLog = logging.getLogger("SCT")
    infoLog.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh = logging.FileHandler(infoLogPath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    infoLog.addHandler(fh)
