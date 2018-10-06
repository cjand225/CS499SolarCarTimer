from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.uic import loadUi


#Semi-Auto Button Widget
class ButtonWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Button Widget'
        self.initUI()
        #self.createSAWidget()

    def initUI(self):
        self.ui = loadUi('./../resources/Buttons.ui', self)
        self.setWindowTitle(self.title)
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
