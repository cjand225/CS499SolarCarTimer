from random import randint
from string import ascii_lowercase
from datetime import datetime, timedelta
import time
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from src.table.CarStorage import CarStorage
from src.system.Time import strptimeMultiple

class LapDataTableModel(QAbstractTableModel):
    def __init__(self, parent, cs=None):
        super().__init__(parent)
        #self.data = [[randint(0,5) for i in range(10)] for j in range(10)]
        if not cs:
            cs = CarStorage()
        self.cs = cs
        self.cs.dataModified.connect(self.storageModifiedEvent)
        # for i, s in enumerate(ascii_lowercase[:8]):
        #     self.cs.addCar(i,s,randint(0,100))
        #     self.cs.storageList[i].initialTime = time.time()
        #     for j in range(5):
        #         self.cs.appendLapTime(i,j)

    def storageModifiedEvent(self,col,row):
        changeIndex = self.index(row,col)
        self.dataChanged.emit(changeIndex,changeIndex)
        self.headerDataChanged.emit(Qt.Horizontal,col,col)
        self.headerDataChanged.emit(Qt.Vertical,row,row)

    def rowCount(self,p):
        lapListLengths = [len(i.LapList) for i in self.cs.storageList]
        if lapListLengths:
            return max(max(lapListLengths)+1,19)
        else:
            return 19

    def columnCount(self,p):
        return max(len(self.cs.storageList),10)

    def data(self,i,role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if i.column()<len(self.cs.storageList) and i.row() < len(self.cs.storageList[i.column()].LapList):
                return str(self.cs.storageList[i.column()].LapList[i.row()])
            else:
                return None

    # def addCar(self,carOrg,carNum):
    #     self.cs.addCar(len(self.cs.storageList),carOrg,carNum)
    #     changeIndex = self.index(len(self.cs.storageList)-1,0)
    #     self.dataChanged.emit(changeIndex,changeIndex)
    #     self.headerDataChanged.emit(Qt.Horizontal,len(self.cs.storageList)-1,len(self.cs.storageList)-1)

    # def addLapTime(self,carNum,time):
    #     self.cs.appendLapTime(carNum,time,0,0,0)
    #     changeIndex = self.index(len(self.cs.storageList[carNum].LapList)-1,carNum)
    #     self.dataChanged.emit(changeIndex,changeIndex)
    #     self.headerDataChanged.emit(Qt.Vertical,len(self.cs.storageList[carNum].LapList)-1,len(self.cs.storageList[carNum].LapList)-1)
        
    def setData(self,i,value,role):
        try:
            value_split = value.split(".")
            value_time = strptimeMultiple(value_split[0],["%H:%M:%S","%M:%S","%S"])
            seconds = timedelta(hours=value_time.hour,minutes=value_time.minute,seconds=value_time.second).total_seconds()
            if len(value_split) == 2:
                milliseconds = int(value_split[1])
                seconds = seconds + (milliseconds/pow(10,len(value_split[1])))
            elif len(value_split) > 2:
                return False
        except ValueError:
            return False
        if role == Qt.EditRole:
            if i.column()<len(self.cs.storageList):
                if not self.cs.storageList[i.column()].initialTime:
                    self.cs.storageList[i.column()].initialTime = time.time()
                #lapTime = Lap_Time(self.cs.storageList[i.column()-1].recordedTime+seconds,seconds)
                if  i.row() < len(self.cs.storageList[i.column()].LapList):
                    #self.cs.storageList[i.column()].LapList[i.row()][1] = value
                    self.cs.storageList[i.column()].editLapTime(i.row(),seconds)
                    return True
                elif i.row()==len(self.cs.storageList[i.column()].LapList):
                    self.cs.appendLapTime(i.column(),seconds)
                    return True
            else:
                return False

    def headerData(self,section,orientation,role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.cs.storageList):
                    return self.cs.storageList[section].OrgName
                else:
                    return None
            elif orientation == Qt.Vertical:
                lengthList = [len(i.LapList) for i in self.cs.storageList]
                if lengthList and section < max(lengthList):
                    return section

    def flags(self,i):
        flags = super().flags(i)
        if i.column() < len(self.cs.storageList) and i.row() <= len(self.cs.storageList[i.column()].LapList):
            flags |= Qt.ItemIsEditable
        return flags
