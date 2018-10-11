from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QApplication
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi


class Graph(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.ui = loadUi('./../resources/GraphCanvas.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))