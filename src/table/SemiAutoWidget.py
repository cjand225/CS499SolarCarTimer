from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi



#Semi-Auto Button Widget
class SemiAutoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        #self.createSAWidget()
        self.carPanelList = [None] * 45
        self.createCarPanel("weee", 0)

    def initUI(self):
        self.ui = loadUi('./../resources/Buttons.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def createSAWidget(self):
        self.initButtons()

    def initButtons(self, totalButtons):
        print("hi")

    def createCarPanel(self, labelText, carPosition):
        layout = QGridLayout()
        groupBox = QGroupBox()
        label = QLabel()
        label.setText(labelText)
        button = QPushButton("START")

        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(label, 0, 0)
        layout.addWidget(button,0, 1)
        layout.addWidget(button, 0, 2)
        layout.addWidget(button, 0, 3)

        groupBox.setLayout(layout)

        self.buttonBoxLayout.addWidget(groupBox, 0, 1)



class carButtonBox(QGroupBox):

    def __init__(self):
        super().__init__();

        self.label = None
        self.carNumber = None
        self.layout = QGridLayout()

    def setButtonBind(self, keybind):
        print("hi")

    def initLayout(self):
        print("hi")

    def getLabel(self):
        return self.label

    def setLabel(self, labeltext):
        self.label = labeltext

    def setCarNum(self, num):
        self.carNumber = num

    def getCarNum(self):
        return self.carNumber

