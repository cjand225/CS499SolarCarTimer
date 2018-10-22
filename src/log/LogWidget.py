from PyQt5.QtWidgets import QWidget, QStyle, QApplication
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi

class LogWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ui = loadUi('./../resources/Log.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def appendLog(self, text):
        self.logText.append(text)