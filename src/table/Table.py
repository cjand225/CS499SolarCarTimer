import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import time
import os
from src.system.Validation import *
from src.table.CarStorage import CarStorage
from src.table.LapDataTableModel import LapDataTableModel
from src.table.TableModel import TableModel
from src.table.TableWidget import TableWidget
from src.table.AddCarDialog import AddCarDialog
from src.table.SemiAutoWidget import SemiAutoWidget
from src.table.AddBatchDialog import AddBatchDialog
from src.table.SemiAuto import SemiAuto

from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class Table():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../../resources"))
    tableUIPath = os.path.join(resourcesDir, 'TableView.ui')
    semiAutoUIPath = os.path.join(resourcesDir, 'SemiAuto.ui')
    addCarDialogUIPath = os.path.join(resourcesDir, 'addCarDialog.ui')
    addBatchCarDialogUIPath = os.path.join(resourcesDir, 'AddBatchDialog.ui')

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
        self.addBatchDialog = None

        # Model > UI > UIModel
        self.initCarStorage()
        self.initUI()
        self.initTableModel()
        self.initTable()
        self.initDialogs()
        self.initSemiAuto()
        self.connectActions()

    def initUI(self):
        self.Widget = TableWidget(self.tableUIPath)
        self.tableView = self.Widget.tableView

    def connectActions(self):
        self.tableView.doubleClicked.connect(self.handleTableDoubleClick)
        self.Widget.addCar.clicked.connect(self.handleAddDialog)
        self.Widget.addBatch.clicked.connect(self.handleAddBatchDialog)
        self.Widget.startRace.clicked.connect(self.handleStart)

    def getTableWidget(self):
        return self.Widget

    def initTableModel(self):
        #self.TableMod = LapDataTableModel(self.Widget, self.CarStoreList)
        self.TableMod = TableModel(self.Widget, self.CarStoreList)

    def initTable(self):
        self.tableView.setModel(self.TableMod)

    def initCarStorage(self):
        self.CarStoreList = CarStorage()

        self.CarStoreList.createCar(1,1)
        self.CarStoreList.createCar(2, 2)


    def getCarStorage(self):
        return self.CarStoreList.getCarListCopy()

    '''

        Function: initSemiAuto(self)
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Semi Auto class (w/ path to view's UI) that is its own controller for handling
                 semi-automatic recording times for the table.

    '''

    def initSemiAuto(self):
        self.semiAuto = SemiAuto(type(self).semiAutoUIPath)
        getDebugLog().debug('[' + __name__ + '] ' + 'Semi-Auto Initialized')

    def getSemiAuto(self):
        return self.semiAuto

    def initDialogs(self):
        self.addDialog = AddCarDialog(self.addCarDialogUIPath)
        self.addBatchDialog = AddBatchDialog(self.addBatchCarDialogUIPath)

    def createCar(self, carNum, teamName):
        self.CarStoreList.createCar(carNum, teamName)
        getInfoLog().debug('[' + __name__ + '] ' + 'Car Created: ' + ' (' + str(carNum) + ',' + str(teamName) + ')')

    def createCars(self, list):
        self.CarStoreList.createCars(list)

    def handleStart(self):
        self.CarStoreList.setSeedValue(time.time())

    def handleTableDoubleClick(self, i):
        if i.column() == len(self.CarStoreList.storageList):
            self.handleAddDialog()

    def handleAddDialog(self):
        retval = self.addDialog.exec()
        if retval == QDialog.Accepted:
            self.createCar(self.addDialog.carNumber, self.addDialog.teamName)
            self.addDialog.clearText()

    def handleAddBatchDialog(self):
        retval = self.addBatchDialog.exec()
        if retval == QDialog.Accepted:
            self.createCars(self.addBatchDialog.getList())
            self.addBatchDialog.clear()

    def updateSemiAuto(self):
        self.semiAuto.updateList(self.CarStoreList.storageList)