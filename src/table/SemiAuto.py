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
        self.predictColumn = 3

        self.indexList = []
        self.labelList = []
        self.buttonList = []
        self.checkBoxList = []
        self.predictList = []

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
        self.clearLists()
        self.carStoreRef = list
        self.createButtons()
        #self.createPredictionLabels()
        self.bindButtons()
        self.bindCheckBoxes()


    #TODO: Create Bindings List based on Modifiers + numbers, etc.
    def createButtons(self):
        labelIndex = 0
        for car in self.carStoreRef:
            #create Label
            label =  ElidedLabel()
            label.setText(str(car.getTeam()))
            label.setMaximumWidth(150)

            button = QPushButton()
            button.setText("Record Time")
            button.setObjectName(str(labelIndex))
            button.setMaximumWidth(150)

            checkBox = QCheckBox()
            checkBox.setText("Lap Prediction ")

            predictLabel = ElidedLabel()
            predictLabel.setText("0:00:00")
            #predictLabel.setStyleSheet("QLabel { color: blue; } ")
            predictLabel.setHidden(True)



            self.indexList.append(labelIndex)
            self.labelList.append(label)
            self.buttonList.append(button)
            self.checkBoxList.append(checkBox)
            self.predictList.append(predictLabel)

            self.buttons.addWidget(label, labelIndex, self.labelColumn)
            self.buttons.addWidget(button, labelIndex, self.buttonColumn)
            self.buttons.addWidget(checkBox, labelIndex, self.checkBoxColumn)
            self.buttons.addWidget(predictLabel, labelIndex, self.predictColumn)
            labelIndex += 1

    def clearLists(self):
        self.unBindButtons()
        self.clearLayout(self.buttons)

        self.labelList = []
        self.checkBoxList = []
        self.buttonList = []
        self.predictList = []


    def unBindButtons(self):
        for button in self.buttonList:
            button.clicked.disconnect()

        for checkBox in self.checkBoxList:
            checkBox.toggled.disconnect()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


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
                self.predictList[index].setVisible(True)
                # put handle calculation function here
        else:
            self.predictList[index].setHidden(True)


    def handleClick(self, index):
        self.carStoreRef[index].addLapTime()






