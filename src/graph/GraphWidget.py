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

import random


class Graph(QWidget):

    def __init__(self, uipath):
        super().__init__()
        self.UIPath = uipath
        self.initUI()

    def initUI(self):
        self.ui = loadUi(self.UIPath, self)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignRight,
                                            self.size(), QApplication.desktop().availableGeometry()))

        self.buttonBox.clicked.connect(self.printTest) #TODO REMOVE
        PlotCanvas(self.GraphWindow, width = 5, height=4)
      




        self.show()

    def printTest(self):
        print("TEST")



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