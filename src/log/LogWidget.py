from PyQt5.QtWidgets import QWidget, QStyle, QApplication, QPlainTextEdit
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi
import logging
from src.log.Log import getLogger


class LogWidget(QWidget):

    def __init__(self, uipath, parent=None):
        super().__init__(parent)
        self.UIPath = uipath
        self.initUI()
        self.logTextBox = QTextEditLogger(self)
        self.log = getLogger()

        # You can format what is printed to text box
        self.logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.log.addHandler(self.logTextBox)
        # You can control the logging level
        self.log.setLevel(logging.DEBUG)
        self.logLayout.addWidget(self.logTextBox.widget)

        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)
