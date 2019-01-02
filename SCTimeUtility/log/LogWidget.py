import logging

from PyQt5.QtWidgets import QWidget, QStyle, QApplication, QPlainTextEdit
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi

from SCTimeUtility.log.Log import getLog
from SCTimeUtility.log.logFilters import infoFilter, debugFilter, criticalFilter, warningFilter, errorFilter


class LogWidget(QWidget):

    def __init__(self, uipath, parent=None):
        super().__init__(parent)
        self.UIPath = uipath

        # get log
        self.log = getLog()
        self.format = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')

        # create handlers
        self.infoLogTextBox = QTextEditLogger(self)
        self.debugLogTextBox = QTextEditLogger(self)
        self.warningLogTextBox = QTextEditLogger(self)
        self.criticalLogTextBox = QTextEditLogger(self)
        self.errorLogTextBox = QTextEditLogger(self)

        # set format for handlers
        self.infoLogTextBox.setFormatter(self.format)
        self.debugLogTextBox.setFormatter(self.format)
        self.warningLogTextBox.setFormatter(self.format)
        self.criticalLogTextBox.setFormatter(self.format)
        self.errorLogTextBox.setFormatter(self.format)

        # add filters to widget handlers
        self.infoLogTextBox.addFilter(infoFilter())
        self.debugLogTextBox.addFilter(debugFilter())
        self.warningLogTextBox.addFilter(warningFilter())
        self.criticalLogTextBox.addFilter(criticalFilter())
        self.errorLogTextBox.addFilter(errorFilter())

        # add new widget handlers
        self.log.addHandler(self.infoLogTextBox)
        self.log.addHandler(self.debugLogTextBox)
        self.log.addHandler(self.warningLogTextBox)
        self.log.addHandler(self.criticalLogTextBox)
        self.log.addHandler(self.errorLogTextBox)

        # create widget UI and add new widgets
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))
        # add widgets to ui
        self.infoLayout.addWidget(self.infoLogTextBox.widget)
        self.debugLayout.addWidget(self.debugLogTextBox.widget)
        self.warningLayout.addWidget(self.warningLogTextBox.widget)
        self.criticalLayout.addWidget(self.criticalLogTextBox.widget)
        self.errorLayout.addWidget(self.errorLogTextBox.widget)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
