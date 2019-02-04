import os
from PyQt5.QtCore import Qt, QSize
from operator import itemgetter

from SCTimeUtility.graph import LeaderBoardUIPath
from SCTimeUtility.graph.LeaderBoardWidget import LeaderBoardWidget
from SCTimeUtility.graph.LeaderBoardModel import LeaderBoardModel
from SCTimeUtility.graph.LeaderBoardSortFilterProxyModel import LeaderBoardSortFilterProxyModel
from SCTimeUtility.log.Log import getLog


class LeaderBoard():

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

    '''  
        Function: sort
        Parameters: self
        Return Value: N/A
        Purpose: sorts the Model based on whats been clicked
    '''

    def sort(self):
        oldSort = self.boardModel.sortColumn()
        self.boardModel.invalidate()
        self.widget.tableView.sortByColumn(oldSort, Qt.AscendingOrder)
        # self.boardModel.sort(self.boardModel.sortColumn())

    '''  
        Function: sortIndicatorChangedEvent
        Parameters: self, index, order
        Return Value: N/A
        Purpose: checks if index is within the alotted columns and then indicates that a sort event has happened.
    '''

    def sortIndicatorChangedEvent(self, index, order):
        if not index in self.sortableColumns:
            self.widget.tableView.horizontalHeader().setSortIndicator(index, self.boardModel.sortOrder())

    '''  
        Function: initWidget
        Parameters: self
        Return Value: N/A
        Purpose: Initializes the widget for the leader board module.
    '''

    def initWidget(self):
        self.widget = LeaderBoardWidget(LeaderBoardUIPath)

    '''  
        Function: getWidget
        Parameters: self
        Return Value: self.widget
        Purpose: Returns a reference to the widget stored within the LeaderBoard Module.
    '''

    def getWidget(self):
        return self.widget

    '''  
        Function: updateData
        Parameters: self, data
        Return Value: N/A
        Purpose: Periodically called function used to update the data contained within leader board module.
    '''

    def updateData(self, data):
        self.dataStorage = data
        self.updateBoard(data)
        self.sortCarByFastestLap()

    '''  
        Function: testLap
        Parameters: self
        Return Value: N/A
        Purpose: test function used to check the sorting by fastest lap function.
    '''

    def testLap(self):
        self.sortCarByFastestLap()

    '''  
        Function: sortCar
        Parameters: self
        Return Value: N/A
        Purpose: Interates through the cars within datastorage and gets their fastest lap, appending it to a list
                 and updating the board based on that.
    '''

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

    '''  
        Function: updateBoard
        Parameters: self, data
        Return Value: N/A
        Purpose: Updates the view of the leader board module with the data supplied from the parameter.
    '''

    def updateBoard(self, data):
        self.widget.resize(QSize(self.widget.width() + 1, self.widget.height()))
        self.boardModel.setModelData(data)
        self.widget.initHeaderHorizontal()
        self.widget.initHeaderVertical()
        self.widget.resize(QSize(self.widget.width() - 1, self.widget.height()))
