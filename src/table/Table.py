import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import os
from src.table.CarStorage import CarStorage
from src.table.LapDataTableModel import LapDataTableModel
from src.table.TableWidget import TableWidget
from src.table.AddCarDialog import AddCarDialog
from src.table.SemiAutoWidget import SemiAutoWidget


class Table():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../../resources"))
    tableUIPath = os.path.join(resourcesDir, 'TableView.ui')
    semiAutoUIPath = os.path.join(resourcesDir, 'SemiAuto.ui')
    addCarDialogUIPath = os.path.join(resourcesDir, 'addCarDialog.ui')

    def __init__(self):
        super().__init__()


        # things to be initialized later
        self.TableMod = None
        self.Widget = None
        self.CarStoreList = None
        self.saveShortcut = None
        self.tableView = None
        self.semiAuto = None
        self.semiWidget = None
        self.addDialog = None


        # Model > UI > UIModel
        self.initCarStorage()
        self.initUI()
        self.initTableModel()
        self.initTable()
        self.initDialog()
        self.initSemiAuto()
        self.connectActions()



    def initUI(self):
        self.Widget = TableWidget(self.tableUIPath)
        self.tableView = self.Widget.tableView

    def connectActions(self):
        self.tableView.doubleClicked.connect(self.tableClickEvent)
        self.Widget.addCar.clicked.connect(self.handleDialog)


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

    def createCar(self, carNum, carOrg):
        if carNum is not None and carNum != '':
            if carOrg is not None and carNum != '':
                print("PH")


    '''
    
    '''
    def initDialog(self):
        self.addDialog = AddCarDialog(self.addCarDialogUIPath)

    '''
    
    '''
    def handleDialog(self):
        retval = self.addDialog.exec()

    '''

        Function: initSemiAuto(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Semi Auto class (w/ path to view's UI) that is its own controller for handling
                 semi-automatic recording times for the table.

    '''

    def initSemiAuto(self):
        self.semiAuto = SemiAutoWidget(type(self).semiAutoUIPath)
        #self.log.debug('[' + __name__ + '] ' + 'Semi-Auto Initialized')

    def getSemiAuto(self):
        return self.semiAuto


    # def addCarDialog(self):
    #     carDialog = AddCarDialog(src.app.App.App.addCarDialogUIPath)
    #     retVal = carDialog.exec()
    #     if retVal == QDialog.Accepted:
    #         carNumber = int(carDialog.carNumber)
    #         return Car(0, carDialog.teamName, carNumber)
    #     else:
    #         return None



