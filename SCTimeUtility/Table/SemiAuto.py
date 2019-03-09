from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from SCTimeUtility.Table.ElidedLabel import ElidedLabel
from SCTimeUtility.Log.Log import getLog


class SemiAuto(QWidget):

    def __init__(self, uiPath):
        super().__init__()
        self.UIPath = uiPath

        self.labelColumn = 0
        self.buttonColumn = 1
        self.checkBoxColumn = 2
        self.startStopButtonColumn = 3
        self.predictColumn = 4

        self.carStoreRef = []
        self.indexList, self.labelList, self.buttonList = [], [], []
        self.startStopList, self.checkBoxList, self.predictList = [], [], []

        # layout of semiAuto
        self.buttons = None

        self.initUI()
        self.initButtonLayout()
        self.createButtons()

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads Resources for SemiAuto Widget.
    '''

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.buttons = self.buttonsLayout

    '''  
        Function: initButtonLayout
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the layout and placement of individual buttons needed for control of each car.
    '''

    def initButtonLayout(self):
        self.buttons.setAlignment(Qt.AlignTop)
        self.buttons.setColumnMinimumWidth(self.labelColumn, 100)
        self.buttons.setColumnMinimumWidth(self.checkBoxColumn, 100)
        self.buttons.setHorizontalSpacing(15)
        self.buttons.setColumnStretch(self.labelColumn, 1)
        self.buttons.setColumnStretch(self.buttonColumn, 1)
        self.buttons.setColumnStretch(self.checkBoxColumn, 0)

    '''  
        Function: updateList
        Parameters: self, list
        Return Value: N/A
        Purpose: Calls all the relevant functions need to re-create the widget controls based on amount of cars.
    '''

    def updateList(self, list):
        self.clearLists()
        self.carStoreRef = list
        self.createButtons()
        # self.createPredictionLabels()
        self.bindButtons()
        self.bindCheckBoxes()

    '''  
        Function: createButtons
        Parameters: self
        Return Value: N/A
        Purpose: creates the actual row for each car control
    '''

    def createButtons(self):
        labelIndex = 0
        for car in self.carStoreRef:
            # create Label
            label = ElidedLabel()
            label.setText(str(car.getTeam()))
            label.setMaximumWidth(150)

            button = QPushButton()
            button.setText("Record Time")
            button.setObjectName(str(labelIndex))
            button.setMaximumWidth(150)

            checkBox = QCheckBox()
            checkBox.setText("Lap Prediction ")

            startStopButton = QPushButton()
            startStopButton.setText("Start")
            startStopButton.setMaximumWidth(150)

            predictLabel = ElidedLabel()
            predictLabel.setText("0:00:00")
            # predictLabel.setStyleSheet("QLabel { color: blue; } ")
            predictLabel.setHidden(True)

            self.indexList.append(labelIndex)
            self.labelList.append(label)
            self.buttonList.append(button)
            self.startStopList.append(startStopButton)
            self.checkBoxList.append(checkBox)
            self.predictList.append(predictLabel)

            self.buttons.addWidget(label, labelIndex, self.labelColumn)
            self.buttons.addWidget(button, labelIndex, self.buttonColumn)
            self.buttons.addWidget(startStopButton, labelIndex, self.startStopButtonColumn)
            self.buttons.addWidget(checkBox, labelIndex, self.checkBoxColumn)
            self.buttons.addWidget(predictLabel, labelIndex, self.predictColumn)
            labelIndex += 1

    '''  
        Function: clearLists
        Parameters: self
        Return Value: N/A
        Purpose: unbinds all the signals, clears layout of widget, clears all logical lists needed to create
                 car controls.
    '''

    def clearLists(self):
        self.unBindButtons()
        self.clearLayout(self.buttons)

        self.labelList.clear()
        self.checkBoxList.clear()
        self.buttonList.clear()
        self.startStopList.clear()
        self.predictList.clear()

    '''  
        Function: unBindButtons
        Parameters: self
        Return Value: N/A
        Purpose: Unbinds each button within their corresponding lists, allowing them to be re-bound at a later time.
    '''

    def unBindButtons(self):
        for button in self.buttonList:
            button.clicked.disconnect()

        for checkBox in self.checkBoxList:
            checkBox.toggled.disconnect()

        for button in self.startStopList:
            button.clicked.disconnect()

    '''  
        Function: clearLayout
        Parameters: self, layout
        Return Value: N/A
        Purpose: Deleted widgets and cycles through sub-items to ensure proper deletion in order for more to be 
                 added at a later time.
    '''

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    '''  
        Function: bindButtons
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper to bind functions of Cars related to recording, starting and stopping to buttons within the 
                 widget.
    '''

    def bindButtons(self):
        if len(self.buttonList) == len(self.carStoreRef):
            index = 0
            for button in self.buttonList:
                self.bindButtonRecord(index - 1, button)
                index += 1
            index = 0
            for button in self.startStopList:
                button.clicked.connect(lambda b: self.clickStartStop(index))
                index += 1

    '''  
        Function: bindButtons
        Parameters: self, index, button
        Return Value: N/A
        Purpose: Binds button to the corresponding index given in parameters located within the button list.
    '''

    def bindButtonRecord(self, index, button):
        button.clicked.connect(lambda b: self.clickRecord(index))

    '''  
        Function: bindCheckBoxes
        Parameters: self
        Return Value: N/A
        Purpose: Wrappter to Bind checkboxes to the corresponding index within the checkbox list.
    '''

    def bindCheckBoxes(self):
        if len(self.checkBoxList) == len(self.carStoreRef):
            index = 0
            for checkBox in self.checkBoxList:
                self.bindCheckBox(index, checkBox)
                index += 1

    '''  
        Function: bindCheckBox
        Parameters: self, index, checkBox
        Return Value: N/A
        Purpose: Binds a given checkbox to their corresponding index within checkbox list.
    '''

    def bindCheckBox(self, index, checkBox):
        checkBox.toggled.connect(lambda b: self.handleCheck(index))

    '''  
        Function: handleCheck
        Parameters: self, index
        Return Value: N/A
        Purpose: function used to calculate prediction times if a given checkbox is clicked for a particular car.
    '''

    def handleCheck(self, index):
        if self.checkBoxList[index].isChecked():
            self.predictList[index].setVisible(True)
            # put handle calculation function here
        else:
            self.predictList[index].setHidden(True)

    '''  
        Function: clickRecord
        Parameters: self, index
        Return Value: N/A
        Purpose: Given the particular index, tells the CarStorage to add a laptime to that particular car index.
    '''

    def clickRecord(self, index):
        self.carStoreRef[index - 1].addLapTime()

    '''  
        Function: clickStartStop 
        Parameters: self, index
        Return Value: N/A
        Purpose: used for starting and stopping individual cars.
    '''

    def clickStartStop(self, index):
        self.startStopList[(index - 1)].setText("Stop")
        # toggle start/stop of car here
