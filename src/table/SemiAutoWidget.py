from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QApplication
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi


#Semi-Auto Button Widget
class SemiAutoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.createSAWidget()

    def initUI(self):
        self.ui = loadUi('./../resources/Buttons.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
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
