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

    def initButtons(self, totalButtons):
        print("hi")