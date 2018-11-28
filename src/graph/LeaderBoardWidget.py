from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.Qt import *


class LeaderBoardWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = None

    def initUI(self, uiPath):
        self.ui = loadUi(uiPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))