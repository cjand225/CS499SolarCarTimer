from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush, QPalette
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog
from src.table.ElidedLabel import ElidedLabel

class SemiAuto(QWidget):

    def __init__(self, uiPath):
        super().__init__()
        self.UIPath = uiPath
        self.carStoreRef = []

        self.labelColumn = 0
        self.buttonColumn = 1
        self.checkBoxColumn = 2

        self.indexList = []
        self.labelList = []
        self.buttonList = []
        self.checkBoxList = []

        #layout of semiAuto
        self.buttons = None


        self.initUI()
        self.initButtonLayout()
        self.createButtons()


    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.buttons = self.buttonsLayout


    def initButtonLayout(self):
        self.buttons.setAlignment(Qt.AlignTop)
        self.buttons.setColumnMinimumWidth(self.labelColumn, 100)
        self.buttons.setColumnMinimumWidth(self.checkBoxColumn, 100)
        self.buttons.setHorizontalSpacing(15)
        self.buttons.setColumnStretch(self.labelColumn, 1)
        self.buttons.setColumnStretch(self.buttonColumn, 1)
        self.buttons.setColumnStretch(self.checkBoxColumn, 0)

    def updateList(self, list):
        self.carStoreRef = list
        self.createButtons()
        self.bindButtons()
        self.bindCheckBoxes()


    #TODO: Create Bindings List based on Modifiers + numbers, etc.
    def createButtons(self):
        labelIndex = 0
        for car in self.carStoreRef:
            #create Label
            label =  ElidedLabel()
            label.setText(str(car.getOrg()))
            label.setMaximumWidth(225)

            button = QPushButton()
            button.setText("Record Time")
            button.setObjectName(str(labelIndex))

            checkBox = QCheckBox()
            checkBox.setText("Lap Prediction ")


            self.indexList.append(labelIndex)
            self.labelList.append(label)
            self.buttonList.append(button)
            self.checkBoxList.append(checkBox)
            self.buttons.addWidget(label, labelIndex, self.labelColumn)
            self.buttons.addWidget(button, labelIndex, self.buttonColumn)
            self.buttons.addWidget(checkBox, labelIndex, self.checkBoxColumn)
            labelIndex += 1


    def bindButtons(self):
        if len(self.buttonList) == len(self.carStoreRef):
            index = 0
            for button in self.buttonList:
                self.bindButton(index, button)


                index+= 1

    def bindButton(self, index, button):
        button.clicked.connect(lambda b: self.handleClick(index))

    def bindCheckBoxes(self):
        if len(self.checkBoxList) == len(self.carStoreRef):
            index = 0
            for checkBox in self.checkBoxList:
                self.bindCheckBox(index, checkBox)
                index += 1

    def bindCheckBox(self, index, checkBox):
        checkBox.toggled.connect(lambda  b: self.handleCheck(index))

    def handleCheck(self, index):
        if self.checkBoxList[index].isChecked():
                print("PH")
                #put handle calculation function here

    def handleClick(self, index):
        self.carStoreRef[index].addLapTime()





