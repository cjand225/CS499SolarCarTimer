"""

    Module:
    Purpose:
    Depends On:

"""

import time, os

from PyQt5.QtWidgets import QDialog

from SCTimeUtility.Table import tableUIPath, semiAutoUIPath, addCarDialogUIPath, addBatchCarDialogUIPath
from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.Table.TableModel import TableModel
from SCTimeUtility.Table.TableWidget import TableWidget
from SCTimeUtility.Table.AddCarDialog import AddCarDialog
from SCTimeUtility.Table.AddBatchDialog import AddBatchDialog
from SCTimeUtility.Table.SemiAuto import SemiAuto
from SCTimeUtility.Log.Log import getLog


class Table():

    def __init__(self):
        super().__init__()

        self.logger = getLog()
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

        self.initTable()

    '''

        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads the gui related Resources for Table class module.

    '''

    def initUI(self):
        self.Widget = TableWidget(tableUIPath)
        self.Widget.initHeaderVertical()
        self.Widget.show()
        self.tableView = self.Widget.tableView

    '''

        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: connects all the necessary signals to their functions for use during runtime.

    '''

    def connectActions(self):
        self.tableView.doubleClicked.connect(self.handleTableDoubleClick)
        self.Widget.addCar.clicked.connect(self.handleAddDialog)
        self.Widget.addBatch.clicked.connect(self.handleAddBatchDialog)
        self.Widget.startRace.clicked.connect(self.handleStart)
        self.CarStoreList.dataModified.connect(self.updateSemiAuto)
        self.CarStoreList.dataModified.connect(self.fixHeaders)

    '''

        Function: getTableWidget
        Parameters: self
        Return Value: TableWidget class instance
        Purpose: Returns the instance of TableWidget stored within the Table Class instance.

    '''

    def getTableWidget(self):
        return self.Widget

    '''

        Function: initTableModel
        Parameters: self
        Return Value: N/A
        Purpose: Initializes an instance of the TableModel Class for usage within the Table Class Module.

    '''

    def initTableModel(self):
        self.TableMod = TableModel(self.Widget, self.CarStoreList)
        self.tableView.setModel(self.TableMod)

    '''

        Function: initTable
        Parameters: self
        Return Value: N/A
        Purpose: Initializes all the functional parts related to the Table class, when an instance of it is created.

    '''

    def initTable(self):
        # Model > UI > UIModel
        self.initCarStorage()
        self.initUI()
        self.initTableModel()
        self.fixHeaders()
        self.initDialogs()
        self.initSemiAuto()
        self.connectActions()

    '''

        Function: initCarStorage
        Parameters: self
        Return Value: N/A
        Purpose: Initializes an instance of the CarStorage Class, used as a backend for storing App data.

    '''

    def initCarStorage(self):
        self.CarStoreList = CarStorage()

    '''

        Function: getCarStorage
        Parameters: self
        Return Value: CarStorage Class Instance
        Purpose: Returns a CarStorage class Instance copy to invoker.

    '''

    def getCarStorage(self):
        return self.CarStoreList.getCarListCopy()

    '''

        Function: initSemiAuto
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the Semi Auto class (w/ path to view's UI) that is its own controller for handling
                 semi-automatic recording times for the Table.

    '''

    def initSemiAuto(self):
        self.semiAuto = SemiAuto(semiAutoUIPath)
        self.logger.debug('[' + __name__ + '] ' + 'Semi-Auto Initialized')

    '''

        Function: getSemiAuto
        Parameters: self
        Return Value: SemiAuto class instance
        Purpose: Returns the instance of the SemiAuto class declared within the Table class module to invoker.

    '''

    def getSemiAuto(self):
        return self.semiAuto

    '''

        Function: initDialogs
        Parameters: self
        Return Value: N/A
        Purpose: Initializes dialogs used for adding car data to Table module.

    '''

    def initDialogs(self):
        self.addDialog = AddCarDialog(addCarDialogUIPath)
        self.addBatchDialog = AddBatchDialog(addBatchCarDialogUIPath)

    '''

        Function: createCar
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper function to pass data onto CarStorage's createCar function.
        
    '''

    def createCar(self, carNum, teamName):
        self.CarStoreList.createCar(carNum, teamName)

    '''

        Function: createCars
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper function to pass data onto CarStorage's createCars function.

    '''

    def createCars(self, list):
        self.CarStoreList.createCars(list)

    '''

        Function: handleStart
        Parameters: self
        Return Value: N/A
        Purpose: Sets a seed value when GlobalStart is Clicked.

    '''

    def handleStart(self):
        self.CarStoreList.setSeedValue(time.time())

    '''

        Function: handleTableDoubleClick
        Parameters: self, i
        Return Value: N/A
        Purpose: Invokes the handleAddDialog function when clicking on an unpopulated column.

    '''

    def handleTableDoubleClick(self, i):
        if i.column() == len(self.CarStoreList.storageList):
            self.handleAddDialog()

    '''

        Function: handleAddDialog
        Parameters: self
        Return Value: N/A
        Purpose: Invokes the actual Dialog to probe user for car information.

    '''

    def handleAddDialog(self):
        retval = self.addDialog.exec()
        if retval == QDialog.Accepted:
            self.createCar(self.addDialog.carNumber, self.addDialog.teamName)
            self.addDialog.clearText()

    '''

        Function: handleAddBatchDialog
        Parameters: self
        Return Value: N/A
        Purpose: Invokes the actual Dialog to probe user for car information of multiple cars.

    '''

    def handleAddBatchDialog(self):
        retval = self.addBatchDialog.exec()
        if retval == QDialog.Accepted:
            self.createCars(self.addBatchDialog.getList())
            self.addBatchDialog.clear()

    '''

        Function: handleStart
        Parameters: self
        Return Value: N/A
        Purpose: Updates SemiAuto with new information from within the CarStorage Module

    '''

    def updateSemiAuto(self):
        self.semiAuto.updateList(self.CarStoreList.storageList)

    '''

        Function: adjustHeaders
        Parameters: self
        Return Value: N/A
        Purpose: Temp fix for widget stuff

    '''

    def fixHeaders(self):
        self.Widget.initHeaderHorizontal()
        self.Widget.initHeaderVertical()
