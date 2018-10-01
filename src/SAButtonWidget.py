import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Semi-Auto Button Widget
class SAButtonWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Button Widget"

        # default position & sizing for Widget
        self.width = 20
        self.height = 20

        self.rows = 2;
        self.cols = 2;
        self.buttonTotal = self.rows * self.cols
        self.layout = QGridLayout()  # Defines Layout - Horizontal

        #initalizes widget
        self.createSAWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(self.width,self.height)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignTop,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.setLayout(self.layout) # applies layout to widget
        self.show() # displays widget

    def createSAWidget(self):
        self.initButtons()

    #initalizes Buttons for each respective car & adds them to the layout
    def initButtons(self):
        self.buttonArray = [None] * (self.rows * self.cols)

        for i in range(self.buttonTotal):
            self.buttonArray[i] = QPushButton("Button " + str(i))
            self.buttonArray[i].setGeometry(10 * i, 10 * i, 100, 100)
            self.buttonArray[i].setCheckable(True)
            self.buttonArray[i].toggle()
            self.layout.addWidget(self.buttonArray[i])  # can take additional parameters to specify what part of grid
