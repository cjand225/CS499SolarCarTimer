"""

    Module:
    Purpose:
    Depends On:

"""

import datetime

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtGui import QColor

from SCTimeUtility.Table.CarStorage import CarStorage
from SCTimeUtility.System.TimeReferences import strptimeMultiple
from SCTimeUtility.Log.Log import getLog


class TableModel(QAbstractTableModel):
    def __init__(self, parent, cs=None):
        super().__init__(parent)

        self.defaultColumns = 10
        self.defaultRows = 20

        self.assignStorage(cs)
        self.connectActions()

    '''
        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: connects the necessary signals/slots to the corresponding functions, which
                 are used to update the model.

    '''

    def connectActions(self):
        self.carStore.dataModified.connect(self.storageModifiedEvent)

    '''
        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: Wrapper function for emitting signals and getting proper index of a cell in the front end
                 or an item in the backend has changed in any way.

    '''

    def storageModifiedEvent(self, col, row):
        changeIndex = self.index(row, col)
        self.dataChanged.emit(changeIndex, changeIndex)
        self.headerDataChanged.emit(Qt.Horizontal, col, col)
        self.headerDataChanged.emit(Qt.Vertical, row, row)

    '''
        Function: rowCount
        Parameters: self, p
        Return Value: N/A
        Purpose: Overloaded PyQt TableModel function, returns the amount of rows that should be in the Table,
                 based on either a default amount or the amount of Laps within each Car class instance.

    '''

    def rowCount(self, p):
        lapListLengths = [len(i.lapList) for i in self.carStore.storageList]
        if lapListLengths:
            return max(max(lapListLengths) + 1, self.defaultRows)
        else:
            return self.defaultRows

    '''
        Function: columnCount
        Parameters: self
        Return Value: N/A
        Purpose: Overloaded PyQt TableModel function, returns the amount of columns that should be in the Table,
                 based on either a default amount or the amount of Cars within CarStorage class instance.

    '''

    def columnCount(self, p):
        return max(len(self.carStore.storageList) + 1, self.defaultColumns)

    '''
        Function: data
        Parameters: self, item, role (default = Qt.DisplayRole)
        Return Value: QVariant() or converted time string
        Purpose: Overloaded PyQt TableModel function, which controls the flow of data between the user
                 and the CarStorage Class instance, based on item entry (items are normally cells from 
                 tableView that have either no data or some time data to be stored and/or currently stored.

    '''

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() < len(self.carStore.storageList) and \
                    item.row() < len(self.carStore.storageList[item.column()].lapList):
                timeData = self.carStore.storageList[item.column()].lapList[item.row()].getElapsed()
                newString = str(datetime.timedelta(seconds=timeData))
                return QVariant(str(newString))
            else:
                return QVariant('')
        if role == Qt.BackgroundRole:
            if item.column() > len(self.carStore.storageList):
                return QColor(Qt.darkGray)
            elif len(self.carStore.storageList) > item.column() and not self.carStore.storageList[item.column()].isRunning():
                return QColor(Qt.lightGray)
            elif not len(self.carStore.storageList) > item.column():
                return QColor(Qt.darkGray)
            else:
                return QColor(Qt.white)

    '''
        Function: setData
        Parameters: self
        Return Value: Boolean Condition
        Purpose: Overloaded PyQt TableModel function, used when actually changing data within a particular cell
                 of the tableView.

    '''

    def setData(self, i, value, role):
        try:
            value_time = strptimeMultiple(value, ["%H:%M:%S", "%M:%S", "%S"])
            delta = datetime.timedelta(hours=value_time.hour, minutes=value_time.minute, seconds=value_time.second)
        except ValueError:
            return False
        if role == Qt.EditRole:
            if i.column() < len(self.carStore.storageList):
                if i.row() < len(self.carStore.storageList[i.column()].lapList):
                    self.carStore.storageList[i.column()].editLapTime(i.row(), delta)
                    return True
                elif i.row() == len(self.carStore.storageList[i.column()].lapList):
                    self.carStore.appendLapTime(i.column(), delta)
                    return True
            else:
                return False

    '''
        Function: headerData
        Parameters: self, section, orientation, role
        Return Value: Boolean Condition
        Purpose: Overloaded PyQt TableModel function, used for populating the header data for both
                 vertical and horizontal headers effectively labeling rows/columns with custom data.

    '''

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.carStore.storageList):
                    return self.carStore.storageList[section].TeamName
                else:
                    return None
            elif orientation == Qt.Vertical:
                lengthList = [len(i.lapList) for i in self.carStore.storageList]
                if lengthList and section < max(lengthList):
                    return section

    '''
        Function: flags
        Parameters: self, i
        Return Value: Boolean Condition
        Purpose: Overloaded PyQt TableModel function, Boolean check used to flag which cells are able to be edited.

    '''

    def flags(self, i):
        flags = super().flags(i)
        if i.column() < len(self.carStore.storageList) and i.row() <= len(
                self.carStore.storageList[i.column()].lapList) and i.row() > 0:
            if self.carStore.storageList[i.column()].isRunning():
                flags |= Qt.ItemIsEditable
            else:
                pass

        return flags

    '''  
        Function: assignStorage
        Parameters: self, storage
        Return Value: Boolean Cond 
        Purpose: gives a reference of the CarStorage Class instance
    '''

    def assignStorage(self, storage):
        if isinstance(storage, CarStorage):
            self.carStore = storage
