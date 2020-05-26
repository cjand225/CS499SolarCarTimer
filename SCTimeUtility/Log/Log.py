"""

    Module:
    Purpose:
    Depends On:

"""
import logging, os, datetime

from SCTimeUtility.Resources import logDir, logFilePath

'''  
    Function: checkDirs
    Parameters: N/A
    Return Value: N/A
    Purpose: Checks if the logging path exists and if not makes the directory to complete the path.
'''


def check_directory():
    if not os.path.exists(logDir):
        os.makedirs(logDir)


'''  
    Function: getLog
    Parameters: N/A
    Return Value: Logging.Logger
    Purpose: Returns the Global Log to be used where ever it may be invoked.
'''


def get_log():
    return logging.getLogger("SCT")


'''  
    Function: initLogs
    Parameters: N/A
    Return Value: N/A
    Purpose: Initializes the functions necessary for setup of logging.
'''


def init_logs():
    check_directory()
    init_log()


'''  
    Function: initLog
    Parameters: N/A
    Return Value: N/A
    Purpose: Initializes the functions necessary for setup of logging.
'''


def init_log():
    info_log = logging.getLogger("SCT")
    info_log.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
    fh = logging.FileHandler(logFilePath)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    info_log.addHandler(fh)
