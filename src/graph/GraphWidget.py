import matplotlib
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QStyle, QFileDialog
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.table.Car import Car
import random

GRAPH_LAPVSTIME = "Lap vs Time"
GRAPH_MINTIME = "Minimum Time"
GRAPH_MAXTIME = "Maximum Time"
GRAPH_AVGVSTIME = "Average Lap vs Time"

graphTypes = [
    GRAPH_LAPVSTIME,
    GRAPH_AVGVSTIME,
    GRAPH_MINTIME,
    GRAPH_MAXTIME
]


class Graph(QWidget):
    maxGraphNumber = 3

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.graphedTeamList = []
        self.currentGraphType = graphTypes[0]

        self.fileDialog = QFileDialog()

        self.teamList = self.dumbData() #TODO CHANGE TO REAL DATA

        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.ApplyGraphBtn.clicked.connect(self.drawGraph)

        self.SaveGraphBtn.clicked.connect(self.saveGraph)

        # ADD TEAMS TO CHOICES COMBO BOX
        index = 0
        for car in self.teamList:
            self.TeamChoiceBox.addItem(car.getOrg(), index)
            index += 1
        # add action listener to team choice
        self.TeamChoiceBox.activated.connect(self.teamChosen)

        # add graph types
        for graphType in graphTypes:
            self.GraphTypes.addItem(graphType)
        # action listener for graph type
        self.GraphTypes.activated[str].connect(self.typeChosen)

        # add team list listener
        self.ChosenTeamList.itemDoubleClicked.connect(self.chosenTeamClick)

        # start the plot canvas
        self.pcanvas = PlotCanvas(self.GraphWindow, width=5, height=4)

        self.show()

    def drawGraph(self):
        self.pcanvas.plot(self.graphedTeamList) #TODO Change

    def saveGraph(self):
        fileName = self.fileDialog.getSaveFileName(self)
        print(fileName)
        if fileName:
            self.pcanvas.saveGraph(fileName[0])

    def teamChosen(self, index):
        self.addTeamToGraphList(self.TeamChoiceBox.itemData(index))

    def addTeamToGraphList(self, index):
        # check for space in list
        if len(self.graphedTeamList) >= self.maxGraphNumber:
            return False

        # if not in list add it
        if self.teamList[index] not in self.graphedTeamList:
            self.ChosenTeamList.addItem(self.teamList[index].getOrg())
            self.graphedTeamList.append(self.teamList[index])
            return True
        return False

    def removeTeamFromGraphList(self, teamName):
        for i in range(len(self.graphedTeamList)):
            team = self.graphedTeamList[i]
            if team.getOrg() == teamName:
                self.graphedTeamList.pop(i)
                return True
        return False

    def chosenTeamClick(self):
        teamName = self.ChosenTeamList.currentItem().text()
        self.removeTeamFromGraphList(teamName)
        self.ChosenTeamList.takeItem(self.ChosenTeamList.currentRow())

    def typeChosen(self, text):
        if text in graphTypes:
            self.currentGraphType = text

    def dumbData(self):
        carList = [Car(0, "Cool", 54),
                   Car(1, "UK", 10),
                   Car(2, "NC", 45),
                   Car(3, "TEST", 2)
                   ]

        for car in carList:
            car.LapList = [random.randint(10, 12) for i in range(20)]

        return carList


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot(self, teams):
        ax = self.figure.add_subplot(111)
        ax.lines = []
        legendText = []

        # set x-axis to be whole numbers
        for axis in [ax.xaxis, ax.yaxis]:
            axis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

        ax.set_title('Lap vs. Time')

        # add team to legend and plot their data
        for team in teams:
            legendText.append(team.getOrg())
            ax.plot(team.LapList)

        # place legend at upper left corner of graph
        ax.legend(legendText, loc='upper left')

        self.draw()

    def winTitle(self, text):
        self.ax.set_title(text)
        self.draw()

    def saveGraph(self, filePath):
        self.figure.savefig(filePath, bbox_inches='tight')
