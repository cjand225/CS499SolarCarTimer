import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VisionWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Vision Widget'

        # default position & sizing for Widget
        self.width = 200
        self.height = 200

        self.layout = QGridLayout()  # Defines Layout - Horizontal

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignLeft,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.setLayout(self.layout)  # applies layout to widget
        self.show()  # displays widget

    #def initVisionWidget(self):
