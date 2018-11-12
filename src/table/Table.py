import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from src.table.CarStorage import CarStorage
from src.table.LapDataTableModel import LapDataTableModel


class Table():

    def __init__(self, uiPath):
        super().__init__()
        self.tableUIPath = uiPath

        # things to be initalized later
        self.TableMod = None
        self.Table = None
        self.CarStoreList = None
        # self.TableView = None

        # Model > UI > UIModel
        self.initCarStorage()
        self.initUI()
        self.initTableModel()

        self.tableView.setModel(self.TableMod)

        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        minSize = 0
        for headerIndex in range(len(self.tableView.horizontalHeader())):
            minSize = min(minSize,self.tableView.horizontalHeader().sectionSize(headerIndex))
        self.tableView.horizontalHeader().setMinimumSectionSize(minSize)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        minSize = 0
        for headerIndex in range(len(self.tableView.verticalHeader())):
            minSize = min(minSize,self.tableView.verticalHeader().sectionSize(headerIndex))
        self.tableView.verticalHeader().setMinimumSectionSize(minSize)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # for i in range(8,20):
        #     self.tableView.model().cs.addCar(i,"foo{0}".format(i),20)
            #self.tableView.model().cs.appendLapTime(i,91,0,0,0)
        # print(self.tableView.model().columnCount(None))
        # self.tableView.repaint()
        # for i in range(1,20):
        #     self.tableView.model().cs.appendLapTime(5,i,0,0,0)

    def initUI(self):
        self.Table = QWidget()

        self.ui = loadUi(self.tableUIPath, self.Table)
        self.Table.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter,
                                                  self.Table.size(), QApplication.desktop().availableGeometry()))
        self.tableView = self.Table.tableView
        self.Table.show()

    def getTableWidget(self):
        return self.Table

    def initTableModel(self):
        self.TableMod = LapDataTableModel(self.Table,self.CarStoreList)

    def initCarStorage(self):
        self.CarStoreList = CarStorage()
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.addCar(0, "WEE", 43)
    #     self.CarStoreList.appendLapTime(0, 1, 1, 1, 1)
    #     self.CarStoreList.appendLapTime(1, 2, 2, 2, 2)

    # def getCarStorage(self):
    #    return self.CarStoreList.getCarListCopy()


# class TableModel(QAbstractTableModel):

#     def __init__(self, carList, parent=None):
#         super().__init__()
#         self.arrayData = carList
#         self.headerData = self.arrayData.getCarNamesList()
#         self.RowNum = self.arrayData.getCarByID(0).getLapCount()
#         self.ColNum = self.arrayData.getCarAmount()
#         self.vertHeaderData = [x for x in range(self.RowNum)]

#     def rowCount(self, parent=QModelIndex()):
#         return self.arrayData.getCarByID(0).getLapCount()

#     def columnCount(self, parent=QModelIndex()):
#         return self.arrayData.getCarAmount()

#     def data(self, index, role):
#         if index.isValid() and (role == Qt.DisplayRole or role == Qt.EditRole) and index.column() < self.ColNum - 1 and index.row() < self.RowNum - 1:
#             if self.arrayData.storageList[index.column()].getLapStringByID(index.row()) == "0:0:0":
#                 return ""
#             else:
#                 return self.arrayData.storageList[index.column()].getLapStringByID(index.row())
#         elif role == Qt.TextAlignmentRole:
#             return Qt.AlignCenter

#     def setData(self, modelIndex, LapData, role):
#         if modelIndex.isValid() and Qt.DisplayRole or Qt.EditRole:
#             list = self.parseCellData(LapData)
#             self.arrayData.storageList[modelIndex.column()].editLapTime(modelIndex.row(), list[0], list[1], list[2])
#             return True
#         else:
#             return False

#     def headerData(self, col, orientation, role):
#         if orientation == Qt.Horizontal and (
#                 role == Qt.DisplayRole or role == Qt.EditRole) and col <= self.columnCount():
#             return self.headerData[col]
#         if orientation == Qt.Vertical and role == Qt.DisplayRole and col <= self.rowCount():
#             return self.vertHeaderData[col]

#     def flags(self, index):
#         flags = super(self.__class__, self).flags(index)

#         flags |= Qt.ItemIsEditable
#         flags |= Qt.ItemIsSelectable
#         flags |= Qt.ItemIsEnabled
#         flags |= Qt.ItemIsDragEnabled
#         flags |= Qt.ItemIsDropEnabled

#         return flags

#     def parseCellData(self, cellData):
#         list = []

#         if cellData.count(':') == 3:
#             first = cellData.find(':')
#             second = cellData.find(':', first + 1 , len(cellData))
#             third = cellData.find(':', second + 1, len(cellData))

#             list.append(int(cellData[0 : first]))
#             list.append(int(cellData[first + 1 : second]))
#             list.append(int(cellData[second + 1: third]))
#             list.append(int(cellData[third + 1: len(cellData)]))

#             return list

#         elif cellData.count(':') == 2:
#             first = cellData.find(':')
#             second = cellData.find(':', first + 1, len(cellData))

#             list.append(int(cellData[0 : first]))
#             list.append(int(cellData[first + 1 : second]))
#             list.append(int(cellData[second + 1: len(cellData)]))
#             list.append(0)

#             return list

#         elif cellData.count(':') == 1:
#             first = cellData.find(':')

#             list.append(int(cellData[0: first]))
#             list.append(int(cellData[first + 1:len(cellData)]))
#             list.append(0)
#             list.append(0)

#             return list

#         elif cellData.count(':') == 0:
#             if(len(cellData) > 0):
#                 list.append(int(cellData))
#                 list.append(0)
#                 list.append(0)
#                 list.append(0)
#                 return list
#             else:
#                 return 0,0,0,0
#         else:
#             return 0, 0, 0, 0
