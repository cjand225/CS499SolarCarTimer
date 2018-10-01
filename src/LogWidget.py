import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class LogWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Log Widget'
        # default sizing for Widget
        self.width = 500
        self.height = 500
        self.layout = QGridLayout()  # Defines Layout - grid
        self.initLogWindow()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.setLayout(self.layout)  # applies layout to widget
        self.show()  # displays widget

    def initLogWindow(self):
        self.logText = QTextEdit()
        self.logText.setReadOnly(True)          #user can't edit it.
        self.layout.addWidget(self.logText)

    def appendLog(self, text):
        self.logText.append(text)