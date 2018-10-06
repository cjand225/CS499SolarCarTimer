from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

class LogWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Log Widget'
        self.initUI()

    def initUI(self):
        self.ui = loadUi('./../resources/Log.ui', self)
        self.setWindowTitle(self.title)
        self.show()

    def appendLog(self, text):
        self.logText.append(text)