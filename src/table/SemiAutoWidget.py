import os
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QBrush, QPalette
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


import sched, time

# Semi-Auto Button Widget
from src.table.Car import Car
from src.table.ElidedLabel import ElidedLabel


class SemiAutoWidget(QWidget):
    carRecord = pyqtSignal(object, int, float)
    startClicked = pyqtSignal(object, int, float)
    predictClicked = pyqtSignal(object, bool, int)
    labelColumn = 0
    buttonColumn = 1
    boxColumn = 2
    predictColor = Qt.green

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self._cars = []

        self.initUI()
        self.initButtonLayout()

    def initButtonLayout(self):
        self.buttonsLayout.setAlignment(Qt.AlignTop)
        self.buttonsLayout.setColumnMinimumWidth(type(self).labelColumn, 100)
        self.buttonsLayout.setColumnMinimumWidth(type(self).boxColumn, 100)
        self.buttonsLayout.setHorizontalSpacing(15)
        self.buttonsLayout.setColumnStretch(type(self).labelColumn, 1)
        self.buttonsLayout.setColumnStretch(type(self).buttonColumn, 1)
        self.buttonsLayout.setColumnStretch(type(self).boxColumn, 0)

    @property
    def cars(self):
        return self._cars

    def deleteAllCars(self):
        self._cars = []
        for i in reversed(range(self.buttonsLayout.count())):
            widget = self.buttonsLayout.itemAt(i).widget()
            self.buttonsLayout.removeWidget(widget)
            widget.setParent(None)
        # for index in reversed(range(len(self._cars))):
        #     self.deleteCarAtIndex(index)

    def recordCar(self, car, carIndex):
        self.carRecord.emit(car, carIndex, time.time())

    def setCar(self, index, car):
        self._cars[index] = car
        self.buttonsLayout.itemAtPosition(index, type(self).labelColumn).widget().setText(car.OrgName)
        recordWidget = self.buttonsLayout.itemAtPosition(index, type(self).buttonColumn).widget()
        recordWidget.clicked.disconnect()
        if car.initialTime:
            recordWidget.clicked.connect(lambda b: self.recordCar(car, index))
            recordWidget.setText("Record time")
        else:
            recordWidget.clicked.connect(lambda b: self.startCar(car, index))
        predictWidget = self.buttonsLayout.itemAtPosition(index, type(self).boxColumn).widget()
        predictWidget.clicked.disconnect()
        predictWidget.clicked.connect(lambda b: self.predictClicked.emit(car, b, index))

    def deleteCar(self, car):
        carIndex = self._cars.index(car)
        self.deleteCarAtIndex(carIndex)

    def deleteCarAtIndex(self, carIndex):
        for i in range(3):
            widget = self.buttonsLayout.itemAtPosition(carIndex, i).widget()
            self.buttonsLayout.removeWidget(widget)
            widget.disconnect()
        for i in range(carIndex + 1, len(self._cars)):
            for j in range(3):
                widget = self.buttonsLayout.itemAtPosition(i, j).widget()
                self.buttonsLayout.removeWidget(widget)
                self.buttonsLayout.addWidget(widget, i - 1, j)
        del self._cars[carIndex]

    def clickRecord(self, index):
        recordWidget = self.buttonsLayout.itemAtPosition(index, type(self).buttonColumn).widget()
        recordWidget.animateClick()

    def clickPredict(self, index):
        predictWidget = self.buttonsLayout.itemAtPosition(index, type(self).boxColumn).widget()
        predictWidget.animateClick()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    def startCar(self, car, carIndex):
        self.startClicked.emit(car, carIndex, time.time())
        recordButton = self.buttonsLayout.itemAtPosition(carIndex, type(self).buttonColumn).widget()
        recordButton.setText("Record time")
        recordButton.clicked.disconnect()
        recordButton.clicked.connect(lambda b: self.recordCar(car, carIndex))

    def addCar(self, car):
        carIndex = len(self._cars)
        carLabel = ElidedLabel(car.OrgName)
        carLabel.setMaximumWidth(225)
        self.buttonsLayout.addWidget(carLabel, carIndex, type(self).labelColumn)
        recordButton = QPushButton()
        self.buttonsLayout.addWidget(recordButton, carIndex, type(self).buttonColumn)
        checkBox = QCheckBox("Predict laps")
        self.buttonsLayout.addWidget(checkBox, carIndex, type(self).boxColumn, Qt.AlignCenter)
        self._cars.append(car)
        if car.initialTime:
            recordButton.clicked.connect(lambda b: self.recordCar(car, carIndex))
            recordButton.setText("Record time")
        else:
            recordButton.clicked.connect(lambda b: self.startCar(car, carIndex))
            recordButton.setText("Start")
        checkBox.clicked.connect(lambda b: self.predictClicked.emit(car, b, carIndex))

    def showPredict(self, car):
        carIndex = self._cars.index(car)
        self.showPredictAtIndex(carIndex)

    def showPredictAtIndex(self, carIndex):
        buttonWidget = self.buttonsLayout.itemAtPosition(carIndex, type(self).buttonColumn).widget()
        palette = QPalette()
        palette.setColor(buttonWidget.backgroundRole(), type(self).predictColor)
        buttonWidget.setPalette(palette)

    def clearPredict(self, car):
        carIndex = self._cars.index(car)
        self.clearPredictAtIndex(carIndex)

    def clearPredictAtIndex(self, carIndex):
        buttonWidget = self.buttonsLayout.itemAtPosition(carIndex, type(self).buttonColumn).widget()
        palette = QPalette()
        # palette.setColor(buttonWidget.backgroundRole(),QBrush())
        buttonWidget.setPalette(palette)
