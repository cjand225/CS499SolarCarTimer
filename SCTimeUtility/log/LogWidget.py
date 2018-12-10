from PyQt5.QtWidgets import QWidget, QStyle, QApplication, QPlainTextEdit
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi
import logging
from SCTimeUtility.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class LogWidget(QWidget):

    def __init__(self, uipath, parent=None):
        super().__init__(parent)
        self.UIPath = uipath

        self.infoLogTextBox = QTextEditLogger(self)
        self.debugLogTextBox = QTextEditLogger(self)
        self.warningLogTextBox = QTextEditLogger(self)
        self.criticalLogTextBox = QTextEditLogger(self)
        self.errorLogTextBox = QTextEditLogger(self)

        self.infoLog = getInfoLog()
        self.debugLog = getDebugLog()
        self.warningLog = getWarningLog()
        self.criticalLog = getCriticalLog()
        self.errorLog = getErrorLog()

        self.setupLogs()
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.infoLayout.addWidget(self.infoLogTextBox.widget)
        self.debugLayout.addWidget(self.debugLogTextBox.widget)
        self.warningLayout.addWidget(self.warningLogTextBox.widget)
        self.criticalLayout.addWidget(self.criticalLogTextBox.widget)
        self.errorLayout.addWidget(self.errorLogTextBox.widget)

    def logSetup(self, log, logBox):
        logBox.setFormatter(logging.Formatter("[ %(asctime)s ][%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
        log.addHandler(logBox)

    def setupLogs(self):
        self.logSetup(self.infoLog, self.infoLogTextBox)
        self.logSetup(self.debugLog, self.debugLogTextBox)
        self.logSetup(self.warningLog, self.warningLogTextBox)
        self.logSetup(self.criticalLog, self.criticalLogTextBox)
        self.logSetup(self.errorLog, self.errorLogTextBox)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
