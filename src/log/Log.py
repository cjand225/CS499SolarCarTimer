import logging
import os
import sys
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QPlainTextEdit, QDialog, QPushButton, QVBoxLayout


# creates logger, used at beginning of App
def createLogger():
    # create logger with file at LogPath
    logPath = os.path.abspath(os.path.join(__file__, '../../log/logFile'))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(logPath)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# returns logger to be used in whatever module calls it
def getLogger():
    logger = logging.getLogger(__name__)
    return logger
