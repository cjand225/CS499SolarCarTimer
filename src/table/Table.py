import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from src.table.CarStorage import CarStorage
from src.table.LapDataTableModel import LapDataTableModel
from src.table.TableWidget import TableWidget


class Table():

    def __init__(self, uiPath):
        super().__init__()
        self.tableUIPath = uiPath

        # things to be initialized later
        self.TableMod = None
        self.Widget = None
        self.CarStoreList = None
        self.saveShortcut = None
        self.tableView = None
        self.semiAuto = None
        self.semiWidget = None

        # Model > UI > UIModel
        self.initCarStorage()
        self.initUI()
        self.initTableModel()
        self.initTable()

        self.tableView.doubleClicked.connect(self.tableClickEvent)

    def initUI(self):
        self.Widget = TableWidget(self.tableUIPath)
        self.tableView = self.Widget.tableView

    def getTableWidget(self):
        return self.Widget

    def initTableModel(self):
        self.TableMod = LapDataTableModel(self.Widget, self.CarStoreList)

    def initTable(self):
        self.tableView.setModel(self.TableMod)

    def initCarStorage(self):
        self.CarStoreList = CarStorage()

    def getCarStorage(self):
        return self.CarStoreList.getCarListCopy()

    def initSemiAuto(self):
        self.semiAuto = None

    def getSemiAutoWidget(self):
        return self.semiWidget


    #TODO: Rework Implementation
    def addCar(self, dialog, newCar=None, ):
        if not newCar:
            newCar = dialog
            if newCar:
                newCar.ID = len(self.table.CarStoreList.storageList)
        if newCar:
            self.table.CarStoreList.addExistingCar(newCar)
            self.mainWindow.semiAutoWidget.addCar(newCar)
            self.graph.addCar(newCar)


    def semiAutoStart(self, car, semiAutoIndex, startTime):
        self.table.CarStoreList.storageList[car.ID].initialTime = startTime

    def semiAutoRecord(self, car, semiAutoIndex, recordedTime):
        if self.table.CarStoreList.storageList[car.ID].LapList:
            elapsedTime = recordedTime - self.table.CarStoreList.storageList[car.ID].LapList[-1].recordedTime
        else:
            elapsedTime = recordedTime - car.initialTime
        self.table.CarStoreList.appendLapTime(car.ID, elapsedTime)

    def tableClickEvent(self, i):
        if i.column() == len(self.CarStoreList.storageList):
            self.addCar()

