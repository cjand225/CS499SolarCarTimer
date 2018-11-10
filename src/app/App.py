'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

import sys
from PyQt5.QtCore import *
from PyQt5.Qt import *
from src.app.AppWindow import AppWindow
from src.table.Table import Table



class App():

    def __init__(self):
        self.Application = None
        self.mainWindow = None
        self.running = False

        #put ui PathFiles Right here
        self.MainUIPath = './../resources/App.ui'
        self.TableUIPath = './../resources/Table.ui'
        self.VisionUIPath = './../resources/Video.ui'
        self.LogUIPath = './../resource/Log.ui'
        self.SemiAutoUIPath = './../resources/Buttons.ui'
        self.QuitDialogPath = './../resources/QuitDialog.ui'

        #read/write paths
        self.LogPath = '../../logs/'
        self.defaultSavePath = ''

        self.vision = None
        self.tableView = None

        #read/write files
        self.writeFile = None
        self.readFile = None

        self.initApplication()
        self.initMainWindow()
        self.initTableView()
        #self.initVision()
        #self.initLog()
        #self.initGraph()

        self.addComponents()
        self.connectActionsMainWindow()

    def initApplication(self):
        self.Application = QApplication(sys.argv)

    def initMainWindow(self):
        self.mainWindow = AppWindow(self.MainUIPath)
        self.mainWindow.initCloseDialog(self.QuitDialogPath)

    def initTableView(self):
        self.tableView = Table(self.TableUIPath)

    def initVision(self):
        self.vision = None

    def initLog(self):
        self.log = None

    def initGraph(self):
        self.graph = None

    def addComponents(self):
        self.mainWindow.addTable(self.tableView.getTableWidget())
        #self.mainWindow.addVision()
        #self.mainWindow.addLog()
        #self.mainWindow.addGraph(graphOptions, GraphWidget)
        #self.mainWindow.addSemiAuto()

    def connectActionsMainWindow(self):
        #FileMenu
        self.mainWindow.actionNew.triggered.connect(self.newFile)
        self.mainWindow.actionOpen.triggered.connect(self.openFile)
        self.mainWindow.actionSave.triggered.connect(self.saveFile)
        self.mainWindow.actionSaveAs.triggered.connect(self.saveAsFile)

        #Edit Menu

        #Help Menu

    def run(self):
        self.running = True
        sys.exit(self.Application.exec_())

    def isRunning(self):
        return self.running

    def getMainWindow(self):
        return self.mainWindow

    def saveFile(self):
        if(self.writeFile == None):
            self.writeFile = self.mainWindow.saveAsFileDialog()

        #continue to dump save file

    def saveAsFile(self):
        self.writeFile = self.mainWindow.saveAsFileDialog()
        #write file to location

    def openFile(self):
        if(self.readFile == None):
            self.readFile = self.mainWindow.openFileDialog()

    def newFile(self):
        self.writeFile = self.mainWindow.saveAsFileDialog()






