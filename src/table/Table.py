import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi


class Table(QWidget):

    def __init__(self, uiPath):
        super().__init__()

        self.tableUIPath = uiPath
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.tableUIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()