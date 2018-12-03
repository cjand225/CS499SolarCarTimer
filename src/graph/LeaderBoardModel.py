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
    def __init__(self, parent, headerData, tableList=None):
        super().__init__(parent)

        self.defaultColumns = 5
        self.defaultRows = 10
        self.dataList = None
        self.tableList = tableList
        self.header = headerData
        self.assignStorage(tableList)

    def setModelData(self, data):
        self.dataList = data

    def rowCount(self, p):
        if len(self.dataList) > self.defaultRows:
            return len(self.dataList)
        else:
            return self.defaultRows

    def columnCount(self, p):
        return self.defaultColumns

    def setData(self, item, value, role):
        if role == Qt.DisplayRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.dataList):
                return str(self.getItemAt(item.row(), item.column()))
            else:
                return QVariant()
        else:
            return QVariant()

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if (item.column() < self.defaultColumns) and item.row() < len(self.dataList):
                return str(self.getItemAt(item.row(), item.column()))
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

    def assignStorage(self, storage):
        if not storage:
            self.dataList = []
        else:
            self.dataList = storage

    def getItemAt(self, index, subIndex):
        if subIndex == 0:
            return self.dataList[index].getID() + 1
        elif subIndex == 1:
            return self.dataList[index].getCarNum()
        elif subIndex == 2:
            return self.dataList[index].getTeam()
        elif subIndex == 3:
            return self.dataList[index].getFastestLap()
        elif subIndex == 4:
            return self.dataList[index].getLapCount()
        else:
            return None
