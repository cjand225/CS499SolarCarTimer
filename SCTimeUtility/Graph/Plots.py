"""

    Module:
    Purpose:
    Depends On:

"""

import matplotlib.pyplot as plt, numpy as np

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
        graphRange = np.arange(0, len(self.graphedTeamList[index].lapList), 1.0)
        plt.xticks(np.arange(1.0, len(self.graphedTeamList[index].lapList) + 1, 1.0))
        for lap in team.lapList:
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
        graphRange = np.arange(0, len(team.lapList), 1.0)
        plt.xticks(np.arange(1.0, len(team.lapList) + 1, 1.0))

        # for every lap for current team calculate the average time
        currLap = 0
        for lap in team.lapList:
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
        for lap in team.lapList:
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
        for lap in team.lapList:
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
