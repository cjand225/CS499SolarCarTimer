from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QComboBox
from PyQt5.uic import loadUi
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog
from enum import IntEnum

import matplotlib.pyplot as plt
import numpy as np


class GraphType(IntEnum):
    LAP_TIME = 0,
    AVG_TIME = 1,
    MIN_TIME = 2,
    MAX_TIME = 3


class Graph(QWidget):
    maxGraphNumber = 100

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.GraphDict = ["Lap vs Time", "Average Lap vs Time", "Minimum Time", "Maximum Time"]
        self.currentGraphType = self.GraphDict[GraphType.LAP_TIME]
        self.graphedTeamList = []
        self.currGraphNum = 1
        self.inMinutes = False

        self.teamList = []


        self.initUI()
        self.addGraphs()
        self.handleUpdate(self.teamList)
        self.bindListeners()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    # add graph types
    def addGraphs(self):
        for graph in self.GraphDict:
            self.GraphTypes.addItem(graph)


    def bindListeners(self):
        self.ApplyGraphBtn.clicked.connect(self.drawGraph)
        self.GraphTypes.activated[str].connect(self.typeChosen)
        self.ChosenTeamList.itemDoubleClicked.connect(self.chosenTeamClick)
        self.MinuteButton.toggled.connect(self.timeToggle)
        self.TeamChoiceBox.activated.connect(self.teamChosen)

    def updateTeamList(self, newTeamList):
        self.teamList = newTeamList

    def populateTeamChoiceBox(self):
        self.graphedTeamList = []
        self.TeamChoiceBox.clear()
        for x in range(0, len(self.teamList)):
            self.TeamChoiceBox.addItem(str(self.teamList[x].getTeam()), x)

    def timeToggle(self):
        self.inMinutes = self.MinuteButton.isChecked()

    def handleUpdate(self, newTeamList):
        self.updateTeamList(newTeamList)
        self.populateTeamChoiceBox()

    def drawGraph(self):
        if self.currentGraphType == self.GraphDict[GraphType.LAP_TIME]:
            self.lapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.AVG_TIME]:
            self.avgLapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MIN_TIME]:
            self.minTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MAX_TIME]:
            self.maxTimeGraph()

    def teamChosen(self, index):
        self.addTeamToGraphList(self.TeamChoiceBox.currentIndex())

    def addTeamToGraphList(self, index):
        # check for space in list
        if len(self.graphedTeamList) >= self.maxGraphNumber:
            return False

        # if not in list add it
        if not (self.teamList[index] in self.graphedTeamList):
            self.ChosenTeamList.addItem(self.teamList[index].getTeam())
            self.graphedTeamList.append(self.teamList[index])
            return True
        return False

    def removeTeamFromGraphList(self, teamName):
        # search graph list and remove found element
        for i in range(0, len(self.graphedTeamList) - 1):
            team = self.graphedTeamList[i]
            if team.getTeam() == teamName:
                self.graphedTeamList.pop(i)
                return True
        return False

    def chosenTeamClick(self):
        # if the team is double clicked then remove it
        teamName = self.ChosenTeamList.currentItem().text()
        self.removeTeamFromGraphList(teamName)
        # remove the team from the list
        self.ChosenTeamList.takeItem(self.ChosenTeamList.currentRow())

    def typeChosen(self, text):
        # checks that type is valid (in types list)
        if text in self.GraphDict:
            self.currentGraphType = text

    def getElapsed(self, lapList):
        elapsed = []
        if self.inMinutes:
            for lap in lapList:
                elapsed.append(lap / 60)
        else:
            for lap in lapList:
                elapsed.append(lap)
        return elapsed

    def lapVsTimeGraph(self):

        plt.figure(self.currGraphNum)
        # set labels
        plt.title('Lap vs Time')
        plt.xlabel('Lap')
        if self.inMinutes:
            plt.ylabel('Time (minutes)')
        else:
            plt.ylabel('Time (seconds)')

        # plot data
        index = 0
        for team in self.graphedTeamList:
            durationList = []
            graphRange = np.arange(0, len(self.graphedTeamList[index].LapList), 1.0)
            plt.xticks(np.arange(1.0, len(self.graphedTeamList[index].LapList) + 1, 1.0))
            for lap in team.LapList:
                durationList.append(lap.getElapsed())
            durationList = self.getElapsed(durationList)
            #plot curent Team
            plt.plot(graphRange, durationList, label=team.getTeam())
            index += 1

        if len(self.graphedTeamList) > 0:
            plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()

        # increments the figure number to guarantee new window for next graph
        self.currGraphNum += 1

    def avgLapVsTimeGraph(self):

        plt.figure(self.currGraphNum)

        # set labels
        plt.title('Lap vs Average Time')
        plt.xlabel('Lap')
        if self.inMinutes:
            plt.ylabel('Average Time (minutes)')
        else:
            plt.ylabel('Average Time (seconds)')

        # plot team lap averages
        index = 0
        for team in self.graphedTeamList:
            lapAverages = []
            graphRange = np.arange(0, len(team.LapList), 1.0)
            plt.xticks(np.arange(1.0, len(team.LapList) + 1, 1.0))

            # for every lap for current team calculate the average time
            currLap = 0
            for lap in team.LapList:
                if self.inMinutes:
                    lapAverages.append((lap.getElapsed() / ((currLap + 1) * 60)))
                else:
                    lapAverages.append(lap.getElapsed() / (currLap + 1))
                currLap += 1

            plt.plot(graphRange, lapAverages, label=team.getTeam())
        if len(self.graphedTeamList) > 0:
            plt.legend()

        plt.tight_layout()
        plt.grid(True)
        plt.show()

        # increments the figure number to guarantee new window
        self.currGraphNum += 1

    def minTimeGraph(self):
        labels = []
        data = []

        # calculate minimum times for teams
        for team in self.graphedTeamList:
            lapList = []
            for lap in team.LapList:
                if lap.getElapsed() != 0:
                    lapList.append(lap.getElapsed())

            data.append(min(lapList))
            labels.append(team.getTeam())

        # send data to bar graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (seconds)')

    def maxTimeGraph(self):
        labels = []
        data = []

        # calculate minimum times for teams
        for team in self.graphedTeamList:
            lapList = []
            for lap in team.LapList:
                if lap.getElapsed() != 0:
                    lapList.append(lap.getElapsed())

            data.append(max(lapList))
            labels.append(team.getTeam())


        # send data to bar graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (seconds)')

    def barGraph(self, data, labels, title, x_axis, y_axis):
        # increments the figure number to guarantee new window
        plt.figure(self.currGraphNum)
        self.currGraphNum += 1

        # graph settings
        # range is 1 because only 1 set of bars
        index = np.arange(1)
        bar_width = .5
        opacity = .8

        # add team to legend and plot their data
        for i in range(len(data)):
            plt.bar(index + bar_width * i, data[i],
                    width=bar_width,
                    label=labels[i],
                    alpha=opacity)

        # set labels
        plt.title(title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        # remove x ticks
        plt.xticks(index, ' ')
        # add legend
        if len(data) > 0:
            plt.legend()

        plt.tight_layout()
        plt.show()
