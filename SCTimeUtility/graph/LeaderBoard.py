from PyQt5.QtGui import *
from PyQt5.Qt import Qt
from PyQt5.QtCore import QObject, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtCore import QSize

from operator import itemgetter
import os

from SCTimeUtility.graph.LeaderBoardWidget import LeaderBoardWidget
from SCTimeUtility.graph.LeaderBoardModel import LeaderBoardModel
from SCTimeUtility.graph.LeaderBoardSortFilterProxyModel import LeaderBoardSortFilterProxyModel
from SCTimeUtility.log.Log import getLog


class LeaderBoard():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../resources"))
    LeaderBoardUIPath = os.path.join(resourcesDir, 'LeaderBoard.ui')

    def sort(self):
        oldSort = self.boardModel.sortColumn()
        self.boardModel.invalidate()
        self.widget.tableView.sortByColumn(oldSort, Qt.AscendingOrder)
        # self.boardModel.sort(self.boardModel.sortColumn())

    def __init__(self, cs=None):
        self.widget = None
        self.dataStorage = None
        self.horzHeader = ['Car Number', 'Team Name', 'Laps Completed', 'Fastest Lap']
        self.sortableColumns = [2, 3]
        self.newCarList = [[]]

        self.initWidget()
        self.carStore = cs
        self.boardModel = LeaderBoardSortFilterProxyModel(self.widget.tableView, self.sortableColumns)
        self.boardModel.setSourceModel(LeaderBoardModel(self.widget.tableView, self.horzHeader, self.carStore))
        self.boardModel.setSortRole(Qt.UserRole)
        # self.boardModel.sort(4)
        self.widget.tableView.setSortingEnabled(True)
        self.boardModel.sourceModel().dataChanged.connect(self.sort)
        self.widget.tableView.horizontalHeader().sortIndicatorChanged.connect(self.sortIndicatorChangedEvent)
        # print(self.boardModel.sortColumn())
        self.widget.tableView.setModel(self.boardModel)
        self.widget.fixHeaders(True)
        self.widget.tableView.sortByColumn(3, Qt.AscendingOrder)
        # self.widget.tableView.horizontalHeader().sectionResized.connect(self.widget.columnResized)

    def sortIndicatorChangedEvent(self, index, order):
        if not index in self.sortableColumns:
            self.widget.tableView.horizontalHeader().setSortIndicator(index, self.boardModel.sortOrder())

    def initWidget(self):
        self.widget = LeaderBoardWidget(self.LeaderBoardUIPath)

    def getWidget(self):
        return self.widget

    def updateData(self, data):
        self.dataStorage = data
        self.updateBoard(data)
        self.sortCarByFastestLap()

    def testLap(self):
        self.sortCarByFastestLap()

    def sortCarByFastestLap(self):
        self.newCarList = [[]]
        self.carList = []
        self.carList.clear()
        self.newCarList.clear()

        for car in self.dataStorage:
            listCar = [car.getID(), car.getFastestLap()]
            self.newCarList.append(listCar)
            if itemgetter(1) is not None:
                self.newCarList = sorted(self.newCarList, key=itemgetter(1))

        for x in range(0, len(self.newCarList)):
            self.carList.append(self.dataStorage[self.newCarList[x][0]])

        self.updateBoard(self.carList)

    def updateBoard(self, data):
        self.widget.resize(QSize(self.widget.width() + 1, self.widget.height()))
        self.boardModel.setModelData(data)
        self.widget.initHeaderHorizontal()
        self.widget.initHeaderVertical()
        self.widget.resize(QSize(self.widget.width() - 1, self.widget.height()))
