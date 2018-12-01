import logging
import os
import time
import sys
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QPlainTextEdit, QDialog, QPushButton, QVBoxLayout

logDir = os.path.abspath(os.path.join(__file__, "./../../../logs/"))

infoLogPath = os.path.abspath(os.path.join(logDir, 'info.txt'))
debugLogPath = os.path.abspath(os.path.join(logDir, 'debug.txt'))
errorLogPath = os.path.abspath(os.path.join(logDir, 'error.txt'))
criticalLogPath = os.path.abspath(os.path.join(logDir, 'critical.txt'))
warningLogPath = os.path.abspath(os.path.join(logDir, 'warning.txt'))


def checkDirs():
    if not os.path.exists(logDir):
        os.makedirs(logDir)


def getInfoLog():
    return logging.getLogger("INFO")


def getDebugLog():
    return logging.getLogger("DEBUG")


def getWarningLog():
    return logging.getLogger("WARNING")


def getCriticalLog():
    return logging.getLogger("CRITICAL")


def getErrorLog():
    return logging.getLogger("ERROR")


def initLogs():
    checkDirs()
    initInfoLog()
    initDebugLog()
    initWarningLog()
    initCriticalLog()
    initErrorLog()


def initInfoLog():
    infoLog = logging.getLogger("INFO")
    infoLog.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh = logging.FileHandler(infoLogPath)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    infoLog.addHandler(fh)


def initDebugLog():
    infoLog = logging.getLogger("DEBUG")
    infoLog.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(debugLogPath)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    infoLog.addHandler(fh)
    infoLog.addHandler(ch)


def initWarningLog():
    warningLog = logging.getLogger("WARNING")
    warningLog.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(warningLogPath)
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)

    # add the handlers to the logger
    warningLog.addHandler(fh)


def initErrorLog():
    errorLog = logging.getLogger("ERROR")
    errorLog.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(errorLogPath)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    errorLog.addHandler(fh)
    errorLog.addHandler(ch)


def initCriticalLog():
    criticalLog = logging.getLogger("CRITICAL")
    criticalLog.setLevel(logging.CRITICAL)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(criticalLogPath)
    fh.setLevel(logging.CRITICAL)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    criticalLog.addHandler(fh)
    criticalLog.addHandler(ch)
