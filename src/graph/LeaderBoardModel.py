from random import randint
from string import ascii_lowercase
import pytimeparse
from datetime import datetime, timedelta
import time

from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant
from src.system.TimeReferences import strptimeMultiple, splitTimes, LapTime
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class LeaderBoardModel(QAbstractTableModel):
    @staticmethod
    def lapsCompletedKey(c):
        return c.getLapCount()

    @staticmethod
    def fastestLapKey(c):
        return c.getFastestLap()
    
    def __init__(self, parent, headerData, cs=None):
        super().__init__(parent)

        self.defaultColumns = len(headerData)
        self.defaultRows = 10
        # self.dataList = None
        # self.tableList = tableList
        self.header = headerData
        self.carStore = cs
        self.connectActions()
        #self.dataChanged.connect(lambda: print("hello world1"))
        #self.sort = type(self).fastestLapKey
        #self.assignStorage(tableList)

    def storageModifiedEvent(self,col,row):
        # print("storage modified: ",col)
        leftChangeIndex = self.index(col, 0)
        rightChangeIndex = self.index(col, self.columnCount())
        self.dataChanged.emit(leftChangeIndex, leftChangeIndex)
        # self.headerDataChanged.emit(Qt.Horizontal, col, col)
        self.headerDataChanged.emit(Qt.Vertical, row, row)
            

    def connectActions(self):
        self.carStore.dataModified.connect(self.storageModifiedEvent)

    # def setModelData(self, data):
    #     self.dataList = data

    def rowCount(self, p):
        #print(max(len(self.carStore.storageList),self.defaultRows))
        return max(len(self.carStore.storageList),self.defaultRows)

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

    def data(self, item, role):
        #print("data called")
        if role == Qt.DisplayRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.carStore.storageList):
                #print("Item at...")
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
                    return section+1
                else:
                    return None
        elif role == Qt.UserRole+1:
            if orientation == Qt.Vertical:
                if section < len(self.carStore.storageList):
                    return len(self.carStore.storageList)-section
                else:
                    return None

    # takes a time string and converts to workable format
    def formatValue(self, value):
        if (value.isdigit()):
            formString = self.valueToTimeString(value)
            return pytimeparse.parse(formString)

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

    def getDisplayItemAt(self, index, subIndex):
        if subIndex == 0:
            return self.carStore.storageList[index].getCarNum()
        elif subIndex == 1:
            return self.carStore.storageList[index].getTeam()
        elif subIndex == 2:
            return max(self.carStore.storageList[index].getLapCount()-1,0)
        elif subIndex == 3:
            fastLap = self.carStore.storageList[index].getFastestLap()
            if fastLap is not None:
                return str(timedelta(seconds=fastLap))
            else:
                return ""
        else:
            return None

    def getSortItemAt(self, index, subIndex):
        if subIndex == 0:
            return self.carStore.storageList[index].getCarNum()
        elif subIndex == 1:
            return self.carStore.storageList[index].getTeam()
        elif subIndex == 2:
            # This is kind of a hack, but it's the easiest way to
            # ensure that getFastestLAp and getLapCount have
            # compatible orders.
            return -max(self.carStore.storageList[index].getLapCount()-1,0)
        elif subIndex == 3:
            return self.carStore.storageList[index].getFastestLap()
        else:
            return None
