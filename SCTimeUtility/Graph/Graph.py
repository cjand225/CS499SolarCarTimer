"""

    Module:
    Purpose:
    Depends On:

    #TODO: Needs Reworking

"""

import matplotlib.pyplot as plt, numpy as np
from enum import IntEnum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QStyle
from PyQt5.uic import loadUi

from SCTimeUtility.Graph import graph_resource_path
from SCTimeUtility.Log.Log import get_log


class GraphType(IntEnum):
    LAP_TIME = 0,
    AVG_TIME = 1,
    MIN_TIME = 2,
    MAX_TIME = 3


class Graph(QWidget):
    maxGraphNumber = 100

    def __init__(self):
        super().__init__()
        self.graph_dictionary = ["Lap vs Time", "Average Lap vs Time", "Minimum Time", "Maximum Time"]
        self.default_graph_type = self.graph_dictionary[GraphType.LAP_TIME]
        self.graphed_team_list = []
        self.currGraphNum = 1
        self.inMinutes = False

        self.teamList = []

        self.init_widget()
        self.add_graphs()
        self.handle_update(self.teamList)
        self.bind_actions()

    '''  
        Function: initUI
        Parameters: self
        Return Value: N/A
        Purpose: Initializes and loads resource file for the Graph Widget.
    '''

    def init_widget(self):
        self.widget = loadUi(graph_resource_path, self)
        self.setGeometry(QStyle.alignedRect(Qt.RightToLeft, Qt.AlignBottom,
                                            self.size(), QApplication.desktop().availableGeometry()))

    '''  
        Function: addGraphics
        Parameters: self
        Return Value: N/A
        Purpose: Adds Graph types to the list of available graphs
    '''

    # add Graph types
    def add_graphs(self):
        for graph in self.graph_dictionary:
            self.GraphTypes.addItem(graph)

    '''  
        Function: bindListeners
        Parameters: self
        Return Value: N/A
        Purpose: Binds all the different functions to corresponding buttons on GUI.
    '''

    def bind_actions(self):
        self.ApplyGraphBtn.clicked.connect(self.create_graph)
        self.GraphTypes.activated[str].connect(self.graph_type_chosen)
        self.ChosenTeamList.itemDoubleClicked.connect(self.chosen_team_click_event)
        self.MinuteButton.toggled.connect(self.time_display_toggle)
        self.TeamChoiceBox.activated.connect(self.team_selected)

    '''  
        Function: updateTeamList
        Parameters: self, newTeamList
        Return Value: N/A
        Purpose: Called periodically on update of model to update the team listing availability for graphing
    '''

    def update_team_lists(self, team_list):
        self.teamList = team_list

    '''  
        Function: populateTeamChoiceBox
        Parameters: self
        Return Value: N/A
        Purpose: Populates the choice of teams into gui related teamChoiceBox.
    '''

    def populate_team_choices(self):
        self.graphed_team_list = []
        self.TeamChoiceBox.clear()
        for x in range(0, len(self.teamList)):
            self.TeamChoiceBox.addItem(str(self.teamList[x].getTeam()), x)

    '''  
        Function: timeToggle
        Parameters: self
        Return Value: N/A
        Purpose: Toggles how time is displayed, whether in seconds or minutes.
    '''

    def time_display_toggle(self):
        self.inMinutes = self.MinuteButton.isChecked()

    '''  
        Function: handleUpdate
        Parameters: self, newTeamList
        Return Value: N/A
        Purpose: called periodically to update team listings.
    '''

    def handle_update(self, team_list):
        self.update_team_lists(team_list)
        self.populate_team_choices()

    '''  
        Function: drawGraph
        Parameters: self
        Return Value: N/A
        Purpose: 
    '''

    def create_graph(self):
        if self.default_graph_type == self.graph_dictionary[GraphType.LAP_TIME]:
            self.lap_over_time_graph()
        elif self.default_graph_type == self.graph_dictionary[GraphType.AVG_TIME]:
            self.average_lap_over_time_graph()
        elif self.default_graph_type == self.graph_dictionary[GraphType.MIN_TIME]:
            self.lowest_time_graph()
        elif self.default_graph_type == self.graph_dictionary[GraphType.MAX_TIME]:
            self.highest_time_graph()

    '''  
        Function: teamChosen
        Parameters: self, index
        Return Value: N/A
        Purpose: Adds current index to the list of chosen teams to Graph.
    '''

    def team_selected(self):
        self.add_team_to_graphing_list(self.TeamChoiceBox.currentIndex())

    '''  
        Function: addTeamToGraphList
        Parameters: self, index
        Return Value: Boolean Condition
        Purpose: Adds the given index to the Graph if its lower than the max amount of teams and its not out of
                 range of the list indices.
    '''

    def add_team_to_graphing_list(self, index):
        # check for space in list
        if len(self.graphed_team_list) >= self.maxGraphNumber:
            return False

        # if not in list add it
        if not (self.teamList[index] in self.graphed_team_list):
            self.ChosenTeamList.addItem(self.teamList[index].getTeam())
            self.graphed_team_list.append(self.teamList[index])
            return True
        return False

    '''  
        Function: removeTeamFromGraphList
        Parameters: self, teamName
        Return Value: Boolean Condition
        Purpose: Returns a boolean value based on if a team was removed from the current graphing list.
    '''

    def remove_team_from_graph_list(self, teamName):
        # search Graph list and remove found element
        for i in range(0, len(self.graphed_team_list) - 1):
            team = self.graphed_team_list[i]
            if team.getTeam() == teamName:
                self.graphed_team_list.pop(i)
                return True
        return False

    '''  
        Function: chosenTeamClick
        Parameters: self
        Return Value: N/A
        Purpose: handles the click events associated with added and removing teams.
    '''

    def chosen_team_click_event(self):
        # if the team is double clicked then remove it
        teamName = self.ChosenTeamList.currentItem().text()
        self.remove_team_from_graph_list(teamName)
        # remove the team from the list
        self.ChosenTeamList.takeItem(self.ChosenTeamList.currentRow())

    '''  
        Function: typeChosen
        Parameters: self, text
        Return Value: N/A
        Purpose: sets the current graphing type to the one selected in the list
    '''

    def graph_type_chosen(self, text):
        # checks that type is valid (in types list)
        if text in self.graph_dictionary:
            self.default_graph_type = text

    '''  
        Function: getElapsed
        Parameters: self, lapList
        Return Value: list of LapTime.elapsedTime values.
        Purpose: Appends a new list of laptimes for plotting Graph, based on either minutes or seconds.
    '''

    def get_elapsed_time(self, lap_list):
        elapsed = []
        if self.inMinutes:
            for lap in lap_list:
                elapsed.append(lap / 60)
        else:
            for lap in lap_list:
                elapsed.append(lap)
        return elapsed

    '''  
        Function: lapVsTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: Creates a Graph based on Lap Vs. Time based on certain intervals of laps and amounts of time.
    '''

    def lap_over_time_graph(self):
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
        for team in self.graphed_team_list:
            duration_list = []
            graph_range = np.arange(0, len(self.graphed_team_list[index].lapList), 1.0)
            plt.xticks(np.arange(1.0, len(self.graphed_team_list[index].lapList) + 1, 1.0))
            for lap in team.lapList:
                duration_list.append(lap.get_elapsed_time())
            duration_list = self.get_elapsed_time(duration_list)
            # plot current Team
            plt.plot(graph_range, duration_list, label=team.getTeam())
            index += 1

        if len(self.graphed_team_list) > 0:
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

    def average_lap_over_time_graph(self):

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
        for team in self.graphed_team_list:
            lapAverages = []
            graphRange = np.arange(0, len(team.lapList), 1.0)
            plt.xticks(np.arange(1.0, len(team.lapList) + 1, 1.0))

            # for every lap for current team calculate the average time
            currLap = 0
            for lap in team.lapList:
                if self.inMinutes:
                    lapAverages.append((lap.get_elapsed_time() / ((currLap + 1) * 60)))
                else:
                    lapAverages.append(lap.get_elapsed_time() / (currLap + 1))
                currLap += 1

            plt.plot(graphRange, lapAverages, label=team.getTeam())
        if len(self.graphed_team_list) > 0:
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
        Purpose: Creates a Graph based on the lowest Time of each Car at certain intervals.
    '''

    def lowest_time_graph(self):
        labels = []
        data = []

        # calculate minimum times for teams
        for team in self.graphed_team_list:
            lapList = []
            for lap in team.lapList:
                if lap.get_elapsed_time() != 0:
                    lapList.append(lap.get_elapsed_time())

            data.append(min(lapList))
            labels.append(team.getTeam())

        # send data to bar Graph
        if self.inMinutes:
            self.bar_graph(data, labels, 'Minimum Times', 'Teams', 'Time (minutes)')
        else:
            self.bar_graph(data, labels, 'Minimum Times', 'Teams', 'Time (seconds)')

    '''  
        Function: maxTimeGraph
        Parameters: self
        Return Value: N/A
        Purpose: Creates a Graph based on the highest Time of each Car at certain intervals.
    '''

    def highest_time_graph(self):
        labels = []
        data = []

        # calculate minimum times for teams
        for team in self.graphed_team_list:
            lapList = []
            for lap in team.lapList:
                if lap.get_elapsed_time() != 0:
                    lapList.append(lap.get_elapsed_time())

            data.append(max(lapList))
            labels.append(team.getTeam())

        # send data to bar Graph
        if self.inMinutes:
            self.bar_graph(data, labels, 'Maximum Times', 'Teams', 'Time (minutes)')
        else:
            self.bar_graph(data, labels, 'Maximum Times', 'Teams', 'Time (seconds)')

    '''  
        Function: barGraph
        Parameters: self, data, labels, title, x_axis, y_axis
        Return Value: N/A
        Purpose: Creates a bar Graph based on laps or Lap Times of each car.
    '''

    def bar_graph(self, data, labels, title, x_axis, y_axis):
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
