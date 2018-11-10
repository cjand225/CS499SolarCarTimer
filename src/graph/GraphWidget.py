from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QApplication
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi


class Graph(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))