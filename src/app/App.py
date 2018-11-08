'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

import sys
from PyQt5.QtCore import *
from PyQt5.Qt import *
from src.app.AppWindow import AppWindow



class App():

    def __init__(self):
        self.Application = None
        self.mainWindow = None
        self.running = False

        #put ui PathFiles Right here
        self.MainUIPath = './../../resources/App.ui'

        self.videoMod = None
        self.tableMod = None

        self.initApplication()
        self.initMainWindow()


    def initApplication(self):
        self.Application = QApplication(sys.argv)

    def initMainWindow(self):
        self.mainWindow = AppWindow(self.MainUIPath)

    def run(self):
        self.running = True
        sys.exit(self.Application.exec_())

    def isRunning(self):
        return self.running

    def getMainWindow(self):
        return self.mainWindow