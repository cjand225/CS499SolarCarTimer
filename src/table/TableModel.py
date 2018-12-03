from random import randint
from string import ascii_lowercase
import pytimeparse
from datetime import datetime, timedelta
import time

from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QVariant
from src.table.CarStorage import CarStorage
from src.system.TimeReferences import strptimeMultiple, splitTimes, LapTime
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


class TableModel(QAbstractTableModel):
    def __init__(self, parent, cs=None):
        super().__init__(parent)

        self.defaultColumns = 10
        self.defaultRows = 20

        self.assignStorage(cs)
        self.connectActions()
        # self.test()

    def connectActions(self):
        self.carStore.dataModified.connect(self.storageModifiedEvent)

    def storageModifiedEvent(self, col, row):
        changeIndex = self.index(row, col)
        self.dataChanged.emit(changeIndex, changeIndex)
        self.headerDataChanged.emit(Qt.Horizontal, col, col)
        self.headerDataChanged.emit(Qt.Vertical, row, row)

    def rowCount(self, p):
        lapListLengths = [len(i.LapList) for i in self.carStore.storageList]
        if lapListLengths:
            return max(max(lapListLengths) + 1, self.defaultRows)
        else:
            return self.defaultRows

    def columnCount(self, p):
        return max(len(self.carStore.storageList) + 1, self.defaultColumns)

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() < len(self.carStore.storageList) and item.row() < len(
                    self.carStore.storageList[item.column()].LapList):
                timeData = self.carStore.storageList[item.column()].LapList[item.row()].getElapsed()
                newString = self.intergerToTimeString(timeData)
                return str(newString)
            else:
                return QVariant()

    def setData(self, item, value, role):
        formattedValue = self.formatValue(value)
        if formattedValue is not None:
            if role == Qt.EditRole:
                if item.column() < len(self.carStore.storageList) and item.row() == len(
                        self.carStore.storageList[item.column()].LapList):
                    self.carStore.appendLapTime(item.column(), formattedValue)
                else:
                    self.carStore.storageList[item.column()].editLapTime(item.row(), formattedValue)
                return True
            else:
                return False
        else:
            return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.carStore.storageList):
                    return self.carStore.storageList[section].TeamName
                else:
                    return None
            elif orientation == Qt.Vertical:
                lengthList = [len(i.LapList) for i in self.carStore.storageList]
                if lengthList and section < max(lengthList):
                    return section

    def flags(self, i):
        flags = super().flags(i)
        if i.column() < len(self.carStore.storageList) and i.row() <= len(
                self.carStore.storageList[i.column()].LapList) and i.row() > 0:
            flags |= Qt.ItemIsEditable
        return flags

    # takes a time string and converts to workable format
    # def formatValue(self, value):
    #     if (value.isdigit()):
    #         formString = self.valueToTimeString(value)
    #         # print(formString)
    #         return pytimeparse.parse(formString)

    def formatValue(self, value):
        if (value.isdigit()):
            formString = self.valueToTimeString(value)
            return pytimeparse.parse(formString)
        else:
            getDebugLog("Format Value {} was not a digit.".format(value))
            # print("Was not digit.")

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

        #print(formString)

        return formString

    def intergerToTimeString(self, int):
        Days = divmod(int, 24 * 3600)
        Hours = divmod(Days[1], 3600)
        Minutes = divmod(Hours[1], 60)
        Seconds = divmod(Minutes[1], 60)

        Hours = str(Hours[0])
        Minutes = str(Minutes[0])
        Seconds = str(Seconds[1])

        #print(Minutes)
        if len(Hours) == 1:
            Hours = '0' + Hours

        if len(Minutes) == 1:
            Minutes = '0' + Minutes

        if len(Seconds) == 1:
            Seconds = '0' + Seconds

        #print(Hours + ':' + Minutes + ":" + Seconds)

        return Hours + ':' + Minutes + ":" + Seconds

    def assignStorage(self, storage):
        if not storage:
            self.carStore = CarStorage()
        else:
            self.carStore = storage

    def test(self):
        for i, s in enumerate(ascii_lowercase[:8]):
            self.carStore.addCar(s, randint(0, 100))
            self.carStore.storageList[i].initialTime = time.time()
            for j in range(5):
                self.carStore.appendLapTime(i, j)

    def reversed_string(self, string):
        return string[::-1]
