'''
Module: AppWindow.py
Purpose: Top level view object that handles most view information and talks with the controller to
         recieve data from modal

Depends On: PyQt5, Table.py, SemiAutoWidget.py,
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


from table.Table import Table
from table.SemiAutoWidget import SemiAutoWidget
from video.VisionWidget import VisionWidget
from log.LogWidget import LogWidget
from graph.GraphOptionsWidget import GraphOptions


class AppWindow(QMainWindow):

    def __init__(self, uipath):
        super(AppWindow, self).__init__()
        # initialize Window
        self.UIPath = uipath


        self.VisionWidget = None
        self.TableWidget = None
        self.SemiAutoWidget = None
        self.GraphWidget = None
        self.GraphOptionsWidget = None
        self.LogWidget = None


        #declare initalizers here
        self.initMainWindow()

    def initMainWindow(self):
        self.mainWindowUI = loadUi(self.UIPath, self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()

    def addVison(self, vision):
        self.VisionWidget = vision

    def addTable(self, table):
        self.TableWidget = table

    def addSemiAuto(self, semiAuto):
        self.SemiAutoWidget = semiAuto

    def addGraph(self, graph):
        self.GraphWidget = graph

    def addGraphOptions(self, graphOps):
        self.GraphOptionsWidget = graphOps

    def addLog(self, log):
        self.LogWidget = log
