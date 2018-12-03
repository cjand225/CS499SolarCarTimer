from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QSize

from operator import itemgetter
import os
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog
from src.graph.LeaderBoardWidget import LeaderBoardWidget
from src.graph.LeaderBoardModel import LeaderBoardModel


class LeaderBoard():
    resourcesDir = os.path.abspath(os.path.join(__file__, "./../../../resources"))
    LeaderBoardUIPath = os.path.join(resourcesDir, 'LeaderBoard.ui')

    def __init__(self):
        self.widget = None
        self.dataStorage = None
        self.horzHeader = ['Position', 'Car Number', 'Team Name', 'Number of Laps Completed', 'Fastest Lap']

        self.newCarList = [[]]

        self.initWidget()
        self.boardModel = LeaderBoardModel(self.widget, self.horzHeader, self.dataStorage)
        self.widget.tableView.setModel(self.boardModel)

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

