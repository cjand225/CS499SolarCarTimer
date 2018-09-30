import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Semi-Auto Button Widget
class SAButtonWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Button Widget"

        self.left = 0           #default sizing for Widget
        self.top = 0
        self.width = 400
        self.height = 700

        self.createSAWidget()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)  #sets position & size
        self.setMaximumSize(200,200)    #temporary


        self.layout = QVBoxLayout()  # Add box layout, add Table to box layout
        self.layout.addWidget(self.buttonWidget)  # and add box layout to widget
        self.setLayout(self.layout) #applies layout to widget

        self.show() #displays widget

    def createSAWidget(self):
        self.buttonWidget = QPushButton("Button 1")
        self.buttonWidget.setGeometry(20,20,20,20)
        self.buttonWidget.setCheckable(True)
        self.buttonWidget.toggle()