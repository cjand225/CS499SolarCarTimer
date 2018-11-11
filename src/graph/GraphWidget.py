'''
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QApplication
from PyQt5.Qt import Qt
from PyQt5.uic import loadUi


class Graph(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()
'''

import sys
from tkinter import Image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from matplotlib import figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from src.table.Car import Car

import random


class Graph(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.graphedTeamList = []
        self.teamList = [Car(0, "Cool", 54), Car(1, "UK", 10)]
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.buttonBox.clicked.connect(self.printTest) #TODO REMOVE


        #TODO get real car list
        cars = [Car(0, "Cool", 54), Car(1, "UK", 10)]
        # ADD TEAMS TO CHOICES COMBO BOX
        for car in cars:
            self.TeamChoiceBox.addItem(car.getOrg())
        #add action listener to team choice
        self.TeamChoiceBox.activated[str].connect(self.teamChosen)

        #add graph types
        self.GraphTypes.addItem("Lap vs. Time")

        #add team list listener
        self.ChosenTeamList.itemClicked.connect(self.chosenTeamClick)

        #start the plot canvas
        self.plot = PlotCanvas(self.GraphWindow, width=5, height=4)






        self.show()

    def printTest(self):
        print("TEST")

    def teamChosen(self, text):
        print("Team chosen:", text)
        self.plot.winTitle(text)
        self.addTeamToList(text)

    def addTeamToList(self, team):
        if len(self.graphedTeamList) > 1:
            return

        if team not in self.graphedTeamList:
            self.ChosenTeamList.addItem(team)
            self.graphedTeamList.append(team)

    def chosenTeamClick(self):
        print(self.ChosenTeamList.currentRow)





class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        data = [random.random() for i in range(25)]
        FigureCanvas.updateGeometry(self)
        self.plot(data)

    def plot(self, data):
        #data = [random.random() for i in range(25)]
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(data, 'r-')
        self.ax.set_title('Lap vs. Time')
        self.draw()

    def winTitle(self, text):
        self.ax .set_title(text)
        self.draw()

'''

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.left = 10
        #self.top = 10
        #self.title = 'PyQt5 matplotlib example - pythonspot.com'
        #self.width = 640
        #self.height = 400
        self.initUI()

    def initUI(self):
        self.ui = loadUi('./../../resources/GraphOptions.ui', self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.pushButton_3.clicked.connect(self.hello)
        #m = PlotCanvas(self, width=5, height=4)
        #m.move(10, 10)

        #button = QPushButton('PyQt5 button', self)
        #button.setToolTip('This s an example button')
        #button.move(500, 0)
        #button.resize(140, 100)

        self.show()

    def hello(self):
        print("HELLO")


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('PyQt Matplotlib Example')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

'''