"""

    Module:
    Purpose:
    Depends On:

"""

# Standard lib Imports
from datetime import datetime, timedelta

# Dependency Imports
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt

# Package Imports
from SCTimeUtility.Log.Log import getLog


class LeaderBoardModel(QAbstractTableModel):
    def __init__(self, parent, headerData, storage=None):
        super().__init__(parent)

        self.defaultColumns = len(headerData)
        self.defaultRows = 10
        self.header = headerData
        self.carStore = storage
        self.connectActions()

    '''  
        Function: lapsCompletedKey
        Parameters: c
        Return Value: int 
        Purpose: Static method that when invoked returns the amount of laps completed for that particular car as a key.
    '''

    @staticmethod
    def lapsCompletedKey(c):
        return c.getLapCount()

    '''  
        Function: fastestLapKey
        Parameters: c
        Return Value: int 
        Purpose: Static method that when invoked returns the fastest completed for that particular car as a key.
    '''

    @staticmethod
    def fastestLapKey(c):
        return c.getFastestLap()

    '''  
        Function: storageModifiedEvent
        Parameters: self, col, row
        Return Value: N/A
        Purpose: Invoked when data has been modified and provides the location within the leaderboard in where data was
                 actually changed.
    '''

    def storageModifiedEvent(self, col, row):
        leftChangeIndex = self.index(col, 0)
        rightChangeIndex = self.index(col, self.columnCount())
        self.dataChanged.emit(leftChangeIndex, leftChangeIndex)
        self.headerDataChanged.emit(Qt.Vertical, row, row)

    '''  
        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: connects the necessary signals for getting updates of data.
    '''

    def connectActions(self):
        self.carStore.dataModified.connect(self.storageModifiedEvent)

    '''  
        Function: rowCount
        Parameters: self, p 
        Return Value: int
        Purpose: Returns the amount of rows that need to be made in view for leaderboard.
    '''

    def rowCount(self, p):
        return max(len(self.carStore.storageList), self.defaultRows)

    '''  
        Function: columnCount
        Parameters: self, p (if not provided p is None)
        Return Value: int
        Purpose: Returns amount of columns that need to be made in the view for the leaderboard.
    '''

    def columnCount(self, p=None):
        return self.defaultColumns

    '''  
        Function: data
        Parameters: self, item, role
        Return Value: QVariant
        Purpose: Sets the data for the LeaderBoard view based on the item's role, the item itself, otherwise
                 returns an empty QVariant.
    '''

    def data(self, item, role):
        if role == Qt.DisplayRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.carStore.storageList):
                return str(self.getDisplayItemAt(item.row(), item.column()))
            else:
                return QVariant()
        elif role == Qt.UserRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.carStore.storageList):
                return self.getSortItemAt(item.row(), item.column())
            else:
                return QVariant()
        else:
            return QVariant()

    '''  
        Function: headerData
        Parameters: self, section, orientation, role
        Return Value: None or headerValue
        Purpose: Sets the headerData for the LeaderBoard view based on orientation of the section, the role of the
                 section, if it doesn't fit under those categories such as Display or UserRole, its returned as None.
    '''

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < self.defaultColumns:
                    return self.header[section]
                else:
                    return None
        elif role == Qt.UserRole:
            if orientation == Qt.Vertical:
                if section < len(self.carStore.storageList):
                    return section + 1
                else:
                    return None
        elif role == Qt.UserRole + 1:
            if orientation == Qt.Vertical:
                if section < len(self.carStore.storageList):
                    return len(self.carStore.storageList) - section
                else:
                    return None

    '''  
        Function: getDisplayItemAt
        Parameters: self, index, subindex
        Return Value: None/int/str
        Purpose: Returns the item to display of the subindex, in the index of carStorage.
    '''

    def getDisplayItemAt(self, index, subIndex):
        if subIndex == 0:
            return self.carStore.storageList[index].getCarNum()
        elif subIndex == 1:
            return self.carStore.storageList[index].getTeam()
        elif subIndex == 2:
            return max(self.carStore.storageList[index].getLapCount() - 1, 0)
        elif subIndex == 3:
            fastLap = self.carStore.storageList[index].getFastestLap()
            if fastLap is not None:
                return str(timedelta(seconds=fastLap))
            else:
                return ""
        else:
            return None

    '''  
        Function: getSortItemAt
        Parameters: self, index, subindex
        Return Value: None or int
        Purpose: Returns the sorted item under the subindex at the specified index within Car Storage.
    '''

    def getSortItemAt(self, index, subIndex):
        if subIndex == 0:
            return self.carStore.storageList[index].getCarNum()
        elif subIndex == 1:
            return self.carStore.storageList[index].getTeam()
        elif subIndex == 2:
            # This is kind of a hack, but it's the easiest way to
            # ensure that getFastestLAp and getLapCount have
            # compatible orders.
            return -max(self.carStore.storageList[index].getLapCount() - 1, 0)
        elif subIndex == 3:
            return self.carStore.storageList[index].getFastestLap()
        else:
            return None
