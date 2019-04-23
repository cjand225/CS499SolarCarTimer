"""

    Module:
    Purpose:
    Depends On:

"""
from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

from collections import OrderedDict

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

        self.carStore = None
        self.carStoreRef = []

        self.carLabel = 0
        self.RecordButton = 1
        self.PredictLabel = 2
        self.CheckBox = 3
        self.StartButton = 4

        self.buttonDict = OrderedDict()

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
        self.move(self.x(), self.y())

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
        self.addButtons()

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

            self.buttonDict.update({labelIndex: [label, button, predictLabel, checkBox, startStopButton]})

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
        self.buttonDict.clear()
        self.clearLayout(self.buttons)

    '''  
        Function: unBindButtons
        Parameters: self
        Return Value: N/A
        Purpose: Unbinds each button within their corresponding lists, allowing them to be re-bound at a later time.
    '''

    def unBindButtons(self):
        for buttonList in self.buttonDict:
            self.buttonDict[buttonList][self.RecordButton].clicked.disconnect()
            self.buttonDict[buttonList][self.StartButton].clicked.disconnect()
            self.buttonDict[buttonList][self.CheckBox].toggled.disconnect()

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
        for buttonList in self.buttonDict:
            self.bindButtonRecord(buttonList, self.buttonDict[buttonList][self.RecordButton])
            self.bindStartStop(buttonList, self.buttonDict[buttonList][self.StartButton])
            self.bindCheckBox(buttonList, self.buttonDict[buttonList][self.CheckBox])

    def addButtons(self):
        for buttonList in self.buttonDict:
            self.buttons.addWidget(self.buttonDict[buttonList][self.carLabel], buttonList, self.labelColumn)
            self.buttons.addWidget(self.buttonDict[buttonList][self.RecordButton], buttonList, self.buttonColumn)
            self.buttons.addWidget(self.buttonDict[buttonList][self.StartButton], buttonList,
                                   self.startStopButtonColumn)
            self.buttons.addWidget(self.buttonDict[buttonList][self.PredictLabel], buttonList, self.checkBoxColumn)
            self.buttons.addWidget(self.buttonDict[buttonList][self.CheckBox], buttonList, self.predictColumn)

    '''  
        Function: bindButtons
        Parameters: self, index, button
        Return Value: N/A
        Purpose: Binds button to the corresponding index given in parameters located within the button list.
    '''

    def bindButtonRecord(self, index, button):
        button.clicked.connect(lambda b: self.clickRecord(index))

    '''  
        Function: bindCheckBox
        Parameters: self, index, checkBox
        Return Value: N/A
        Purpose: Binds a given checkbox to their corresponding index within checkbox list.
    '''

    def bindCheckBox(self, index, checkBox):
        checkBox.toggled.connect(lambda b: self.handleCheck(self.carStoreRef[index].ID))

    def bindStartStop(self, index, button):
        button.clicked.connect(lambda b: self.toggleCar(self.carStoreRef[index].ID))

    def bindRunning(self, index):
        car = self.carStoreRef[index]
        car.runningSignal.connect(lambda b: self.clickStartStop(self.carStoreRef[index].ID))

    '''  
        Function: handleCheck
        Parameters: self, index
        Return Value: N/A
        Purpose: function used to calculate prediction times if a given checkbox is clicked for a particular car.
    '''

    def handleCheck(self, ID):
        if self.buttonDict[ID][self.CheckBox].isChecked():
            self.buttonDict[ID][self.PredictLabel].setVisiible(True)
            # put handle calculation function here
        else:
            self.buttonDict[ID][self.PredictLabel].setHidden(True)

    '''  
        Function: clickRecord
        Parameters: self, index
        Return Value: N/A
        Purpose: Given the particular index, tells the CarStorage to add a laptime to that particular car index.
    '''

    def clickRecord(self, ID):
        self.carStoreRef[ID].addLapTime()

    '''  
        Function: clickStartStop 
        Parameters: self, index
        Return Value: N/A
        Purpose: used for starting and stopping individual cars.
    '''

    def clickStartStop(self, ID):
        if not self.carStoreRef[ID].isRunning():
            self.buttonDict[ID][self.StartButton].setText("Start")
        else:
            self.buttonDict[ID][self.StartButton].setText("Stop")

    '''  
        Function: toggleCar
        Parameters: self, index
        Return Value: N/A
        Purpose: used for starting and stopping individual cars.
    '''

    def toggleCar(self, ID):
        if self.carStoreRef[ID].isRunning():
            self.carStoreRef[ID].stop()
            # Disabled Buttons for specific car
            self.buttonDict[ID][self.RecordButton].setDisabled(True)
            self.buttonDict[ID][self.CheckBox].setDisabled(True)
        elif not self.carStoreRef[ID].isRunning():
            self.carStoreRef[ID].start()
            # Re-enable buttons for specific car
            self.buttonDict[ID][self.RecordButton].setDisabled(False)
            self.buttonDict[ID][self.CheckBox].setDisabled(False)
