import logging, os

logDir = os.path.abspath(os.path.join(__file__, "./../../settings/logs"))
infoLogPath = os.path.abspath(os.path.join(logDir, 'SCT.log'))

'''  
    Function: checkDirs
    Parameters: N/A
    Return Value: N/A
    Purpose: Checks if the logging path exists and if not makes the directory to complete the path.
'''


def checkDirs():
    if not os.path.exists(logDir):
        os.makedirs(logDir)


'''  
    Function: getLog
    Parameters: N/A
    Return Value: Logging.Logger
    Purpose: Returns the Global log to be used where ever it may be invoked.
'''


def getLog():
    return logging.getLogger("SCT")


'''  
    Function: initLogs
    Parameters: N/A
    Return Value: N/A
    Purpose: Initializes the functions necessary for setup of logging.
'''


def initLogs():
    checkDirs()
    initLog()


'''  
    Function: initLog
    Parameters: N/A
    Return Value: N/A
    Purpose: Initializes the functions necessary for setup of logging.
'''


def initLog():
    infoLog = logging.getLogger("SCT")
    infoLog.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh = logging.FileHandler(infoLogPath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    infoLog.addHandler(fh)
