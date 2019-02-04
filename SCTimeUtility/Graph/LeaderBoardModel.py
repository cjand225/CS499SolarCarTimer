import pytimeparse
from datetime import datetime, timedelta

from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt
from SCTimeUtility.Log.Log import getLog


class LeaderBoardModel(QAbstractTableModel):
    def __init__(self, parent, headerData, cs=None):
        super().__init__(parent)

        self.defaultColumns = len(headerData)
        self.defaultRows = 10
        # self.dataList = None
        # self.tableList = tableList
        self.header = headerData
        self.carStore = cs
        self.connectActions()
        # self.dataChanged.connect(lambda: print("hello world1"))
        # self.sort = type(self).fastestLapKey
        # self.assignStorage(tableList)

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
        # print("storage modified: ",col)
        leftChangeIndex = self.index(col, 0)
        rightChangeIndex = self.index(col, self.columnCount())
        self.dataChanged.emit(leftChangeIndex, leftChangeIndex)
        # self.headerDataChanged.emit(Qt.Horizontal, col, col)
        self.headerDataChanged.emit(Qt.Vertical, row, row)

    '''  
        Function: connectActions
        Parameters: self
        Return Value: N/A
        Purpose: connects the necessary signals for getting updates of data.
    '''

    def connectActions(self):
        self.carStore.dataModified.connect(self.storageModifiedEvent)

    # def setModelData(self, data):
    #     self.dataList = data

    '''  
        Function: rowCount
        Parameters: self, p 
        Return Value: int
        Purpose: Returns the amount of rows that need to be made in view for leaderboard.
    '''

    def rowCount(self, p):
        # print(max(len(self.carStore.storageList),self.defaultRows))
        return max(len(self.carStore.storageList), self.defaultRows)

    '''  
        Function: columnCount
        Parameters: self, p (if not provided p is None)
        Return Value: int
        Purpose: Returns amount of columns that need to be made in the view for the leaderboard.
    '''

    def columnCount(self, p=None):
        return self.defaultColumns

    # def setData(self, item, value, role):
    #     if role == Qt.EditRole:

    # if role == Qt.DisplayRole:
    #     if (item.column() < self.defaultColumns) and item.row() < len(self.dataList):
    #         return str(self.getItemAt(item.row(), item.column()))
    #     else:
    #         return QVariant()
    # else:
    #     return QVariant()

    '''  
        Function: data
        Parameters: self, item, role
        Return Value: QVariant
        Purpose: Sets the data for the LeaderBoard view based on the item's role, the item itself, otherwise
                 returns an empty QVariant.
    '''

    def data(self, item, role):
        # print("data called")
        if role == Qt.DisplayRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.carStore.storageList):
                # print("Item at...")
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
        Function: formatValue
        Parameters: self, value
        Return Value: str
        Purpose: Returns a formatted parsed string using pytimeparse when given a value.
    '''

    # takes a time string and converts to workable format
    def formatValue(self, value):
        if (value.isdigit()):
            formString = self.valueToTimeString(value)
            return pytimeparse.parse(formString)

    '''  
        Function: valueToTimeString
        Parameters: self, value
        Return Value: str
        Purpose: Returns a time formatted string based on a given value.
    '''

    def valueToTimeString(self, val):
        timeList = [val[i:i + 2] for i in range(0, len(val), 2)]
        formString = ''

        for x in range(0, len(timeList)):
            if len(timeList[x]) < 2:
                newString = timeList[x] + '0'
                newString = self.reversed_string(newString)
                timeList[x] = newString

        timeList.reverse()

        for x in range(0, len(timeList)):
            if x != 0:
                formString = formString + ':' + timeList[x]
            else:
                formString = formString + timeList[x]

        if len(formString) <= 2:
            formString = formString + "s"

        return formString

    '''  
        Function: integerToTimeString
        Parameters: self, int
        Return Value: str
        Purpose: Converts a given int to a time formatted string.
    '''

    def intergerToTimeString(self, int):
        Hours = divmod(int, 3600)
        Minutes = divmod(int, 60)
        Seconds = divmod(int, 60)

        Hours = str(Hours[0])
        Minutes = str(Minutes[0])
        Seconds = str(Seconds[1])

        if len(Hours) == 1:
            Hours = '0' + Hours

        if len(Minutes) == 1:
            Minutes = '0' + Minutes

        if len(Seconds) == 1:
            Seconds = '0' + Seconds

        return Hours + ':' + Minutes + ":" + Seconds

    # def assignStorage(self, storage):
    #     if not storage:
    #         self.dataList = []
    #     else:
    #         self.dataList = storage

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
