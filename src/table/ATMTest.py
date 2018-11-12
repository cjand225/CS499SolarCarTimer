from random import randint
from string import ascii_lowercase
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractTableModel, QModelIndex
from src.table.CarStorage import CarStorage

class ATMTest(QAbstractTableModel):
    def __init__(self, parent, cs=None):
        super().__init__(parent)
        #self.data = [[randint(0,5) for i in range(10)] for j in range(10)]
        self.cs = CarStorage()
        self.cs.dataModified.connect(self.storageModifiedEvent)
        for i, s in enumerate(ascii_lowercase[:8]):
            self.cs.addCar(i,s,randint(0,100))
            for j in range(5):
                self.cs.appendLapTime(i,randint(1,50),0,0,0)

    def storageModifiedEvent(self,col,row):
        changeIndex = self.index(row,col)
        self.dataChanged.emit(changeIndex,changeIndex)
        self.headerDataChanged.emit(Qt.Horizontal,col,col)
        self.headerDataChanged.emit(Qt.Vertical,row,row)

    def rowCount(self,p):
        return max(max([len(i.LapList) for i in self.cs.storageList])+1,19)

    def columnCount(self,p):
        return max(len(self.cs.storageList),10)

    def data(self,i,role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if i.column()<len(self.cs.storageList) and i.row() < len(self.cs.storageList[i.column()].LapList):
                return self.cs.storageList[i.column()].LapList[i.row()][1]
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
        if role == Qt.EditRole:
            if i.column()<len(self.cs.storageList):
                if  i.row() < len(self.cs.storageList[i.column()].LapList):
                    self.cs.storageList[i.column()].LapList[i.row()][1] = value
                    return True
                elif i.row()==len(self.cs.storageList[i.column()].LapList):
                    self.cs.appendLapTime(i.column(),value,0,0,0)
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
                if section < max([len(i.LapList) for i in self.cs.storageList]):
                    return section

    def flags(self,i):
        flags = super().flags(i)
        if i.column() < len(self.cs.storageList) and i.row() <= len(self.cs.storageList[i.column()].LapList):
            flags |= Qt.ItemIsEditable
        return flags
