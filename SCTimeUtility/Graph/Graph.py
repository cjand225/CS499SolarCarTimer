import matplotlib.pyplot as plt, numpy as np
from enum import IntEnum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QStyle
from PyQt5.uic import loadUi

from SCTimeUtility.Log.Log import getLog


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

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads resource file for the Graph Widget.
    '''

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''  
        Function: addGraphcs
        Parameters: self
        Return Value: N/A
        Purpose: Adds Graph types to the list of available graphs
    '''

    # add Graph types
    def addGraphs(self):
        for graph in self.GraphDict:
            self.GraphTypes.addItem(graph)

    '''  
        Function: bindListeners
        Parameters: self
        Return Value: N/A
        Purpose: Binds all the different functions to corresponding buttons on GUI.
    '''

    def bindListeners(self):
        self.ApplyGraphBtn.clicked.connect(self.drawGraph)
        self.GraphTypes.activated[str].connect(self.typeChosen)
        self.ChosenTeamList.itemDoubleClicked.connect(self.chosenTeamClick)
        self.MinuteButton.toggled.connect(self.timeToggle)
        self.TeamChoiceBox.activated.connect(self.teamChosen)

    '''  
        Function: updateTeamList
        Parameters: self, newTeamList
        Return Value: N/A
        Purpose: Called periodically on update of model to update the team listing availability for graphing
    '''

    def updateTeamList(self, newTeamList):
        self.teamList = newTeamList

    '''  
        Function: populateTeamChoiceBox
        Parameters: self
        Return Value: N/A
        Purpose: Populates the choice of teams into gui related teamChoiceBox.
    '''

    def populateTeamChoiceBox(self):
        self.graphedTeamList = []
        self.TeamChoiceBox.clear()
        for x in range(0, len(self.teamList)):
            self.TeamChoiceBox.addItem(str(self.teamList[x].getTeam()), x)

    '''  
        Function: timeToggle
        Parameters: self
        Return Value: N/A
        Purpose: Toggles how time is displayed, whether in seconds or minutes.
    '''

    def timeToggle(self):
        self.inMinutes = self.MinuteButton.isChecked()

    '''  
        Function: handleUpdate
        Parameters: self, newTeamList
        Return Value: N/A
        Purpose: called periodically to update team listings.
    '''

    def handleUpdate(self, newTeamList):
        self.updateTeamList(newTeamList)
        self.populateTeamChoiceBox()

    '''  
        Function: drawGraph
        Parameters: self
        Return Value: N/A
        Purpose: 
    '''

    def drawGraph(self):
        if self.currentGraphType == self.GraphDict[GraphType.LAP_TIME]:
            self.lapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.AVG_TIME]:
            self.avgLapVsTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MIN_TIME]:
            self.minTimeGraph()
        elif self.currentGraphType == self.GraphDict[GraphType.MAX_TIME]:
            self.maxTimeGraph()

    '''  
        Function: teamChosen
        Parameters: self, index
        Return Value: N/A
        Purpose: Adds current index to the list of chosen teams to Graph.
    '''

    def teamChosen(self, index):
        self.addTeamToGraphList(self.TeamChoiceBox.currentIndex())

    '''  
        Function: addTeamToGraphList
        Parameters: self, index
        Return Value: Boolean Condition
        Purpose: Adds the given index to the Graph if its lower than the max amount of teams and its not out of
                 range of the list indices.
    '''

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

    '''  
        Function: removeTeamFromGraphList
        Parameters: self, teamName
        Return Value: Boolean Condition
        Purpose: Returns a boolean value based on if a team was removed from the current graphing list.
    '''

    def removeTeamFromGraphList(self, teamName):
        # search Graph list and remove found element
        for i in range(0, len(self.graphedTeamList) - 1):
            team = self.graphedTeamList[i]
            if team.getTeam() == teamName:
                self.graphedTeamList.pop(i)
                return True
        return False

    '''  
        Function: chosenTeamClick
        Parameters: self
        Return Value: N/A
        Purpose: handles the click events associated with added and removing teams.
    '''

    def chosenTeamClick(self):
        # if the team is double clicked then remove it
        teamName = self.ChosenTeamList.currentItem().text()
        self.removeTeamFromGraphList(teamName)
        # remove the team from the list
        self.ChosenTeamList.takeItem(self.ChosenTeamList.currentRow())

    '''  
        Function: typeChosen
        Parameters: self, text
        Return Value: N/A
        Purpose: sets the current graphing type to the one selected in the list
    '''

    def typeChosen(self, text):
        # checks that type is valid (in types list)
        if text in self.GraphDict:
            self.currentGraphType = text

    '''  
        Function: getElapsed
        Parameters: self, lapList
        Return Value: list of LapTime.elapsedTime values.
        Purpose: Appends a new list of laptimes for plotting Graph, based on either minutes or seconds.
    '''

    def getElapsed(self, lapList):
        elapsed = []
        if self.inMinutes:
            for lap in lapList:
                elapsed.append(lap / 60)
        else:
            for lap in lapList:
                elapsed.append(lap)
        return elapsed

    '''  
        Function: lapVsTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: Creates a Graph based on Lap Vs. Time based on certain intervals of laps and amounts of time.
    '''

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
            # plot curent Team
            plt.plot(graphRange, durationList, label=team.getTeam())
            index += 1

        if len(self.graphedTeamList) > 0:
            plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()

        # increments the figure number to guarantee new window for next Graph
        self.currGraphNum += 1

    '''  
        Function: avgLapVsTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: creates a Graph based on Average Lap Vs. Time of all participating cars selected.
    '''

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

    '''  
        Function: minTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: Creates a Graph based on the minimum Time of each Car at certain intervals.
    '''

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

        # send data to bar Graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Minimum Times', 'Teams', 'Time (seconds)')

    '''  
        Function: maxTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: Creates a Graph based on the minimum Time of each Car at certain intervals.
    '''

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

        # send data to bar Graph
        if self.inMinutes:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (minutes)')
        else:
            self.barGraph(data, labels, 'Maximum Times', 'Teams', 'Time (seconds)')

    '''  
        Function: barGraph
        Parameters: self, data, labels, title, x_axis, y_axis
        Return Value: N/A
        Purpose: Creates a bar Graph based on laps or Lap Times of each car.
    '''

    def barGraph(self, data, labels, title, x_axis, y_axis):
        # increments the figure number to guarantee new window
        plt.figure(self.currGraphNum)
        self.currGraphNum += 1

        # Graph Settings
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
