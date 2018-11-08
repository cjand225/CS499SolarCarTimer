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

    def __init__(self):
        super(AppWindow, self).__init__()
        # initialize Window
        self.initMainWindow()

    def initMainWindow(self):
        self.mainWindowUI = loadUi('./../resources/App.ui', self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter,
                                            self.size(), QApplication.desktop().availableGeometry()))
        self.show()






